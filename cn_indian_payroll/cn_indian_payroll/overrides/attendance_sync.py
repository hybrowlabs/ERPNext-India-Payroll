

import frappe
from frappe.utils import getdate
from dateutil.relativedelta import relativedelta


def get_status_value(status):
    return {
        "Present": 1,
        "Half Day": 0.5,
        "Absent": 0,
        "On Leave": 1,
        "Work From Home": 1,
    }.get(status, 0)


def on_update_after_submit(self, method):
    insert_lop_reversal(self)


def on_submit(self, method):
    insert_lop_reversal(self)




def insert_lop_reversal(attendance):
    attendance_date = getdate(attendance.attendance_date)
    new_status = attendance.status
    new_value = get_status_value(new_status)

    attendance_logs = frappe.get_list(
        "Attendance Log",
        filters={
            "employee": attendance.employee,
            "from_date": ["<=", attendance_date],
            "to_date": [">=", attendance_date],
            "docstatus": 1,
        },
        fields=["name"],
        limit=1,
    )

    if not attendance_logs:
        return

    log = frappe.get_doc("Attendance Log", attendance_logs[0].name)

    for child in log.attendance_log_child:
        if child.date != attendance_date:
            continue

        old_status = child.status
        old_value = get_status_value(old_status)


        if old_status == new_status:
            child.regularize = 0
            child.regularized_status = new_status
            child.regularized_count = 0
            break


        diff = new_value - old_value

        child.regularize = 1
        child.regularized_status = new_status
        child.regularized_count = diff
        break


    log.attendance_regularisationlop_reversal = sum(
        row.regularized_count or 0 for row in log.attendance_log_child
    )


    last_slip = frappe.get_list(
        "Salary Slip",
        filters={"employee": attendance.employee, "docstatus": 1},
        fields=["end_date"],
        order_by="end_date desc",
        limit=1,
    )

    if last_slip:
        log.additional_salary_date = (
            getdate(last_slip[0].end_date) + relativedelta(months=1)
        )

    log.save(ignore_permissions=True)
