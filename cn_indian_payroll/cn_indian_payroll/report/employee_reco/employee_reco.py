import frappe

def get_salary_slips(filters=None):
    if filters is None:
        filters = {}

    conditions = {"docstatus": ["in", [0, 1]]}

    if filters.get("select_month"):
        conditions["custom_month"] = filters["select_month"]

    if filters.get("payroll_period"):
        conditions["custom_payroll_period"] = filters["payroll_period"]

    if "custom_month" in conditions and "custom_payroll_period" in conditions:
        frappe.msgprint(str(conditions))  

def execute(filters=None):
    columns = []

    data = get_salary_slips(filters)

    return columns, data
