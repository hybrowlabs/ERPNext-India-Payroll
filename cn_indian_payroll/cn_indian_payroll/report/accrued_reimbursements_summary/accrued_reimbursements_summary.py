# Copyright (c) 2025, Hybrowlabs Technologies
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_all_accrued_reimbursements(filters)
    return columns, data


def get_all_accrued_reimbursements(filters=None):
    if filters is None:
        filters = {}

    conditions = {"docstatus": 1}

    if filters.get("employee"):
        conditions["employee"] = filters["employee"]
    if filters.get("payroll_period"):
        conditions["payroll_period"] = filters["payroll_period"]
    if filters.get("salary_component"):
        conditions["salary_component"] = filters["salary_component"]
    if filters.get("company"):
        conditions["company"] = filters["company"]

    records = frappe.get_list(
        'Employee Benefit Accrual',
        filters=conditions,
        fields=[
            "employee",
            "employee_name",
            "company",
            "payroll_period",
            "benefit_accrual_date",
            "salary_component",
            "amount",
            "total_settlement"
        ]
    )

    data = []

    for row in records:
        data.append({
            "employee": row.employee,
            "employee_name": row.employee_name,
            "company": row.company,
            "payroll_period": row.payroll_period,
            "accrued_date": row.benefit_accrual_date,
            "salary_component": row.salary_component,
            "amount": row.amount,
            "total_settlement": row.total_settlement
        })

    return data


def get_columns():
    return [
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 150},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
        {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
        {"label": "Payroll Period", "fieldname": "payroll_period", "fieldtype": "Link", "options": "Payroll Period", "width": 150},
        {"label": "Accrued Date", "fieldname": "accrued_date", "fieldtype": "Date", "width": 120},
        {"label": "Salary Component", "fieldname": "salary_component", "fieldtype": "Link", "options": "Salary Component", "width": 180},
        {"label": "Accrued Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 120},
        {"label": "Total Settlement", "fieldname": "total_settlement", "fieldtype": "Currency", "width": 150},
    ]
