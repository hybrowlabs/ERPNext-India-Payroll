import frappe


# http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.attendance_regularisation.get_employee_with_lwp?employee=37001&company=PW&from_date=2025-12-01&to_date=2025-12-27


@frappe.whitelist()
def get_employee_with_lwp(company=None, employee=None, from_date=None, to_date=None):

    if not company or not employee or not from_date or not to_date:
        frappe.throw("Please select Company, Employee, From Date and To Date")

    lwp_dates = []


    attendances = frappe.db.get_all(
        "Attendance",
        filters={
            "employee": employee,
            "company": company,
            "attendance_date": ["between", [from_date, to_date]],
            "status": ["in", ["Absent", "On Leave", "Half Day"]],
        },
        fields=["attendance_date", "status", "leave_type"]
    )


    for attendance in attendances:


        if attendance.status == "Absent":
            lwp_dates.append({
                "attendance_date": attendance.attendance_date,
                "status": "Absent",
                "leave_type": None
            })


        elif attendance.status in ["On Leave", "Half Day"] and attendance.leave_type:
            leave_type = frappe.get_doc("Leave Type", attendance.leave_type)

            if leave_type.is_lwp:
                lwp_dates.append({
                    "attendance_date": attendance.attendance_date,
                    "status": attendance.status,
                    "leave_type": attendance.leave_type
                })

    return lwp_dates



# import frappe
# from frappe.utils import getdate, nowdate
# from dateutil.relativedelta import relativedelta


# def update_attendance(company, employee, dates, status):
#     """Update attendance status and return updated count"""
#     updated = []

#     for d in dates:
#         att_name = frappe.db.get_value(
#             "Attendance",
#             {
#                 "company": company,
#                 "employee": employee,
#                 "attendance_date": d
#             },
#             "name"
#         )

#         if att_name:
#             frappe.db.set_value("Attendance", att_name, "status", status)
#             updated.append(d)

#     return updated


# from dateutil.relativedelta import relativedelta
# from frappe.utils import getdate, nowdate

# @frappe.whitelist(methods=["POST"])
# def edit_attendance():

#     # ----------------------------
#     # 1. Parse JSON Body
#     # ----------------------------
#     data = frappe.request.get_json()
#     if not data:
#         frappe.throw("Request body is empty")

#     company = data.get("company")
#     employee = data.get("employee")
#     attendance_dates = data.get("attendance_dates")
#     status = data.get("status", "Present")

#     if not company or not employee or not attendance_dates:
#         frappe.throw("company, employee and attendance_dates are mandatory")

#     attendance_dates = [getdate(d) for d in attendance_dates]
#     today = getdate(nowdate())

#     # ----------------------------
#     # 2. Payroll Settings
#     # ----------------------------
#     payroll_setting = frappe.get_single("Payroll Settings")

#     current_cycle_dates = []
#     before_cycle_dates = []
#     after_cycle_dates = []

#     cycle_start = None
#     cycle_end = None

#     # ==================================================
#     # 3. LEAVE BASED PAYROLL (Calendar Month)
#     # ==================================================
#     if payroll_setting.payroll_based_on == "Leave":

#         for d in attendance_dates:
#             if d.month == today.month and d.year == today.year:
#                 current_cycle_dates.append(d)
#             else:
#                 before_cycle_dates.append(d)

#     # ==================================================
#     # 4. ATTENDANCE BASED PAYROLL (Custom Cycle)
#     # Example: 21 → 20
#     # ==================================================
#     elif payroll_setting.payroll_based_on == "Attendance":

#         start_day = payroll_setting.custom_attendance_start_date
#         end_day = payroll_setting.custom_attendance_end_date

#         if not start_day or not end_day:
#             frappe.throw("Attendance cycle not configured in Payroll Settings")

#         # ---- Calculate LAST COMPLETED cycle ----
#         if today.day > end_day:
#             cycle_end = today.replace(day=end_day)
#         else:
#             cycle_end = (today - relativedelta(months=1)).replace(day=end_day)

#         cycle_start = cycle_end - relativedelta(months=1) + relativedelta(days=1)
#         cycle_start = cycle_start.replace(day=start_day)

#         # ---- Classify Dates ----
#         for d in attendance_dates:
#             if cycle_start <= d <= cycle_end:
#                 current_cycle_dates.append(d)
#             elif d < cycle_start:
#                 before_cycle_dates.append(d)
#             else:
#                 after_cycle_dates.append(d)

#     else:
#         frappe.throw("Invalid Payroll Based On value")

#     # ----------------------------
#     # 5. Update Attendance
#     # ----------------------------
#     updated_current = update_attendance(company, employee, current_cycle_dates, status)
#     updated_before = update_attendance(company, employee, before_cycle_dates, status)
#     updated_after = update_attendance(company, employee, after_cycle_dates, status)

#     frappe.db.commit()


#     last_date = getdate(nowdate()) + relativedelta(day=31)


#     # ----------------------------
#     # 6. Response
#     # ----------------------------
#     return {
#         "payroll_based_on": payroll_setting.payroll_based_on,
#         "cycle_start": str(cycle_start) if cycle_start else None,
#         "cycle_end": str(cycle_end) if cycle_end else None,
#         "last_date": str(last_date),


#         "current_cycle_dates": [str(d) for d in current_cycle_dates],
#         "current_cycle_count": len(current_cycle_dates),
#         "current_cycle_updated": len(updated_current),

#         "before_cycle_dates": [str(d) for d in before_cycle_dates],
#         "before_cycle_count": len(before_cycle_dates),
#         "before_cycle_updated": len(updated_before),

#         "after_cycle_dates": [str(d) for d in after_cycle_dates],
#         "after_cycle_count": len(after_cycle_dates),
#         "after_cycle_updated": len(updated_after),

#         "total_updated_attendance": (
#             len(updated_current)
#             + len(updated_before)
#             + len(updated_after)
#         )
#     }



import frappe
from frappe.utils import getdate, nowdate
from dateutil.relativedelta import relativedelta
from collections import defaultdict


# --------------------------------------------------
# Helper: Group dates by Month + Year
# --------------------------------------------------
def group_dates_by_month(dates):
    grouped = defaultdict(list)

    for d in dates:
        grouped[(d.year, d.month)].append(d)

    result = []
    for (year, month), date_list in sorted(grouped.items()):
        result.append({
            "month": date_list[0].strftime("%B"),
            "year": year,
            "dates": [str(dt) for dt in date_list],
            "count": len(date_list)
        })

    return result


# --------------------------------------------------
# Helper: Update Attendance
# --------------------------------------------------
def update_attendance(company, employee, dates, status):
    updated = []

    for d in dates:
        att_name = frappe.db.get_value(
            "Attendance",
            {
                "company": company,
                "employee": employee,
                "attendance_date": d
            },
            "name"
        )

        if att_name:
            frappe.db.set_value("Attendance", att_name, "status", status)
            updated.append(d)

    return updated


# --------------------------------------------------
# MAIN API
# --------------------------------------------------
@frappe.whitelist(methods=["POST"])
def edit_attendance():

    # ----------------------------
    # 1. Parse JSON Body
    # ----------------------------
    data = frappe.request.get_json()
    if not data:
        frappe.throw("Request body is empty")

    company = data.get("company")
    employee = data.get("employee")
    attendance_dates = data.get("attendance_dates")
    status = data.get("status", "Present")

    if not company or not employee or not attendance_dates:
        frappe.throw("company, employee and attendance_dates are mandatory")

    attendance_dates = [getdate(d) for d in attendance_dates]
    today = getdate(nowdate())

    # ----------------------------
    # 2. Payroll Settings
    # ----------------------------
    payroll_setting = frappe.get_single("Payroll Settings")

    current_cycle_dates = []
    before_cycle_dates = []
    after_cycle_dates = []

    cycle_start = None
    cycle_end = None

    # ==================================================
    # 3. LEAVE BASED PAYROLL (Calendar Month)
    # ==================================================
    if payroll_setting.payroll_based_on == "Leave":

        for d in attendance_dates:
            if d.month == today.month and d.year == today.year:
                current_cycle_dates.append(d)
            else:
                before_cycle_dates.append(d)

    # ==================================================
    # 4. ATTENDANCE BASED PAYROLL (21 → 20 Cycle)
    # ==================================================
    elif payroll_setting.payroll_based_on == "Attendance":

        start_day = payroll_setting.custom_attendance_start_date  # 21
        end_day = payroll_setting.custom_attendance_end_date      # 20

        if not start_day or not end_day:
            frappe.throw("Attendance cycle not configured")

        # ---- LAST COMPLETED PAYROLL CYCLE ----
        if today.day > end_day:
            cycle_end = today.replace(day=end_day)
        else:
            cycle_end = (today - relativedelta(months=1)).replace(day=end_day)

        cycle_start = (cycle_end - relativedelta(months=1)) + relativedelta(days=1)
        cycle_start = cycle_start.replace(day=start_day)

        # ---- Classify Dates ----
        for d in attendance_dates:
            if cycle_start <= d <= cycle_end:
                current_cycle_dates.append(d)
            elif d < cycle_start:
                before_cycle_dates.append(d)
            else:
                after_cycle_dates.append(d)

    else:
        frappe.throw("Invalid Payroll Based On value")

    # ----------------------------
    # 5. Update Attendance
    # ----------------------------
    updated_current = update_attendance(company, employee, current_cycle_dates, status)
    updated_before = update_attendance(company, employee, before_cycle_dates, status)
    updated_after = update_attendance(company, employee, after_cycle_dates, status)

    frappe.db.commit()

    # ----------------------------
    # 6. Last Date of Current Month
    # ----------------------------
    last_date = today + relativedelta(day=31)

    # ----------------------------
    # 7. Grouped Output
    # ----------------------------
    grouped_current = group_dates_by_month(current_cycle_dates)
    grouped_before = group_dates_by_month(before_cycle_dates)
    grouped_after = group_dates_by_month(after_cycle_dates)


    # ----------------------------
    # 8. Response
    # ----------------------------
    return {
        "payroll_based_on": payroll_setting.payroll_based_on,
        "cycle_start": str(cycle_start) if cycle_start else None,
        "cycle_end": str(cycle_end) if cycle_end else None,
        "last_date": str(last_date),

        "current_cycle": grouped_current,
        "current_cycle_count": len(current_cycle_dates),
        "current_cycle_updated": len(updated_current),

        "before_cycle": grouped_before,
        "before_cycle_count": len(before_cycle_dates),
        "before_cycle_updated": len(updated_before),

        "after_cycle": grouped_after,
        "after_cycle_count": len(after_cycle_dates),
        "after_cycle_updated": len(updated_after),

        "total_updated_attendance": (
            len(updated_current)
            + len(updated_before)
            + len(updated_after)
        )
    }
