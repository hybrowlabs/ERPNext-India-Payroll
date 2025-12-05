import frappe
from collections import defaultdict


def execute(filters=None):
    data = get_all_accrued_bonus(filters)
    columns = get_columns(data)
    return columns, data


def get_all_accrued_bonus(filters=None):
    if filters is None:
        filters = {}

    conditions = {"docstatus": 1, "is_paid": 0}

    if filters.get("employee"):
        conditions["employee"] = filters["employee"]
    if filters.get("payroll_period"):
        conditions["payroll_period"] = filters["payroll_period"]
    if filters.get("salary_component"):
        conditions["salary_component"] = filters["salary_component"]
    if filters.get("company"):
        conditions["company"] = filters["company"]

    records = frappe.get_list(
        "Employee Bonus Accrual",
        filters=conditions,
        fields=[
            "employee",
            "employee_name",
            "company",
            "payroll_period",
            "accrual_date",
            "salary_component",
            "amount",
            "name",
            "working_days",
            "payment_day",
            "total_lwp",
            "arrear_days",
        ],
        order_by="employee, accrual_date",
    )

    # Group by employee
    grouped = defaultdict(list)
    for r in records:
        grouped[r.employee].append(r)

    final_data = []
    for employee, rows in grouped.items():
        base = {
            "employee": rows[0].employee,
            "employee_name": rows[0].employee_name,
            "company": rows[0].company,
            "payroll_period": rows[0].payroll_period,
        }

        total_payment = 0
        for idx, r in enumerate(rows, start=1):
            base[f"date_{idx}"] = r.accrual_date
            base[f"working_days_{idx}"] = r.working_days
            base[f"payment_days_{idx}"] = r.payment_day
            base[f"lwp_{idx}"] = r.total_lwp
            base[f"arrear_days_{idx}"] = r.arrear_days
            base[f"amount_{idx}"] = r.amount
            total_payment += r.amount or 0

        base["total_payment"] = total_payment
        final_data.append(base)

    return final_data


def get_columns(data):
    columns = [
        {
            "label": "Employee",
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 150,
        },
        {
            "label": "Employee Name",
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 180,
        },
        {
            "label": "Company",
            "fieldname": "company",
            "fieldtype": "Link",
            "options": "Company",
            "width": 150,
        },
        {
            "label": "Payroll Period",
            "fieldname": "payroll_period",
            "fieldtype": "Link",
            "options": "Payroll Period",
            "width": 150,
        },
    ]

    # Dynamically detect how many accrual entries exist max
    max_entries = 0
    for row in data:
        count = sum(1 for k in row.keys() if k.startswith("date_"))
        max_entries = max(max_entries, count)

    for i in range(1, max_entries + 1):
        columns.extend(
            [
                {
                    "label": f"Date",
                    "fieldname": f"date_{i}",
                    "fieldtype": "Date",
                    "width": 120,
                },
                {
                    "label": f"Working Days",
                    "fieldname": f"working_days_{i}",
                    "fieldtype": "Float",
                    "width": 100,
                },
                {
                    "label": f"Payment Days",
                    "fieldname": f"payment_days_{i}",
                    "fieldtype": "Float",
                    "width": 100,
                },
                {
                    "label": f"LWP",
                    "fieldname": f"lwp_{i}",
                    "fieldtype": "Float",
                    "width": 80,
                },
                {
                    "label": f"Arrear Days",
                    "fieldname": f"arrear_days_{i}",
                    "fieldtype": "Float",
                    "width": 100,
                },
                {
                    "label": f"Accrued Amount",
                    "fieldname": f"amount_{i}",
                    "fieldtype": "Currency",
                    "width": 120,
                },
            ]
        )

    # ✅ Add Total Payment column at the end
    columns.append(
        {
            "label": "Total Payment",
            "fieldname": "total_payment",
            "fieldtype": "Currency",
            "width": 150,
        }
    )

    return columns
