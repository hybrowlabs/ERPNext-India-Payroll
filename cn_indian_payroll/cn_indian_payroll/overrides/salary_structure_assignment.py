import json
from datetime import datetime

import frappe
from frappe import _
from frappe.utils import getdate
from frappe.utils.pdf import get_pdf
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip
from hrms.payroll.doctype.salary_structure_assignment.salary_structure_assignment import (
    SalaryStructureAssignment,
)


class CustomSalaryStructureAssignment(SalaryStructureAssignment):
    def on_submit(self):
        self.insert_tax_declaration_list()

    def on_cancel(self):
        self.cancel_declaration()

    def cancel_declaration(self):
        declarations = frappe.db.get_list(
            "Employee Tax Exemption Declaration",
            filters={
                "payroll_period": self.custom_payroll_period,
                "docstatus": ["in", [0, 1]],
                "employee": self.employee,
                "custom_salary_structure_assignment": self.name,
            },
            fields=["name", "docstatus"],
        )

        if declarations:
            declaration = declarations[0]
            declaration_doc = frappe.get_doc("Employee Tax Exemption Declaration", declaration.name)

            if declaration_doc.docstatus == 0:
                frappe.delete_doc("Employee Tax Exemption Declaration", declaration_doc.name)

            elif declaration_doc.docstatus == 1:
                declaration_doc.cancel()
                frappe.delete_doc("Employee Tax Exemption Declaration", declaration_doc.name)

    # def insert_tax_declaration_list(self):
    #     if not self.employee:
    #         return

    #     sub_categories = []
    #     payroll_period = frappe.get_doc("Payroll Period", self.custom_payroll_period)
    #     from_date = getdate(self.from_date)
    #     payroll_start_date = getdate(payroll_period.start_date)
    #     payroll_end_date = getdate(payroll_period.end_date)

    #     declaration_start_date = max(from_date, payroll_start_date)
    #     start = declaration_start_date if not isinstance(declaration_start_date, str) else datetime.strptime(declaration_start_date, "%Y-%m-%d").date()
    #     end = payroll_end_date if not isinstance(payroll_end_date, str) else datetime.strptime(payroll_end_date, "%Y-%m-%d").date()

    #     num_months = (end.year - start.year) * 12 + (end.month - start.month) + 1

    #     salary_slip = make_salary_slip(
    #         source_name=self.salary_structure,
    #         employee=self.employee,
    #         print_format='Salary Slip Standard',
    #         posting_date=self.from_date,
    #         for_preview=1,
    #     )

    #     def add_exemption(component_type, monthly_amount):
    #         total_amount = monthly_amount * num_months
    #         exemption_components = frappe.get_all(
    #             'Employee Tax Exemption Sub Category',
    #             filters={'custom_component_type': component_type,"is_active":1},
    #             fields=['name', 'max_amount']
    #         )
    #         for comp in exemption_components:
    #             allowed_amount = min(total_amount, comp.max_amount or total_amount)
    #             sub_categories.append({
    #                 "sub_category": comp.name,
    #                 "max_amount": comp.max_amount,
    #                 "amount": allowed_amount
    #             })

    #     if self.custom_tax_regime == "New Regime" or self.custom_tax_regime == "Old Regime":
    #         for earning in salary_slip.earnings:
    #             comp_doc = frappe.get_doc("Salary Component", earning.salary_component)
    #             if comp_doc.component_type == "NPS" and comp_doc.custom_component_sub_type == "Fixed":
    #                 add_exemption("NPS", earning.amount)

    #         if self.custom_tax_regime == "Old Regime":
    #             for deduction in salary_slip.deductions:
    #                 comp_doc = frappe.get_doc("Salary Component", deduction.salary_component)
    #                 if comp_doc.component_type in ["Provident Fund", "Professional Tax"] and comp_doc.custom_component_sub_type == "Fixed":
    #                     add_exemption(comp_doc.component_type, deduction.amount)

    #     existing_declaration = frappe.get_list(
    #         'Employee Tax Exemption Declaration',
    #         filters={
    #             'employee': self.employee,
    #             'payroll_period': self.custom_payroll_period,
    #             'docstatus': ['in', [0, 1]]
    #         },
    #         fields=['name']
    #     )

    #     if existing_declaration:
    #         return

    #     new_declaration = frappe.get_doc({
    #         'doctype': 'Employee Tax Exemption Declaration',
    #         'employee': self.employee,
    #         'company': self.company,
    #         'payroll_period': self.custom_payroll_period,
    #         'currency': self.currency,
    #         'custom_income_tax': self.income_tax_slab,
    #         'custom_salary_structure_assignment': self.name,
    #         'custom_posting_date': self.from_date
    #     })

    #     for category in sub_categories:
    #         new_declaration.append("declarations", {
    #             "exemption_sub_category": category["sub_category"],
    #             "max_amount": category["max_amount"],
    #             "amount": category["amount"]
    #         })

    #     new_declaration.insert()
    #     new_declaration.submit()
    #     frappe.db.commit()

    def insert_tax_declaration_list(self):
        if not self.employee:
            return

        sub_categories = {}

        payroll_period = frappe.get_doc("Payroll Period", self.custom_payroll_period)
        payroll_start = getdate(payroll_period.start_date)
        payroll_end = getdate(payroll_period.end_date)

        # get all structure assignments in the payroll period
        assignments = frappe.get_all(
            "Salary Structure Assignment",
            filters={"employee": self.employee, "docstatus": 1, "from_date": ["<=", payroll_end]},
            fields=["name", "salary_structure", "from_date"],
            order_by="from_date",
        )

        for i, ass in enumerate(assignments):
            start = max(getdate(ass.from_date), payroll_start)

            if i + 1 < len(assignments):
                end = getdate(assignments[i + 1].from_date) - timedelta(days=1)
            else:
                end = payroll_end

            if start > payroll_end:
                continue

            months = (end.year - start.year) * 12 + (end.month - start.month) + 1

            salary_slip = make_salary_slip(
                source_name=ass.salary_structure, employee=self.employee, posting_date=start, for_preview=1
            )

            def add_exemption(component_type, monthly_amount):
                total = monthly_amount * months

                exemption_components = frappe.get_all(
                    "Employee Tax Exemption Sub Category",
                    filters={"custom_component_type": component_type, "is_active": 1},
                    fields=["name", "max_amount"],
                )

                for comp in exemption_components:
                    if comp.name not in sub_categories:
                        sub_categories[comp.name] = {"max_amount": comp.max_amount or 0, "amount": 0}

                    sub_categories[comp.name]["amount"] += total

            # NPS (allowed both regimes)
            for earning in salary_slip.earnings:
                comp_doc = frappe.get_doc("Salary Component", earning.salary_component)

                if comp_doc.component_type == "NPS" and comp_doc.custom_component_sub_type == "Fixed":
                    add_exemption("NPS", earning.amount)

            # Old regime components
            if self.custom_tax_regime == "Old Regime":
                for deduction in salary_slip.deductions:
                    comp_doc = frappe.get_doc("Salary Component", deduction.salary_component)

                    if (
                        comp_doc.component_type in ["Provident Fund", "Professional Tax"]
                        and comp_doc.custom_component_sub_type == "Fixed"
                    ):
                        add_exemption(comp_doc.component_type, deduction.amount)

        # Apply max limits
        final_categories = []
        for key, val in sub_categories.items():
            allowed = min(val["amount"], val["max_amount"] or val["amount"])

            final_categories.append({"sub_category": key, "max_amount": val["max_amount"], "amount": allowed})

        existing = frappe.get_list(
            "Employee Tax Exemption Declaration",
            filters={
                "employee": self.employee,
                "payroll_period": self.custom_payroll_period,
                "docstatus": ["in", [0, 1]],
            },
            fields=["name"],
        )

        if existing:
            declaration = frappe.get_doc("Employee Tax Exemption Declaration", existing[0].name)
            declaration.declarations = []

            for category in final_categories:
                declaration.append(
                    "declarations",
                    {
                        "exemption_sub_category": category["sub_category"],
                        "max_amount": category["max_amount"],
                        "amount": category["amount"],
                    },
                )

            declaration.save()
            declaration.submit()

        else:
            declaration = frappe.get_doc(
                {
                    "doctype": "Employee Tax Exemption Declaration",
                    "employee": self.employee,
                    "company": self.company,
                    "payroll_period": self.custom_payroll_period,
                    "currency": self.currency,
                    "custom_income_tax": self.income_tax_slab,
                    "custom_salary_structure_assignment": self.name,
                    "custom_posting_date": self.from_date,
                }
            )

            for category in final_categories:
                declaration.append(
                    "declarations",
                    {
                        "exemption_sub_category": category["sub_category"],
                        "max_amount": category["max_amount"],
                        "amount": category["amount"],
                    },
                )

            declaration.insert()
            declaration.submit()

        frappe.db.commit()


@frappe.whitelist()
def generate_ctc_pdf(employee, salary_structure, posting_date=None, employee_benefits=None):
    """
    Generate CTC PDF for a given employee and salary structure.
    """

    slip = make_salary_slip(
        source_name=salary_structure,
        employee=employee,
        print_format="Salary Slip Standard",
        posting_date=posting_date,
        for_preview=1,
    )

    if not slip:
        frappe.throw("Unable to generate salary breakup. Check Salary Structure or Employee.")

    earnings_list = []
    total_monthly_earnings = 0
    total_annual_earnings = 0
    for e in slip.get("earnings", []):
        comp_doc = frappe.get_doc("Salary Component", e.salary_component)
        if comp_doc.custom_is_part_of_ctc:
            amount = e.amount or 0
            earnings_list.append(
                {
                    "salary_component": e.salary_component,
                    "monthly_amount": round(amount),
                    "annual_amount": round(amount) * 12,
                }
            )
            total_monthly_earnings += round(amount)
            total_annual_earnings += round(amount) * 12

    deduction_list = []
    total_monthly_ded = 0
    total_annual_ded = 0
    for d in slip.get("deductions", []):
        comp_doc = frappe.get_doc("Salary Component", d.salary_component)
        if comp_doc.custom_is_part_of_ctc:
            amount = d.amount or 0
            deduction_list.append(
                {
                    "salary_component": d.salary_component,
                    "monthly_amount": round(amount),
                    "annual_amount": round(amount) * 12,
                }
            )
            total_monthly_ded += round(amount)
            total_annual_ded += round(amount) * 12

    if employee_benefits and isinstance(employee_benefits, str):
        try:
            employee_benefits = json.loads(employee_benefits)
        except Exception:
            employee_benefits = []

    reimbursement_list = []
    total_monthly_reim = 0
    total_annual_reim = 0

    for r in employee_benefits:
        comp_name = r.get("salary_component")
        amount = r.get("amount", 0)
        if comp_name:
            reimbursement_list.append(
                {"salary_component": comp_name, "monthly_amount": amount / 12, "annual_amount": amount}
            )
            total_monthly_reim += amount / 12
            total_annual_reim += amount

    total_monthly_ctc = total_monthly_earnings + total_monthly_reim + total_monthly_ded
    total_annual_ctc = total_annual_earnings + total_annual_reim + total_annual_ded

    employee_doc = frappe.get_doc("Employee", employee)

    context = {
        "employee": employee,
        "employee_name": employee_doc.employee_name if employee_doc else "",
        "department": employee_doc.department if employee_doc else "",
        "designation": employee_doc.designation if employee_doc else "",
        "company": slip.get("company") or "",
        "posting_date": slip.get("posting_date") or "",
        "salary_structure": slip.get("salary_structure") or "",
        "earnings": earnings_list,
        "reimbursements": reimbursement_list,
        "deductions": deduction_list,
        "total_monthly_earnings": total_monthly_earnings,
        "total_annual_earnings": total_annual_earnings,
        "total_monthly_reim": total_monthly_reim,
        "total_annual_reim": total_annual_reim,
        "total_monthly_ded": total_monthly_ded,
        "total_annual_ded": total_annual_ded,
        "total_monthly_ctc": total_monthly_ctc,
        "total_annual_ctc": total_annual_ctc,
    }

    html = frappe.render_template("cn_indian_payroll/templates/ctc_breakup_pdf.html", context)

    pdf_bytes = get_pdf(html)

    file_doc = frappe.get_doc(
        {
            "doctype": "File",
            "file_name": f"CTC_Breakup_{employee}.pdf",
            "attached_to_doctype": "Employee",
            "attached_to_name": employee,
            "content": pdf_bytes,
            "is_private": 0,
        }
    )
    file_doc.insert(ignore_permissions=True)

    return {"pdf_url": file_doc.file_url}
