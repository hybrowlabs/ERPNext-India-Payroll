import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_all_income_tax(filters)
    return columns, data


def get_all_income_tax(filters=None):
    if not filters:
        filters = {}

    conditions = {"docstatus": ["in", [0, 1]]}

    if filters.get("employee"):
        conditions["employee"] = filters["employee"]
    if filters.get("payroll_period"):
        conditions["custom_payroll_period"] = filters["payroll_period"]
    if filters.get("company"):
        conditions["company"] = filters["company"]

    months = [
        "April","May","June","July","August","September",
        "October","November","December","January","February","March"
    ]

    employee_map = {}

    salary_slips = frappe.get_all(
        "Salary Slip",
        filters=conditions,
        fields=[
            "name", "employee", "employee_name",
            "custom_month", "custom_tax_regime"
        ]
    )

    for slip in salary_slips:
        slip_doc = frappe.get_doc("Salary Slip", slip.name)

        income_tax = 0

        for d in slip_doc.deductions:
            comp = frappe.get_doc("Salary Component", d.salary_component)
            if comp.variable_based_on_taxable_salary:
                income_tax += d.amount

        if not income_tax:
            continue

        emp = slip.employee

        if emp not in employee_map:
            employee_map[emp] = {
                "emp_id": emp,
                "employee_name": slip.employee_name,
                "tax_regime": slip_doc.custom_tax_regime,

                # months init
                **{m.lower(): 0 for m in months},

                "total_tax_liability": 0,
                "total_tax_deducted": 0,
                "tax_deducted_by_previous_employer": 0,
                "outside_tax": 0,
                "pending_tax_for_next_year": 0,
                "refund": 0
            }

        month = slip.custom_month

        if month in months:
            employee_map[emp][month.lower()] += income_tax

        employee_map[emp]["total_tax_deducted"] += income_tax

    return list(employee_map.values())


def get_columns():
    return [
        {"label": "EMP ID", "fieldname": "emp_id", "fieldtype": "Link", "options": "Employee", "width": 140},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
        {"label": "Tax Regime", "fieldname": "tax_regime", "fieldtype": "Data", "width": 120},

        {"label": "April", "fieldname": "april", "fieldtype": "Currency", "width": 100},
        {"label": "May", "fieldname": "may", "fieldtype": "Currency", "width": 100},
        {"label": "June", "fieldname": "june", "fieldtype": "Currency", "width": 100},
        {"label": "July", "fieldname": "july", "fieldtype": "Currency", "width": 100},
        {"label": "August", "fieldname": "august", "fieldtype": "Currency", "width": 100},
        {"label": "September", "fieldname": "september", "fieldtype": "Currency", "width": 100},
        {"label": "October", "fieldname": "october", "fieldtype": "Currency", "width": 100},
        {"label": "November", "fieldname": "november", "fieldtype": "Currency", "width": 100},
        {"label": "December", "fieldname": "december", "fieldtype": "Currency", "width": 100},
        {"label": "January", "fieldname": "january", "fieldtype": "Currency", "width": 100},
        {"label": "February", "fieldname": "february", "fieldtype": "Currency", "width": 100},
        {"label": "March", "fieldname": "march", "fieldtype": "Currency", "width": 100},

        {"label": "Total Tax Liability For The Year", "fieldname": "total_tax_liability", "fieldtype": "Currency", "width": 200},
        {"label": "Total Tax Deducted", "fieldname": "total_tax_deducted", "fieldtype": "Currency", "width": 180},
        {"label": "Tax Deducted By Previous Employer", "fieldname": "tax_deducted_by_previous_employer", "fieldtype": "Currency", "width": 220},
        {"label": "Outside Tax", "fieldname": "outside_tax", "fieldtype": "Currency", "width": 150},
        {"label": "Pending Tax For The Year", "fieldname": "pending_tax_for_next_year", "fieldtype": "Currency", "width": 220},
        {"label": "Refund", "fieldname": "refund", "fieldtype": "Currency", "width": 120},
    ]