import frappe


@frappe.whitelist()
def get_salary_slip_list(employee=None, company=None):
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
        ],
        order_by="end_date desc",
    )
    return salary_slips



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
