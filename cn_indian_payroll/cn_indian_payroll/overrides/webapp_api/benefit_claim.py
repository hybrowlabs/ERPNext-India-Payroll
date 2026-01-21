import frappe
from frappe.utils import getdate

from frappe.utils import add_months
import frappe
from frappe import _
from datetime import datetime

from frappe.utils import formatdate
from datetime import datetime
from dateutil.relativedelta import relativedelta


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
#http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.benefit_claim.benefit_data_list_view?employee=37001&payroll_period=25-26&limit_start=0&limit_page_length=10


@frappe.whitelist()
def benefit_data_list_view(
    employee,
    company=None,
    payroll_period=None,
    start=0,
    page_length=1
):
    if not employee:
        return {"status": "failed", "message": "Employee is required"}

    # Ensure integers
    start = int(start)
    page_length = int(page_length)

    filters = {
        "employee": employee,
        "docstatus": ("in", [0, 1])
    }

    if company:
        filters["company"] = company

    if payroll_period:
        filters["custom_payroll_period"] = payroll_period

    # -----------------------------
    # Total count (optional)
    # -----------------------------
    total_count = frappe.db.count(
        "Employee Benefit Claim",
        filters=filters
    )

    # -----------------------------
    # Data with limit
    # -----------------------------
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
        order_by="claim_date desc",
        start=start,
        page_length=page_length
    )

    if not claims:
        return {
            "status": "success",
            "data": [],
            "total_records": total_count
        }

    # -----------------------------
    # Attachments
    # -----------------------------
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
        "data": claims,
        "total_count": total_count,
        "start": start,
        "page_length":page_length
    }


#http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.benefit_claim.benefit_payslip_list_view?employee=37001&payroll_period=25-26&limit_start=0&limit_page_length=10


@frappe.whitelist()
def benefit_payslip_list_view(
    employee,
    company=None,
    payroll_period=None,
    start=0,
    page_length=1
):
    target_employee = frappe.request.headers.get("X-Target-Employee-Id")
    if target_employee:
        employee = target_employee
    if not employee:
        return {"status": "failed", "message": "Employee is required"}

    # Ensure integers
    start = int(start)
    page_length = int(page_length)

    filters = {
        "employee": employee,
        "docstatus": ("in", [1])
    }

    if company:
        filters["company"] = company

    if payroll_period:
        filters["custom_payroll_period"] = payroll_period

    # -----------------------------
    # Total count (optional)
    # -----------------------------
    total_count = frappe.db.count(
        "Employee Benefit Claim",
        filters=filters
    )

    # -----------------------------
    # Data with limit
    # -----------------------------
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
        order_by="claim_date desc",
        start=start,
        page_length=page_length
    )

    if not claims:
        return {
            "status": "success",
            "data": [],
            "total_records": total_count
        }

    # -----------------------------
    # Attachments
    # -----------------------------
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
        "data": claims,
        "total_count": total_count,
        "start": start,
        "page_length": page_length
    }



#getting payroll period
#http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.benefit_claim.get_payroll_period

@frappe.whitelist()
def get_payroll_period(company):
    payroll_period = frappe.db.get_all("Payroll Period", fields=["name"],filters={"company": company}, order_by="start_date desc")
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
        target_employee = frappe.request.headers.get("X-Target-Employee-Id")
        if target_employee:
            employee = target_employee
            doc.employee = target_employee

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

                            "monthly_reimbursement": monthly_amount,
                            "payroll_period":payroll_period,
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
    target_employee = frappe.request.headers.get("X-Target-Employee-Id")
    if target_employee:
        employee = target_employee
        doc.employee = target_employee

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








# http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.benefit_claim.get_all_accrued_reimbursements?employee=37001&company=PW&payroll_period=25-26

# @frappe.whitelist()
# def get_all_accrued_reimbursements(filters=None):
#     if not filters:
#         filters = {}

#     from datetime import datetime


#     ssa_map = {}  # key → (employee, component)

#     ssa_filters = {}
#     target_employee = frappe.request.headers.get("X-Target-Employee-Id")
#     if target_employee:
#         filters["employee"] = target_employee
#     if filters.get("employee"):
#         ssa_filters["employee"] = filters["employee"]
#     if filters.get("payroll_period"):
#         ssa_filters["payroll_period"] = filters["payroll_period"]

#     salary_slips = frappe.get_list(
#         "Salary Slip",
#         filters=ssa_filters,
#         fields=["name", "employee", "custom_salary_structure_assignment"]
#     )

#     for slip in salary_slips:
#         if not slip.custom_salary_structure_assignment:
#             continue

#         ssa = frappe.get_doc("Salary Structure Assignment", slip.custom_salary_structure_assignment)

#         for row in ssa.custom_employee_reimbursements:
#             advance_period = (
#                 frappe.db.get_value("Salary Component", row.reimbursements, "custom_advance_period")
#                 or 0
#             )

#             ssa_map[(slip.employee, row.reimbursements)] = {
#                 "periodic_original_amount": row.monthly_total_amount or 0,
#                 "advance_period": advance_period,
#                 "advance_amount": (row.monthly_total_amount or 0) * advance_period,
#             }


#     accrual_filters = {"docstatus": 1}
#     if filters.get("employee"):
#         accrual_filters["employee"] = filters["employee"]
#     if filters.get("payroll_period"):
#         accrual_filters["payroll_period"] = filters["payroll_period"]
#     if filters.get("company"):
#         accrual_filters["company"] = filters["company"]

#     accrual_records = frappe.get_list(
#         "Employee Benefit Accrual",
#         filters=accrual_filters,
#         fields=["*"],
#         order_by="benefit_accrual_date"
#     )


#     claim_filters = {"docstatus": 1}
#     if filters.get("employee"):
#         claim_filters["employee"] = filters["employee"]
#     if filters.get("company"):
#         claim_filters["company"] = filters["company"]

#     claim_records = frappe.get_list(
#         "Employee Benefit Claim",
#         filters=claim_filters,
#         fields=[
#             "employee",
#             "company",
#             "custom_payroll_period",
#             "claim_date",
#             "earning_component",
#             "custom_paid_amount",
#             "claimed_amount",
#         ]
#     )





#     grouped = {}

#     for accrual in accrual_records:
#         # Convert date → "April 2025"
#         dt = datetime.strptime(str(accrual.benefit_accrual_date), "%Y-%m-%d")
#         month_label = dt.strftime("%B %Y")

#         # Find matching monthly claim amount
#         paid_amount = 0
#         claimed_amount=0
#         for claim in claim_records:
#             if (
#                 claim.employee == accrual.employee
#                 and claim.company == accrual.company
#                 and claim.custom_payroll_period == accrual.payroll_period
#                 and claim.earning_component == accrual.salary_component
#             ):

#                 if claim.claim_date:
#                     cdt = datetime.strptime(str(claim.claim_date), "%Y-%m-%d")
#                     if cdt.month == dt.month and cdt.year == dt.year:
#                         claimed_amount += round(claim.claimed_amount or 0)
#                         paid_amount += round(claim.custom_paid_amount or 0)


#         # SSA values
#         ssa_key = (accrual.employee, accrual.salary_component)
#         periodic_original_amount = ssa_map.get(ssa_key, {}).get("periodic_original_amount", 0)
#         advance_period = ssa_map.get(ssa_key, {}).get("advance_period", 0)
#         advance_amount = ssa_map.get(ssa_key, {}).get("advance_amount", 0)

#         # Initialise group per component
#         if accrual.salary_component not in grouped:
#             grouped[accrual.salary_component] = {
#                 "salary_component": accrual.salary_component,
#                 "carry_forward_amount": 0,
#                 "total_accrued_amount": 0,
#                 "periodic_original_amount": periodic_original_amount,
#                 "advance_period": advance_period,
#                 "advance_amount": advance_amount,
#                 "total_claimed_amount": 0,
#                 "total_balance_amount": 0,
#                 "details": []
#             }

#         # Calculate closing balance
#         closing_balance = (accrual.bill_amount or 0) - (paid_amount or 0)


#         grouped[accrual.salary_component]["details"].append({
#             "month": month_label,
#             "amount": accrual.amount,
#             "working_days": accrual.working_days,
#             "payment_days": accrual.payment_days,
#             "periodic_original_amount": periodic_original_amount,
#             "lop_days": accrual.lwp_days,
#             "arrear_days": accrual.lop_reversal_days,
#             "claimed_amount": round(claimed_amount),
#             "paid_amount": round(paid_amount),
#             "bill_amount": 0,
#             "balance_bill_amount": 0,
#             # "closing_balance": closing_balance,
#             "closing_balance": 0,
#         })

#         # Update summary totals
#         grouped[accrual.salary_component]["total_accrued_amount"] += accrual.amount
#         grouped[accrual.salary_component]["total_claimed_amount"] += paid_amount


#     for comp, row in grouped.items():
#         row["total_balance_amount"] = (
#             row["total_accrued_amount"]
#             - row["total_claimed_amount"]
#             + row["carry_forward_amount"]
#         )


#     return {"data": list(grouped.values())}







# http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.benefit_claim.get_all_accrued_reimbursements?company=PW&payroll_period=24-25&employee=37001

@frappe.whitelist()
def get_all_accrued_reimbursements(employee=None, company=None, payroll_period=None):

    target_employee = frappe.request.headers.get("X-Target-Employee-Id")
    if target_employee:
        employee = target_employee


    filters = {}
    if employee:
        filters["employee"] = employee
    if company:
        filters["company"] = company
    if payroll_period:
        filters["payroll_period"] = payroll_period

    ssa_map = {}

    ssa_filters = {}
    if employee:
        ssa_filters["employee"] = employee
    if payroll_period:
        ssa_filters["custom_payroll_period"] = payroll_period

    salary_slips = frappe.get_list(
        "Salary Slip",
        filters=ssa_filters,
        fields=["employee", "custom_salary_structure_assignment"]
    )

    for slip in salary_slips:
        if not slip.custom_salary_structure_assignment:
            continue

        ssa = frappe.get_doc(
            "Salary Structure Assignment",
            slip.custom_salary_structure_assignment
        )

        for row in ssa.custom_employee_reimbursements:
            advance_period = (
                frappe.db.get_value(
                    "Salary Component",
                    row.reimbursements,
                    "custom_advance_period"
                ) or 0
            )

            ssa_map[(slip.employee, row.reimbursements)] = {
                "periodic_original_amount": row.monthly_total_amount or 0,
                "advance_period": advance_period,
                "advance_amount": (row.monthly_total_amount or 0) * advance_period,
            }


    accrual_filters = {"docstatus": 1}
    if employee:
        accrual_filters["employee"] = employee
    if company:
        accrual_filters["company"] = company
    if payroll_period:
        accrual_filters["payroll_period"] = payroll_period

    accrual_records = frappe.get_list(
        "Employee Benefit Accrual",
        filters=accrual_filters,
        fields=["*"],
        order_by="benefit_accrual_date"
    )

    claim_filters = {"docstatus": 1}
    if employee:
        claim_filters["employee"] = employee
    if company:
        claim_filters["company"] = company

    claim_records = frappe.get_list(
        "Employee Benefit Claim",
        filters=claim_filters,
        fields=[
            "employee",
            "company",
            "custom_payroll_period",
            "claim_date",
            "earning_component",
            "claimed_amount",
            "custom_paid_amount"
        ]
    )

    payroll_period_doc = frappe.get_doc("Payroll Period", payroll_period)
    period_end_date = payroll_period_doc.end_date

    grouped = {}

    for accrual in accrual_records:
        accrual_date = accrual.benefit_accrual_date
        month_label = accrual_date.strftime("%B %Y")


        paid_amount = 0
        claimed_amount=0
        for claim in claim_records:
            if (
                claim.employee == accrual.employee
                and claim.company == accrual.company
                and claim.custom_payroll_period == accrual.payroll_period
                and claim.earning_component == accrual.salary_component
                and claim.claim_date
                and claim.claim_date.month == accrual_date.month
                and claim.claim_date.year == accrual_date.year
            ):
                claimed_amount += claim.claimed_amount or 0
                paid_amount += claim.custom_paid_amount or 0

        ssa_key = (accrual.employee, accrual.salary_component)
        ssa_data = ssa_map.get(ssa_key, {})

        if accrual.salary_component not in grouped:
            grouped[accrual.salary_component] = {
                "salary_component": accrual.salary_component,
                "carry_forward_amount": 0,
                "total_accrued_amount": 0,
                "periodic_original_amount": ssa_data.get("periodic_original_amount", 0),
                "advance_period": ssa_data.get("advance_period", 0),
                "advance_amount": ssa_data.get("advance_amount", 0),
                "total_claimed_amount": 0,
                "total_balance_amount": 0,
                "details": [],
                "last_accrual_date": accrual_date,
            }

        grouped[accrual.salary_component]["details"].append({
            "month": month_label,
            "amount": accrual.amount,
            "working_days": accrual.working_days,
            "payment_days": accrual.payment_days,
            "periodic_original_amount": ssa_data.get("periodic_original_amount", 0),
            "lop_days": accrual.lwp_days,
            "arrear_days": accrual.lop_reversal_days,
            "claimed_amount": round(claimed_amount),
            "paid_amount": round(paid_amount),
            "bill_amount": 0,
            "balance_bill_amount": 0,
            "closing_balance": 0,
            "is_projection": 0,
        })

        grouped[accrual.salary_component]["total_accrued_amount"] += round(accrual.amount)
        grouped[accrual.salary_component]["total_claimed_amount"] += round(paid_amount)
        grouped[accrual.salary_component]["last_accrual_date"] = accrual_date


    for comp, row in grouped.items():
        next_date = row["last_accrual_date"] + relativedelta(months=1)
        periodic_amount = row["periodic_original_amount"]

        while next_date <= period_end_date:
            row["details"].append({
                "month": next_date.strftime("%B %Y"),
                "amount": periodic_amount,
                "working_days": 0,
                "payment_days": 0,
                "periodic_original_amount": periodic_amount,
                "lop_days": 0,
                "arrear_days": 0,
                "claimed_amount": 0,
                "paid_amount": 0,
                "bill_amount": 0,
                "balance_bill_amount": 0,
                "closing_balance": 0,
                "is_projection": 1,
            })

            next_date += relativedelta(months=1)


        row["total_balance_amount"] = (
            row["total_accrued_amount"]
            - row["total_claimed_amount"]
            + row["carry_forward_amount"]
        )

        del row["last_accrual_date"]


    return {"data": list(grouped.values())}






#http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.benefit_claim.benefit_claim_locking_period?employee=37001&payroll_period=25-26&posting_date=2025-12-01&doctype_name=Employee%20Benefit%20Claim


@frappe.whitelist()
def benefit_claim_locking_period(
    employee,
    payroll_period,
    posting_date,
    doctype_name,
):

    if not (employee and payroll_period and posting_date and doctype_name):
        return {
            "status": "failed",
            "message": "Missing required details (Employee, Payroll Period, Posting Date, or Doctype).",
        }

    posting_date = getdate(posting_date)


    payroll_period_doc = frappe.get_doc("Payroll Period", payroll_period)
    start_date = getdate(payroll_period_doc.start_date)
    company = payroll_period_doc.company

    employee_doc = frappe.get_doc("Employee", employee)
    date_of_joining = getdate(employee_doc.date_of_joining)

    if date_of_joining > start_date:
        release_configs = frappe.get_list(
            "Release Config",
            filters={
                "company": company,
                "payroll_period": payroll_period,
                "frequency_type": "New Joinee",
            },
            pluck="name",
        )

        if not release_configs:
            return {
                "status": "success",
                "message": "No release configuration found. Claim allowed.",
            }

        config_doc = frappe.get_doc("Release Config", release_configs[0])

        if not any(
            d.declaration_type == doctype_name
            for d in (config_doc.locking_doctypes or [])
        ):
            return {
                "status": "success",
                "message": "Doctype not locked in release configuration.",
            }

        if not config_doc.user_assignment:

            for entry in config_doc.individual_benefit_claim_child or []:
                if entry.employee == employee:
                    if (
                        entry.active
                        and getdate(entry.start_date)
                        <= posting_date
                        <= getdate(entry.end_date)
                    ):
                        return {
                            "status": "success",
                            "message": "Claim allowed as per individual configuration.",
                        }

                    return {
                        "status": "failed",
                        "message": "Claim date is outside the allowed period for this employee.",
                    }

            for period in config_doc.locking_period_months_new_joining or []:
                if (
                    period.enable
                    and getdate(period.start_date)
                    <= posting_date
                    <= getdate(period.end_date)
                ):
                    return {
                        "status": "success",
                        "message": "Claim allowed within new joinee claim period.",
                    }

            return {
                "status": "failed",
                "message": "Claim date is outside the allowed new joinee claim period.",
            }

        for period in config_doc.locking_period_months_new_joining or []:
            if (
                period.enable
                and getdate(period.start_date)
                <= posting_date
                <= getdate(period.end_date)
            ):
                for assignment in config_doc.user_assignment:
                    assignment_doc = frappe.get_doc(
                        "Dynamic User Assignment",
                        assignment.select_visibility_restriction,
                    )
                    for user in assignment_doc.assigned_users or []:
                        if user.employee_id == employee:
                            return {
                                "status": "success",
                                "message": "Claim allowed based on user assignment (new joinee).",
                            }

        return {
            "status": "failed",
            "message": "Claims are not permitted for the selected date as the declaration period has been closed.",
        }



    release_configs = frappe.get_list(
        "Release Config",
        filters={
            "company": company,
            "payroll_period": payroll_period,
            "frequency_type": "Monthly",
        },
        pluck="name",
    )

    if not release_configs:
        return {
            "status": "success",
            "message": "No monthly release configuration found for " + doctype_name + ".allowed.",
        }

    config_doc = frappe.get_doc("Release Config", release_configs[0])

    if not any(
        d.declaration_type == doctype_name
        for d in (config_doc.locking_doctypes or [])
    ):
        return {
            "status": "success",
            "message": "Doctype not locked for this payroll period.",
        }

    if not config_doc.user_assignment:

        for entry in config_doc.individual_benefit_claim_child or []:
            if entry.employee == employee:
                if (
                    entry.active
                    and getdate(entry.start_date)
                    <= posting_date
                    <= getdate(entry.end_date)
                ):
                    return {
                        "status": "success",
                        "message": doctype_name+" allowed as per individual configuration." + formatdate(entry.start_date) + " to " + formatdate(entry.end_date),
                    }

                return {
                    "status": "failed",
                    "message": doctype_name+" period is locked for this employee From " + formatdate(entry.start_date) + " to " + formatdate(entry.end_date),
                }

        for period in config_doc.locking_period_months or []:
            if (
                period.enable
                and getdate(period.start_date)
                <= posting_date
                <= getdate(period.end_date)
            ):
                return {
                    "status": "success",
                    "message": doctype_name+" allowed within common locking period " + formatdate(period.start_date) + " to " + formatdate(period.end_date),
                }

        return {
            "status": "failed",
            "message": "The " + doctype_name + " period is locked." + formatdate(period.end_date),
        }


    for period in config_doc.locking_period_months or []:
        if (
            period.enable
            and getdate(period.start_date)
            <= posting_date
            <= getdate(period.end_date)
        ):
            for assignment in config_doc.user_assignment:
                assignment_doc = frappe.get_doc(
                    "Dynamic User Assignment",
                    assignment.select_visibility_restriction,
                )
                for user in assignment_doc.assigned_users or []:
                    if user.employee_id == employee:
                        return {
                            "status": "success",
                            "message": doctype_name+" allowed based on user assignment " + formatdate(period.start_date) + " to " + formatdate(period.end_date),
                        }

    return {
            "status": "failed",
            "message": doctype_name+" are not permitted for the selected date as the declaration period has been closed on"+ formatdate(period.end_date),
            }













#http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.benefit_claim.benefit_claim_locking_period_visibility?employee=37001&payroll_period=25-26&posting_date=2025-12-02&doctype=Employee%20Benefit%20Claim

def _claim_window_message(start_date, end_date):
    return (
        f"For this month, claims can be submitted between "
        f"{formatdate(start_date)} and {formatdate(end_date)}. "
        f"Please submit your claim before the end date."
    )


@frappe.whitelist()
def benefit_claim_locking_period_visibility(employee, payroll_period, posting_date, doctype):
    # -----------------------------------
    # Basic validation
    # -----------------------------------
    if not (employee and payroll_period and posting_date and doctype):
        return {
            "status": "failed",
            "message": "Missing required details to validate benefit claim.",
        }

    if doctype != "Employee Benefit Claim":
        return {
            "status": "success",
            "message": "No locking rules applicable for this document type.",
        }

    posting_date = getdate(posting_date)


    payroll_period_doc = frappe.get_doc("Payroll Period", payroll_period)
    period_start_date = getdate(payroll_period_doc.start_date)
    company = payroll_period_doc.company

    employee_doc = frappe.get_doc("Employee", employee)
    date_of_joining = getdate(employee_doc.date_of_joining)


    frequency_type = "Monthly"
    if date_of_joining > period_start_date:
        frequency_type = "New Joinee"


    release_configs = frappe.get_list(
        "Release Config",
        filters={
            "company": company,
            "payroll_period": payroll_period,
            "frequency_type": frequency_type,
        },
        pluck="name",
    )

    if not release_configs:
        return {
            "status": "success",
            "message": "No claim restrictions configured for this payroll period.",
        }

    config_doc = frappe.get_doc("Release Config", release_configs[0])


    if not any(
        d.declaration_type == "Employee Benefit Claim"
        for d in config_doc.locking_doctypes or []
    ):
        return {
            "status": "success",
            "message": "Benefit claims are not restricted for this payroll period.",
        }

    # Select correct date range table
    locking_periods = (
        config_doc.locking_period_months_new_joining
        if frequency_type == "New Joinee"
        else config_doc.locking_period_months
    )

    if not config_doc.user_assignment:

        # Individual override
        for entry in config_doc.individual_benefit_claim_child or []:
            if entry.employee == employee:
                if (
                    entry.active
                    and getdate(entry.start_date) <= posting_date <= getdate(entry.end_date)
                ):
                    return {
                        "status": "success",
                        "message": _claim_window_message(
                            entry.start_date, entry.end_date
                        ),
                    }

                return {
                    "status": "failed",
                    "message": _claim_window_message(
                        entry.start_date, entry.end_date
                    ),
                }

        # Common period
        for period in locking_periods or []:
            if period.enable:
                start = getdate(period.start_date)
                end = getdate(period.end_date)

                if start <= posting_date <= end:
                    return {
                        "status": "success",
                        "message": _claim_window_message(start, end),
                    }

                return {
                    "status": "failed",
                    "message": _claim_window_message(start, end),
                }


    for period in locking_periods or []:
        if period.enable:
            start = getdate(period.start_date)
            end = getdate(period.end_date)

            if start <= posting_date <= end:
                for assignment in config_doc.user_assignment:
                    assignment_doc = frappe.get_doc(
                        "Dynamic User Assignment",
                        assignment.select_visibility_restriction,
                    )
                    for user in assignment_doc.assigned_users or []:
                        if user.employee_id == employee:
                            return {
                                "status": "success",
                                "message": _claim_window_message(start, end),
                            }

                return {
                    "status": "failed",
                    "message": "You are not authorized to submit a claim during this period.",
                }


    return {
        "status": "failed",
        "message": "The claim submission window is currently closed.",
    }
