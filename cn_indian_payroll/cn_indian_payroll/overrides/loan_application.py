import frappe
import frappe
from frappe.utils import add_months, getdate,flt
# from frappe.utils import flt, getdate, add_months



def before_submit(self, method):
    if  not self.custom_note_remark:
        frappe.throw("Please add Note/Remarks before Submit")


def validate(self,method):
    if self.applicant_type=="Employee" and self.applicant:
        self.custom_employee=self.applicant



@frappe.whitelist()
def hold_installments(employee, payment_date, company, type, number_of_months, doc_id):
    if not (doc_id and company):
        return

    leave = frappe.get_all(
        "Loan",
        filters={
            "loan_application": doc_id,
            "company": company,
            "applicant": employee,
            "repay_from_salary": 1
        },
        fields=["*"]
    )

    if not leave:
        return

    loan_repayment = frappe.get_all(
        "Loan Repayment Schedule",
        # filters={"status": "Active", "loan": leave[0].name},
        filters={"loan": leave[0].name},
        fields=["*"]
    )

    if not loan_repayment:
        return

    repayment_doc = frappe.get_doc("Loan Repayment Schedule", loan_repayment[0].name)

    if not repayment_doc.repayment_schedule:
        return

    if type == "Extend Repayment Period" and number_of_months:
        try:
            number_of_months = int(number_of_months)
        except Exception:
            frappe.throw("Number of months must be a valid integer")

        skip_date = getdate(payment_date)
        skip_started = False

        for repayment in repayment_doc.repayment_schedule:
            current_date = getdate(repayment.payment_date)

            if current_date == skip_date:
                skip_started = True

            if skip_started:
                repayment.payment_date = add_months(current_date, number_of_months)
                repayment.db_update()

        repayment_doc.save(ignore_permissions=True)
        frappe.db.commit()

        return "success"

    if type == "Recover Pending in Next Month" and number_of_months:
        try:
            number_of_months = int(number_of_months)
        except Exception:
            frappe.throw("Number of months must be a valid integer")

        skip_date = getdate(payment_date)
        skipped_rows = []

        # collect rows to skip (current month + following months till number_of_months)
        for i in range(number_of_months):
            current_date = add_months(skip_date, i)
            for repayment in repayment_doc.repayment_schedule:
                if getdate(repayment.payment_date) == current_date:
                    skipped_rows.append(repayment)
                    break

        if not skipped_rows:
            frappe.throw(f"No repayment found for date {payment_date} and subsequent {number_of_months} months")

        # target date = skip_date + number_of_months
        target_date = add_months(skip_date, number_of_months)
        target_row = None
        for repayment in repayment_doc.repayment_schedule:
            if getdate(repayment.payment_date) == target_date:
                target_row = repayment
                break

        if not target_row:
            frappe.throw(f"No repayment found for target date {target_date}")

        # aggregate skipped rows amounts
        total_principal = sum(r.principal_amount or 0 for r in skipped_rows)
        total_interest = sum(r.interest_amount or 0 for r in skipped_rows)
        total_payment = sum(r.total_payment or 0 for r in skipped_rows)

        # add to target row
        target_row.principal_amount = (target_row.principal_amount or 0) + total_principal
        target_row.interest_amount = (target_row.interest_amount or 0) + total_interest
        target_row.total_payment = (target_row.total_payment or 0) + total_payment

        # remove skipped rows
        for r in skipped_rows:
            repayment_doc.remove(r)

        repayment_doc.save(ignore_permissions=True)
        frappe.db.commit()

        return "success"

    if type == "Distribute Across Future Months" and number_of_months:
        try:
            number_of_months = int(number_of_months)
        except Exception:
            frappe.throw("Number of months must be a valid integer")

        skip_date = getdate(payment_date)
        skipped_rows = []

        # Collect all rows to skip based on number_of_months
        for i in range(number_of_months):
            current_skip_date = add_months(skip_date, i)
            for repayment in repayment_doc.repayment_schedule:
                if getdate(repayment.payment_date) == current_skip_date:
                    skipped_rows.append(repayment)
                    break

        if not skipped_rows:
            frappe.throw(f"No repayment found for date {payment_date} and subsequent {number_of_months} month(s)")

        # Remove all skipped rows
        for r in skipped_rows:
            repayment_doc.remove(r)

        # Collect all future rows after the last skipped row
        last_skip_date = add_months(skip_date, number_of_months - 1)
        future_rows = [r for r in repayment_doc.repayment_schedule if getdate(r.payment_date) > last_skip_date]

        if not future_rows:
            frappe.throw("No future rows to distribute amounts")

        # Sum amounts of skipped rows
        total_principal = sum(flt(r.principal_amount) for r in skipped_rows)
        total_interest = sum(flt(r.interest_amount) for r in skipped_rows)
        total_payment = sum(flt(r.total_payment) for r in skipped_rows)

        # Distribute evenly across future rows
        n = len(future_rows)
        principal_share = total_principal / n
        interest_share = total_interest / n
        total_share = total_payment / n

        for r in future_rows:
            r.principal_amount = flt(r.principal_amount) + principal_share
            r.interest_amount = flt(r.interest_amount) + interest_share
            r.total_payment = flt(r.total_payment) + total_share

        # Recalculate balance_loan_amount sequentially
        prev_balance = flt(repayment_doc.loan_amount)
        for repayment in repayment_doc.repayment_schedule:
            repayment.balance_loan_amount = prev_balance - flt(repayment.principal_amount)
            prev_balance = repayment.balance_loan_amount

        repayment_doc.save(ignore_permissions=True)
        frappe.db.commit()
        return "success"



# @frappe.whitelist()
# def edit_installment(employee, payment_date, company, hold_option, number_of_months, repayment_amount,doc_id):

#     leave = frappe.get_all(
#         "Loan",
#         filters={
#             "loan_application": doc_id,
#             "company": company,
#             "applicant": employee,
#             "repay_from_salary": 1
#         },
#         fields=["*"]
#     )

#     if not leave:
#         return

#     loan_repayment = frappe.get_all(
#         "Loan Repayment Schedule",
#         # filters={"status": "Active", "loan": leave[0].name},
#         filters={"loan": leave[0].name},
#         fields=["*"]
#     )

#     if not loan_repayment:
#         return

#     repayment_doc = frappe.get_doc("Loan Repayment Schedule", loan_repayment[0].name)

#     if not repayment_doc.repayment_schedule:
#         return


#     if hold_option=="Recover Pending in Next Month" and number_of_months:

# @frappe.whitelist()
# def edit_installment(employee, payment_date, company, hold_option, number_of_months, repayment_amount, doc_id):
#     """
#     Edit loan installment for partial payment on multiple months and redistribute balance.
#     """

#     number_of_months = int(number_of_months)
#     repayment_amount = flt(repayment_amount)

#     # 1️⃣ Fetch the Loan
#     loans = frappe.get_all(
#         "Loan",
#         filters={
#             "loan_application": doc_id,
#             "company": company,
#             "applicant": employee,
#             "repay_from_salary": 1
#         },
#         fields=["*"]
#     )
#     if not loans:
#         frappe.throw("Loan not found")
#     loan = loans[0]

#     # 2️⃣ Fetch Loan Repayment Schedule
#     repayment_schedules = frappe.get_all(
#         "Loan Repayment Schedule",
#         filters={"loan": loan.name},
#         fields=["*"]
#     )
#     if not repayment_schedules:
#         frappe.throw("Repayment schedule not found")

#     repayment_doc = frappe.get_doc("Loan Repayment Schedule", repayment_schedules[0].name)
#     schedule = repayment_doc.repayment_schedule
#     if not schedule:
#         frappe.throw("No repayment rows found")

#     # 3️⃣ Find the start index for selected payment date
#     start_idx = None
#     for idx, row in enumerate(schedule):
#         if str(row.payment_date) == str(payment_date):
#             start_idx = idx
#             break
#     if start_idx is None:
#         frappe.throw("Payment date not found in schedule")

#     # 4️⃣ Apply partial payment for the selected months
#     remaining_total = 0
#     for i in range(number_of_months):
#         idx = start_idx + i
#         if idx >= len(schedule):
#             break

#         row = schedule[idx]
#         original_payment = flt(row.total_payment) or (flt(row.principal_amount) + flt(row.interest_amount))
#         # Apply the partial payment amount (repayment_amount)
#         partial_payment = min(repayment_amount, original_payment)
#         row.principal_amount = round(partial_payment - flt(row.interest_amount), 2)
#         row.total_payment = round(partial_payment, 2)
#         # Calculate remaining amount to distribute
#         remaining_total += original_payment - partial_payment

#     # 5️⃣ Distribute the remaining amount across future months
#     future_rows = schedule[start_idx + number_of_months :]
#     if remaining_total > 0 and future_rows:
#         per_row_extra = round(remaining_total / len(future_rows), 2)
#         for row in future_rows:
#             row.principal_amount = round(flt(row.principal_amount) + per_row_extra, 2)
#             row.total_payment = round(row.principal_amount + flt(row.interest_amount), 2)

#     # 6️⃣ Recalculate balance for all rows
#     prev_balance = flt(loan.loan_amount)
#     for row in schedule:
#         row.balance_loan_amount = round(prev_balance - flt(row.principal_amount), 2)
#         prev_balance = row.balance_loan_amount

#     repayment_doc.save()
#     frappe.msgprint("Installment updated and future schedule recalculated successfully.")



import frappe
from frappe.utils import flt, getdate

@frappe.whitelist()
def edit_installment(employee, payment_date, company, hold_option, number_of_months, repayment_amount, doc_id):
    """
    Edit loan installment for partial payment and redistribute balance to future months.
    """
    # 1️⃣ Fetch the Loan
    loans = frappe.get_all(
        "Loan",
        filters={
            "loan_application": doc_id,
            "company": company,
            "applicant": employee,
            "repay_from_salary": 1
        },
        fields=["*"]
    )

    if not loans:
        frappe.throw("Loan not found")
    loan = loans[0]

    # 2️⃣ Fetch Loan Repayment Schedule
    repayment_schedules = frappe.get_all(
        "Loan Repayment Schedule",
        filters={"loan": loan.name},
        fields=["*"]
    )
    if not repayment_schedules:
        frappe.throw("Repayment schedule not found")

    repayment_doc = frappe.get_doc("Loan Repayment Schedule", repayment_schedules[0].name)
    schedule = repayment_doc.repayment_schedule

    if not schedule:
        frappe.throw("No repayment rows found")

    # 3️⃣ Find the payment row
    payment_idx = None
    for idx, row in enumerate(schedule):
        if str(row.payment_date) == str(payment_date):
            payment_idx = idx
            break

    if payment_idx is None:
        frappe.throw("Payment date not found in schedule")

    # 4️⃣ Convert inputs to float/int safely
    repayment_amount = flt(repayment_amount)
    number_of_months = int(number_of_months)

    if hold_option == "Distribute Across Future Months" and number_of_months > 0:
        # Process selected months
        total_remaining = 0
        for i in range(number_of_months):
            idx_curr = payment_idx + i
            if idx_curr >= len(schedule):
                break

            row = schedule[idx_curr]
            total_payment = flt(row.total_payment) or (flt(row.principal_amount) + flt(row.interest_amount))

            # Apply partial payment
            partial_payment = min(repayment_amount, total_payment)
            principal = partial_payment - flt(row.interest_amount)
            if principal < 0:
                principal = 0

            row.principal_amount = round(principal, 2)
            row.total_payment = round(partial_payment, 2)

            # Remaining amount for redistribution
            total_remaining += total_payment - partial_payment

        # 5️⃣ Distribute remaining to future months
        future_idx_start = payment_idx + number_of_months
        if total_remaining > 0:
            remaining_months = len(schedule) - future_idx_start
            if remaining_months > 0:
                per_month_extra = round(total_remaining / remaining_months, 2)

                for i in range(future_idx_start, len(schedule)):
                    row = schedule[i]
                    row.principal_amount = round(flt(row.principal_amount) + per_month_extra, 2)
                    row.total_payment = round(row.principal_amount + flt(row.interest_amount), 2)

        # 6️⃣ Recalculate balances for all rows
        prev_balance = flt(loan.loan_amount)
        for row in schedule:
            row.balance_loan_amount = round(prev_balance - flt(row.principal_amount), 2)
            prev_balance = row.balance_loan_amount

        repayment_doc.save()
        frappe.msgprint("Installment updated and future schedule recalculated successfully.")

    elif hold_option == "Recover Pending in Next Month":
        # Implement logic if needed for this option
        frappe.msgprint("Recover Pending in Next Month option is not implemented yet.")
