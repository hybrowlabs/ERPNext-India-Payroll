import frappe
from frappe.utils import getdate, nowdate







@frappe.whitelist()
def get_individual_employee_locking_period(employee):

    if not employee:
        frappe.throw("Employee is required")

    # Get Employee document
    employee_data = frappe.get_doc("Employee", employee)

    doj = employee_data.date_of_joining
    company = employee_data.company
    today = getdate(nowdate())

    if not doj:
        frappe.throw("Date of Joining not found for Employee")

    # Get Active Payroll Period
    payroll_period = frappe.get_value(
        "Payroll Period",
        {
            "company": company,
            "start_date": ["<=", today],
            "end_date": [">=", today]
        },
        ["name", "start_date", "end_date"],
        as_dict=True
    )

    if not payroll_period:
        frappe.throw("No active Payroll Period found for this company")

    # Decide frequency type
    if getdate(doj) <= getdate(payroll_period.start_date):
        frequency_type = "Monthly"
    else:
        frequency_type = "New Joinee"

    # Get Release Config document
    release_config_name = frappe.get_value(
        "Release Config",
        {
            "company": company,
            "frequency_type": frequency_type
        },
        "name"
    )

    if not release_config_name:
        frappe.throw("Release Config not found")

    release_doc = frappe.get_doc("Release Config", release_config_name)

    # Default values
    child_start_date = None
    child_end_date = None
    active = 0
    release_type=None

    # Check individual declaration child table
    for row in release_doc.individual_declaration_child:
        if row.employee == employee:
            child_start_date = row.start_date
            child_end_date = row.end_date
            active = row.active
            release_type=row.doctype_name

            break

    return {
        "employee": employee,
        "company": company,
        "payroll_period": payroll_period.name,
        "frequency_type": frequency_type,
        "release_config": release_config_name,
        "individual_start_date": child_start_date,
        "individual_end_date": child_end_date,
        "active": active,
        "status": "Open" if active == 0 else "Closed",
        "type":release_type
    }



@frappe.whitelist()
def set_individual_employee_locking_period(employee, start_date, end_date, status,doctype_name):

    if not employee:
        frappe.throw("Employee is required")

    if not start_date or not end_date:
        frappe.throw("Start Date and End Date are required")

    # Convert status to active flag
    active = 0 if status == "Open" else 1

    # Get Employee
    employee_data = frappe.get_doc("Employee", employee)
    doj = employee_data.date_of_joining
    company = employee_data.company
    today = getdate(nowdate())

    if not doj:
        frappe.throw("Date of Joining not found for Employee")

    # Get Active Payroll Period
    payroll_period = frappe.get_value(
        "Payroll Period",
        {
            "company": company,
            "start_date": ["<=", today],
            "end_date": [">=", today]
        },
        ["name", "start_date", "end_date"],
        as_dict=True
    )

    if not payroll_period:
        frappe.throw("No active Payroll Period found for this company")

    # Decide frequency
    if getdate(doj) <= getdate(payroll_period.start_date):
        frequency_type = "Monthly"
    else:
        frequency_type = "New Joinee"

    # Get Release Config
    release_config_name = frappe.get_value(
        "Release Config",
        {
            "company": company,
            "frequency_type": frequency_type
        },
        "name"
    )

    if not release_config_name:
        frappe.throw("Release Config not found")

    release_doc = frappe.get_doc("Release Config", release_config_name)

    employee_found = False

    # Update if exists
    for row in release_doc.individual_declaration_child:
        if row.employee == employee:
            row.start_date = start_date
            row.end_date = end_date
            row.active = active
            employee_found = True
            doctype_name=doctype_name
            break

    # Insert if not exists
    if not employee_found:
        release_doc.append("individual_declaration_child", {
            "employee": employee,
            "start_date": start_date,
            "end_date": end_date,
            "active": active,
            "doctype_name":doctype_name
        })

    # Save document
    release_doc.save(ignore_permissions=True)
    frappe.db.commit()

    return {
        "employee": employee,
        "company": company,
        "payroll_period": payroll_period.name,
        "frequency_type": frequency_type,
        "release_config": release_config_name,
        "individual_start_date": start_date,
        "individual_end_date": end_date,
        "active": active,
        "status": status,
        "type": "Declaration"
    }