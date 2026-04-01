# Copyright (c) 2026, Hybrowlabs technologies
# For license information, please see license.txt

import frappe

def execute(filters=None):

    columns = get_columns()
    data = get_data(filters)

    return columns, data


def get_columns():

    columns = [

        {"label":"EMP ID","fieldname":"employee","fieldtype":"Link","options":"Employee","width":120},
        {"label":"Employee Name","fieldname":"employee_name","fieldtype":"Data","width":180},

        {"label":"Loan Name","fieldname":"loan_name","fieldtype":"Data","width":180},

        {"label":"Installment Amount","fieldname":"installment_amount","fieldtype":"Currency","width":160},

        {"label":"Interest (1)","fieldname":"interest_amount","fieldtype":"Currency","width":140},

        {"label":"Loan EMI","fieldname":"emi_amount","fieldtype":"Currency","width":140},

        {"label":"Standard Interest (2)","fieldname":"standard_interest","fieldtype":"Percent","width":160},

        {"label":"Principal Balance","fieldname":"balance_loan_amount","fieldtype":"Currency","width":170},

        {"label":"Override","fieldname":"override","fieldtype":"Data","width":120},

        {"label":"Loan Installment Override","fieldname":"loan_installment_override","fieldtype":"Currency","width":200},

        {"label":"Reason For Loan Override","fieldname":"override_reason","fieldtype":"Data","width":220},

        {"label":"Loan Type","fieldname":"loan_type","fieldtype":"Data","width":160},

        {"label":"Emi Type","fieldname":"emi_type","fieldtype":"Data","width":120},

        {"label":"Loan Id","fieldname":"loan","fieldtype":"Link","options":"Loan","width":150},

        {"label":"Loan Period","fieldname":"loan_period","fieldtype":"Int","width":120},

        {"label":"Loan Category","fieldname":"loan_category","fieldtype":"Data","width":160},

        {"label":"Loan Recovery Frequency","fieldname":"repayment_frequency","fieldtype":"Data","width":200},
    ]

    return columns


def get_data(filters):

    conditions = ""
    values = {}

    if filters.get("employee"):
        conditions += " AND loan.applicant = %(employee)s"
        values["employee"] = filters.get("employee")

    if filters.get("loan"):
        conditions += " AND loan.name = %(loan)s"
        values["loan"] = filters.get("loan")

    data = frappe.db.sql(f"""

        SELECT

            loan.applicant as employee,
            emp.employee_name,

            la.loan_product as loan_name,

            loan.monthly_repayment_amount as installment_amount,
            la.total_payable_interest,

            rs.adjusted_interest as emi_amount,

            loan.rate_of_interest as standard_interest,

            loan.total_principal_paid,
            la.description as override_reason,
            '' as override,
            '' as loan_installment_override,
            

            la.loan_product as loan_type,

            loan.repayment_method as emi_type,

            loan.name as loan,

            loan.repayment_periods as loan_period,

            la.loan_product as loan_category,

            loan.repayment_schedule_type as repayment_frequency

        FROM `tabLoan` loan

        LEFT JOIN `tabLoan Repayment Schedule` rs
            ON rs.loan = loan.name

        LEFT JOIN `tabLoan Application` la
            ON la.name = loan.loan_application

        LEFT JOIN `tabEmployee` emp
            ON emp.name = loan.applicant

        WHERE loan.docstatus = 1
        {conditions}

        ORDER BY loan.name, rs.posting_date

    """, values, as_dict=True)

    return data