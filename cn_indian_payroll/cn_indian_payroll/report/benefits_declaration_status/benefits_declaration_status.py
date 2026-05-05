import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {
            "label": _("EMP ID"),
            "fieldname": "emp_id",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 120
        },
        {
            "label": _("Employee Name"),
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "label": _("Location"),
            "fieldname": "location",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Designation"),
            "fieldname": "designation",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Department"),
            "fieldname": "department",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Benefit Proof Open"),
            "fieldname": "benefit_proof_open",
            "fieldtype": "Data",
            "width": 150
        }
    ]


def get_data(filters):
    conditions = ""

    if filters.get("company"):
        conditions += " AND emp.company = %(company)s"

    if filters.get("employee"):
        conditions += " AND emp.name = %(employee)s"

    if filters.get("from_date") and filters.get("to_date"):
        conditions += " AND ebc.posting_date BETWEEN %(from_date)s AND %(to_date)s"

    query = f"""
        SELECT
            emp.name AS emp_id,
            emp.employee_name,
            emp.branch AS location,
            emp.designation,
            emp.department,
            ebc.custom_status as benefit_proof_open

        FROM `tabEmployee Benefit Claim` ebc

        LEFT JOIN `tabEmployee` emp
            ON emp.name = ebc.employee

        WHERE emp.status = 'Active'
        {conditions}

        ORDER BY emp.name
    """

    return frappe.db.sql(query, filters, as_dict=True)