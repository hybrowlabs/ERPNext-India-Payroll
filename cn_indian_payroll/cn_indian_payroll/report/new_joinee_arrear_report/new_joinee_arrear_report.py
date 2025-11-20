

import frappe


def execute(filters=None):
    data, components = get_new_joinee_arrear(filters)
    columns = get_columns(components)
    return columns, data


def get_new_joinee_arrear(filters=None):
    if filters is None:
        filters = {}

    conditions = {"docstatus": 1}

    if filters.get("employee"):
        conditions["employee"] = filters["employee"]

    if filters.get("company"):
        conditions["company"] = filters["company"]

    if filters.get("joining_from") and filters.get("joining_to"):
        conditions["joining_date"] = ["between", [filters["joining_from"], filters["joining_to"]]]
    elif filters.get("joining_from"):
        conditions["joining_date"] = [">=", filters["joining_from"]]
    elif filters.get("joining_to"):
        conditions["joining_date"] = ["<=", filters["joining_to"]]

    records = frappe.get_list(
        "New Joining Arrear",
        filters=conditions,
        fields=[
            "name",
            "employee",
            "employee_name",
            "company",
            "joining_date",
            "number_of_present_days",
            "payout_date",
            "department",
            "designation",
        ],
    )

    data = []
    all_components = set()

    for row in records:
        arrear_doc = frappe.get_doc("New Joining Arrear", row.name)

        row_data = {
            "doc_id": row.name,
            "employee": row.employee,
            "employee_name": row.employee_name,
            "department": row.department,
            "designation": row.designation,
            "company": row.company,
            "joining_date": row.joining_date,
            "number_of_present_days": row.number_of_present_days,
            "payout_date": row.payout_date,
        }

        # Add earnings
        for e in arrear_doc.earning_component or []:
            row_data[e.salary_component] = e.amount
            all_components.add(e.salary_component)

        # Add deductions
        for d in arrear_doc.deduction_component or []:
            row_data[d.salary_component] = d.amount
            all_components.add(d.salary_component)

        data.append(row_data)

    return data, sorted(all_components)


def get_columns(components):
    base_columns = [
        {"label": "Document ID", "fieldname": "doc_id", "fieldtype": "Link", "options": "New Joining Arrear", "width": 120},
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 120},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 150},
        {"label": "Department", "fieldname": "department", "fieldtype": "Data", "width": 150},
        {"label": "Designation", "fieldname": "designation", "fieldtype": "Data", "width": 150},
        {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
        {"label": "Joining Date", "fieldname": "joining_date", "fieldtype": "Date", "width": 120},
        {"label": "Present Days", "fieldname": "number_of_present_days", "fieldtype": "Float", "width": 120},
        {"label": "Payout Date", "fieldname": "payout_date", "fieldtype": "Date", "width": 120},
    ]

    component_columns = [
        {"label": comp, "fieldname": comp, "fieldtype": "Currency", "width": 120}
        for comp in components
    ]

    return base_columns + component_columns



def get_columns(components):
    base_columns = [
		{"label": "Document ID", "fieldname": "doc_id", "fieldtype": "Link", "options": "New Joining Arrear", "width": 120},
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 120},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 150},
		{"label": "Department", "fieldname": "department", "fieldtype": "Data", "width": 150},
		{"label": "Designation", "fieldname": "designation", "fieldtype": "Data", "width": 150},
        {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
        {"label": "Joining Date", "fieldname": "joining_date", "fieldtype": "Date", "width": 120},
        {"label": "Present Days", "fieldname": "number_of_present_days", "fieldtype": "Float", "width": 120},
        {"label": "Payout Date", "fieldname": "payout_date", "fieldtype": "Date", "width": 120},
    ]

    # Dynamically add each salary component as a column
    component_columns = [
        {"label": comp, "fieldname": comp, "fieldtype": "Currency", "width": 120}
        for comp in components
    ]

    return base_columns + component_columns
