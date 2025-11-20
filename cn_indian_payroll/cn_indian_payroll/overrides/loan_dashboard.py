import frappe



@frappe.whitelist()
def print_loan_dashboard_erp(employee,id,loan_product):
    if not employee:
        return []


    loan_product = frappe.get_doc("Loan Product", loan_product)

    loan_docs = frappe.get_doc("Loan",id)

    repayment_schedule = []
    paid_months=[]
    unpaid_months=[]
    results=[]
    loan_tenure=0
    monthly_repayment=0
    total_loan_amount=0
    if loan_docs:
        repayment_entries = frappe.get_list(
            "Loan Repayment Schedule",
            filters={"loan": loan_docs.name},
            fields=["*"]
        )

        if repayment_entries:

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
        else:
            repayment_schedule = []

        paid_months_count=len(paid_months)
        unpaid_months_count=len(unpaid_months)
        total_paid=sum(paid_months)
        total_unpaid=sum(unpaid_months)



    results.append({

        "loan_type": loan_docs.loan_product,
        "emi_type": loan_docs.repayment_method,
        "loan_requested_amount": loan_docs.loan_amount,
        "loan_approved_amount": loan_docs.loan_amount if loan_docs else None,
        "rate_of_interest": loan_docs.rate_of_interest if loan_docs else None,
        "standard_interest": loan_product.rate_of_interest if loan_product else None,
        "loan_start_date": loan_docs.repayment_start_date if loan_docs else None,
        "loan_tenure": loan_tenure,
        "status": loan_docs.status,
        "monthly_repayment_amount": monthly_repayment,
        "total_months": loan_tenure,
        "paid_months": paid_months_count,
        "remaining_months": unpaid_months_count,
        "total_loan_amount": total_loan_amount,
        "total_paid_amount": total_paid,
        "remaining_amount": total_unpaid,
        "repayment_schedule": repayment_schedule,
        "total_payment":round(loan_docs.total_payment,2),
        "total_interest_payable":round(loan_docs.total_interest_payable,2),
        "total_principal_paid":round(loan_docs.total_principal_paid,2),
    })

    return results
