import frappe
from hrms.payroll.doctype.salary_structure_assignment.salary_structure_assignment import SalaryStructureAssignment

from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip
from frappe.utils import getdate
from datetime import datetime
from frappe import _

from cn_indian_payroll.cn_indian_payroll.overrides.tds_projection_calculation import get_state_from_branch
from datetime import datetime, timedelta


class CustomSalaryStructureAssignment(SalaryStructureAssignment):

    def on_submit(self):
        self.insert_tax_declaration_list()
        self.update_employee_promotion()
        self.update_ctc_value()

    def on_cancel(self):
        self.cancel_declaration()

    def validate(self):
        super().validate()
        self.update_min_wages()
        self.reimbursement_amount()
        self.set_state_from_branch()






    def set_state_from_branch(self):
        branch_state = get_state_from_branch(self.employee,self.company)
        if branch_state:

            self.custom_state = branch_state
            if self.custom_lwf:
                self.custom_lwf_state = branch_state


    def before_update_after_submit(self):
        # self.insert_tax_declaration_list()
        self.update_min_wages()
        self.reimbursement_amount()

        self.update_ctc_value_after_update()
        


    def update_ctc_value(self):
        if self.custom_fixed_gross_annual:
            ctc_amount_annual = 0
            fixed_ctc_annual=0
            reimbursement = round(self.custom_total_reimbursement_amount * 12 or 0)

            ctc_salary_slip = make_salary_slip(
                source_name=self.salary_structure,
                employee=self.employee,
                print_format='Salary Slip Standard',
                posting_date=self.from_date,
                for_preview=1,
            )

            for new_earning in ctc_salary_slip.earnings:
                earning_component = frappe.get_doc("Salary Component", new_earning.salary_component)
                if earning_component.custom_is_part_of_ctc == 1:
                    ctc_amount_annual += round(new_earning.amount * 12)
                    fixed_ctc_annual += round(new_earning.amount * 12)

            for new_deduction in ctc_salary_slip.deductions:
                deduction_component = frappe.get_doc("Salary Component", new_deduction.salary_component)
                if deduction_component.custom_is_part_of_ctc == 1:
                    ctc_amount_annual += round(new_deduction.amount * 12)
                    fixed_ctc_annual += round(new_deduction.amount * 12)

            if self.custom_variable_pay_components:
                for value in self.custom_variable_pay_components:
                    if value.part_of_ctc:
                        ctc_amount_annual+=value.amount

            frappe.db.set_value(self.doctype, self.name, "base", ctc_amount_annual + reimbursement, update_modified=False)
            frappe.db.set_value(self.doctype, self.name, "custom_fixed_ctc_annual", fixed_ctc_annual + reimbursement, update_modified=False)

            self.reload()

    def update_ctc_value_after_update(self):
        if self.custom_fixed_gross_annual:
            ctc_amount_annual = 0
            fixed_ctc_annual=0
            reimbursement = round(self.custom_total_reimbursement_amount * 12 or 0)

            ctc_salary_slip = make_salary_slip(
                source_name=self.salary_structure,
                employee=self.employee,
                print_format='Salary Slip Standard',
                posting_date=self.from_date,
                for_preview=1,
            )

            for new_earning in ctc_salary_slip.earnings:
                earning_component = frappe.get_doc("Salary Component", new_earning.salary_component)
                if earning_component.custom_is_part_of_ctc == 1:
                    ctc_amount_annual += round(new_earning.amount * 12)
                    fixed_ctc_annual+=round(new_earning.amount * 12)

            for new_deduction in ctc_salary_slip.deductions:
                deduction_component = frappe.get_doc("Salary Component", new_deduction.salary_component)
                if deduction_component.custom_is_part_of_ctc == 1:
                    ctc_amount_annual += round(new_deduction.amount * 12)
                    fixed_ctc_annual+=round(new_deduction.amount * 12)


            if self.custom_variable_pay_components:
                for value in self.custom_variable_pay_components:
                    if value.part_of_ctc:
                        ctc_amount_annual+=value.amount


            self.base = ctc_amount_annual + reimbursement
            self.custom_fixed_ctc_annual=fixed_ctc_annual+reimbursement






    def reimbursement_amount(self):
        total_amount = 0
        not_included_total=0
        if len(self.custom_employee_reimbursements) > 0:
            for reimbursement in self.custom_employee_reimbursements:
                component=frappe.get_doc("Salary Component",reimbursement.reimbursements)
                if component.custom_include_ctc_total:
                    total_amount += reimbursement.monthly_total_amount
                else:
                    not_included_total += reimbursement.monthly_total_amount

        self.custom_total_reimbursement_amount = total_amount
        self.custom_not_included_total=not_included_total





    def update_min_wages(self):
        if self.custom_minimum_wages_applicable:
            state = frappe.get_doc("State Master", self.custom_minimum_wages_state)
            if not state:
                frappe.throw(_("Selected state does not exist."))

            match_found = False
            for wages in state.min_wages:
                if (
                    wages.zone == self.custom_zone
                    and wages.skill_level == self.custom_skill_level
                ):
                    self.custom_basic_value = wages.basic_daily_wage
                    self.custom_hra_value = wages.vda_daily_wages
                    match_found = True
                    break

            if not match_found:
                self.custom_basic_value = 0
                self.custom_hra_value = 0



    def cancel_declaration(self):

        declarations = frappe.get_list(
            "Employee Tax Exemption Declaration",
            filters={
                "payroll_period": self.custom_payroll_period,
                "employee": self.employee,
                "docstatus": ["in", [0, 1]],
            },
            fields=["name", "docstatus"],
        )

        if declarations:
            declaration = declarations[0]
            declaration_doc = frappe.get_doc(
                "Employee Tax Exemption Declaration", declaration.name
            )

            # Cancel if submitted
            if declaration_doc.docstatus == 1:
                declaration_doc.cancel()

            # Delete declaration
            frappe.delete_doc(
                "Employee Tax Exemption Declaration",
                declaration_doc.name,
                force=1,
            )

        # Check if another Salary Structure Assignment exists
        assignment_exists = frappe.db.exists(
            "Salary Structure Assignment",
            {
                "employee": self.employee,
                "custom_payroll_period": self.custom_payroll_period,
                "docstatus": 1,
                "name": ["!=", self.name],
            },
        )

        # Recreate declaration only if another assignment exists
        if assignment_exists:
            self.insert_tax_declaration_list()


    def update_employee_promotion(self):
        if self.custom_promotion_id:
            get_promotion_doc=frappe.get_doc("Employee Promotion",self.custom_promotion_id)
            get_promotion_doc.custom_status="Payroll Configured"
            get_promotion_doc.save()




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
            filters={
                "employee": self.employee,
                "docstatus": 1,
                "from_date": ["<=", payroll_end]
            },
            fields=["name", "salary_structure", "from_date"],
            order_by="from_date"
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
                source_name=ass.salary_structure,
                employee=self.employee,
                posting_date=start,
                for_preview=1
            )

            def add_exemption(component_type, monthly_amount):
                total = monthly_amount * months

                exemption_components = frappe.get_all(
                    "Employee Tax Exemption Sub Category",
                    filters={
                        "custom_component_type": component_type,
                        "is_active": 1
                    },
                    fields=["name", "max_amount"]
                )

                for comp in exemption_components:

                    if comp.name not in sub_categories:
                        sub_categories[comp.name] = {
                            "max_amount": comp.max_amount or 0,
                            "amount": 0
                        }

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

                    if comp_doc.component_type in ["Provident Fund", "Professional Tax"] \
                            and comp_doc.custom_component_sub_type == "Fixed":

                        add_exemption(comp_doc.component_type, deduction.amount)

        # Apply max limits
        final_categories = []
        for key, val in sub_categories.items():
            allowed = min(val["amount"], val["max_amount"] or val["amount"])

            final_categories.append({
                "sub_category": key,
                "max_amount": val["max_amount"],
                "amount": allowed
            })

        existing = frappe.get_list(
            "Employee Tax Exemption Declaration",
            filters={
                "employee": self.employee,
                "payroll_period": self.custom_payroll_period,
                "docstatus": ["in", [0, 1]]
            },
            fields=["name"]
        )

        if existing:
            declaration = frappe.get_doc("Employee Tax Exemption Declaration", existing[0].name)
            declaration.declarations = []

            for category in final_categories:
                declaration.append("declarations", {
                    "exemption_sub_category": category["sub_category"],
                    "max_amount": category["max_amount"],
                    "amount": category["amount"]
                })

            declaration.save()
            declaration.submit()

        else:
            declaration = frappe.get_doc({
                "doctype": "Employee Tax Exemption Declaration",
                "employee": self.employee,
                "company": self.company,
                "payroll_period": self.custom_payroll_period,
                "currency": self.currency,
                "custom_income_tax": self.income_tax_slab,
                "custom_salary_structure_assignment": self.name,
                "custom_posting_date": self.from_date
            })

            for category in final_categories:
                declaration.append("declarations", {
                    "exemption_sub_category": category["sub_category"],
                    "max_amount": category["max_amount"],
                    "amount": category["amount"]
                })

            declaration.insert()
            declaration.submit()

        frappe.db.commit()
