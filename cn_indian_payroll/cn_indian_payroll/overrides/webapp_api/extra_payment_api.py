import frappe

@frappe.whitelist()
def get_extra_payment_list(employee=None, company=None):
    # Validate inputs
    if not employee:
        return {"error": "Please select an employee."}

    if not company:
        return {"error": "Please select a company."}

    # Fetch all Additional Salary entries for this employee
    additional_salary_list = frappe.db.get_all(
        "Additional Salary",
        filters={
            "employee": employee,
            "company": company,
            "docstatus": 1
        },
        fields=["name", "salary_component", "amount", "payroll_date"]
    )

    if not additional_salary_list:
        return {
            "employee": employee,
            "company": company,
            "extra_payments": []
        }

    extra_payments = []

    for entry in additional_salary_list:
        comp = frappe.get_cached_doc("Salary Component", entry.salary_component)

        if comp.custom_is_extra_payment == 1:
            extra_payments.append({
                "name": entry.name,
                "salary_component": entry.salary_component,
                "amount": entry.amount,
                "payment_date": entry.payroll_date,
                "is_tax_applicable": comp.is_tax_applicable
            })

    return {
        "employee": employee,
        "company": company,
        "extra_payments": extra_payments
    }



@frappe.whitelist()
def get_extra_payment_summary(employee=None, company=None, from_date=None, to_date=None):
    # Validate inputs
    if not employee:
        return {"error": "Please select an employee."}

    if not company:
        return {"error": "Please select a company."}

    if not from_date or not to_date:
        return {"error": "Please select a start and end date."}

    # Fetch Additional Salary entries
    additional_salary_list = frappe.db.get_all(
        "Additional Salary",
        filters={
            "employee": employee,
            "company": company,
            "docstatus": 1,
            "payroll_date": ["between", [from_date, to_date]]
        },
        fields=["name", "salary_component", "amount", "payroll_date"]
    )

    if not additional_salary_list:
        return {
            "employee": employee,
            "company": company,
            "extra_payments": []
        }

    extra_payments = []

    # Process components
    for entry in additional_salary_list:
        comp = frappe.get_cached_doc("Salary Component", entry.salary_component)

        if comp.custom_is_extra_payment == 1:
            extra_payments.append({
                "name": entry.name,
                "salary_component": entry.salary_component,
                "amount": entry.amount,
                "payment_date": entry.payroll_date,
                "is_tax_applicable": comp.is_tax_applicable,
            })

    return {
        "employee": employee,
        "company": company,
        "extra_payments": extra_payments
    }
