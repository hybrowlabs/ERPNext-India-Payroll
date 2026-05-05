# Copyright (c) 2025, Hybrowlabs Technologies
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AttendanceLog(Document):
    pass

    # def on_update_after_submit(self):
    #     self.insert_lop_reversal()


    # def on_cancel(self):
    #     self.delete_lop_reversal()


    # def delete_lop_reversal(self):

    #     lop_reversals = frappe.get_list(
    #         "LOP Reversal",
    #         filters={"attendance_log": self.name},
    #         pluck="name"
    #     )

    #     if not lop_reversals:
    #         return


    #     additional_salaries = frappe.get_list(
    #         "Additional Salary",
    #         filters={
    #             "ref_doctype": "LOP Reversal",
    #             "ref_docname": ["in", lop_reversals],
    #         },
    #         pluck="name"
    #     )

    #     for add_sal in additional_salaries:
    #         doc = frappe.get_doc("Additional Salary", add_sal)

    #         if doc.docstatus == 1:
    #             doc.cancel()

    #         frappe.delete_doc(
    #             "Additional Salary",
    #             add_sal,
    #             ignore_permissions=True,
    #             force=True
    #         )

    #     for lop in lop_reversals:
    #         doc = frappe.get_doc("LOP Reversal", lop)

    #         if doc.docstatus == 1:
    #             doc.cancel()

    #         frappe.delete_doc(
    #             "LOP Reversal",
    #             lop,
    #             ignore_permissions=True,
    #             force=True
    #         )





    # def insert_lop_reversal(self):

    #     if self.attendance_regularisationlop_reversal in (None, 0):

    #         lop_reversals = frappe.get_list(
    #             "LOP Reversal",
    #             filters={"attendance_log": self.name},
    #             pluck="name"
    #         )

    #         if lop_reversals:
    #             additional_salaries = frappe.get_list(
    #                 "Additional Salary",
    #                 filters={
    #                     "ref_doctype": "LOP Reversal",
    #                     "ref_docname": ["in", lop_reversals],
    #                 },
    #                 pluck="name"
    #             )

    #             # Delete Additional Salary first
    #             for add_sal in additional_salaries:
    #                 doc = frappe.get_doc("Additional Salary", add_sal)
    #                 if doc.docstatus == 1:
    #                     doc.cancel()
    #                 frappe.delete_doc(
    #                     "Additional Salary",
    #                     add_sal,
    #                     ignore_permissions=True,
    #                     force=True
    #                 )

    #             # Delete LOP Reversal
    #             for lop in lop_reversals:
    #                 doc = frappe.get_doc("LOP Reversal", lop)
    #                 if doc.docstatus == 1:
    #                     doc.cancel()
    #                 frappe.delete_doc(
    #                     "LOP Reversal",
    #                     lop,
    #                     ignore_permissions=True,
    #                     force=True
    #                 )

    #         return

    #     existing_lop_reversal = frappe.get_all(
    #         "LOP Reversal",
    #         filters={
    #             "payroll_period": self.payroll_period,
    #             "company": self.company,
    #             "salary_slip": self.salary_slip_id,
    #             "attendance_log": self.name,
    #         },
    #         pluck="name"
    #     )

    #     if not existing_lop_reversal:
    #         reversal = frappe.new_doc("LOP Reversal")
    #         reversal.attendance_log = self.name
    #         reversal.salary_slip = self.salary_slip_id
    #         reversal.employee = self.employee
    #         reversal.company = self.company
    #         reversal.payroll_period = self.payroll_period
    #         reversal.lop_month_reversal = self.month
    #         reversal.additional_salary_date = self.additional_salary_date
    #         reversal.number_of_days = self.attendance_regularisationlop_reversal

    #         reversal.insert(ignore_permissions=True)
    #         reversal.submit()

    #     else:
    #         reversal = frappe.get_doc("LOP Reversal", existing_lop_reversal[0])
    #         reversal.number_of_days = self.attendance_regularisationlop_reversal
    #         reversal.additional_salary_date = self.additional_salary_date
    #         reversal.lop_month_reversal = self.month
    #         reversal.save(ignore_permissions=True)

    #     frappe.db.commit()
