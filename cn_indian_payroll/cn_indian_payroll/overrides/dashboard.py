import frappe

@frappe.whitelist()
def delete_extra_payment(from_date=None, to_date=None, employee=None):

    if not from_date or not to_date:
        return "From Date and To Date are required"

    filters = {
        "payroll_date": ["between", [from_date, to_date]]
    }

    if employee:
        filters["employee"] = employee

    additional_salaries = frappe.get_all(
        "Additional Salary",
        filters=filters,
        fields=["name", "docstatus"]
    )

    if not additional_salaries:
        return "No records found"

    deleted_count = 0

    for row in additional_salaries:
        try:
            doc = frappe.get_doc("Additional Salary", row.name)

            if doc.docstatus == 1:
                doc.cancel()

            frappe.delete_doc("Additional Salary", doc.name, force=1)

            deleted_count += 1

        except Exception as e:
            frappe.log_error(f"Error deleting {row.name}: {str(e)}")

    return f"{deleted_count} Additional Salary records deleted successfully"



@frappe.whitelist()
def delete_salary_slip(from_date=None, to_date=None, employee=None):

    if not from_date or not to_date:
        return "From Date and To Date are required"

    filters = {
        "start_date": ["between", [from_date, to_date]]
    }

    if employee:
        filters["employee"] = employee

    salary_slips = frappe.get_all(
        "Salary Slip",
        filters=filters,
        fields=["name", "docstatus"]
    )

    if not salary_slips:
        return "No records found"

    deleted_count = 0

    for row in salary_slips:
        try:
            doc = frappe.get_doc("Salary Slip", row.name)

            if doc.docstatus == 1:
                doc.cancel()

            frappe.delete_doc("Salary Slip", doc.name, force=1)

            deleted_count += 1

        except Exception as e:
            frappe.log_error(f"Error deleting {row.name}: {str(e)}")

    return f"{deleted_count} Salary Slip records deleted successfully"