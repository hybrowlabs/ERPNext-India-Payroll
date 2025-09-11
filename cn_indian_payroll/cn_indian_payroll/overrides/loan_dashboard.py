import frappe

@frappe.whitelist()
def print_loan_dashboard(employee):
    if not employee:
        return []

    loan_details = frappe.get_all(
        "Loan Application",
        filters={
            "applicant_type": "Employee",
            "applicant": employee,
            "docstatus": ["in", [0, 1]]
        },
        fields=["*"]
    )

    results = []
    loan_tenure=None
    total_loan_amount=None

    for loan in loan_details:
        # Fetch Loan Product details
        loan_product = None
        if loan.loan_product:
            loan_product = frappe.get_doc("Loan Product", loan.loan_product)

        # Fetch linked Loan (if exists)
        loan_docs = frappe.get_list(
            "Loan",
            filters={"loan_application": loan.name},
            fields=["*"]
        )
        loan_doc = loan_docs[0] if loan_docs else None

        # Repayment schedule
        repayment_schedule = []
        if loan_doc:
            repayment_entries = frappe.get_list(
                "Loan Repayment Schedule",
                filters={"loan": loan_doc.name},
                fields=["*"]
            )

            loan_repayment=repayment_entries[0].name

            get_doc=frappe.get_doc("Loan Repayment Schedule",loan_repayment)
            loan_tenure=get_doc.repayment_periods



            total_loan_amount=get_doc.loan_amount
            for entry in get_doc.repayment_schedule:
                repayment_schedule.append({
                    "payment_date": entry.payment_date,
                    "principal_amount": entry.principal_amount,
                    "interest_amount": entry.interest_amount,
                    "total_payment": entry.total_payment,
                    "balance_loan_amount": entry.balance_loan_amount
                })

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
            "monthly_repayment_amount": loan.repayment_amount,
            "total_months": loan_tenure,
            "paid_months": None,
            "remaining_months": None,
            "total_loan_amount": total_loan_amount,
            "total_paid_amount": None,
            "remaining_amount": None,
            "repayment_schedule": repayment_schedule
        })

    return results,repayment_schedule
