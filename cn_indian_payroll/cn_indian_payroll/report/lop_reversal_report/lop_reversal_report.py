

import frappe

def execute(filters=None):
    data, components = get_lop_reversal(filters)
    columns = get_columns(components)
    return columns, data


def get_lop_reversal(filters=None):
    if filters is None:
        filters = {}

    conditions = {"docstatus": 1}

    if filters.get("employee"):
        conditions["employee"] = filters["employee"]

    if filters.get("company"):
        conditions["company"] = filters["company"]


    if filters.get("payroll_period"):
        conditions["payroll_period"] = filters["payroll_period"]

    if filters.get("lop_reversal_month"):
        conditions["lop_month_reversal"] = filters["lop_reversal_month"]



    records = frappe.get_list(
        "LOP Reversal",
        filters=conditions,
        fields=["*"],
    )

    data = []
    all_components = set()

    for row in records:
        arrear_doc = frappe.get_doc("LOP Reversal", row.name)

        # Replace these field names with actual ones in your doctype
        row_data = {
            "doc_id": row.name,
			"month":row.lop_month_reversal,
            "employee": row.employee,
            "employee_name": row.employee_name,

            "company": row.company,
            "working_days": getattr(row, "working_days", 0),

            "max_lop_days": getattr(row, "max_lop_days", 0),
            "number_of_days": getattr(row, "number_of_days", 0),
            "additional_salary_date": getattr(row, "additional_salary_date", None),
        }

        # Add earnings
        for e in arrear_doc.arrear_breakup or []:
            row_data[e.salary_component] = e.amount
            all_components.add(e.salary_component)

        # Add deductions
        for d in arrear_doc.arrear_deduction_breakup or []:
            row_data[d.salary_component] = d.amount
            all_components.add(d.salary_component)

        data.append(row_data)

    return data, sorted(all_components)


def get_columns(components):
    base_columns = [
        {"label": "Document ID", "fieldname": "doc_id", "fieldtype": "Link", "options": "LOP Reversal", "width": 120},
        {"label": "Month", "fieldname": "month", "fieldtype": "Data","width": 120},
		{"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 120},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 150},

        {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
        {"label": "Working Days", "fieldname": "working_days", "fieldtype": "Float", "width": 120},
        {"label": "Max LOP Days", "fieldname": "max_lop_days", "fieldtype": "Float", "width": 120},
        {"label": "Number of Days Reversed", "fieldname": "number_of_days", "fieldtype": "Float", "width": 120},
        {"label": "Payout Date", "fieldname": "additional_salary_date", "fieldtype": "Date", "width": 120},
    ]

    component_columns = [
        {"label": comp, "fieldname": comp, "fieldtype": "Currency", "width": 120}
        for comp in components
    ]

    return base_columns + component_columns
