# Copyright (c) 2025, Hybrowlabs Technologies
# For license information, please see license.txt

import frappe

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


    records = frappe.get_list(
        'Employee Advance',
        filters=conditions,
        fields=[
            "*"
        ]
    )

    data = []

    for row in records:
        data.append({
            "reference_id": row.name,
            "employee": row.employee,
            "employee_name": row.employee_name,
            "company": row.company,
			"advance_amount":row.advance_amount,
			"paid_amount":row.custom_total_paid_amount,
			"balance_amount":row.custom_total_balance_amount,

            "custom_note_remarks": getattr(row, "custom_note_remarks", ""),
            "custom_advance_type": getattr(row, "custom_advance_type", ""),
            "custom_repayment_type": getattr(row, "custom_repayment_type", ""),
            "custom_repayment_start_date": getattr(row, "custom_repayment_start_date", ""),
            "purpose": getattr(row, "purpose", "")
        })

    return data


def get_columns():
    return [
        {"label": "Reference ID", "fieldname": "reference_id", "fieldtype": "Link", "options": "Employee Advance", "width": 150},
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 150},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
        {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
        {"label": "Advance Type", "fieldname": "custom_advance_type", "fieldtype": "Data", "width": 150},
        {"label": "Repayment Type", "fieldname": "custom_repayment_type", "fieldtype": "Data", "width": 150},
        {"label": "Repayment Start Date", "fieldname": "custom_repayment_start_date", "fieldtype": "Date", "width": 120},

		{"label": "Advance Amount", "fieldname": "advance_amount", "fieldtype": "Currency",  "width": 150},
		{"label": "Paid Amount", "fieldname": "paid_amount", "fieldtype": "Currency",  "width": 150},
		{"label": "Balance Amount", "fieldname": "balance_amount", "fieldtype": "Currency",  "width": 150},
		{"label": "Purpose", "fieldname": "purpose", "fieldtype": "Data", "width": 180},
        {"label": "Note/Remarks", "fieldname": "custom_note_remarks", "fieldtype": "Data", "width": 180},


    ]
