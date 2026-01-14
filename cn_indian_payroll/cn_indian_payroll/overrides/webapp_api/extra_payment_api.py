import frappe
from frappe.utils import getdate

#http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.extra_payment_api.get_extra_payment_list?employee=37001&company=PW&payroll_period=25-26

@frappe.whitelist()
def get_extra_payment_list(employee=None, company=None,payroll_period=None):

    target_employee = frappe.request.headers.get("X-Target-Employee-Id")
    if target_employee:
        employee = target_employee

    if not employee:
        return {
            "status": "failed",
            "message": "Employee is required."
        }

    if not company:
        return {
            "status": "failed",
            "message": "Company is required."
        }

    filters = {
        "employee": employee,
        "company": company,
        "docstatus": 1
    }

    payroll_period_name = None


    if payroll_period:
        pp_doc = frappe.get_doc("Payroll Period", payroll_period)
        payroll_period_name = pp_doc.name

        filters["payroll_date"] = [
            "between",
            [getdate(pp_doc.start_date), getdate(pp_doc.end_date)]
        ]

    additional_salary_list = frappe.db.get_all(
        "Additional Salary",
        filters=filters,
        fields=[
            "name",
            "salary_component",
            "amount",
            "payroll_date"
        ],
        order_by="payroll_date desc"
    )

    if not additional_salary_list:
        return {
            "status": "success",
            "employee": employee,
            "company": company,
            "payroll_period": payroll_period_name,
            "total_records": 0,
            "extra_payments": []
        }


    extra_payments = []

    for entry in additional_salary_list:
        comp = frappe.get_cached_doc(
            "Salary Component",
            entry.salary_component
        )

        if comp.custom_is_extra_payment:
            extra_payments.append({
                "name": entry.name,
                "salary_component": entry.salary_component,
                "amount": entry.amount,
                "payment_date": entry.payroll_date,
                "is_tax_applicable": comp.is_tax_applicable
            })

    return {
        "status": "success",
        "employee": employee,
        "company": company,
        "payroll_period": payroll_period_name,
        "total_records": len(extra_payments),
        "extra_payments": extra_payments
    }




@frappe.whitelist()
def get_extra_payment_summary(employee=None, company=None, from_date=None, to_date=None):

    target_employee = frappe.request.headers.get("X-Target-Employee-Id")
    if target_employee:
        employee = target_employee



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






# fetch('/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.extra_payment_api.create_additional_salary', {
#     method: 'POST',
#     headers: {
#         'Content-Type': 'application/json',
#         'X-Frappe-CSRF-Token': frappe.csrf_token
#     },
#     body: JSON.stringify({
#         employee: "37001",
#         company: "PW",
#         salary_component: "Incenive Regular (Taxable)",
#         amount: 2000,
#         payroll_date: "2025-05-01",
#         is_recurring: 0,
#         deduct_full_tax_on_selected_payroll_date: 1,
#         custom_is_tax_manual_calculate: 0,
#         overwrite_salary_structure_amount: 0,

#     })
# })
# .then(res => res.json())
# .then(data => console.log(data))
# .catch(err => console.error(err));

# import frappe
# from frappe import _
# from frappe.utils import getdate

# @frappe.whitelist(methods=["POST"])
# def create_additional_salary():

#     data = frappe.request.get_json() or {}

#     if not data.get("employee"):
#         return {"status": "failed", "message": "Employee is required"}

#     if not data.get("company"):
#         return {"status": "failed", "message": "Company is required"}

#     if not data.get("salary_component"):
#         return {"status": "failed", "message": "Salary Component is required"}

#     if not data.get("amount"):
#         return {"status": "failed", "message": "Amount is required"}

#     if not data.get("payroll_date"):
#         return {"status": "failed", "message": "Payroll Date is required"}

#     doc = frappe.new_doc("Additional Salary")
#     doc.employee = data.get("employee")
#     doc.company = data.get("company")
#     doc.salary_component = data.get("salary_component")
#     doc.amount = data.get("amount")
#     doc.payroll_date = getdate(data.get("payroll_date"))

#     # Optional fields
#     doc.is_recurring = data.get("is_recurring", 0)
#     doc.deduct_full_tax_on_selected_payroll_date = data.get(
#         "deduct_full_tax_on_selected_payroll_date", 0
#     )
#     doc.custom_is_tax_manual_calculate = data.get(
#         "custom_is_tax_manual_calculate", 0
#     )
#     doc.overwrite_salary_structure_amount = data.get(
#         "overwrite_salary_structure_amount", 0
#     )

#     # Insert & Submit
#     doc.insert(ignore_permissions=True)
#     doc.submit()

#     return {
#         "status": "success",
#         "message": "Additional Salary created successfully",
#         "name": doc.name
#     }



#http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.extra_payment_api.get_extra_payment_component?custom_is_reimbursement=1
#http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.extra_payment_api.get_extra_payment_component?custom_is_offcycle_component=1

@frappe.whitelist()
def get_extra_payment_component(
    custom_is_offcycle_component=None,
    custom_is_reimbursement=None
):

    filters = {
        "custom_is_extra_payment": 1
    }


    if custom_is_offcycle_component is not None:
        filters["custom_is_offcycle_component"] = int(custom_is_offcycle_component)

    if custom_is_reimbursement is not None:
        filters["custom_is_reimbursement"] = int(custom_is_reimbursement)


    components = frappe.get_all(
        "Salary Component",
        filters=filters,
        fields=[
            "name",
            "type",
            "description",
            "is_tax_applicable",
            "depends_on_payment_days",
            "custom_is_offcycle_component",
            "custom_is_reimbursement"
        ],
        order_by="name asc"
    )

    return {
        "status": "success",
        "total_records": len(components),
        "components": components
    }
