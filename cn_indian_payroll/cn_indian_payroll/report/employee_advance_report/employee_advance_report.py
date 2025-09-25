# Copyright (c) 2025, Hybrowlabs Technologies
# For license information, please see license.txt

# import frappe

# def execute(filters=None):
#     columns = get_columns()
#     data = get_all_accrued_bonus(filters)
#     return columns, data


# def get_all_accrued_bonus(filters=None):
#     if filters is None:
#         filters = {}

#     conditions = {"docstatus": 1}

#     if filters.get("employee"):
#         conditions["employee"] = filters["employee"]

#     if filters.get("company"):
#         conditions["company"] = filters["company"]

#     if filters.get("advance_from") and filters.get("advance_to"):
#         conditions["posting_date"] = ["between", [filters["advance_from"], filters["advance_to"]]]

#     elif filters.get("advance_from"):
#         conditions["posting_date"] = [">=", filters["advance_from"]]

#     elif filters.get("advance_to"):
#         conditions["posting_date"] = ["<=", filters["advance_to"]]

#     if filters.get("advance_type"):
#         conditions["custom_type"] = filters["advance_type"]


#     records = frappe.get_list(
#         'Employee Advance',
#         filters=conditions,
#         fields=[
#             "*"
#         ]
#     )

#     data = []

#     for row in records:
#         data.append({
#             "reference_id": row.name,
#             "employee": row.employee,
#             "employee_name": row.employee_name,
#             "company": row.company,
# 			"advance_amount":row.advance_amount,
# 			"paid_amount":row.custom_total_paid_amount,
# 			"balance_amount":row.custom_total_balance_amount,

#             "custom_note_remarks": getattr(row, "custom_note_remarks", ""),
#             "custom_advance_type": getattr(row, "custom_advance_type", ""),
#             "custom_repayment_type": getattr(row, "custom_repayment_type", ""),
#             "custom_repayment_start_date": getattr(row, "custom_repayment_start_date", ""),
#             "purpose": getattr(row, "purpose", "")
#         })

#     return data


# def get_columns():
#     return [
#         {"label": "Reference ID", "fieldname": "reference_id", "fieldtype": "Link", "options": "Employee Advance", "width": 150},
#         {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 150},
#         {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
#         {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
#         {"label": "Advance Type", "fieldname": "custom_advance_type", "fieldtype": "Data", "width": 150},
#         {"label": "Repayment Type", "fieldname": "custom_repayment_type", "fieldtype": "Data", "width": 150},
#         {"label": "Repayment Start Date", "fieldname": "custom_repayment_start_date", "fieldtype": "Date", "width": 120},

# 		{"label": "Advance Amount", "fieldname": "advance_amount", "fieldtype": "Currency",  "width": 150},
# 		{"label": "Paid Amount", "fieldname": "paid_amount", "fieldtype": "Currency",  "width": 150},
# 		{"label": "Balance Amount", "fieldname": "balance_amount", "fieldtype": "Currency",  "width": 150},
# 		{"label": "Purpose", "fieldname": "purpose", "fieldtype": "Data", "width": 180},
#         {"label": "Note/Remarks", "fieldname": "custom_note_remarks", "fieldtype": "Data", "width": 180},


#     ]




import frappe
from frappe.utils import flt, getdate, add_months

def execute(filters=None):
    columns = get_columns()
    data = get_all_accrued_bonus(filters)
    return columns, data


def get_all_accrued_bonus(filters=None):
    if filters is None:
        filters = {}

    conditions = {"docstatus": 1}
    if filters.get("employee"):
        conditions["employee"] = filters["employee"]
    if filters.get("company"):
        conditions["company"] = filters["company"]

    if filters.get("advance_from") and filters.get("advance_to"):
        conditions["posting_date"] = ["between", [filters["advance_from"], filters["advance_to"]]]

    elif filters.get("advance_from"):
        conditions["posting_date"] = [">=", filters["advance_from"]]

    elif filters.get("advance_to"):
        conditions["posting_date"] = ["<=", filters["advance_to"]]

    if filters.get("advance_type"):
        conditions["custom_type"] = filters["advance_type"]



    records = frappe.get_all("Employee Advance", filters=conditions, fields=["*"])
    data = []

    for row in records:
        # 1️⃣ Add advance header row (NO repayment fields here)
        data.append({
            "reference_id": row.name,
            "employee": row.employee,
            "employee_name": row.employee_name,
            "company": row.company,
            "advance_type": row.custom_advance_type,
            "repayment_type": row.custom_repayment_type,
            "repayment_start_date": row.custom_repayment_start_date,
            "advance_amount": row.advance_amount,
            "total_paid_amount": row.custom_total_paid_amount,
            "total_balance_amount": row.custom_total_balance_amount,
            "purpose": row.purpose,
            "note_remarks": row.custom_note_remarks,
            # repayment columns excluded here
        })

        # 2️⃣ Add repayment schedule rows
        repayment_schedule = get_repayment_schedule(row)
        for repayment in repayment_schedule:
            data.append({
                "reference_id": "",   # blank to avoid repeat
                "employee": "",
                "employee_name": "",
                "company": "",
                "advance_type": "",
                "repayment_type": "",
                "repayment_start_date": "",
                "advance_amount": "",
                "total_paid_amount": "",
                "total_balance_amount": "",
                "purpose": "",
                "note_remarks": "",
                # repayment details only
                "idx": repayment.get("idx"),
                "payment_date": repayment.get("payment_date"),
                "payment_amount": repayment.get("payment_amount"),
                "balance_amount": repayment.get("balance_amount"),
                "deducted": repayment.get("deducted"),
            })


    return data



def get_repayment_schedule(advance):
    """Build repayment schedule like your dashboard function"""
    repayment_schedule = []
    balance_amount = float(advance.advance_amount or 0)
    start_date = advance.custom_repayment_start_date
    idx = 0

    get_additional_salary = frappe.db.get_all(
        "Additional Salary",
        filters={
            "employee": advance.employee,
            "company": advance.company,
            "ref_doctype": "Employee Advance",
            "ref_docname": advance.name,
            "docstatus": 1
        },
        fields=['name', 'amount', 'payroll_date'],
        order_by='from_date asc'
    )

    if get_additional_salary:
        for rec in get_additional_salary:
            current_date = getdate(rec.payroll_date)
            idx += 1
            pay_amount = min(balance_amount, flt(rec.amount))
            balance_amount -= pay_amount

            salary_slips = frappe.db.get_all(
                "Salary Slip",
                filters=[
                    ["employee", "=", advance.employee],
                    ["company", "=", advance.company],
                    ["docstatus", "=", 1],
                    ["start_date", "<=", current_date],
                    ["end_date", ">=", current_date],
                ],
                fields=["name"],
                limit=1,
            )
            deducted = 1 if salary_slips else 0

            repayment_schedule.append({
                "idx": idx,
                "payment_date": current_date,
                "payment_amount": pay_amount,
                "balance_amount": balance_amount,
                "deducted": deducted,
                "deducted": "✔" if deducted == 1 else "",

            })
    else:
        # fallback: One Time or Recurring logic
        if advance.custom_repayment_type == "One Time":
            repayment_schedule.append({
                "idx": 1,
                "payment_date": start_date,
                "payment_amount": float(advance.advance_amount or 0),
                "balance_amount": float(advance.advance_amount or 0),
                "deducted": ""
            })

    return repayment_schedule


def get_columns():
    return [
        {"label": "Reference ID", "fieldname": "reference_id", "fieldtype": "Link", "options": "Employee Advance", "width": 150},
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 150},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
        {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
        {"label": "Advance Type", "fieldname": "advance_type", "fieldtype": "Data", "width": 150},
        {"label": "Repayment Type", "fieldname": "repayment_type", "fieldtype": "Data", "width": 150},
        {"label": "Repayment Start Date", "fieldname": "repayment_start_date", "fieldtype": "Date", "width": 120},
        {"label": "Advance Amount", "fieldname": "advance_amount", "fieldtype": "Data", "width": 150},
        {"label": "Paid Amount", "fieldname": "total_paid_amount", "fieldtype": "Data", "width": 150},
        {"label": "Balance Amount", "fieldname": "total_balance_amount", "fieldtype": "Data", "width": 150},
        {"label": "Purpose", "fieldname": "purpose", "fieldtype": "Data", "width": 180},
        {"label": "Note/Remarks", "fieldname": "note_remarks", "fieldtype": "Data", "width": 180},

        # Repayment Schedule Columns
        {"label": "Installment No", "fieldname": "idx", "fieldtype": "Int", "width": 100},
        {"label": "Payment Date", "fieldname": "payment_date", "fieldtype": "Date", "width": 120},
        {"label": "Payment Amount", "fieldname": "payment_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Balance After", "fieldname": "balance_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Deducted?", "fieldname": "deducted", "fieldtype": "Data", "width": 100},
    ]
