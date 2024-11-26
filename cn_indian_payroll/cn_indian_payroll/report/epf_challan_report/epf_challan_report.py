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

    # Fetch all Salary Slips based on conditions
    salary_slips = frappe.get_list(
        'Salary Slip',
        fields=["name", "employee", "custom_month", "custom_payroll_period", "company", "custom_statutory_grosspay"],
        filters=conditions,
        order_by="name DESC",
        limit_page_length=0  # Fetch all records
    )

    # Prepare list of salary slips with additional details
    detailed_salary_slips = []
    for slip in salary_slips:
        each_salary_slip = frappe.get_doc('Salary Slip', slip["name"])
        each_employee = frappe.get_doc("Employee", each_salary_slip.employee)

        # Calculate EPF value from deductions
        epf_value = 0
        if hasattr(each_salary_slip, "deductions") and each_salary_slip.deductions:
            for deduction in each_salary_slip.deductions:
                salary_component = frappe.get_doc("Salary Component", deduction.salary_component)
                if salary_component.component_type == "EPF":
                    epf_value += deduction.amount

        # Calculate EPF Employer value from earnings
        epf_value_employer = 0
        if hasattr(each_salary_slip, "earnings") and each_salary_slip.earnings:
            for earning in each_salary_slip.earnings:
                salary_component = frappe.get_doc("Salary Component", earning.salary_component)
                if salary_component.component_type == "EPF Employer":
                    epf_value_employer += earning.amount

        # Append enriched data for the report
        detailed_salary_slips.append({
            "employee": each_salary_slip.employee,
            "employee_name": each_salary_slip.employee_name,
            "custom_month": each_salary_slip.custom_month,
            "custom_payroll_period": each_salary_slip.custom_payroll_period,
            "company": each_salary_slip.company,
            "uan": getattr(each_employee, "custom_uan", None),
            "gross_pay": each_salary_slip.custom_statutory_grosspay,
            "epf_value_employee": epf_value,
            "epf_value_employer": epf_value_employer,
            "epf_wages":0,
            "eps_wages":0,
            "edli_wages":0,
            "epf_eps_diff":epf_value-epf_value_employer,
            "ncp_days":0,
            "refund":0

        })

    return detailed_salary_slips

def execute(filters=None):
    # Define columns for the report
    columns = [
        {"fieldname": "uan", "label": "UAN", "fieldtype": "Data", "width": 150},
        {"fieldname": "employee", "label": "Employee", "fieldtype": "Link", "options": "Employee", "width": 150},
        {"fieldname": "employee_name", "label": "Employee Name", "fieldtype": "Data", "width": 200},
        {"fieldname": "custom_month", "label": "Month", "fieldtype": "Data", "width": 100},
        {"fieldname": "custom_payroll_period", "label": "Payroll Period", "fieldtype": "Data", "width": 150},
        {"fieldname": "company", "label": "Company", "fieldtype": "Link", "options": "Company", "width": 150},
        {"fieldname": "gross_pay", "label": "Gross Pay", "fieldtype": "Currency", "width": 150},
        {"fieldname": "epf_wages", "label": "EPF Wages", "fieldtype": "Currency", "width": 150},
        {"fieldname": "eps_wages", "label": "EPS Wages", "fieldtype": "Currency", "width": 150},
        {"fieldname": "edli_wages", "label": "EDLI Wages", "fieldtype": "Currency", "width": 150},
        {"fieldname": "epf_value_employee", "label": "EPF Contri Remitted", "fieldtype": "Currency", "width": 150},
        {"fieldname": "epf_value_employer", "label": "EPS Contri Remitted", "fieldtype": "Currency", "width": 150},
        {"fieldname": "epf_eps_diff", "label": "EPF EPS Diff Remitted", "fieldtype": "Currency", "width": 150},
        {"fieldname": "ncp_days", "label": "NCP Days", "fieldtype": "Currency", "width": 150},
        {"fieldname": "refund", "label": "Refund Of Advances", "fieldtype": "Currency", "width": 150},
    ]

    # Fetch data using get_salary_slips
    data = get_salary_slips(filters)

    return columns, data
