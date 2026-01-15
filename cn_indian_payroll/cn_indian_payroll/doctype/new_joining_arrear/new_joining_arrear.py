# Copyright (c) 2025, Hybrowlabs technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip
from datetime import datetime
import calendar


class NewJoiningArrear(Document):
    def before_save(self):
        self.insert_breakup_table()

    def on_submit(self):
        self.insert_additional_salary()


    def insert_additional_salary(self):
        if not (self.earning_component or self.deduction_component):
            return

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



        if self.benefit_arrear:
            for row in self.benefit_arrear:
                additional_salary = frappe.new_doc("Employee Benefit Accrual")
                additional_salary.employee = self.employee
                additional_salary.salary_component = row.salary_component
                additional_salary.amount = row.amount
                additional_salary.company = self.company
                additional_salary.payroll_entry = self.payroll_entry
                additional_salary.payroll_period=self.payroll_period
                additional_salary.benefit_accrual_date=self.posting_date

                additional_salary.payment_days = self.number_of_present_days
                additional_salary.working_days = self.working_days
                additional_salary.insert()
                additional_salary.submit()


    def insert_breakup_table(self):
        if not self.employee:
            return

        payout_date = self.payout_date

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
        ssa = salary_structure_assignment[0].name
        from_date = salary_structure_assignment[0].from_date

        # Generate salary slip for preview
        new_salary_slip = make_salary_slip(
            source_name=salary_structure,
            employee=self.employee,
            print_format="Salary Slip Standard",
            posting_date=from_date,
            for_preview=1,
        )

        processed_components = []
        earning_component = []
        deduction_component = []

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
                earning_component.append(
                    {
                        "salary_component": component_doc.name,
                        "amount": round(
                            (new_earning.amount / new_salary_slip.total_working_days)
                            * self.number_of_present_days
                        ),
                        "actual_amount":round(new_earning.amount)
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
                deduction_component.append(
                    {
                        "salary_component": component_doc.name,
                        "amount": round(
                            (new_deduction.amount / new_salary_slip.total_working_days)
                            * self.number_of_present_days
                        ),
                        "actual_amount":round(new_deduction.amount)
                    }
                )
                processed_components.append(component_doc.name)




        self.working_days=new_salary_slip.total_working_days

        self.set("earning_component", [])
        self.set("deduction_component", [])
        self.set("benefit_arrear", [])

        for row in earning_component:
            self.append("earning_component", row)

        for row in deduction_component:
            self.append("deduction_component", row)



        salary_structure_doc = frappe.get_doc(
            "Salary Structure Assignment",
            ssa
        )

        if salary_structure_doc.custom_employee_reimbursements:
            for benefit in salary_structure_doc.custom_employee_reimbursements:
                per_day_amount = (
                    (benefit.monthly_total_amount or 0)
                    / new_salary_slip.total_working_days
                )

                calculated_amount = per_day_amount * self.number_of_present_days

                self.append("benefit_arrear", {
                    "salary_component": benefit.reimbursements,
                    "amount": round(calculated_amount),
                    "actual_amount": round(benefit.monthly_total_amount or 0),
                })
