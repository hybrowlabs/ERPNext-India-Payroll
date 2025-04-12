# Copyright (c) 2025, Hybrowlabs technologies and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_all_income_tax(filters)
    return columns, data

def get_all_income_tax(filters=None):
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
            "name", "employee", "employee_name", "company", "custom_payroll_period",
            "custom_month", "branch", "department", "designation",
            "total_working_days", "custom_total_leave_without_pay", 
            "payment_days", "current_month_income_tax"
        ]
    )

    for slip in salary_slips:
        data.append({
            "salary_slip": slip.name,
            "employee": slip.employee,
            "employee_name": slip.employee_name,
            "company": slip.company,
            "payroll_period": slip.custom_payroll_period,
            "month": slip.custom_month,
            "branch": slip.branch,
            "department": slip.department,
            "designation": slip.designation,
            "working_days": slip.total_working_days,
            "total_lwp": slip.custom_total_leave_without_pay,
            "payment_day": slip.payment_days,
            "salary_component": "Income Tax",
            "amount": slip.current_month_income_tax,
        })

    return data

def get_columns():
    return [
        {"label": "Salary Slip", "fieldname": "salary_slip", "fieldtype": "Link", "options": "Salary Slip", "width": 150},
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 150},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
        {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
        {"label": "Payroll Period", "fieldname": "payroll_period", "fieldtype": "Link", "options": "Payroll Period", "width": 150},
        {"label": "Month", "fieldname": "month", "fieldtype": "Data", "width": 100},
        {"label": "Branch", "fieldname": "branch", "fieldtype": "Link", "options": "Branch", "width": 120},
        {"label": "Department", "fieldname": "department", "fieldtype": "Link", "options": "Department", "width": 150},
        {"label": "Designation", "fieldname": "designation", "fieldtype": "Link", "options": "Designation", "width": 150},
        {"label": "Working Days", "fieldname": "working_days", "fieldtype": "Float", "width": 120},
        {"label": "LWP Days", "fieldname": "total_lwp", "fieldtype": "Float", "width": 120},
        {"label": "Payment Days", "fieldname": "payment_day", "fieldtype": "Float", "width": 120},
        {"label": "Salary Component", "fieldname": "salary_component", "fieldtype": "Data", "width": 180},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 150},
    ]
