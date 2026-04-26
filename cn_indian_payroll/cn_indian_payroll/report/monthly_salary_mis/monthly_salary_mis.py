import frappe


def execute(filters=None):
    return get_columns(), get_salary_slips(filters)


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

    slips = frappe.get_all(
        "Salary Slip",
        filters=conditions,
        fields=[
            "custom_month",
            "custom_payroll_period",
            "custom_annual_ctc",
            "custom_total_income",
            "custom_total_deduction_amount",
            "custom_net_pay_amount",
        ],
        order_by="name desc",
    )

    aggregated = {}
    for slip in slips:
        key = (slip.custom_month, slip.custom_payroll_period)
        if key not in aggregated:
            aggregated[key] = {
                "no_of_employee": 0,
                "ctc_pa": 0,
                "ctc_pm": 0,
                "gross_pay": 0,
                "total_income": 0,
                "total_deduction": 0,
                "total_net_pay": 0,
            }
        agg = aggregated[key]
        agg["no_of_employee"] += 1
        agg["ctc_pa"] += slip.custom_annual_ctc or 0
        agg["ctc_pm"] += (slip.custom_annual_ctc or 0) / 12
        agg["gross_pay"] += slip.gross_pay or 0
        agg["total_income"] += slip.custom_total_income or 0
        agg["total_deduction"] += slip.custom_total_deduction_amount or 0
        agg["total_net_pay"] += slip.custom_net_pay_amount or 0

    return [
        {"month": month, "payroll_period": period, **values} for (month, period), values in aggregated.items()
    ]


def get_columns():
    return [
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
