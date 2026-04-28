import frappe

def execute(filters=None):

    columns = [
        {"label":"EMP ID","fieldname":"employee","fieldtype":"Link","options":"Employee","width":120},
        {"label":"Employee Name","fieldname":"employee_name","fieldtype":"Data","width":180},
        {"label":"Loan Id","fieldname":"loan","fieldtype":"Link","options":"Loan","width":140},
        {"label":"Loan Type","fieldname":"loan_type","fieldtype":"Data","width":140},
        {"label":"Loan Name","fieldname":"loan_name","fieldtype":"Data","width":160},
        {"label":"Loan Period","fieldname":"loan_period","fieldtype":"Int","width":120},
        {"label":"Loan Category","fieldname":"loan_category","fieldtype":"Data","width":150},
        {"label":"Loan Recovery Frequency","fieldname":"repayment_frequency","fieldtype":"Data","width":180},
        {"label":"Loan Taken Date","fieldname":"posting_date","fieldtype":"Date","width":130},
        {"label":"Loan Start Date","fieldname":"repayment_start_date","fieldtype":"Date","width":130},
        {"label":"Loan End Date","fieldname":"repayment_end_date","fieldtype":"Date","width":130},
        {"label":"Interest Start Date","fieldname":"interest_start_date","fieldtype":"Date","width":140},
        {"label":"Requested Repayment Tenure (Months)","fieldname":"requested_repayment","fieldtype":"Int","width":210},
        {"label":"Eligible Repayment Tenure (Months)","fieldname":"eligible_repayment","fieldtype":"Int","width":210},
        {"label":"Interest Rate","fieldname":"interest_rate","fieldtype":"Percent","width":120},
        {"label":"Standard Interest Rate","fieldname":"standard_interest_rate","fieldtype":"Percent","width":160},
        {"label":"EMI Type","fieldname":"emi_type","fieldtype":"Data","width":120},
        {"label":"Currency ISO Code","fieldname":"currency","fieldtype":"Data","width":120},
        {"label":"Requested Loan Amount","fieldname":"requested_amount","fieldtype":"Currency","width":170},
        {"label":"Eligible Loan Amount","fieldname":"loan_amount","fieldtype":"Currency","width":160},
        {"label":"Total Principal","fieldname":"total_principal","fieldtype":"Currency","width":150},
        {"label":"Total Interest","fieldname":"total_interest","fieldtype":"Currency","width":150},
        {"label":"Total Principal With Interest","fieldname":"total_payment","fieldtype":"Currency","width":200},
        {"label":"Recovered Installments","fieldname":"paid_installments","fieldtype":"Int","width":170},
        {"label":"Recovered Principal","fieldname":"recovered_principal","fieldtype":"Currency","width":170},
        {"label":"Recovered Interest","fieldname":"recovered_interest","fieldtype":"Currency","width":170},
        {"label":"Pending Principal With Interest","fieldname":"pending_total","fieldtype":"Currency","width":220},
        {"label":"Pending Months","fieldname":"pending_months","fieldtype":"Int","width":140},
        {"label":"Pending Principal","fieldname":"pending_principal","fieldtype":"Currency","width":170},
        {"label":"Pending Interest","fieldname":"pending_interest","fieldtype":"Currency","width":170},
        {"label":"Paid Principal With Interest","fieldname":"paid_total","fieldtype":"Currency","width":200},
        {"label":"Loan Status","fieldname":"status","fieldtype":"Data","width":120},
        {"label":"Completed Date","fieldname":"closure_date","fieldtype":"Date","width":140},
    ]

    conditions = []
    values = {}

    if filters.get("employee"):
      conditions.append("loan.applicant = %(employee)s")
      values["employee"] = filters.get("employee")
    if filters.get("loan_product"):
      conditions.append("la.loan_product = %(loan_product)s")
      values["loan_product"] = filters.get("loan_product")
    condition_str = ""
    if conditions:
        condition_str = " AND " + " AND ".join(conditions)


    data = frappe.db.sql(f"""
        SELECT
        loan.applicant as employee,
        emp.employee_name,

        loan.name as loan,
        la.loan_product as loan_type,
        la.loan_product as loan_name,

        loan.repayment_periods as loan_period,
        la.loan_product as loan_category,
        loan.repayment_schedule_type as repayment_frequency,

        loan.posting_date,
        loan.repayment_start_date,

        DATE_ADD(
            loan.repayment_start_date,
            INTERVAL loan.repayment_periods MONTH
        ) as repayment_end_date,

        loan.repayment_start_date as interest_start_date,

        loan.tenure_post_restructure as requested_repayment,
        la.repayment_periods as eligible_repayment,

        loan.rate_of_interest as interest_rate,
        loan.rate_of_interest as standard_interest_rate,

        loan.repayment_method as emi_type,
        'INR' as currency,

        la.loan_amount as requested_amount,
        loan.loan_amount,

        loan.total_principal_paid as total_principal,
        loan.total_interest_payable as total_interest,
        loan.total_payment as total_payment,

        ROUND(
            la.total_payable_amount / la.repayment_amount
                         ) 
                         as repayment_installments,
        loan.total_principal_paid as recovered_principal,
        loan.total_interest_payable as recovered_interest,
                         
        (loan.total_payment - la.total_payable_amount) as pending_total,
        ROUND(
            la.total_payable_amount / la.repayment_amount
                         ) 
                         as pending_months,
        (loan.total_payment - loan.total_principal_paid) as pending_principal,
                         
        loan.total_interest_payable as pending_interest,

        loan.total_amount_paid as paid_total,

        loan.status,
        loan.closure_date

    FROM `tabLoan` loan

    LEFT JOIN `tabLoan Application` la
        ON la.name = loan.loan_application

    LEFT JOIN `tabEmployee` emp
        ON emp.name = loan.applicant
    LEFT JOIN `tabLoan Product` lp
        ON lp.name = la.loan_product

    WHERE loan.docstatus = 1
    {condition_str}

    """, filters, as_dict=True)

    return columns, data