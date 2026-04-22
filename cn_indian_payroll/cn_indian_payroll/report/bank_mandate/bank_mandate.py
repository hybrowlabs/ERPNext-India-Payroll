# Copyright (c) 2025, Hybrowlabs Technologies
# For license information, please see license.txt

import frappe


def execute(filters=None):
    return get_columns(), get_all_net_pay(filters)


def get_all_net_pay(filters=None):
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

    salary_slips = frappe.get_all(
        "Salary Slip",
        filters=conditions,
        fields=[
            "name",
            "employee",
            "employee_name",
            "company",
            "custom_payroll_period",
            "custom_month",
            "net_pay",
        ],
    )

    if not salary_slips:
        return []

    # Batch-fetch bank details — one query instead of N get_doc calls
    emp_ids = list({s.employee for s in salary_slips})
    emp_bank_map = {
        row.name: row
        for row in frappe.get_all(
            "Employee",
            filters={"name": ["in", emp_ids]},
            fields=["name", "bank_ac_no", "ifsc_code"],
        )
    }

    return [
        {
            "salary_slip": slip.name,
            "account_number": emp_bank_map.get(slip.employee, frappe._dict()).bank_ac_no,
            "ifsc_code": emp_bank_map.get(slip.employee, frappe._dict()).ifsc_code,
            "employee": slip.employee,
            "employee_name": slip.employee_name,
            "company": slip.company,
            "payroll_period": slip.custom_payroll_period,
            "month": slip.custom_month,
            "net_pay": slip.net_pay,
        }
        for slip in salary_slips
    ]


def get_columns():
    return [
        {
            "label": "Salary Slip",
            "fieldname": "salary_slip",
            "fieldtype": "Link",
            "options": "Salary Slip",
            "width": 150,
        },
        {"label": "Account Number", "fieldname": "account_number", "fieldtype": "Data", "width": 150},
        {"label": "IFSC Code", "fieldname": "ifsc_code", "fieldtype": "Data", "width": 150},
        {
            "label": "Employee",
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 150,
        },
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
        {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
        {
            "label": "Payroll Period",
            "fieldname": "payroll_period",
            "fieldtype": "Link",
            "options": "Payroll Period",
            "width": 150,
        },
        {"label": "Month", "fieldname": "month", "fieldtype": "Data", "width": 100},
        {"label": "Amount Paid", "fieldname": "net_pay", "fieldtype": "Currency", "width": 200},
    ]
