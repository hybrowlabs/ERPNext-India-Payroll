import frappe

def after_insert(doc, method):
    # Create User Assignment for Employee
    if doc.employment_type=="Consultant":
        if not frappe.get_all("Vendor", filters={"employee_id": doc.name}):
            user_assignment = frappe.new_doc("Vendor")
            user_assignment.employee_id = doc.name

            user_assignment.insert()
            frappe.db.commit()
