

import frappe
from frappe.model.document import Document
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip


class NewJoiningArrear(Document):
    def before_save(self):
        self.insert_breakup_table()

    def on_submit(self):
        self.insert_additional_salary()

    def insert_additional_salary(self):
        if not (self.earning_component or self.deduction_component or self.reimbursement_component):
            return

        # Create Additional Salary for earnings
        for row in self.earning_component:
            additional_salary = frappe.new_doc("Additional Salary")
            additional_salary.employee = self.employee
            additional_salary.salary_component = row.salary_component
            additional_salary.amount = row.amount
            additional_salary.company = self.company
            additional_salary.payroll_date = self.payout_date
            additional_salary.currency = "INR"
            additional_salary.ref_doctype = "New Joining Arrear"
            additional_salary.ref_docname = self.name
            additional_salary.insert()
            additional_salary.submit()

        # Create Additional Salary for deductions
        for row in self.deduction_component:
            additional_salary = frappe.new_doc("Additional Salary")
            additional_salary.employee = self.employee
            additional_salary.salary_component = row.salary_component
            additional_salary.amount = row.amount
            additional_salary.company = self.company
            additional_salary.payroll_date = self.payout_date
            additional_salary.currency = "INR"
            additional_salary.ref_doctype = "New Joining Arrear"
            additional_salary.ref_docname = self.name
            additional_salary.insert()
            additional_salary.submit()


        for row in self.reimbursement_component:
            additional_salary = frappe.new_doc("Employee Benefit Accrual")
            additional_salary.employee = self.employee
            additional_salary.salary_component = row.salary_component
            additional_salary.amount = row.amount
            additional_salary.company = self.company
            additional_salary.payroll_period = self.payroll_period

            additional_salary.benefit_accrual_date = self.posting_date
            additional_salary.working_days = self.working_days
            additional_salary.arrear_days = self.number_of_present_days
            additional_salary.insert()
            additional_salary.submit()





    def insert_breakup_table(self):
        if not self.employee:
            return

        # Get the latest approved salary structure assignment
        salary_structure_assignment = frappe.get_list(
            "Salary Structure Assignment",
            filters={
                "employee": self.employee,
                "company": self.company,
                "docstatus": 1,
            },
            fields=["*"],
            order_by="from_date desc",
            limit=1,
        )

        if not salary_structure_assignment:
            return

        salary_structure = salary_structure_assignment[0].salary_structure
        from_date = salary_structure_assignment[0].from_date

        ssa=frappe.get_doc("Salary Structure Assignment",salary_structure_assignment[0].name)

        # Generate salary slip for preview
        new_salary_slip = make_salary_slip(
            source_name=salary_structure,
            employee=self.employee,
            print_format="Salary Slip Standard",
            posting_date=from_date,
            for_preview=1,
        )



        processed_components = []
        earning_breakup = []
        deduction_breakup = []

        reimbursement_components = []


        for accrued_benefit in ssa.custom_employee_reimbursements:
            salary_component_doc = frappe.get_doc("Salary Component", accrued_benefit.reimbursements)



            if salary_component_doc.depends_on_payment_days == 1 and salary_component_doc.custom_is_reimbursement == 1:
                reimbursement_components.append({
                    "salary_component": accrued_benefit.reimbursements,
                    "amount": round(
                        ((accrued_benefit.monthly_total_amount / 12) / new_salary_slip.total_working_days) * self.number_of_present_days
                    ),
                    "actual_amount":round(accrued_benefit.monthly_total_amount)
                })

            if salary_component_doc.depends_on_payment_days == 0 and salary_component_doc.custom_is_reimbursement == 1:
                reimbursement_components.append({
                    "salary_component": accrued_benefit.reimbursements,
                    "amount": round(
                        round(accrued_benefit.monthly_total_amount)
                    ),
                    "actual_amount":round(accrued_benefit.monthly_total_amount)
                })

        for new_earning in new_salary_slip.earnings:
            component_doc = frappe.get_value(
                "Salary Component",
                filters={
                    "custom_component": new_earning.salary_component,
                    "disabled": 0,
                },
                fieldname=["name", "custom_is_arrear"],
                as_dict=True,
            )

            if not component_doc or component_doc.name in processed_components:
                continue

            if component_doc.custom_is_arrear == 1:
                earning_breakup.append(
                    {
                        "salary_component": component_doc.name,
                        "amount": round(
                            (new_earning.amount / new_salary_slip.total_working_days)
                            * self.number_of_present_days
                        ),
                        "actual_amount":new_earning.amount,
                    }
                )
                processed_components.append(component_doc.name)

        # Process deductions
        for new_deduction in new_salary_slip.deductions:
            component_doc = frappe.get_value(
                "Salary Component",
                filters={
                    "custom_component": new_deduction.salary_component,
                    "disabled": 0,
                },
                fieldname=["name", "custom_is_arrear"],
                as_dict=True,
            )

            if not component_doc or component_doc.name in processed_components:
                continue

            if component_doc.custom_is_arrear == 1:
                deduction_breakup.append(
                    {
                        "salary_component": component_doc.name,
                        "amount": round(
                            (new_deduction.amount / new_salary_slip.total_working_days)
                            * self.number_of_present_days
                        ),
                        "actual_amount":new_deduction.amount,
                    }
                )
                processed_components.append(component_doc.name)



        self.working_days=new_salary_slip.total_working_days

        self.set("earning_component", [])
        self.set("deduction_component", [])
        self.set("reimbursement_component",[])

        for row in earning_breakup:
            self.append("earning_component", row)

        for row in deduction_breakup:
            self.append("deduction_component", row)

        for row in reimbursement_components:
            self.append("reimbursement_component", row)
