import frappe


def execute(filters=None):
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": "EMP ID", "fieldname": "employee", "fieldtype": "Data"},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data"},
        {"label": "Location", "fieldname": "branch", "fieldtype": "Data"},
        {"label": "Business Unit", "fieldname": "company", "fieldtype": "Data"},
        {"label": "Designation", "fieldname": "designation", "fieldtype": "Data"},
        {"label": "Department", "fieldname": "department", "fieldtype": "Data"},
        {"label": "Financial Year", "fieldname": "financial_year", "fieldtype": "Data"},
        {"label": "Perquisite Type", "fieldname": "perq_type", "fieldtype": "Data"},
        {"label": "Month", "fieldname": "month", "fieldtype": "Data"},
        {"label": "Perquisite Value", "fieldname": "perq_value", "fieldtype": "Currency"},
        {"label": "Perquisite Paid Value", "fieldname": "perq_paid", "fieldtype": "Currency"},
    ]


def get_data(filters):
    conditions = ""

    # ✅ Filters
    if filters.get("company"):
        conditions += " AND emp.company = %(company)s"

    if filters.get("employee"):
        conditions += " AND ss.employee = %(employee)s"

    if filters.get("branch"):
        conditions += " AND emp.branch = %(branch)s"

    if filters.get("department"):
        conditions += " AND emp.department = %(department)s"

    if filters.get("designation"):
        conditions += " AND emp.designation = %(designation)s"

    if filters.get("from_date") and filters.get("to_date"):
        conditions += " AND ss.start_date BETWEEN %(from_date)s AND %(to_date)s"

    # ✅ Final Query (LWF Style Aggregation)
    data = frappe.db.sql("""
        SELECT
            emp.name as employee,
            emp.employee_name,
            emp.branch,
            emp.company,
            emp.designation,
            emp.department,

            CONCAT(YEAR(ss.start_date), '-', YEAR(ss.start_date)+1) as financial_year,

            sd.salary_component AS perq_type,

            DATE_FORMAT(ss.start_date, '%%b-%%Y') as month,
            COALESCE(SUM(CASE 
                WHEN sd.salary_component LIKE '%%Perquisite%%'
                THEN sd.amount 
            END), 0) as perq_value,
            COALESCE(SUM(CASE 
                WHEN sd.salary_component LIKE '%%Perquisite%%'
                THEN sd.amount 
            END), 0) as perq_paid

        FROM `tabSalary Slip` ss

        LEFT JOIN `tabEmployee` emp 
            ON emp.name = ss.employee

        LEFT JOIN `tabSalary Detail` sd 
        ON sd.parent = ss.name
        AND sd.parentfield = 'earnings'
        AND sd.salary_component LIKE '%%Perquisite%%'

        WHERE ss.docstatus = 1
        {conditions}

        GROUP BY ss.name
        ORDER BY ss.start_date DESC
    """.format(conditions=conditions), filters, as_dict=1)

    return data