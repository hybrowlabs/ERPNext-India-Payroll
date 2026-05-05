# # Copyright (c) 2025, Hybrowlabs Technologies
# # For license information, please see license.txt

# import frappe

# def execute(filters=None):
#     columns = get_columns()
#     data = get_all_accrued_reimbursements(filters)
#     return columns, data


# def get_all_accrued_reimbursements(filters=None):
#     if filters is None:
#         filters = {}

#     conditions = {"docstatus": 1}

#     if filters.get("employee"):
#         conditions["employee"] = filters["employee"]
#     if filters.get("payroll_period"):
#         conditions["payroll_period"] = filters["payroll_period"]
#     if filters.get("salary_component"):
#         conditions["salary_component"] = filters["salary_component"]
#     if filters.get("company"):
#         conditions["company"] = filters["company"]

#     records = frappe.get_list(
#         'Employee Benefit Accrual',
#         filters=conditions,
#         fields=[
#             "employee",
#             "employee_name",
#             "company",
#             "payroll_period",
#             "benefit_accrual_date",
#             "salary_component",
#             "amount",

#         ]
#     )

#     benefit_claim_records = frappe.get_list(
#         'Employee Benefit Claim',
#         filters=conditions,
#         fields=[
#             "employee",
#             "company",
#             "payroll_period",
#             "claim_date",

#             "earning_component",
#             "custom_paid_amount",

#         ]
#     )
#     if benefit_claim_records:
#         if records.benefit_accrual_date and benefit_claim_records.claim_date is same month


#     data = []

#     for row in records:
#         data.append({
#             "employee": row.employee,
#             "employee_name": row.employee_name,
#             "company": row.company,
#             "payroll_period": row.payroll_period,
#             "accrued_date": row.benefit_accrual_date,
#             "salary_component": row.salary_component,
#             "amount": row.amount,
#             "total_settlement": paid_amount
#         })

#     return data


# def get_columns():
#     return [
#         {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 150},
#         {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
#         {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
#         {"label": "Payroll Period", "fieldname": "payroll_period", "fieldtype": "Link", "options": "Payroll Period", "width": 150},
#         {"label": "Accrued Date", "fieldname": "accrued_date", "fieldtype": "Date", "width": 120},
#         {"label": "Salary Component", "fieldname": "salary_component", "fieldtype": "Link", "options": "Salary Component", "width": 180},
#         {"label": "Accrued Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 120},
#         {"label": "Total Settlement", "fieldname": "total_settlement", "fieldtype": "Currency", "width": 150},
#     ]

# Copyright (c) 2025, Hybrowlabs Technologies
# For license information, please see license.txt

import frappe
from datetime import datetime

def execute(filters=None):
    columns = get_columns()
    data = get_all_accrued_reimbursements(filters)
    return columns, data

@frappe.whitelist()

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

    # Get all accrual records matching filters
    accrual_records = frappe.get_list(
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
            "working_days",
            "payment_days"
        ],
        order_by="benefit_accrual_date"
    )

    # Get all claim records matching filters
    # Note: use the actual fieldname for payroll_period in Employee Benefit Claim (e.g. custom_payroll_period)
    claim_conditions = {"docstatus": 1}
    if filters.get("employee"):
        claim_conditions["employee"] = filters["employee"]
    if filters.get("company"):
        claim_conditions["company"] = filters["company"]

    claim_records = frappe.get_list(
        'Employee Benefit Claim',
        filters=claim_conditions,
        fields=[
            "employee",
            "company",
            "custom_payroll_period",  # adjust this field if your doctype uses different field
            "claim_date",
            "earning_component",
            "custom_paid_amount",
        ]
    )

    data = []

    for accrual in accrual_records:
        # Parse accrual date month and year
        accrual_date = accrual.benefit_accrual_date
        accrual_month = datetime.strptime(str(accrual_date), "%Y-%m-%d").month
        accrual_year = datetime.strptime(str(accrual_date), "%Y-%m-%d").year

        # frappe.msgprint(str(accrual_month) + " " + str(accrual_year))

        paid_amount = 0.0
        for claim in claim_records:
            if (
                claim.employee == accrual.employee and
                claim.company == accrual.company and
                claim.custom_payroll_period == accrual.payroll_period and
                claim.earning_component == accrual.salary_component and
                claim.claim_date is not None
            ):
                claim_month = datetime.strptime(str(claim.claim_date), "%Y-%m-%d").month
                claim_year = datetime.strptime(str(claim.claim_date), "%Y-%m-%d").year

                # frappe.msgprint(str(claim_month) + " " + str(claim_year))

                if claim_month == accrual_month and claim_year == accrual_year:
                    paid_amount += claim.custom_paid_amount or 0.0

        # frappe.msgprint(str(paid_amount))

        data.append({
            "employee": accrual.employee,
            "employee_name": accrual.employee_name,
            "company": accrual.company,
            "payroll_period": accrual.payroll_period,
            "accrued_date": accrual.benefit_accrual_date,
            "salary_component": accrual.salary_component,
            "working_days": accrual.working_days,
            "payment_days": accrual.payment_days,
            "amount": accrual.amount,
            "total_settlement": paid_amount
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
        {"label": "Working Days", "fieldname": "working_days", "fieldtype": "Float", "width": 120},
        {"label": "Payment Days", "fieldname": "payment_days", "fieldtype": "Float", "width": 120},
        {"label": "Accrued Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 120},
        {"label": "Total Settlement", "fieldname": "total_settlement", "fieldtype": "Currency", "width": 150},
    ]
