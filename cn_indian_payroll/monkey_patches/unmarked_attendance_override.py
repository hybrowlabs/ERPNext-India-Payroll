import frappe
from frappe.utils import add_days, getdate, nowdate

from hrms.hr.utils import get_holiday_dates_for_employee
from hrms.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry


def _format_unmarked_dates(dates):
    return ", ".join(str(d.day) for d in dates)


@frappe.whitelist()
def custom_get_employees_with_unmarked_attendance(self):
    if not self.validate_attendance:
        return

    today = getdate(nowdate())
    employee_details = self.get_employee_and_attendance_details()
    if not employee_details:
        return []

    default_holiday_list = frappe.db.get_value(
        "Company", self.company, "default_holiday_list", cache=True
    )

    employee_ids = [e.name for e in employee_details]
    attendance_rows = frappe.get_all(
        "Attendance",
        filters={
            "employee": ["in", employee_ids],
            "attendance_date": ["between", [self.start_date, self.end_date]],
            "docstatus": ["!=", 2],
        },
        fields=["employee", "attendance_date"],
    )
    attendance_by_emp = {}
    for row in attendance_rows:
        attendance_by_emp.setdefault(row.employee, set()).add(getdate(row.attendance_date))

    unmarked_attendance = []
    for emp in self.employees:
        details = next((r for r in employee_details if r.name == emp.employee), None)
        if not details:
            continue

        start_date, end_date = self.get_payroll_dates_for_employee(details)
        start_date = getdate(start_date)
        end_date = min(getdate(end_date), today)

        if start_date > end_date:
            continue

        holiday_list = details.holiday_list or default_holiday_list
        holiday_dates = (
            set(getdate(d) for d in get_holiday_dates_for_employee(emp.employee, start_date, end_date))
            if holiday_list
            else set()
        )
        marked_dates = attendance_by_emp.get(emp.employee, set())

        unmarked_dates = []
        d = start_date
        while d <= end_date:
            if d not in marked_dates and d not in holiday_dates:
                unmarked_dates.append(d)
            d = add_days(d, 1)

        if unmarked_dates:
            unmarked_attendance.append(
                {
                    "employee": emp.employee,
                    "employee_name": emp.employee_name,
                    "unmarked_days": len(unmarked_dates),
                    "unmarked_dates": _format_unmarked_dates(unmarked_dates),
                }
            )

    return unmarked_attendance


PayrollEntry.get_employees_with_unmarked_attendance = custom_get_employees_with_unmarked_attendance
