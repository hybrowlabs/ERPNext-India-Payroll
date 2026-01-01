
# import frappe
# from frappe.utils import getdate
# from dateutil.relativedelta import relativedelta

# def on_update_after_submit(self, method):
#     insert_lop_reversal(self)

# def insert_lop_reversal(attendance):
#     attendance_date = getdate(attendance.attendance_date)


#     if attendance.status=="Present":

#         attendance_logs = frappe.get_list(
#             "Attendance Log",
#             filters={
#                 "employee": attendance.employee,
#                 "from_date": ["<=", attendance_date],
#                 "to_date": [">=", attendance_date],
#                 "docstatus": 1,
#             },
#             fields=[
#                 "name",
#                 "attendance_regularisationlop_reversal",
#             ],
#             limit=1,
#         )

#         if not attendance_logs:
#             return

#         log = frappe.get_doc("Attendance Log", attendance_logs[0].name)


#         reversal_value = 1

#         existing_value = log.attendance_regularisationlop_reversal or 0
#         log.attendance_regularisationlop_reversal = existing_value + reversal_value

#         log.save(ignore_permissions=True)


#     elif attendance.status == "Half Day":


import frappe
from frappe.utils import getdate

def on_update_after_submit(self, method):
    insert_lop_reversal(self)


def insert_lop_reversal(attendance):
    attendance_date = getdate(attendance.attendance_date)

    # ---------------------------------------
    # Decide reversal value
    # ---------------------------------------
    if attendance.status == "Present":
        reversal_value = 1
    elif attendance.status == "Half Day":
        reversal_value = 0.5
    else:
        return

    # ---------------------------------------
    # Fetch Attendance Log
    # ---------------------------------------
    attendance_logs = frappe.get_list(
        "Attendance Log",
        filters={
            "employee": attendance.employee,
            "from_date": ["<=", attendance_date],
            "to_date": [">=", attendance_date],
            "docstatus": 1,
        },
        fields=["name", "attendance_regularisationlop_reversal"],
        limit=1,
    )

    if not attendance_logs:
        return

    log = frappe.get_doc("Attendance Log", attendance_logs[0].name)

    # ---------------------------------------
    # Add value (accumulate)
    # ---------------------------------------
    existing_value = log.attendance_regularisationlop_reversal or 0
    log.attendance_regularisationlop_reversal = existing_value + reversal_value

    log.save(ignore_permissions=True)
