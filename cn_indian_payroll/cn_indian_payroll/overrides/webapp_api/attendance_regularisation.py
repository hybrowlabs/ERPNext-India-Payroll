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
                "posting_date": attendance.attendance_date,
                "status": "Absent",
                "leave_type": None
            })


        elif attendance.status in ["On Leave", "Half Day"] and attendance.leave_type:
            leave_type = frappe.get_doc("Leave Type", attendance.leave_type)

            if leave_type.is_lwp:
                lwp_dates.append({
                    "posting_date": attendance.attendance_date,
                    "status": attendance.status,
                    "leave_type": attendance.leave_type
                })

    return lwp_dates
