import frappe

def get_salary_slips(filters=None):
    if filters is None:
        filters = {}

    # Initialize conditions for filtering Salary Slips
    conditions = {"docstatus": ["in", [0, 1]]}

    if filters.get("month"):
        conditions["custom_month"] = filters["month"]

    if filters.get("payroll_period"):
        conditions["custom_payroll_period"] = filters["payroll_period"]

    if filters.get("company"):
        conditions["company"] = filters["company"]

    # Debugging message to display applied conditions
    # frappe.msgprint(f"Filters Applied: {str(conditions)}")

    # Fetch all Salary Slips based on conditions
    salary_slips = frappe.get_list(
        'Salary Slip',
        fields=["name", "employee", "custom_month", "custom_payroll_period", "company"],
        filters=conditions,
        order_by="name DESC",
        limit_page_length=0  # Fetch all records
    )

    # Prepare list of salary slips with additional details
    detailed_salary_slips = []
    for slip in salary_slips:
        each_salary_slip = frappe.get_doc('Salary Slip', slip.name)
        each_employee = frappe.get_doc("Employee", each_salary_slip.employee)


        # Append enriched data for the report
        detailed_salary_slips.append({
            "employee": each_salary_slip.employee,
			"employee_name": each_salary_slip.employee_name,
            "custom_month": each_salary_slip.custom_month,
            "custom_payroll_period": each_salary_slip.custom_payroll_period,
            "company": each_salary_slip.company,
            "uan": each_employee.custom_uan if hasattr(each_employee, "custom_uan") else None,
			"gross_pay":each_salary_slip.custom_statutory_grosspay
        })

    return detailed_salary_slips

def execute(filters=None):
    # Define columns for the report
    columns = [
		{"fieldname": "uan", "label": "UAN", "fieldtype": "Data"},
        {"fieldname": "employee", "label": "Employee", "fieldtype": "Link", "options": "Employee"},
		{"fieldname": "employee_name", "label": "Employee Name", "fieldtype": "Data"},
        {"fieldname": "custom_month", "label": "Month", "fieldtype": "Data"},
        {"fieldname": "custom_payroll_period", "label": "Payroll Period", "fieldtype": "Data"},
        {"fieldname": "company", "label": "Company", "fieldtype": "Link", "options": "Company"},
		{"fieldname": "gross_pay", "label": "Gross Pay", "fieldtype": "Float"},
		
       
    ]

    # Fetch data using get_salary_slips
    data = get_salary_slips(filters)

    return columns, data
