import frappe


def execute(filters=None):
    data, components = get_new_joinee_arrear(filters)
    columns = get_columns(components)
    return columns, data


def get_new_joinee_arrear(filters=None):
    if filters is None:
        filters = {}

    conditions = {"docstatus": ["in", [0, 1]]}

    if filters.get("employee"):
        conditions["employee"] = filters["employee"]

    if filters.get("company"):
        conditions["company"] = filters["company"]

    if filters.get("status"):
        conditions["status"] = filters["status"]

    records = frappe.get_list(
        "Salary Appraisal Calculation",
        filters=conditions,
        fields=[
            "name",
            "employee",
            "employee_name",
            "company",
            "posting_date",
            "status",
            "new_from_date",
        ],
    )

    data = []
    all_components = set()

    for row in records:
        arrear_doc = frappe.get_doc("Salary Appraisal Calculation", row.name)

        row_data = {
            "doc_id": row.name,
            "employee": row.employee,
            "employee_name": row.employee_name,
            "revised_effective_date": row.posting_date,
            "company": row.company,
        }

        # Add earnings
        for e in arrear_doc.arrear_summary or []:
            row_data[e.salary_component] = e.arrear_amount
            all_components.add(e.salary_component)

        data.append(row_data)

    return data, sorted(all_components)


def get_columns(components):
    base_columns = [
        {
            "label": "Document ID",
            "fieldname": "doc_id",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": "Employee",
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 120,
        },
        {
            "label": "Employee Name",
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "Company",
            "fieldname": "company",
            "fieldtype": "Link",
            "options": "Company",
            "width": 150,
        },
        {
            "label": "Date",
            "fieldname": "revised_effective_date",
            "fieldtype": "Date",
            "width": 120,
        },
    ]

    component_columns = [
        {"label": comp, "fieldname": comp, "fieldtype": "Currency", "width": 120}
        for comp in components
    ]

    return base_columns + component_columns


def get_columns(components):
    base_columns = [
        {
            "label": "Document ID",
            "fieldname": "doc_id",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": "Employee",
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 120,
        },
        {
            "label": "Employee Name",
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "Company",
            "fieldname": "company",
            "fieldtype": "Link",
            "options": "Company",
            "width": 150,
        },
        {
            "label": " Date",
            "fieldname": "revised_effective_date",
            "fieldtype": "Date",
            "width": 120,
        },
    ]

    # Dynamically add each salary component as a column
    component_columns = [
        {"label": comp, "fieldname": comp, "fieldtype": "Currency", "width": 120}
        for comp in components
    ]

    return base_columns + component_columns
