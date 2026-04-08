
import frappe
from cn_indian_payroll.cn_indian_payroll.doctype.contract_employee_setting.contract_employee_setting import get_invoice_status



@frappe.whitelist()
def get_salary_slip_list(employee=None, company=None,start=0,page_length=10,order_by=None,search_term=None):

    target_employee = frappe.request.headers.get("X-Target-Employee-Id")
    if target_employee:
        employee = target_employee

    salary_slips = frappe.get_all(
        "Salary Slip",
        filters={
            "employee": employee,
            "company": company,
            "docstatus": ["in", [0, 1]],
        },
        fields=[
            "name",
            "employee_name",
            "start_date",
            "end_date",
            "gross_pay",
            "net_pay",
            "employee",
            "custom_payroll_period",
            "custom_month",
            "custom_attach",
            "status",
            
        ],
        # order_by="end_date desc",
        order_by=order_by
    )


    if search_term:
        search = search_term.lower()

        salary_slips = [
            row for row in salary_slips
            if (
                search in (row.get("name") or "").lower()
                or search in (row.get("employee_name") or "").lower()
                or search in (row.get("custom_month") or "").lower()
            )
        ]

    total_count = len(salary_slips)
    salary_slips = salary_slips[start:start + page_length]

    result = []

    for slip in salary_slips:

        # Call imported function
        invoice_status = get_invoice_status(slip["name"])

        # Add status to response
        slip["invoice_status"] = invoice_status

        result.append(slip)

    return {
        "status": "success",
        "total_count": total_count,
        "start": start,
        "page_length": page_length,
        "data": result
    }




@frappe.whitelist()
def get_consultant_payslip_pdf(slip_id):
    try:
        slip = frappe.get_doc("Salary Slip", slip_id)
    except frappe.DoesNotExistError:
        return {"html": "<p>No salary slip found.</p>"}

    context = {"doc": slip}

    html = frappe.render_template(
        "cn_indian_payroll/templates/includes/invoice.html",
        context
    )

    return {"html": html}
