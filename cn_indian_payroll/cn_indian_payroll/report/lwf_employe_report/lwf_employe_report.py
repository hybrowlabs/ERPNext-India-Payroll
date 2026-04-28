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
        {"label": "Designation", "fieldname": "designation", "fieldtype": "Data"},
        {"label": "Department", "fieldname": "department", "fieldtype": "Data"},
        {"label": "LWF State", "fieldname": "custom_lwf_state", "fieldtype": "Data"},
        {"label": "LWF Designation", "fieldname": "custom_lwf_designation", "fieldtype": "Data"},
        {"label": "LWF Gross", "fieldname": "lwf_gross", "fieldtype": "Currency"},
        {"label": "LWF Employee Contribution", "fieldname": "lwf_employee", "fieldtype": "Currency"},
        {"label": "LWF Employer Contribution", "fieldname": "lwf_employer", "fieldtype": "Currency"},
        {"label": "Total LWF Contribution", "fieldname": "total_lwf", "fieldtype": "Currency"},
    ]


def get_data(filters):
    conditions = ""

    if filters.get("from_date") and filters.get("to_date"):
        conditions += " AND ss.start_date BETWEEN %(from_date)s AND %(to_date)s"

    if filters.get("employee"):
        conditions += " AND ss.employee = %(employee)s"

    data = frappe.db.sql("""
        SELECT
            emp.name as employee,
            emp.employee_name,
            emp.branch,
            emp.designation,
            emp.department,

            ssa.custom_lwf_state,
            ssa.custom_lwf_designation,

            ss.gross_pay as lwf_gross,

            COALESCE(SUM(CASE 
                WHEN sd.salary_component LIKE 'LWF Employee%%' 
                THEN sd.amount END), 0) as lwf_employee,

            COALESCE(SUM(CASE 
                WHEN sd.salary_component LIKE 'LWF Employer%%' 
                THEN sd.amount END), 0) as lwf_employer,

            COALESCE(SUM(CASE 
                WHEN sd.salary_component LIKE 'LWF Employee%%' 
                THEN sd.amount END), 0)
            +
            COALESCE(SUM(CASE 
                WHEN sd.salary_component LIKE 'LWF Employer%%' 
                THEN sd.amount END), 0)
            as total_lwf

        FROM `tabSalary Slip` ss

        LEFT JOIN `tabEmployee` emp 
            ON emp.name = ss.employee

        LEFT JOIN `tabSalary Structure Assignment` ssa 
            ON ssa.employee = ss.employee
            AND ssa.docstatus = 1
            AND ssa.from_date <= ss.start_date

        LEFT JOIN `tabSalary Detail` sd 
            ON sd.parent = ss.name

        WHERE ss.docstatus = 1
        {conditions}

        GROUP BY ss.name
        ORDER BY ss.start_date DESC
    """.format(conditions=conditions), filters, as_dict=1)

    return data