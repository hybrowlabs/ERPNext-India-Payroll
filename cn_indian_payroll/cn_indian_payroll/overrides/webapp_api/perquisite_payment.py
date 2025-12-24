# import frappe
# from frappe.utils import getdate



# #http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.perquisite_payment.get_perquisite_payment_list?employee=37001&company=PW&payroll_period=25-26
# @frappe.whitelist()
# def get_perquisite_payment_list(employee=None, company=None, payroll_period=None):
#     target_employee = frappe.request.headers.get("X-Target-Employee-Id")
#     if target_employee:
#         employee = target_employee

#     if not employee:
#         return {
#             "status": "failed",
#             "message": "Employee is required."
#         }

#     if not company:
#         return {
#             "status": "failed",
#             "message": "Company is required."
#         }

#     filters = {
#         "employee": employee,
#         "company": company,
#         "docstatus": 1
#     }

#     payroll_period_name = None


#     if payroll_period:
#         pp_doc = frappe.get_doc("Payroll Period", payroll_period)
#         payroll_period_name = pp_doc.name

#         filters["payroll_date"] = [
#             "between",
#             [getdate(pp_doc.start_date), getdate(pp_doc.end_date)]
#         ]

#     additional_salary_list = frappe.db.get_all(
#         "Additional Salary",
#         filters=filters,
#         fields=[
#             "name",
#             "salary_component",
#             "amount",
#             "payroll_date"
#         ],
#         order_by="payroll_date desc"
#     )

#     if not additional_salary_list:
#         return {
#             "status": "success",
#             "employee": employee,
#             "company": company,
#             "payroll_period": payroll_period_name,
#             "total_records": 0,
#             "extra_payments": []
#         }


#     extra_payments = []

#     for entry in additional_salary_list:
#         comp = frappe.get_cached_doc(
#             "Salary Component",
#             entry.salary_component
#         )

#         if comp.custom_perquisite:
#             extra_payments.append({
#                 "name": entry.name,
#                 "salary_component": entry.salary_component,
#                 "amount": entry.amount,
#                 "payment_date": entry.payroll_date,
#                 "is_tax_applicable": comp.is_tax_applicable
#             })

#     return {
#         "status": "success",
#         "employee": employee,
#         "company": company,
#         "payroll_period": payroll_period_name,
#         "total_records": len(extra_payments),
#         "extra_payments": extra_payments
#     }
import frappe
from frappe.utils import getdate


@frappe.whitelist()
def get_perquisite_payment_list(employee=None, company=None, payroll_period=None):
    target_employee = frappe.request.headers.get("X-Target-Employee-Id")
    if target_employee:
        employee = target_employee

    # ----------- Validation (return, not throw) -----------
    if not employee or not company:
        return ({
            "status": "failed",
            "message": "Employee and Company are required."
        })

    filters = {
        "employee": employee,
        "company": company,
        "docstatus": 1
    }

    payroll_period_name = None

    if payroll_period and frappe.db.exists("Payroll Period", payroll_period):
        pp_doc = frappe.get_doc("Payroll Period", payroll_period)
        payroll_period_name = pp_doc.name
        filters["payroll_date"] = [
            "between",
            [getdate(pp_doc.start_date), getdate(pp_doc.end_date)]
        ]

    additional_salary_list = frappe.db.get_all(
        "Additional Salary",
        filters=filters,
        fields=["name", "salary_component", "amount", "payroll_date"],
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
        comp = frappe.get_cached_doc("Salary Component", entry.salary_component)

        if comp.custom_perquisite:
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
