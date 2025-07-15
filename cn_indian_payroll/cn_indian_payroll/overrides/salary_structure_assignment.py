import frappe
from hrms.payroll.doctype.salary_structure_assignment.salary_structure_assignment import SalaryStructureAssignment

from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip
from frappe.utils import getdate
from datetime import datetime

class CustomSalaryStructureAssignment(SalaryStructureAssignment):

    def on_submit(self):
        self.insert_tax_declaration_list()
        self.update_employee_promotion()

    def on_cancel(self):
        self.cancel_declaration()

    def cancel_declaration(self):
        declarations = frappe.db.get_list(
            'Employee Tax Exemption Declaration',
            filters={
                'payroll_period': self.custom_payroll_period,
                'docstatus': ['in', [0, 1]],
                'employee': self.employee,
                'custom_salary_structure_assignment': self.name,
            },
            fields=['name', 'docstatus']
        )

        if declarations:
            declaration = declarations[0]
            declaration_doc = frappe.get_doc('Employee Tax Exemption Declaration', declaration.name)

            if declaration_doc.docstatus == 0:
                frappe.delete_doc('Employee Tax Exemption Declaration', declaration_doc.name)

            elif declaration_doc.docstatus == 1:
                declaration_doc.cancel()
                frappe.delete_doc('Employee Tax Exemption Declaration', declaration_doc.name)


    def update_employee_promotion(self):
        if self.custom_promotion_id:
            get_promotion_doc=frappe.get_doc("Employee Promotion",self.custom_promotion_id)
            get_promotion_doc.custom_status="Payroll Configured"
            get_promotion_doc.save()


    def insert_tax_declaration_list(self):
        if not self.employee:
            return

        sub_categories = []
        payroll_period = frappe.get_doc("Payroll Period", self.custom_payroll_period)
        from_date = getdate(self.from_date)
        payroll_start_date = getdate(payroll_period.start_date)
        payroll_end_date = getdate(payroll_period.end_date)

        declaration_start_date = max(from_date, payroll_start_date)
        start = declaration_start_date if not isinstance(declaration_start_date, str) else datetime.strptime(declaration_start_date, "%Y-%m-%d").date()
        end = payroll_end_date if not isinstance(payroll_end_date, str) else datetime.strptime(payroll_end_date, "%Y-%m-%d").date()

        num_months = (end.year - start.year) * 12 + (end.month - start.month) + 1

        salary_slip = make_salary_slip(
            source_name=self.salary_structure,
            employee=self.employee,
            print_format='Salary Slip Standard',
            # posting_date=self.from_date,
            for_preview=1,
        )

        def add_exemption(component_type, monthly_amount):
            total_amount = monthly_amount * num_months
            exemption_components = frappe.get_all(
                'Employee Tax Exemption Sub Category',
                filters={'custom_component_type': component_type,"is_active":1},
                fields=['name', 'max_amount']
            )
            for comp in exemption_components:
                allowed_amount = min(total_amount, comp.max_amount or total_amount)
                sub_categories.append({
                    "sub_category": comp.name,
                    "max_amount": comp.max_amount,
                    "amount": allowed_amount
                })

        if self.custom_tax_regime == "New Regime" or self.custom_tax_regime == "Old Regime":
            for earning in salary_slip.earnings:
                comp_doc = frappe.get_doc("Salary Component", earning.salary_component)
                if comp_doc.component_type == "NPS":
                    add_exemption("NPS", earning.amount)

            if self.custom_tax_regime == "Old Regime":
                for deduction in salary_slip.deductions:
                    comp_doc = frappe.get_doc("Salary Component", deduction.salary_component)
                    if comp_doc.component_type in ["Provident Fund", "Professional Tax"]:
                        add_exemption(comp_doc.component_type, deduction.amount)

        existing_declaration = frappe.get_list(
            'Employee Tax Exemption Declaration',
            filters={
                'employee': self.employee,
                'payroll_period': self.custom_payroll_period,
                'docstatus': ['in', [0, 1]]
            },
            fields=['name']
        )

        if existing_declaration:
            return

        new_declaration = frappe.get_doc({
            'doctype': 'Employee Tax Exemption Declaration',
            'employee': self.employee,
            'company': self.company,
            'payroll_period': self.custom_payroll_period,
            'currency': self.currency,
            'custom_income_tax': self.income_tax_slab,
            'custom_salary_structure_assignment': self.name,
            'custom_posting_date': self.from_date
        })

        for category in sub_categories:
            new_declaration.append("declarations", {
                "exemption_sub_category": category["sub_category"],
                "max_amount": category["max_amount"],
                "amount": category["amount"]
            })

        new_declaration.insert()
        new_declaration.submit()
        frappe.db.commit()
