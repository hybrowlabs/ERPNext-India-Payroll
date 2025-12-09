import frappe

#view and dowaload benefit payslip

#http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.benefit_claim.get_benefit_payslip_pdf?id=HR-BEN-CLM-25-12-00001

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


#benefit claim list view
#http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.benefit_claim.benefit_payslip_list_view?employee=37001&payroll_period=25-26



@frappe.whitelist()
def benefit_payslip_list_view(employee, company=None, payroll_period=None):

    if not employee:
        return {"status": "failed", "message": "Employee is required"}

    filters = {"employee": employee, "docstatus": ("in", [0, 1])}

    if company:
        filters["company"] = company


    if payroll_period:
        filters["custom_payroll_period"] = payroll_period

    claims = frappe.db.get_all(
        "Employee Benefit Claim",
        filters=filters,
        fields=[
            "name",
            "employee",
            "employee_name",
            "custom_payroll_period",
            "claim_date",
            "company",
            "custom_status",
            "earning_component",
            "claimed_amount",
            "custom_note_by_employee",
            "custom_note_by_approver",
            "custom_is_taxable",
            "custom_taxable_amount",
            "custom_is_non_taxable",
            "custom_non_taxable_amount",
        ],
        order_by="claim_date desc"
    )


    if not claims:
        return {"status": "success", "data": []}


    for row in claims:
        row["attachments"] = frappe.db.get_all(
            "File",
            filters={
                "attached_to_doctype": "Employee Benefit Claim",
                "attached_to_name": row["name"],
            },
            fields=["file_url"]
        )

    return {
        "status": "success",
        "data": claims
    }


# @frappe.whitelist()
# def benefit_payslip_list_view(employee, payroll_period):
#     if not (employee and payroll_period):
#         return {"status": "failed", "message": "Employee and Payroll Period required"}

#     # Fetch records
#     claims = frappe.db.get_all(
#         "Employee Benefit Claim",
#         filters={
#             "employee": employee,
#             "custom_payroll_period":  payroll_period,
#             "docstatus": ("in", [0, 1])
#         },
#         fields=[
#             "name",
#             "employee",
#             "employee_name",
#             "custom_payroll_period",
#             "claim_date",
#             "company",
#             "custom_status",
#             "earning_component",
#             "claimed_amount",
#             "custom_note_by_employee",
#             "custom_note_by_approver",
#             "custom_is_taxable",
#             "custom_taxable_amount",
#             "custom_is_non_taxable",
#             "custom_non_taxable_amount",

#         ],
#         order_by="claim_date desc"
#     )

#     # Return empty list if no records
#     if not claims:
#         return {"status": "success", "data": []}

#     # Add attachments for each claim
#     for row in claims:
#         row["attachments"] = frappe.db.get_all(
#             "File",
#             filters={"attached_to_doctype": "Employee Benefit Claim", "attached_to_name": row["name"]},
#             fields=["file_url"]
#         )

#     return {
#         "status": "success",
#         "data": claims
#     }



#getting payroll period
#http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.benefit_claim.get_payroll_period

@frappe.whitelist()
def get_payroll_period():
    payroll_period = frappe.db.get_all("Payroll Period", fields=["name"])
    return payroll_period
