# Copyright (c) 2025, Hybrowlabs Technologies and Contributors
# For license information, please see license.txt

import frappe

def get_salary_slips(filters=None):
    if filters is None:
        filters = {}

    conditions = {"docstatus": ["in", [0, 1]]}

    if filters.get("company"):
        conditions["company"] = filters["company"]

    if filters.get("payroll_period"):
        conditions["custom_payroll_period"] = filters["payroll_period"]
        
    if filters.get("employee"):
        conditions["employee"] = filters["employee"]

    # Fetch salary structure assignments ordered by `from_date` DESC (latest first)
    salary_structure_assignments = frappe.get_all(
        "Salary Structure Assignment", 
        filters=conditions, 
        fields=["*"],  
        order_by="from_date DESC"
    )

    # Dictionary to store the latest salary structure per employee
    latest_salary_structure = {}

    for structure in salary_structure_assignments:
        if structure["employee"] not in latest_salary_structure:
            latest_salary_structure[structure["employee"]] = structure  # Store only the latest assignment

    unique_salary_structures = list(latest_salary_structure.values())

    # Fetch PAN Number and Email for each employee and update the records
    for structure in unique_salary_structures:
        employee = frappe.get_value("Employee", structure["employee"], ["pan_number", "personal_email","company_email"], as_dict=True)
        structure["pan_number"] = employee.get("pan_number") if employee else ""
        structure["personal_email"] = employee.get("personal_email") if employee else ""
        structure["company_email"] = employee.get("company_email") if employee else ""

    return unique_salary_structures

def execute(filters=None):
    columns = [
        {"label": "Employee ID", "fieldname": "employee", "fieldtype": "Data", "width": 120},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 120},
        {"label": "Company", "fieldname": "company", "fieldtype": "Data", "width": 150},
        {"label": "Payroll Period", "fieldname": "custom_payroll_period", "fieldtype": "Data", "width": 150},
        
        {"label": "Effective From Date", "fieldname": "from_date", "fieldtype": "Date", "width": 120},
        {"label": "Joining Date", "fieldname": "custom_date_of_joining", "fieldtype": "Date", "width": 120},
        
        {"label": "Opted Slab", "fieldname": "custom_tax_regime", "fieldtype": "Data", "width": 120},
        {"label": "Department", "fieldname": "department", "fieldtype": "Data", "width": 120},
        {"label": "Designation", "fieldname": "designation", "fieldtype": "Data", "width": 120},

        {"label": "PAN Number", "fieldname": "pan_number", "fieldtype": "Data", "width": 150},
        {"label": "Personal Email", "fieldname": "personal_email", "fieldtype": "Data", "width": 200},
        {"label": "Company Email", "fieldname": "company_email", "fieldtype": "Data", "width": 200},
    ]

    data = get_salary_slips(filters)  # Fetch latest records without duplicates

    return columns, data
