import frappe

# from cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.benefit_claim import _get_todo_info_for_doc
from frappe import _
from cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.benefit_claim import get_open_approval_todos





@frappe.whitelist()
def print_loan_dashboard(employee,todo_status=None,search_term=None,start=0,page_length=10,order_by=None,status=None,filters=None,include_allocated_todos=False,date=None):
    target_employee = frappe.request.headers.get("X-Target-Employee-Id")
    if target_employee:
        employee = target_employee
    if not employee:
        return []

    start = int(start)
    page_length = int(page_length)

    loan_details = frappe.get_all(
        "Loan Application",
        filters={
            "applicant_type": "Employee",
            "applicant": employee,
            "docstatus": ["in", [0, 1]]
        },
        fields=["*"],
        order_by=order_by
    )

    if search_term:
        search = search_term.lower()

        loan_details = [
            loan for loan in loan_details
            if any([
                search in (loan.get("name") or "").lower(),
                search in (loan.get("applicant_name") or "").lower(),
                search in (loan.get("loan_product") or "").lower(),
                search in (loan.get("status") or "").lower(),
            ])
        ]

    total_count = len(loan_details)

    loan_details = loan_details[start:start + page_length]


    todo_response = get_open_approval_todos(
        doctype="Loan Application",
        start=0,
        page_length=20,
        todo_status=todo_status,
        search_term=search_term,
        filters=filters,
        date=date,
        status=status,
        include_allocated_todos=include_allocated_todos
    
    )

    todo_map = {}

    if todo_response and todo_response.get("data"):
        for todo in todo_response.get("data"):
            ref_name = todo.get("reference_name")
            if ref_name:
                todo_map.setdefault(ref_name, []).append(todo)

    results = []

    monthly_repayment=0
    loan_tenure=0
    total_loan_amount=0

    total_payment=0
    total_interest_payable=0
    total_principal_paid=0


    for loan in loan_details:

        loan_product = None
        if loan.loan_product:
            loan_product = frappe.get_doc("Loan Product", loan.loan_product)


        loan_docs = frappe.get_list(
            "Loan",
            filters={"loan_application": loan.name},
            fields=["*"]
        )
        loan_doc = loan_docs[0] if loan_docs else None


        repayment_schedule = []
        paid_months=[]
        unpaid_months=[]

        if loan_doc:

            total_payment = round(loan_doc.total_payment, 2)
            total_interest_payable = round(loan_doc.total_interest_payable, 2)
            total_principal_paid = round(loan_doc.total_principal_paid, 2)

            repayment_entries = frappe.get_list(
                "Loan Repayment Schedule",
                filters={"loan": loan_doc.name},
                fields=["*"]
            )


            if repayment_entries:
                loan_repayment = repayment_entries[0].name
                get_doc = frappe.get_doc("Loan Repayment Schedule", loan_repayment)

                if get_doc.docstatus == 1 and get_doc.status in ["Initiated", "Active"]:
                    loan_tenure = get_doc.repayment_periods
                    monthly_repayment = get_doc.monthly_repayment_amount
                    total_loan_amount = get_doc.loan_amount

                    for entry in get_doc.repayment_schedule:
                        repayment_schedule.append({
                            "payment_date": entry.payment_date,
                            "principal_amount": entry.principal_amount,
                            "interest_amount": entry.interest_amount,
                            "total_payment": entry.total_payment,
                            "balance_loan_amount": entry.balance_loan_amount
                        })

                        if entry.custom_deducted:
                            paid_months.append(entry.total_payment)
                        else:
                            unpaid_months.append(entry.total_payment)

        paid_months_count = len(paid_months)
        unpaid_months_count = len(unpaid_months)
        total_paid = sum(paid_months)
        total_unpaid = sum(unpaid_months)

        loan_todos = todo_map.get(loan.name, [])


        results.append({
            "loan_name": loan.name,
            "employee":loan.applicant,
            "employee_name":loan.applicant_name,
            "loan_type": loan.loan_product,
            "emi_type": loan.repayment_method,
            "loan_requested_amount": loan.loan_amount,

            "loan_approved_amount": loan.loan_amount or 0,
            "rate_of_interest": loan.rate_of_interest or 0,
            "standard_interest": loan_product.rate_of_interest or 0,
            "loan_start_date": loan.custom_repayment_start_date or None,
            "loan_end_date": None,

            "loan_tenure": loan_tenure,
            "status": loan.status,
            "monthly_repayment_amount": monthly_repayment,
            "total_months": loan_tenure,
            "paid_months": paid_months_count,
            "remaining_months": unpaid_months_count,
            "total_loan_amount": total_loan_amount,
            "total_paid_amount": total_paid,
            "remaining_amount": total_unpaid,
            "repayment_schedule": repayment_schedule,

            "total_payment":total_payment,
            "total_interest_payable":total_interest_payable,
            "total_principal_paid":total_principal_paid,
            "can_edit":loan.can_edit,
            "name":loan.name,
            "todo_list": loan_todos


        })

    return {
        "status": "success",
        "total_count": total_count,
        "start": start,
        "page_length": page_length,
        "data": results
    }

@frappe.whitelist()
def print_loan_dashboard_erp(employee,id):
    if not employee:
        return []

    loan_details = frappe.get_all(
        "Loan Application",
        filters={
            "applicant_type": "Employee",
            "applicant": employee,
            "docstatus": ["in", [0, 1]],
            "name": id
        },
        fields=["*"]
    )

    results = []



    monthly_repayment=0
    loan_tenure=0
    total_loan_amount=0

    total_payment=0
    total_interest_payable=0
    total_principal_paid=0

    for loan in loan_details:

        loan_product = None
        if loan.loan_product:
            loan_product = frappe.get_doc("Loan Product", loan.loan_product)


        loan_docs = frappe.get_list(
            "Loan",
            filters={"loan_application": loan.name},
            fields=["*"]
        )
        loan_doc = loan_docs[0] if loan_docs else None

        if loan_doc:
            total_payment = round(loan_doc.total_payment, 2)
            total_interest_payable = round(loan_doc.total_interest_payable, 2)
            total_principal_paid = round(loan_doc.total_principal_paid, 2)



        repayment_schedule = []
        paid_months=[]
        unpaid_months=[]
        if loan_doc:
            repayment_entries = frappe.get_list(
                "Loan Repayment Schedule",
                filters={"loan": loan_doc.name},
                fields=["*"]
            )

            loan_repayment=repayment_entries[0].name

            get_doc=frappe.get_doc("Loan Repayment Schedule",loan_repayment)
            loan_tenure=get_doc.repayment_periods
            monthly_repayment=get_doc.monthly_repayment_amount

            if get_doc.docstatus == 1 and get_doc.status in ["Initiated", "Active"]:
                total_loan_amount=get_doc.loan_amount
                for entry in get_doc.repayment_schedule:
                    repayment_schedule.append({
                        "payment_date": entry.payment_date,
                        "principal_amount": entry.principal_amount,
                        "interest_amount": entry.interest_amount,
                        "total_payment": entry.total_payment,
                        "balance_loan_amount": entry.balance_loan_amount,
                        "deducted":entry.custom_deducted,
                    })
                    if entry.custom_deducted:
                        paid_months.append(
                            entry.total_payment
                        )
                    if not entry.custom_deducted:
                        unpaid_months.append(entry.total_payment)



            else:
                repayment_schedule = []


        paid_months_count=len(paid_months)
        unpaid_months_count=len(unpaid_months)
        total_paid=sum(paid_months)
        total_unpaid=sum(unpaid_months)



        results.append({
            "loan_name": loan.name,
            "loan_type": loan.loan_product,
            "emi_type": loan.repayment_method,
            "loan_requested_amount": loan.loan_amount,
            "loan_approved_amount": loan_doc.loan_amount if loan_doc else None,
            "rate_of_interest": loan_doc.rate_of_interest if loan_doc else None,
            "standard_interest": loan_product.rate_of_interest if loan_product else None,
            "loan_start_date": loan_doc.repayment_start_date if loan_doc else None,
            "loan_tenure": loan_tenure,
            "status": loan.status,
            "monthly_repayment_amount": monthly_repayment,
            "total_months": loan_tenure,
            "paid_months": paid_months_count,
            "remaining_months": unpaid_months_count,
            "total_loan_amount": total_loan_amount,
            "total_paid_amount": total_paid,
            "remaining_amount": total_unpaid,
            "repayment_schedule": repayment_schedule,

            "total_payment":total_payment,
            "total_interest_payable":total_interest_payable,
            "total_principal_paid":total_principal_paid,
        })

    return results
