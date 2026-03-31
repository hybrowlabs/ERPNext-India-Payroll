import frappe
from frappe.utils import getdate

from frappe.utils import add_months
import frappe
from frappe import _
from datetime import datetime

from frappe.utils import formatdate
from datetime import datetime
from dateutil.relativedelta import relativedelta
import frappe
from datetime import datetime
import calendar


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


# @frappe.whitelist()
# def benefit_data_list_view(
#     employee,
#     company=None,
#     payroll_period=None,
#     start=0,
#     page_length=1,
#     custom_status=None,
#     earning_component=None,
# ):
#     if not employee:
#         return {"status": "failed", "message": "Employee is required"}

#     # Ensure integers
#     start = int(start)
#     page_length = int(page_length)

#     filters = {
#         "employee": employee,
#         "docstatus": ("in", [0, 1])
#     }

#     if company:
#         filters["company"] = company

#     if payroll_period:
#         filters["custom_payroll_period"] = payroll_period

#     if earning_component:
#         filters["earning_component"] = earning_component

#     if custom_status and custom_status != "All":
#         filters["custom_status"] = custom_status

#     # -----------------------------
#     # Total count (optional)
#     # -----------------------------
#     total_count = frappe.db.count(
#         "Employee Benefit Claim",
#         filters=filters
#     )

#     # -----------------------------
#     # Data with limit
#     # -----------------------------
#     claims = frappe.db.get_all(
#         "Employee Benefit Claim",
#         filters=filters,
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
#             "can_edit",
#             # "attachments"
#         ],
#         order_by="claim_date desc",
#         start=start,
#         page_length=page_length
#     )

#     if not claims:
#         return {
#             "status": "success",
#             "data": [],
#             "total_records": total_count
#         }

#     # -----------------------------
#     # Attachments
#     # -----------------------------
#     for row in claims:
#         row["attachments"] = frappe.db.get_all(
#             "File",
#             filters={
#                 "attached_to_doctype": "Employee Benefit Claim",
#                 "attached_to_name": row["name"],
#             },
#             fields=["file_url"]
#         )

       

#     return {
#         "status": "success",
#         "data": claims,
#         "total_count": total_count,
#         "start": start,
#         "page_length":page_length
#     }


# http://127.0.0.1:8002/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.benefit_claim.benefit_data_list_view?employee=PW0220&payroll_period=25-26&limit_start=0&limit_page_length=10&todo_status=Open&serach_term=HR-BEN-CLM-26-03-00009

@frappe.whitelist()
def benefit_data_list_view(
    employee,
    company=None,
    payroll_period=None,
    start=0,
    page_length=10,
    custom_status=None,
    earning_component=None,
    todo_status=None,
    # filters=None,
    search_term=None,
):
    if not employee:
        return {"status": "failed", "message": "Employee is required"}

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

    if earning_component:
        filters["earning_component"] = earning_component

    if custom_status and custom_status != "All":
        filters["custom_status"] = custom_status


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
            "can_edit",
        ],
        order_by="claim_date desc",
        start=start,
        page_length=page_length
    )

    total_count = frappe.db.count("Employee Benefit Claim", filters=filters)

    if not claims:
        return {
            "status": "success",
            "data": [],
            "total_count": total_count,
            "todo_list": []
        }


    for row in claims:
        row["attachments"] = frappe.db.get_all(
            "File",
            filters={
                "attached_to_doctype": "Employee Benefit Claim",
                "attached_to_name": row["name"],
            },
            fields=["file_url"]
        )


    todo_response = get_open_approval_todos(
        doctype="Employee Benefit Claim",
        start=0,
        page_length=1000,
        include_allocated_todos=False,
        todo_status=todo_status,
        # filters=filters
        search_term=search_term

    )


    # Create mapping: claim_name -> todos
    todo_map = {}

    if todo_response and todo_response.get("data"):
        for todo in todo_response.get("data"):
            ref_name = todo.get("reference_name")
            if ref_name:
                todo_map.setdefault(ref_name, []).append(todo)

    # Attach todos to each claim
    for row in claims:
        row["todo_list"] = todo_map.get(row["name"], [])

    # -----------------------------
    # Final Response
    # -----------------------------
    return {
        "status": "success",
        "data": claims,   
        "total_count": total_count,
        "start": start,
        "page_length": page_length,
        
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
            "message": doctype_name+" are not permitted for the selected date as the period has been closed.",
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




def _declaration_window_message(start_date, end_date, doctype):
    return (
        f"For this month, {doctype} can be submitted between "
        f"{formatdate(start_date)} and {formatdate(end_date)}. "
        f"Please submit your {doctype} before the end date."
    )


@frappe.whitelist()
def declaration_locking_period_visibility(employee, payroll_period, posting_date, doctype):

    if not (employee and payroll_period and posting_date and doctype):
        return {
            "status": "failed",
            "message": "The declaration form is not valid because no Salary Structure Assignment is assigned to the employee.",
        }

    posting_date = getdate(posting_date)

    payroll_period_doc = frappe.get_doc("Payroll Period", payroll_period)
    period_start_date = getdate(payroll_period_doc.start_date)
    company = payroll_period_doc.company

    employee_doc = frappe.get_doc("Employee", employee)
    date_of_joining = getdate(employee_doc.date_of_joining)

    frequency_type = (
        "New Joinee"
        if date_of_joining and date_of_joining > period_start_date
        else "Monthly"
    )

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
            "status": "failed",
            "message": f"No {doctype} restrictions configured for Current Release Config.",
        }

    config_doc = frappe.get_doc("Release Config", release_configs[0])

    locking_periods = (
        config_doc.locking_period_months_new_joining
        if frequency_type == "New Joinee"
        else config_doc.locking_period_months
    )


    if not config_doc.user_assignment:

        for entry in config_doc.individual_benefit_claim_child or []:
            if entry.employee == employee:
                start = getdate(entry.start_date)
                end = getdate(entry.end_date)

                if entry.active and start <= posting_date <= end:
                    return {
                        "status": "success",
                        "message": _declaration_window_message(start, end, doctype),
                    }

                return {
                    "status": "failed",
                    "message": _declaration_window_message(start, end, doctype),
                }

        # Common locking period
        for period in locking_periods or []:
            if period.enable:
                start = getdate(period.start_date)
                end = getdate(period.end_date)

                if start <= posting_date <= end:
                    return {
                        "status": "success",
                        "message": _declaration_window_message(start, end, doctype),
                    }

        return {
            "status": "failed",
            "message": f"The {doctype} submission window is currently closed.Yocannot select and enter the investments",

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
                                "message": _declaration_window_message(start, end, doctype),
                            }

                return {
                    "status": "failed",
                    "message": f"You are not authorized to submit {doctype} during this period.",
                }

    return {
        "status": "failed",
        "message": f"The {doctype} submission window is currently closed. You cannot select or enter investments.",
    }



@frappe.whitelist()
def benefit_data_dashboard(company=None, payroll_period=None, status=None, month=None):

    filters = {
        "docstatus": ("in", [0, 1]),
    }

    if company:
        filters["company"] = company

    if payroll_period:
        filters["custom_payroll_period"] = payroll_period

    if status:
        filters["custom_status"] = status

    from_date = None
    to_date = None

    # 🔥 FIXED MONTH LOGIC
    if month and payroll_period:

        period = frappe.db.get_value(
            "Payroll Period",
            payroll_period,
            ["start_date", "end_date"],
            as_dict=True
        )

        if period:

            start_year = period.start_date.year   # 2025
            end_year = period.end_date.year       # 2026

            month_number = datetime.strptime(month, "%B").month

            # ✅ FINANCIAL YEAR LOGIC
            if month_number >= 4:
                year = start_year
            else:
                year = end_year

            last_day = calendar.monthrange(year, month_number)[1]

            from_date = f"{year}-{month_number:02d}-01"
            to_date = f"{year}-{month_number:02d}-{last_day}"

            filters["claim_date"] = ["between", [from_date, to_date]]

    # FETCH DATA
    claims = frappe.db.get_all(
        "Employee Benefit Claim",
        filters=filters,
        fields=[
            "name",
            "employee_name",
            "custom_payroll_period",
            "claim_date",
            "custom_status",
            "earning_component",
            "claimed_amount",
        ],
        order_by="claim_date desc",
    )

    return {
        "status": "success",
        "data": claims,
        "total_records": len(claims),
        "from_date": from_date,
        "to_date": to_date
    }



@frappe.whitelist()
def _get_todo_info_for_doc(doctype, docname):
    """Get allocated_to, username, allocated_to_user, and allocated_to_roles from open ToDo."""
    info = {"allocated_to": [], "username": None, "allocated_to_user": None, "allocated_to_roles": []}
    try:
        todo = frappe.db.get_value(
            "ToDo",
            {"reference_type": doctype, "reference_name": docname, "status": "Open"},
            ["name", "allocated_to", "role"],
            as_dict=True
        )
        if not todo:
            return info

        allocated_to_names = []
        allocated_roles = []

        if todo.allocated_to:
            full_name = frappe.db.get_value("User", todo.allocated_to, "full_name")
            info["username"] = full_name
            info["allocated_to_user"] = todo.allocated_to
            allocated_to_names.append(full_name or todo.allocated_to)

        if todo.role:
            allocated_roles.append(todo.role)

        try:
            alloc_users = frappe.get_all(
                "Nextai User Select",
                filters={"parent": todo.name, "parentfield": "custom_allocated_to_users"},
                fields=["user"]
            )
            for u in alloc_users:
                if u.user and u.user != todo.allocated_to:
                    uname = frappe.db.get_value("User", u.user, "full_name")
                    allocated_to_names.append(uname or u.user)
        except Exception:
            pass

        try:
            assigned_roles = frappe.get_all(
                "Nextai Role Select",
                filters={"parent": todo.name, "parentfield": "custom_assigned_to_roles"},
                fields=["role"]
            )
            for r in assigned_roles:
                if r.role:
                    allocated_roles.append(r.role)
        except Exception:
            pass

        info["allocated_to"] = allocated_to_names
        info["allocated_to_roles"] = list(dict.fromkeys(allocated_roles))
    except Exception:
        pass
    return info   




@frappe.whitelist()
def get_open_approval_todos(doctype=None, status=None, filters=None, start=0, page_length=20, include_allocated_todos=False, date=None, todo_status=None, search_term=None, order_by=None):
    current_user = frappe.session.user

    # Check if target employee is passed in header
    target_employee = frappe.request.headers.get("X-Target-Employee-Id")


    # If target employee is provided, use it; otherwise fall back to session user's employee
    if target_employee:
        # Validate that target employee exists
        if not frappe.db.exists("Employee", target_employee):
            return {"data": [], "total_count": 0, "error": "Target employee not found"}
        employee = target_employee
    else:
        employee = frappe.get_value("Employee", {"user_id": current_user}, "name")
        
        if not employee:
            return {"data": [], "total_count": 0}
        

    user_roles = frappe.get_roles(current_user)


    # Get direct reportees for team todos filtering
    direct_reportees = set()
    if employee:
        direct_reportees = set(
            frappe.get_all("Employee", filters={"reports_to": employee, "status": "Active"}, pluck="name")
        )

    if isinstance(filters, str):
        try:
            filters = frappe.parse_json(filters)
        except:
            filters = {}
    elif not filters:
        filters = {}

    # Convert search_term to lowercase for case-insensitive search
    if search_term:
        search_term = str(search_term).lower().strip()

    todo_filters = {
        "custom_approval_type": "Approval Matrix"
    }

    if doctype:
        todo_filters["reference_type"] = doctype

    if date:
        date_parts = [d.strip() for d in date.split(",") if d.strip()]
        if len(date_parts) >= 2:
            start_date, end_date = date_parts[0], date_parts[1]
            todo_filters["date"] = ["Between", [start_date, end_date]]
        elif len(date_parts) == 1:
            todo_filters["date"] = ["=", date_parts[0]]


    start = int(start) if start else 0
    page_length = int(page_length) if page_length else 20

    if isinstance(include_allocated_todos, str):
        include_allocated_todos = include_allocated_todos.lower() in ['true', '1', 'yes']
    else:
        include_allocated_todos = bool(include_allocated_todos)


    all_todos = frappe.db.get_all(
        "ToDo",
        filters=todo_filters,
        fields=[
            "name",
            "allocated_to",
            "role",
            "reference_type",
            "reference_name",
            "custom_doctype_actions",
            "custom_allow_revoke",
            "date",
            "description",
            "custom_doctype_actions_with_form",
            "custom_approval_type",
            "status",
            "modified",
            "custom_selected_doctype_action"
        ]
    )

    

    reference_todos_map = {}
    for todo in all_todos:
        if todo.reference_type and todo.reference_name:
            ref_key = f"{todo.reference_type}::{todo.reference_name}"
            if ref_key not in reference_todos_map:
                reference_todos_map[ref_key] = []
            reference_todos_map[ref_key].append(todo)

    filtered_unique_todos = []
    for ref_key, todos in reference_todos_map.items():
        if todo_status:
            filtered_unique_todos.extend(todos)
        elif include_allocated_todos:
            open_todos = [t for t in todos if t.status == "Open"]
            if open_todos:
                filtered_unique_todos.extend(open_todos)
            else:
                filtered_unique_todos.extend(todos)
        else:
            latest_todo = max(todos, key=lambda t: t.modified)
            filtered_unique_todos.append(latest_todo)

    filtered_todos = []

    # Build a set of permitted document references using frappe.get_list (respects user permissions)
    permitted_docs = set()
    reference_types = list(set([t.reference_type for t in filtered_unique_todos if t.reference_type]))

    for ref_type in reference_types:
        # Get all document names of this type that current_user has permission to read
        ref_names_for_type = [t.reference_name for t in filtered_unique_todos if t.reference_type == ref_type and t.reference_name]
        if ref_names_for_type:
            # frappe.get_list automatically applies user permissions
            permitted_list = frappe.db.get_all(
                ref_type,
                filters={"name": ["in", ref_names_for_type]},
                fields=["name"],
                ignore_ifnull=True
            )
            for doc in permitted_list:
                permitted_docs.add(f"{ref_type}::{doc.name}")


    for todo in filtered_unique_todos:
        if todo.reference_type and todo.reference_name:
            try:
                # Permission check: Only include documents the session user has permission to read (using get_list result)
                ref_key = f"{todo.reference_type}::{todo.reference_name}"
                if ref_key not in permitted_docs:
                    continue

                reference_doc = frappe.get_doc(todo.reference_type, todo.reference_name)
                meta = frappe.get_meta(todo.reference_type)

                employee_fields = []
                for field in meta.get("fields"):
                    if field.fieldtype == "Link" and field.options == "Employee":
                        employee_fields.append(field.fieldname)

                should_include = False
                is_allocated_todo = False

                # If target_employee is provided via header, skip allocation check and just match employee field
                if target_employee:
                    for field_name in employee_fields:
                        field_value = reference_doc.get(field_name)
                        if field_value == employee:
                            should_include = True
                            break
                else:
                    # Original allocation logic when no target_employee header
                    if todo.allocated_to == current_user:
                        is_allocated_todo = True
                    elif todo.get("role") and todo.role in user_roles:
                        is_allocated_todo = True

                    if not is_allocated_todo:
                        try:
                            allocated_users = frappe.get_all(
                                "Nextai User Select",
                                filters={"parent": todo.name, "parentfield": "custom_allocated_to_users"},
                                fields=["user"]
                            )
                            if any(u.user == current_user for u in allocated_users):
                                is_allocated_todo = True
                        except Exception:
                            pass

                    if not is_allocated_todo:
                        try:
                            assigned_roles = frappe.get_all(
                                "Nextai Role Select",
                                filters={"parent": todo.name, "parentfield": "custom_assigned_to_roles"},
                                fields=["role"]
                            )
                            if any(r.role in user_roles for r in assigned_roles):
                                is_allocated_todo = True
                        except Exception:
                            pass

                    is_own_document = False
                    if todo.reference_type == "Employee":
                        if reference_doc.name == employee:
                            is_own_document = True
                    else:
                        for field_name in employee_fields:
                            field_value = reference_doc.get(field_name)
                            if field_value == employee:
                                is_own_document = True
                                break

                    if is_own_document:
                        if not include_allocated_todos:
                            should_include = True
                    elif is_allocated_todo:
                        if include_allocated_todos:
                            # Only show team todos for direct reportees
                            doc_employee = None
                            if todo.reference_type == "Employee":
                                doc_employee = reference_doc.name
                            else:
                                for field_name in employee_fields:
                                    field_value = reference_doc.get(field_name)
                                    if field_value:
                                        doc_employee = field_value
                                        break
                            if doc_employee and doc_employee in direct_reportees:
                                should_include = True

                if should_include:
                    passes_all_filters = True

                    if status and not filters.get("status"):
                        filters["status"] = status

                    for field_name, filter_condition in filters.items():
                        field_value = None

                        if hasattr(reference_doc, field_name):
                            field_value = reference_doc.get(field_name)
                        elif hasattr(todo, field_name):
                            field_value = getattr(todo, field_name)

                        if not evaluate_filter_condition(field_value, filter_condition):
                            passes_all_filters = False
                            break

                    # Apply global search term across all searchable fields
                    if passes_all_filters and search_term:
                        found_match = False

                        # Define searchable field types
                        searchable_fieldtypes = ["Data", "Text", "Small Text", "Long Text",
                                                "Select", "Link", "Dynamic Link", "Read Only"]

                        # Search in reference document fields
                        for field in meta.get("fields"):
                            if field.fieldtype in searchable_fieldtypes:
                                field_value = reference_doc.get(field.fieldname)
                                if field_value:
                                    # Convert to string and lowercase for comparison
                                    field_str = str(field_value).lower()
                                    # Check if search term is in field value (partial match)
                                    if search_term in field_str:
                                        found_match = True
                                        break

                        # Also search in common standard fields
                        if not found_match:
                            standard_fields = ["name", "owner", "modified_by"]
                            for field_name in standard_fields:
                                if hasattr(reference_doc, field_name):
                                    field_value = reference_doc.get(field_name)
                                    if field_value:
                                        field_str = str(field_value).lower()
                                        if search_term in field_str:
                                            found_match = True
                                            break

                        # Also search in todo description
                        if not found_match and todo.description:
                            if search_term in str(todo.description).lower():
                                found_match = True

                        # If no match found, filter out this record
                        if not found_match:
                            passes_all_filters = False

                    if passes_all_filters:
                        filtered_todos.append({
                            "todo": todo,
                            "reference_doc": reference_doc,
                            "is_allocated_todo": is_allocated_todo
                        })

            except (frappe.DoesNotExistError, Exception):
                continue


    if todo_status:
        if isinstance(todo_status, str):
            try:
                todo_status = frappe.parse_json(todo_status)
            except:
                pass
        filtered_todos = [t for t in filtered_todos if evaluate_filter_condition(t["todo"].status, todo_status)]

    # Apply order_by sorting on reference document fields before pagination
    # Supports format: "field_name" (asc) or "field_name desc" / "field_name asc"
    if order_by:
        parts = order_by.strip().split()
        sort_field = parts[0]
        sort_desc = len(parts) > 1 and parts[1].lower() == "desc"

        def get_sort_value(item):
            val = item["reference_doc"].get(sort_field)
            return val if val is not None else ""

        filtered_todos = sorted(filtered_todos, key=get_sort_value, reverse=sort_desc)

    total_filtered_count = len(filtered_todos)
    paginated_todos = filtered_todos[start:start + page_length]

    result = []
    for item in paginated_todos:
        todo = item["todo"]
        reference_doc = item["reference_doc"]
        is_allocated_todo = item.get("is_allocated_todo", False)

        allocated_to_full_name = frappe.get_value("User", todo.allocated_to, "full_name") if todo.allocated_to else None
        allocated_to_emp_id = frappe.get_value("Employee", {"user_id": todo.allocated_to}, "name") if todo.allocated_to else None

        status_value = reference_doc.get("status") if hasattr(reference_doc, "status") else None


        has_send_back = False
        send_back_user = None
        can_edit = False

        if todo.custom_doctype_actions:
            try:
                actions = frappe.parse_json(todo.custom_doctype_actions) if isinstance(todo.custom_doctype_actions, str) else todo.custom_doctype_actions
                if isinstance(actions, list) and "Send Back" in actions:
                    has_send_back = True
            except:
                if isinstance(todo.custom_doctype_actions, str) and "Send Back" in todo.custom_doctype_actions:
                    has_send_back = True

        if not has_send_back and todo.custom_doctype_actions_with_form:
            try:
                actions_with_form = frappe.parse_json(todo.custom_doctype_actions_with_form) if isinstance(todo.custom_doctype_actions_with_form, str) else todo.custom_doctype_actions_with_form
                if isinstance(actions_with_form, list) and "Send Back" in actions_with_form:
                    has_send_back = True
            except:
                if isinstance(todo.custom_doctype_actions_with_form, str) and "Send Back" in todo.custom_doctype_actions_with_form:
                    has_send_back = True

        if has_send_back:
            try:
                approval_tracker = frappe.get_all(
                    "Approval Tracker",
                    filters={
                        "doc_type": todo.reference_type,
                        "doc_name": todo.reference_name,
                        "status": "Send Back"
                    },
                    fields=["name"],
                    limit=1
                )

                if approval_tracker:
                    tracker_doc = frappe.get_doc("Approval Tracker", approval_tracker[0].name)

                    for log_entry in tracker_doc.get("approval_logs", []):
                        if log_entry.status == "Send Back" and log_entry.todo_reference == todo.name:
                            send_back_user = log_entry.send_back_user
                            if send_back_user == current_user:
                                can_edit = True
                            break

                    if not send_back_user:
                        for log_entry in tracker_doc.get("approval_logs", []):
                            if log_entry.status == "Send Back" and log_entry.send_back_user:
                                send_back_user = log_entry.send_back_user
                                if send_back_user == current_user:
                                    can_edit = True
                                break
            except Exception as e:
                frappe.log_error(f"Error finding Approval Tracker for todo {todo.name}: {str(e)}")

        approval_tracker_doc = None
        mapped_stages_status = []
        try:
            approval_tracker_name_list = frappe.db.sql(
                """
                SELECT name FROM `tabApproval Tracker`
                WHERE doc_name = %s AND doc_type = %s
                LIMIT 1
                """,
                (todo.reference_name, todo.reference_type),
                as_dict=True
            )
            if approval_tracker_name_list:
                approval_tracker_name = approval_tracker_name_list[0]['name']
                approval_tracker_doc = frappe.get_doc("Approval Tracker", approval_tracker_name).as_dict()

                approval_stages = approval_tracker_doc.get("approval_stages", [])
                approval_logs = approval_tracker_doc.get("approval_logs", [])
                log_count = len(approval_logs)

                for idx, stage in enumerate(approval_stages):
                    stage_role = stage.get("role")
                    
                    final_user = None
                    final_user_id = None
                    stage_status = "Pending"
                    approval_response_data = None
                    form_json = None
                    approval_time = None
                    if idx < log_count:
                        log_user = approval_logs[idx].get("user")
                        stage_status = approval_logs[idx].get("status", "Pending")
                        log_entry = approval_logs[idx]
                        approval_time = log_entry.get("approval_time")
                        if log_user:
                            final_user = frappe.get_value("User", log_user, "full_name")
                            final_user_id = log_user

                        form_for_approval = log_entry.get("form_for_approval")
                        if form_for_approval:
                            approval_response_data = log_entry.get("approval_response_data")
                            try:
                                custom_form_data = frappe.db.get_value(
                                    "Microapp Form Widget",
                                    form_for_approval,
                                    "custom_form_data"
                                )
                                if custom_form_data:
                                    parsed_form = frappe.parse_json(custom_form_data) if isinstance(custom_form_data, str) else custom_form_data
                                    if parsed_form and isinstance(parsed_form, dict) and "components" in parsed_form:
                                        parsed_form["components"] = [c for c in parsed_form["components"] if c.get("type") != "button"]
                                    form_json = parsed_form
                            except Exception:
                                pass

                    if not final_user:
                        stage_user = stage.get("user")
                        if stage_user:
                            final_user = frappe.get_value("User", stage_user, "full_name")
                            final_user_id = stage_user

                    stage_entry = {
                        "stage_name": stage.get("approval_name"),
                        "user_id": final_user_id,
                        "user": final_user,
                        "role": stage_role,
                        "status": stage_status,
                        "approval_time": approval_time
                    }
                    if approval_response_data is not None:
                        stage_entry["approval_response_data"] = approval_response_data
                    if form_json is not None:
                        stage_entry["form_json"] = form_json
                    mapped_stages_status.append(stage_entry)
        except Exception as e:
            frappe.log_error(f"Error fetching linked Approval Tracker for todo ref {todo.reference_type} {todo.reference_name}: {str(e)}")

        attachments = frappe.get_all("File", filters={
            "attached_to_doctype": todo.reference_type,
            "attached_to_name": todo.reference_name
        }
        , fields=["file_url"])

        allocated_to_names = []
        allocated_roles = []
        if todo.allocated_to:
            aname = frappe.db.get_value("User", todo.allocated_to, "full_name")
            allocated_to_names.append(aname or todo.allocated_to)
        if todo.role:
            allocated_roles.append(todo.role)
        try:
            alloc_users = frappe.get_all(
                "Nextai User Select",
                filters={"parent": todo.name, "parentfield": "custom_allocated_to_users"},
                fields=["user"]
            )
            for u in alloc_users:
                if u.user and u.user != todo.allocated_to:
                    uname = frappe.db.get_value("User", u.user, "full_name")
                    allocated_to_names.append(uname or u.user)
        except Exception:
            pass
        try:
            assigned_roles = frappe.get_all(
                "Nextai Role Select",
                filters={"parent": todo.name, "parentfield": "custom_assigned_to_roles"},
                fields=["role"]
            )
            for r in assigned_roles:
                if r.role:
                    allocated_roles.append(r.role)
        except Exception:
            pass
        allocated_roles = list(dict.fromkeys(allocated_roles))

        # For Leave Application, add reason name to reference document
        reference_doc_dict = reference_doc.as_dict()
        if todo.reference_type == "Leave Application":
            custom_reason_id = reference_doc_dict.get("custom_reason")
            if custom_reason_id:
                try:
                    reason_name = frappe.db.get_value("Reason", custom_reason_id, "reason")
                    if reason_name:
                        reference_doc_dict["reason_name"] = reason_name
                except Exception:
                    pass

        todo_data = {
            "todo_id": todo.name,
            "allocated_to": allocated_to_names,
            "allocated_roles": allocated_roles,
            "allocated_to_emp_id": allocated_to_emp_id,
            "role": todo.role,
            "username": allocated_to_full_name,
            "reference_type": todo.reference_type,
            "reference_name": todo.reference_name,
            "custom_doctype_actions": todo.custom_doctype_actions ,
            "custom_allow_revoke": todo.custom_allow_revoke,
            "status": status_value,
            "due_date": frappe.utils.formatdate(todo.date) if todo.date else None,
            "description": todo.description,
            "custom_doctype_actions_with_form": todo.custom_doctype_actions_with_form,
            "is_allocated_todo": is_allocated_todo,
            "custom_approval_type": todo.custom_approval_type,
            "send_back_user": send_back_user,
            "can_edit": can_edit,
            "todo_status": todo.status,
            "reference_document": reference_doc_dict,
            "approval_stages_status": mapped_stages_status,
            "attachments":attachments,
            "custom_selected_doctype_action": todo.custom_selected_doctype_action
        }
        result.append(todo_data)

    return {
        "data": result,
        "total_count": total_filtered_count,
        "start": start,
        "page_length": page_length
    }



def evaluate_filter_condition(field_value, filter_condition):

    if not filter_condition:
        return True

    def parse_date_value(val):
        try:
            from frappe.utils import getdate
            return getdate(val)
        except:
            return val

    if isinstance(filter_condition, list) and len(filter_condition) == 2:
        operator, value = filter_condition

        if operator in [">", ">=", "<", "<=", "between"]:
            try:
                field_value = parse_date_value(field_value)
                if operator == "between" and isinstance(value, (list, tuple)) and len(value) == 2:
                    value = [parse_date_value(v) for v in value]
                else:
                    value = parse_date_value(value)
            except:
                pass 

        if operator == "=":
            return field_value == value
        elif operator == "!=":
            return field_value != value
        elif operator == "in":
            return field_value in value if isinstance(value, (list, tuple)) else field_value == value
        elif operator == "not in":
            return field_value not in value if isinstance(value, (list, tuple)) else field_value != value
        elif operator == "like":
            return value.lower() in str(field_value).lower() if field_value else False
        elif operator == "not like":
            return value.lower() not in str(field_value).lower() if field_value else True
        elif operator == ">":
            return field_value > value if field_value else False
        elif operator == ">=":
            return field_value >= value if field_value else False
        elif operator == "<":
            return field_value < value if field_value else False
        elif operator == "<=":
            return field_value <= value if field_value else False
        elif operator == "between":
            if isinstance(value, (list, tuple)) and len(value) == 2:
                start_val, end_val = value
                return start_val <= field_value <= end_val if field_value else False
            return False
        elif operator == "is":
            return field_value is None if value == "null" else field_value == value
        elif operator == "is not":
            return field_value is not None if value == "null" else field_value != value
    else:
        return field_value == filter_condition

    return True
