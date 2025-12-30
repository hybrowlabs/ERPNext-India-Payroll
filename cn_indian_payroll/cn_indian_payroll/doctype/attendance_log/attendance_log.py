# Copyright (c) 2025, Hybrowlabs Technologies
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AttendanceLog(Document):

    def on_update_after_submit(self):
        self.insert_lop_reversal()

    def insert_lop_reversal(self):

        # -----------------------------------------
        # Skip if no LOP reversal days
        # -----------------------------------------
        if not self.attendance_regularisationlop_reversal:
            return

        # -----------------------------------------
        # Check if LOP Reversal already exists
        # -----------------------------------------
        existing_lop_reversal = frappe.get_all(
            "LOP Reversal",
            filters={
                "payroll_period": self.payroll_period,
                "company": self.company,
                "salary_slip": self.salary_slip_id
            },
            pluck="name"
        )

        if not existing_lop_reversal:

            reversal = frappe.new_doc("LOP Reversal")
            reversal.salary_slip = self.salary_slip_id
            reversal.employee = self.employee
            reversal.company = self.company
            reversal.payroll_period = self.payroll_period
            reversal.lop_month_reversal = self.month
            reversal.additional_salary_date = self.additional_salary_date
            reversal.number_of_days = self.attendance_regularisationlop_reversal
            reversal.additional_salary_date=self.additional_salary_date

            reversal.insert(ignore_permissions=True)
            reversal.submit()


        else:
            for reversal_name in existing_lop_reversal:
                reversal = frappe.get_doc("LOP Reversal", reversal_name)


                reversal.number_of_days = self.attendance_regularisationlop_reversal
                reversal.additional_salary_date = self.additional_salary_date
                reversal.lop_month_reversal = self.month

                reversal.save(ignore_permissions=True)

        frappe.db.commit()
