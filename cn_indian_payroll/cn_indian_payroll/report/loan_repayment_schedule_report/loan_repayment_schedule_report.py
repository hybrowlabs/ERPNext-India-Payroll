import frappe
from frappe.utils import flt, getdate, add_months

def execute(filters=None):
    columns = get_columns()
    data = get_all_accrued_bonus(filters)
    return columns, data

def get_all_accrued_bonus(filters=None):
    if filters is None:
        filters = {}

    conditions = {"docstatus": 1}
    if filters.get("employee"):
        conditions["custom_employee"] = filters["employee"]
    if filters.get("company"):
        conditions["company"] = filters["company"]

    if filters.get("loan_from") and filters.get("loan_to"):
        conditions["posting_date"] = ["between", [filters["loan_from"], filters["loan_to"]]]
    elif filters.get("loan_from"):
        conditions["posting_date"] = [">=", filters["loan_from"]]
    elif filters.get("loan_to"):
        conditions["posting_date"] = ["<=", filters["loan_to"]]

    if filters.get("loan_product"):
        conditions["loan_product"] = filters["loan_product"]

    records = frappe.get_all("Loan Repayment Schedule", filters=conditions, fields=["*"])
    data = []


    for row in records:

        loan=frappe.get_doc("Loan",row.loan)


        data.append({
            "reference_id": row.name,
            "employee": row.custom_employee,
            "employee_name": row.custom_employee_name,
            "company": row.company,
            "loan_type": row.loan_product,
            "repayment_type": row.repayment_method,
            "repayment_start_date": row.repayment_start_date,
            "loan_amount": row.loan_amount,
            "monthly_repayment_amount": row.monthly_repayment_amount,
            "repayment_periods": row.repayment_periods,
            "rate_of_interest": row.rate_of_interest,
            "total_payable_amount":loan.total_payment,
            "total_interest_payable":loan.total_interest_payable,
            "total_principal_paid":loan.total_principal_paid,
            "total_amount_paid":loan.total_amount_paid,


        })

        # 2️⃣ Add repayment schedule rows
        repayment_schedule = get_repayment_schedule(row)
        for repayment in repayment_schedule:
            data.append({
                "reference_id": "",  # blank to avoid repeat
                "employee": "",
                "employee_name": "",
                "company": "",
                "loan_type": "",
                "repayment_type": "",
                "repayment_start_date": "",
                "advance_amount": "",
                "total_paid_amount": "",
                "total_balance_amount": "",
                "purpose": "",
                "note_remarks": "",
                # repayment details
                "idx": repayment.get("idx"),
                "payment_date": repayment.get("payment_date"),
                "principal": repayment.get("principal_amount"),
                "interest": repayment.get("interest_amount"),
                "payment_amount": repayment.get("total_payment"),
                "balance_amount": repayment.get("balance_loan_amount"),
                "deducted": repayment.get("custom_deducted"),
            })

    return data


def get_repayment_schedule(loan_doc):
    """Fetch repayment schedule from Loan Repayment Schedule Doc"""
    repayment_schedule = []

    doc = frappe.get_doc("Loan Repayment Schedule", loan_doc.name)

    prev_balance = flt(doc.loan_amount or 0)

    if doc.repayment_schedule:
        for idx, row in enumerate(doc.repayment_schedule, start=1):
            principal = flt(row.principal_amount, 2)
            interest = flt(row.interest_amount, 2)
            total_payment = flt(row.total_payment, 2) or round(principal + interest, 2)

            balance = flt(prev_balance - principal, 2)
            prev_balance = balance

            repayment_schedule.append({
                "idx": idx,
                "payment_date": row.payment_date,
                "principal_amount": principal,
                "interest_amount": interest,
                "total_payment": total_payment,
                "balance_loan_amount": balance,
                "custom_deducted": "✔" if row.custom_deducted == 1 else ""

            })

    return repayment_schedule


def get_columns():
    return [
        {"label": "Reference ID", "fieldname": "reference_id", "fieldtype": "Link", "options": "Loan Repayment Schedule", "width": 150},
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 150},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
        {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
        {"label": "Loan Type", "fieldname": "loan_type", "fieldtype": "Data", "width": 150},
        {"label": "Repayment Type", "fieldname": "repayment_type", "fieldtype": "Data", "width": 150},
        {"label": "Repayment Start Date", "fieldname": "repayment_start_date", "fieldtype": "Date", "width": 120},
        {"label": "Loan Amount", "fieldname": "loan_amount", "fieldtype": "Data", "width": 150},
        {"label": "Monthly Repayment", "fieldname": "monthly_repayment_amount", "fieldtype": "Data", "width": 150},
        {"label": "Repayment Periods", "fieldname": "repayment_periods", "fieldtype": "Int", "width": 120},
        {"label": "Rate of Interest", "fieldname": "rate_of_interest", "fieldtype": "Percentage", "width": 120},

        {"label": "Total Payable Amount", "fieldname": "total_payable_amount", "fieldtype": "Int", "width": 120},

        {"label": "Total Interest Payable", "fieldname": "total_interest_payable", "fieldtype": "Int", "width": 120},

        {"label": "Total Principal Paid", "fieldname": "total_principal_paid", "fieldtype": "Int", "width": 120},

        {"label": "Total Amount Paid", "fieldname": "total_amount_paid", "fieldtype": "Int", "width": 120},


        # Repayment Schedule Columns
        {"label": "Installment No", "fieldname": "idx", "fieldtype": "Int", "width": 100},
        {"label": "Payment Date", "fieldname": "payment_date", "fieldtype": "Date", "width": 120},
        {"label": "Principal Amount", "fieldname": "principal", "fieldtype": "Currency", "width": 120},
        {"label": "Interest Amount", "fieldname": "interest", "fieldtype": "Currency", "width": 120},
        {"label": "Payment Amount", "fieldname": "payment_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Balance After", "fieldname": "balance_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Deducted?", "fieldname": "deducted", "fieldtype": "Data", "width": 100},
    ]
