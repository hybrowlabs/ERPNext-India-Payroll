import calendar

import frappe
from frappe import _
from hrms.payroll.doctype.payroll_correction.payroll_correction import PayrollCorrection


class CustomPayrollCorrection(PayrollCorrection):
    @frappe.whitelist()
    def fetch_salary_slip_details(self):
        if not (self.employee and self.payroll_period and self.company):
            return {"months": [], "slip_details": []}

        slips = frappe.get_all(
            "Salary Slip",
            filters={
                "employee": self.employee,
                "docstatus": 1,
                "current_payroll_period": self.payroll_period,
                "company": self.company,
                "leave_without_pay": [">", 0],
            },
            fields=["name", "payment_days", "start_date", "total_working_days"],
            order_by="start_date asc",
        )

        if not slips:
            frappe.msgprint(
                _("No Salary Slips with {0} found for employee {1} for payroll period {2}.").format(
                    frappe.bold(_("Leave Without Pay")), self.employee, self.payroll_period
                )
            )
            return

        slip_details = []
        month_labels = []

        for slip in slips:
            start_date = slip.get("start_date")
            # Include year to disambiguate the same calendar month across different years
            month_label = f"{calendar.month_name[start_date.month]}-{start_date.year}"
            month_labels.append(month_label)

            slip_details.append(
                {
                    "salary_slip_reference": slip.get("name"),
                    "month_name": month_label,
                    "working_days": slip.get("total_working_days"),
                    "payment_days": slip.get("payment_days"),
                    "start_date": str(slip.get("start_date")),
                }
            )

        return {"months": month_labels, "slip_details": slip_details}
