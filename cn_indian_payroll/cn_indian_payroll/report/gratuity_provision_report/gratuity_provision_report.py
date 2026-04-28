import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_all_gratuity(filters)
    return columns, data


def get_all_gratuity(filters=None):
    if filters is None:
        filters = {}

    conditions = {"docstatus": ["in", [0, 1]]}

    if filters.get("employee"):
        conditions["employee"] = filters["employee"]
    if filters.get("payroll_period"):
        conditions["custom_payroll_period"] = filters["payroll_period"]
    if filters.get("month"):
        conditions["custom_month"] = filters["month"]
    if filters.get("company"):
        conditions["company"] = filters["company"]

    data = []

    salary_slips = frappe.get_all(
        "Salary Slip",
        filters=conditions,
        fields=[
            "name", "employee", "employee_name", "company",
            "custom_payroll_period", "custom_month",
            "branch", "department", "designation",
            "total_working_days", "custom_total_leave_without_pay",
            "payment_days", "gross_pay"
        ]
    )

    for slip in salary_slips:
        slip_doc = frappe.get_doc("Salary Slip", slip.name)
        employee_doc = frappe.get_doc("Employee", slip.employee)
        company_doc = frappe.get_doc("Company", slip.company)

        gratuity_amount = 0
        gratuity_component = None
        basic_amount = 0
        pt_amount = 0

        # 🔁 Earnings Loop
        for earning in slip_doc.earnings:
            comp = frappe.get_doc("Salary Component", earning.salary_component)

            if comp.component_type == "Gratuity":
                gratuity_amount += earning.amount
                gratuity_component = comp.name

            if earning.salary_component == company_doc.basic_component:
                basic_amount += earning.amount

        # 🔁 Deductions Loop (PT)
        for deduction in slip_doc.deductions:
            comp = frappe.get_doc("Salary Component", deduction.salary_component)

            if comp.component_type == "Professional Tax":
                pt_amount += deduction.amount

        # Only append if gratuity exists
        if gratuity_amount:
            data.append({
                "salary_slip": slip.name,
                "employee": slip.employee,
                "employee_name": slip.employee_name,
                "designation": employee_doc.designation,
                "department": employee_doc.department,
                "branch": employee_doc.branch,
                "company": slip.company,
                "payroll_period": slip.custom_payroll_period,
                "month": slip.custom_month,

                "pt_state": employee_doc.custom_pt_state if hasattr(employee_doc, "custom_pt_state") else "",
                "pt_location": employee_doc.custom_pt_location if hasattr(employee_doc, "custom_pt_location") else "",

                "working_days": slip.total_working_days,
                "total_lwp": slip.custom_total_leave_without_pay,
                "payment_day": slip.payment_days,
                "gross_pay": slip.gross_pay,

                "pt_amount": pt_amount,

                "gratuity_amount": gratuity_amount,
                "gratuity_component": gratuity_component,
                "basic": basic_amount,
                "number_of_years_completed": 5
            })

    return data


def get_columns():
    return [
        {"label": "Salary Slip", "fieldname": "salary_slip", "fieldtype": "Link", "options": "Salary Slip", "width": 150},
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 150},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},

        {"label": "Designation", "fieldname": "designation", "fieldtype": "Data", "width": 150},
        {"label": "Department", "fieldname": "department", "fieldtype": "Link", "options": "Department", "width": 150},
        {"label": "Branch", "fieldname": "branch", "fieldtype": "Link", "options": "Branch", "width": 150},

        {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
        {"label": "Payroll Period", "fieldname": "payroll_period", "fieldtype": "Link", "options": "Payroll Period", "width": 150},
        {"label": "Month", "fieldname": "month", "fieldtype": "Data", "width": 100},




        {"label": "Gratuity Component", "fieldname": "gratuity_component", "fieldtype": "Data", "width": 180},
        {"label": "Gratuity Amount", "fieldname": "gratuity_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Basic Amount", "fieldname": "basic", "fieldtype": "Currency", "width": 150},

        {"label": "Years Completed", "fieldname": "number_of_years_completed", "fieldtype": "Data", "width": 150},
    ]