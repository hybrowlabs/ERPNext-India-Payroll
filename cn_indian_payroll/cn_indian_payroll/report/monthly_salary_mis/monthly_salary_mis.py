import frappe

# Column definitions
columns = [
    {"fieldname": "month", "label": "Month", "fieldtype": "Data", "width": 150},
    {"fieldname": "payroll_period", "label": "Payroll Period", "fieldtype": "Data", "width": 150},
    {"fieldname": "no_of_employee", "label": "No. of Employee", "fieldtype": "Data", "width": 150},
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

    # Initialize conditions for filtering salary slips
    conditions = {"docstatus": ["in", [0, 1]]}

    if filters.get("select_month"):
        conditions["custom_month"] = filters["select_month"]

    if filters.get("payroll_period"):
        conditions["custom_payroll_period"] = filters["payroll_period"]

    if filters.get("company"):
        conditions["company"] = filters["company"]

    # Debugging: print conditions to check filters being applied
    # frappe.msgprint(str(conditions))

    # Fetch salary slips based on conditions
    all_salary_slips = frappe.get_list(
        'Salary Slip',
        fields=["*"],
        filters=conditions,
        order_by="name DESC",
    )

    # Debugging: print fetched salary slips
    # frappe.msgprint(str(all_salary_slips))

    # Aggregating results
    aggregated_data = {}

    for slip in all_salary_slips:
        month = slip.custom_month
        payroll_period = slip.custom_payroll_period

        key = (month, payroll_period)

        if key not in aggregated_data:
            aggregated_data[key] = {
                "no_of_employee": 0,
                "ctc_pa": 0,
                "ctc_pm": 0,
                "gross_pay": 0,
                "total_income": 0,
                "total_deduction": 0,
                "total_net_pay": 0
            }

        # Increment the employee count
        aggregated_data[key]["no_of_employee"] += 1

        # Accumulate financial details
        aggregated_data[key]["ctc_pa"] += slip.custom_annual_ctc or 0
        aggregated_data[key]["ctc_pm"] += (slip.custom_annual_ctc or 0) / 12
        aggregated_data[key]["gross_pay"] += slip.custom_statutory_grosspay or 0
        aggregated_data[key]["total_income"] += slip.custom_total_income or 0
        aggregated_data[key]["total_deduction"] += slip.custom_total_deduction_amount or 0
        aggregated_data[key]["total_net_pay"] += slip.custom_net_pay_amount or 0

    # Prepare final data for return
    data = []
    for (month, payroll_period), values in aggregated_data.items():
        data.append({
            "month": month,
            "payroll_period": payroll_period,
            "no_of_employee": values["no_of_employee"],
            "ctc_pa": values["ctc_pa"],
            "ctc_pm": values["ctc_pm"],
            "gross_pay": values["gross_pay"],
            "total_income": values["total_income"],
            "total_deduction": values["total_deduction"],
            "total_net_pay": values["total_net_pay"],
        })

    return data

def execute(filters=None):
    # Fetch the salary slips data
    data = get_salary_slips(filters)

    # Return the column definitions and the data for rendering
    return columns, data
