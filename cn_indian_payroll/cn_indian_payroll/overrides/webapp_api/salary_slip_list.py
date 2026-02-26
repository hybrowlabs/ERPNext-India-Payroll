
import frappe

from cn_indian_payroll.cn_indian_payroll.doctype.contract_employee_setting.contract_employee_setting import get_invoice_status


@frappe.whitelist()
def get_salary_slip_list(employee=None, company=None):

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
        ],
        order_by="end_date desc",
    )

    result = []

    for slip in salary_slips:

        # Call imported function
        invoice_status = get_invoice_status(slip["name"])

        # Add status to response
        slip["invoice_status"] = invoice_status

        result.append(slip)

    return result




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
