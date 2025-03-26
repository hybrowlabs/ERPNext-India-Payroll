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
        
        try:
            company_doc = frappe.get_doc("Company", filters["company"])
        except frappe.DoesNotExistError:
            frappe.throw("Invalid company specified.")
        
        if not company_doc.basic_component or not company_doc.custom_da_component:
            frappe.throw("Please set Basic Component and DA Component in Company Master.")
        
        basic_component = company_doc.basic_component
        da_component = company_doc.custom_da_component
    else:
        frappe.throw("Company is a mandatory filter.")

    salary_slips = frappe.get_list(
        'Salary Slip',
        fields=["name", "employee", "custom_month", "custom_payroll_period", "company", "custom_statutory_grosspay"],
        filters=conditions,
        order_by="name DESC",
    )

    # Prepare list of salary slips with additional details
    detailed_salary_slips = []

    for slip in salary_slips:
        each_salary_slip = frappe.get_doc('Salary Slip', slip["name"])
        each_employee = frappe.get_doc("Employee", each_salary_slip.employee)

        # Initialize basic and DA
        basic = 0
        da = 0

        for earning in each_salary_slip.earnings:
            if earning.salary_component == basic_component:
                basic = earning.amount
            elif earning.salary_component == da_component:
                da = earning.amount

        # Calculate EPF values
        # epf_value = sum(
        #     d.amount for d in each_salary_slip.get("deductions", [])
        #     if frappe.get_value("Salary Component", d.salary_component, "component_type") == "EPF"
        # )
        
        # epf_value_employer = sum(
        #     d.amount for d in each_salary_slip.get("deductions", [])
        #     if frappe.get_value("Salary Component", d.salary_component, "component_type") == "EPF Employer"
        # )

        epf_employee=(min(round(float(basic or 0) + float(da or 0)), 15000) * 12) / 100,
        epf_employer=(min(round(float(basic or 0) + float(da or 0)), 15000) * 8.33) / 100,

        detailed_salary_slips.append({
            "employee": each_salary_slip.employee,
            "employee_name": each_salary_slip.employee_name,
            "custom_month": each_salary_slip.custom_month,
            "custom_payroll_period": each_salary_slip.custom_payroll_period,
            "company": each_salary_slip.company,
            "uan": getattr(each_employee, "custom_uan", None),
            "gross_pay": each_salary_slip.custom_statutory_grosspay,
            "epf_value_employee": (min(round(float(basic or 0) + float(da or 0)), 15000) * 12) / 100,
            "epf_value_employer": (min(round(float(basic or 0) + float(da or 0)), 15000) * 8.33) / 100,

            "epf_eps_diff": epf_employee-epf_employer,

            "epf_wages": min(round(basic + da), 15000),
            "eps_wages": min(round(basic + da), 15000),
            "edli_wages": min(round(basic + da), 15000),
            "ncp_days": each_salary_slip.custom_total_leave_without_pay,
            "refund": 0,
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
        {"fieldname": "epf_value_employee", "label": "EPF Contri Remitted(12%)", "fieldtype": "Currency", "width": 200},
        {"fieldname": "epf_value_employer", "label": "EPS Contri Remitted(8.33%)", "fieldtype": "Currency", "width": 200},
        {"fieldname": "epf_eps_diff", "label": "EDLI Contribution(0.5%)", "fieldtype": "Currency", "width": 200},
        {"fieldname": "ncp_days", "label": "NCP Days", "fieldtype": "Currency", "width": 150},
        {"fieldname": "refund", "label": "Refund Of Advances", "fieldtype": "Currency", "width": 150},
    ]

    # Fetch data using get_salary_slips
    data = get_salary_slips(filters)

    return columns, data
