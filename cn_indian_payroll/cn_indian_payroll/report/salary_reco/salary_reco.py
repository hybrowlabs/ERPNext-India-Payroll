import frappe

columns = [
    {
        "fieldname": "employee",
        "label": "Employee ID",
        "fieldtype": "Link",
        "width": 150,
        "options": "Employee",
    },
    {"fieldname": "employee_name", "label": "Employee Name", "fieldtype": "Data", "width": 150},
    {"fieldname": "current_month", "label": "Current Month", "fieldtype": "Data", "width": 150},
    {"fieldname": "current_gross_pay", "label": "Gross Pay", "fieldtype": "Data", "width": 150},
    {"fieldname": "previous_month", "label": "Previous Month", "fieldtype": "Data", "width": 150},
    {"fieldname": "previous_gross_pay", "label": "Gross Pay", "fieldtype": "Data", "width": 150},
    {"fieldname": "difference", "label": "Difference", "fieldtype": "Data", "width": 150},
    {"fieldname": "remark", "label": "Remark", "fieldtype": "Data", "width": 150},
    {"fieldname": "status", "label": "Status", "fieldtype": "Data", "width": 150},
]

_MONTH_NAMES = [
    "",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def get_salary_slips(filters=None):
    if filters is None:
        filters = {}

    current_date = frappe.utils.getdate(frappe.utils.nowdate())
    month_number = current_date.month
    year_number = current_date.year

    if month_number == 1:
        previous_month_number = 12
        year_number = year_number - 1  # fix: was a no-op (year_number - 1 without assignment)
    else:
        previous_month_number = month_number - 1

    current_month_name = _MONTH_NAMES[month_number]
    previous_month_name = _MONTH_NAMES[previous_month_number]

    conditions1 = {
        "docstatus": ["in", [0, 1]],
        "custom_month": filters.get("previous_month") or previous_month_name,
    }
    conditions2 = {
        "docstatus": ["in", [0, 1]],
        "custom_month": filters.get("current_month") or current_month_name,
    }

    if filters.get("employee"):
        conditions1["employee"] = filters["employee"]
        conditions2["employee"] = filters["employee"]

    if filters.get("company"):
        conditions1["company"] = filters["company"]
        conditions2["company"] = filters["company"]

    slip_fields = ["name", "employee", "employee_name", "custom_month", "custom_statutory_grosspay"]

    prev_slips = frappe.get_list(
        "Salary Slip", fields=slip_fields, filters=conditions1, order_by="name desc", limit_page_length=0
    )
    curr_slips = frappe.get_list(
        "Salary Slip", fields=slip_fields, filters=conditions2, order_by="name desc", limit_page_length=0
    )

    # Batch-fetch employee status — one query instead of N
    all_emp_ids = list({s.employee for s in prev_slips} | {s.employee for s in curr_slips})
    emp_status_map = {}
    if all_emp_ids:
        for row in frappe.get_all(
            "Employee", filters={"name": ["in", all_emp_ids]}, fields=["name", "status"]
        ):
            emp_status_map[row.name] = row.status

    final_data_map = {}

    for slip in prev_slips:
        final_data_map[slip.employee] = {
            "employee": slip.employee,
            "employee_name": slip.employee_name,
            "previous_month": slip.custom_month,
            "previous_gross_pay": slip.custom_statutory_grosspay or 0,
            "current_month": "-",
            "current_gross_pay": 0,
            "difference": 0,
            "status": emp_status_map.get(slip.employee, ""),
            "remark": "",
        }

    for slip in curr_slips:
        gross = slip.custom_statutory_grosspay or 0
        if slip.employee not in final_data_map:
            final_data_map[slip.employee] = {
                "employee": slip.employee,
                "employee_name": slip.employee_name,
                "previous_month": "-",
                "previous_gross_pay": 0,
                "current_month": slip.custom_month,
                "current_gross_pay": gross,
                "difference": gross,
                "status": emp_status_map.get(slip.employee, ""),
                "remark": "",
            }
        else:
            rec = final_data_map[slip.employee]
            rec["current_month"] = slip.custom_month
            rec["current_gross_pay"] = gross
            rec["difference"] = gross - rec["previous_gross_pay"]
            rec["status"] = emp_status_map.get(slip.employee, "")

    return list(final_data_map.values())


def execute(filters=None):
    return columns, get_salary_slips(filters)
