# Copyright (c) 2025, Hybrowlabs Technologies
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_all_esic(filters)
    return columns, data

def get_all_esic(filters=None):
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
            "name", "employee", "employee_name", "company",
            "custom_payroll_period", "custom_month", "branch",
            "department", "designation", "total_working_days",
            "custom_total_leave_without_pay", "payment_days", "gross_pay","custom_salary_structure_assignment"
        ]
    )

    for slip in salary_slips:
        slip_doc = frappe.get_doc("Salary Slip", slip.name)
        employee_doc = frappe.get_doc("Employee", slip.employee)

        ssa=frappe.get_doc("Salary Structure Assignment",slip.custom_salary_structure_assignment)

        pt_amount = 0

        for deduction in slip_doc.deductions:
            salary_component_doc = frappe.get_doc("Salary Component", deduction.salary_component)

            if salary_component_doc.component_type == "Professional Tax":
                pt_amount += deduction.amount

            

        if pt_amount:
            data.append({
                "salary_slip": slip.name,
                "employee": slip.employee,
                "employee_name": slip.employee_name,
                "company": slip.company,
                "payroll_period": slip.custom_payroll_period,
                "month": slip.custom_month,
                "working_days": slip.total_working_days,
                "total_lwp": slip.custom_total_leave_without_pay,
                "payment_day": slip.payment_days,
                "gross_pay": round(slip.gross_pay),
                "pt_amount": pt_amount,
                "pt_state":ssa.custom_state,
                "pt_location":ssa.custom_state
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

		{"label": "PT State", "fieldname": "pt_state", "fieldtype": "Data", "width": 100},
		{"label": "PT Location", "fieldname": "pt_location", "fieldtype": "Data", "width": 100},

        {"label": "Working Days", "fieldname": "working_days", "fieldtype": "Float", "width": 120},
        {"label": "LWP Days", "fieldname": "total_lwp", "fieldtype": "Float", "width": 120},
        {"label": "Payment Days", "fieldname": "payment_day", "fieldtype": "Float", "width": 120},
        {"label": "Gross Pay", "fieldname": "gross_pay", "fieldtype": "Currency", "width": 150},
		{"label": "PT Amount", "fieldname": "pt_amount", "fieldtype": "Currency", "width": 200},
    ]
