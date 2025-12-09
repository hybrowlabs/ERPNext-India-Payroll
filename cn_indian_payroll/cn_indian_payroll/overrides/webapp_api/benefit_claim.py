import frappe
from frappe.utils import getdate

from frappe.utils import add_months

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



#getting payroll period
#http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.benefit_claim.get_payroll_period

@frappe.whitelist()
def get_payroll_period():
    payroll_period = frappe.db.get_all("Payroll Period", fields=["name"])
    return payroll_period




#get max amount eligible for claim
#http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.benefit_claim.get_max_amount?employee=37001&earning_component=Car%20Lease%20Rental&claim_date=2025-07-4


@frappe.whitelist()
def get_max_amount(doc=None, employee=None, earning_component=None, claim_date=None):
    try:
        if doc:
            doc = frappe.parse_json(doc)
        else:
            doc = frappe._dict({
                "employee": employee,
                "earning_component": earning_component,
                "claim_date": claim_date
            })

        claim_dt = getdate(doc.claim_date)

        get_ssa = frappe.get_list(
            "Salary Structure Assignment",
            filters={
                "employee": doc.employee,
                "docstatus": 1,
                "from_date": ["<=", claim_dt],
            },
            fields=["name", "custom_payroll_period"],
            order_by="from_date desc",
            limit=1,
        )

        if not get_ssa:
            return {"status": "failed", "message": "No Salary Structure Assignment Found"}

        ssa_doc = frappe.get_doc("Salary Structure Assignment", get_ssa[0].name)
        payroll_period = get_ssa[0].custom_payroll_period

        pp = frappe.get_doc("Payroll Period", payroll_period)
        pp_start = getdate(pp.start_date)
        pp_end = getdate(pp.end_date)

        emp = frappe.get_doc("Employee", doc.employee)
        doj = getdate(emp.date_of_joining)
        accrual_start_date = max(pp_start, doj)

        if ssa_doc.custom_employee_reimbursements:

            for component in ssa_doc.custom_employee_reimbursements:

                if component.reimbursements == doc.earning_component:

                    salary_component = frappe.get_doc("Salary Component", component.reimbursements)

                    monthly_amount = component.monthly_total_amount or 0
                    advance_period = salary_component.custom_advance_period or 0

                    accruals = frappe.get_all(
                        "Employee Benefit Accrual",
                        filters={
                            "employee": doc.employee,
                            "salary_component": doc.earning_component,
                            "docstatus": 1,
                            "payroll_period": payroll_period,
                        },
                        fields=["amount"],
                    )
                    accrued_total = sum([row.amount for row in accruals])

                    claims = frappe.get_all(
                        "Employee Benefit Claim",
                        filters={
                            "employee": doc.employee,
                            "earning_component": doc.earning_component,
                            "docstatus": 1,
                            "custom_payroll_period": payroll_period,
                        },
                        fields=["custom_paid_amount", "claim_date"],
                        order_by="claim_date desc"
                    )

                    claimed_total = sum([row.custom_paid_amount for row in claims]) or 0

                    if claims:
                        last_claim = claims[0]
                        last_claim_date = getdate(last_claim.claim_date)

                        last_claim_allowed = monthly_amount * advance_period

                        if last_claim.custom_paid_amount > monthly_amount:

                            months_passed = (
                                (claim_dt.year - last_claim_date.year) * 12 +
                                (claim_dt.month - last_claim_date.month)
                            )

                            if months_passed < advance_period:
                                next_allowed = add_months(last_claim_date, advance_period)

                                return {
                                    "status": "failed",
                                    "message": f"You claimed an advance in {last_claim_date.strftime('%B')}. "
                                            f"Next eligible month: {next_allowed.strftime('%B %Y')}"
                                }

                    advance_allowed = monthly_amount * advance_period
                    max_allowed = accrued_total + advance_allowed

                    max_claimable = max_allowed - claimed_total
                    if max_claimable < 0:
                        max_claimable = 0

                    return {
                        "status": "success",
                        "data": {
                            "currently_allowed": max_claimable,

                            "monthly_reimbursement": monthly_amount
                        }
                    }
        else:
            return {"status": "failed", "message": "Component not found in Salary Structure"}

    except Exception as e:
        return {
            "status": "failed",
            "message": f"Server Error: {e}"
        }



#listing reimbursement components
#http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.benefit_claim.benefit_claim?employee=37001&claim_date=2025-07-4


@frappe.whitelist()
def benefit_claim(doc=None, employee=None, claim_date=None):
    # Handle both JSON doc and URL params
    if doc:
        doc = frappe.parse_json(doc)
    else:
        doc = frappe._dict({
            "employee": employee,
            "claim_date": claim_date
        })

    component_array = []

    # Get LTA reimbursement component (only first)
    lta_component_list = frappe.get_list(
        "Salary Component",
        filters={"component_type": "LTA Reimbursement"},
        fields=["name"],
        limit=1,
    )
    lta_component = lta_component_list[0].name if lta_component_list else None

    # Get Salary Structure Assignment valid for claim_date
    get_ssa = frappe.get_list(
        "Salary Structure Assignment",
        filters={
            "employee": doc.employee,
            "docstatus": 1,
            "from_date": ["<=", getdate(doc.claim_date)],
        },
        fields=["name", "custom_payroll_period"],
        order_by="from_date desc",
        limit=1,
    )

    payroll_period = None

    if get_ssa:
        ssa_doc = frappe.get_doc("Salary Structure Assignment", get_ssa[0].name)
        payroll_period = get_ssa[0].custom_payroll_period

        # Loop through reimbursement components in SSA
        for component in ssa_doc.custom_employee_reimbursements:
            if component.reimbursements != lta_component:
                salary_component = frappe.get_doc("Salary Component", component.reimbursements)
                if salary_component.pay_against_benefit_claim == 1:
                    component_array.append(component.reimbursements)

    return {
        "component_array": component_array,
        "payroll_period": payroll_period
    }
