
import frappe
from frappe.utils import getdate



#http://127.0.0.1:8002/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.perquisite_payment.get_perquisite_payment_list?employee=PW0220&company=Pen pencil&payroll_period=25-26
@frappe.whitelist()
def get_perquisite_payment_list(employee=None, company=None, payroll_period=None, start=0, page_length=10, order_by=None, search_term=None):

    target_employee = frappe.request.headers.get("X-Target-Employee-Id")
    if target_employee:
        employee = target_employee

    if not employee or not company:
        return {
            "status": "failed",
            "message": "Employee and Company are required."
        }

    start = int(start)
    page_length = int(page_length)

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

    additional_salary_list = frappe.get_all(
        "Additional Salary",
        filters=filters,
        fields=["name", "salary_component", "amount", "payroll_date","employee","employee_name"],
        order_by=order_by or "creation desc"
    )

    result = []

    for entry in additional_salary_list:
        comp = frappe.get_cached_doc("Salary Component", entry.salary_component)

        if comp.custom_perquisite:
            result.append({
                "employee":entry.employee,
                "employee_name":entry.employee_name,
                "name": entry.name,
                "salary_component": entry.salary_component,
                "amount": round(entry.amount or 0),
                "payment_date": entry.payroll_date,
                "is_tax_applicable": comp.is_tax_applicable
            })

    if search_term:
        search = search_term.lower()
        result = [
            row for row in result
            if (
                search in str(row.get("name") or "").lower()
                or search in str(row.get("salary_component") or "").lower()
                or search in str(row.get("amount") or "").lower()
            )
        ]

    total_count = len(result)

    paginated_data = result[start:start + page_length]

    return {
        "status": "success",
        "total_count": total_count,
        "start": start,
        "page_length": page_length,
        "data": paginated_data
    }
