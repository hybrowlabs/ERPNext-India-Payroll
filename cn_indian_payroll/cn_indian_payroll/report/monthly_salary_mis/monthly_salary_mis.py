import frappe

# Column definitions
columns = [
    {"fieldname": "month", "label": "Month", "fieldtype": "Data", "width": 150},
    {"fieldname": "payroll_period", "label": "Payroll Period", "fieldtype": "Data", "width": 150},
    {"fieldname": "no_of_employee", "label": "No.of Employee", "fieldtype": "Data", "width": 150},
    {"fieldname": "ctc_pa", "label": "CTC P.A", "fieldtype": "Currency", "width": 150},
    {"fieldname": "ctc_pm", "label": "CTC P.M", "fieldtype": "Currency", "width": 150},
    {"fieldname": "gross_pay", "label": "Gross Pay", "fieldtype": "Currency", "width": 150},
    {"fieldname": "total_income", "label": "Total Income", "fieldtype": "Currency", "width": 150},
    {"fieldname": "total_deduction", "label": "Total Deduction", "fieldtype": "Currency", "width": 150},
    {"fieldname": "total_net_pay", "label": "Total Net Pay", "fieldtype": "Currency", "width": 150},
]

def get_salary_slips(filters=None):
    if filters is None:
        filters = {}

    conditions = {"docstatus": ["in", [0, 1]]}

    if filters.get("select_month"):
        conditions["custom_month"] = filters["select_month"]

    if filters.get("payroll_period"):
        conditions["custom_payroll_period"] = filters["payroll_period"]

    if filters.get("company"):
        conditions["company"] = filters["company"]

    all_salary_slip = frappe.get_list(
        'Salary Slip',
        fields=["*"],
        filters=conditions,
        order_by="name DESC",
    )

    total_ctc_pa = 0  
    total_employees = len(all_salary_slip)
    total_grosspay = 0
    total_income = 0
    total_deductions = 0
    total_net_pay = 0
    
    custom_month = ""
    payroll_period = ""

    for eachdoc in all_salary_slip:
        total_ctc_pa += eachdoc.custom_annual_ctc or 0
        custom_month = eachdoc.custom_month
        payroll_period = eachdoc.custom_payroll_period

        total_grosspay += eachdoc.custom_statutory_grosspay or 0
        total_income += eachdoc.custom_total_income or 0
        total_deductions += eachdoc.custom_total_deduction_amount or 0
        total_net_pay += eachdoc.custom_net_pay_amount or 0

    ctc_pm = total_ctc_pa / 12 if total_ctc_pa else 0

    data = [{
        "month": custom_month,
        "payroll_period": payroll_period,
        "no_of_employee": total_employees,
        "ctc_pa": total_ctc_pa,
        "ctc_pm": ctc_pm,
        "gross_pay": total_grosspay,
        "total_income": total_income,
        "total_deduction": total_deductions,
        "total_net_pay": total_net_pay,
    }]

    return data

def execute(filters=None):
    # Fetch the salary slips data
    data = get_salary_slips(filters)

    return columns, data
