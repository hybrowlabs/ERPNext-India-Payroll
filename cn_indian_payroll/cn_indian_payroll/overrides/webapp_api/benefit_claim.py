import frappe


@frappe.whitelist()
def get_benefit_payslip_pdf(id):
    try:
        slip = frappe.get_doc("Employee Benefit Claim", id)


    except frappe.DoesNotExistError:
        return {"html": "<p>No Benefit slip found.</p>"}

    context = {"doc": slip}

    if slip.name:
        html = frappe.render_template(
            "cn_indian_payroll/templates/includes/benefit_payslip.html",
            context
        )
        return {"html": html}
    else:
        return {
            "html": """
                <div style="
                    padding: 12px;
                    margin: 10px 0;
                    border: 1px solid #f5c2c7;
                    background-color: #f8d7da;
                    color: #842029;
                    border-radius: 6px;
                    font-size: 14px;
                    font-family: Arial, sans-serif;
                ">
                    ⚠️ No Reimbursement component found in salary slip.
                </div>
            """
        }
