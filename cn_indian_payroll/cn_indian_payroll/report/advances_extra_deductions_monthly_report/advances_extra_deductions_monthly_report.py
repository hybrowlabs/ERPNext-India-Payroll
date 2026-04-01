import frappe

def execute(filters=None):

    columns = [
        {"label": "EMP ID", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 120},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
        {"label": "Deduction Name", "fieldname": "deduction_name", "fieldtype": "Data", "width": 180},
        {"label": "Deduction Category", "fieldname": "deduction_category", "fieldtype": "Data", "width": 160},
        {"label": "Start Date", "fieldname": "start_date", "fieldtype": "Date", "width": 120},
        {"label": "End Date", "fieldname": "end_date", "fieldtype": "Date", "width": 120},
        {"label": "Currency ISO Code", "fieldname": "currency", "fieldtype": "Data", "width": 120},
        {"label": "Amount / Percent / Hours / Days", "fieldname": "amount_type", "fieldtype": "Data", "width": 200},
        {"label": "Deduction Amount", "fieldname": "deduction_amount", "fieldtype": "Currency", "width": 150},
        {"label": "No of Installment", "fieldname": "no_of_installment", "fieldtype": "Int", "width": 140},
        {"label": "Period Deduction Amount", "fieldname": "period_deduction_amount", "fieldtype": "Currency", "width": 180},
        {"label": "Installments Recovered", "fieldname": "installments_recovered", "fieldtype": "Int", "width": 160},
        {"label": "Amount Recovered", "fieldname": "amount_recovered", "fieldtype": "Currency", "width": 160},
        {"label": "Installments Pending", "fieldname": "installments_pending", "fieldtype": "Int", "width": 160},
        {"label": "Amount Pending", "fieldname": "amount_pending", "fieldtype": "Currency", "width": 160},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
    ]

    data = frappe.db.sql("""
        SELECT
            ea.employee,
            emp.employee_name,
            ea.name as deduction_name,
            ea.custom_type as deduction_category,
            ea.posting_date as start_date,
            ea.custom_repayment_start_date as end_date,
            ea.currency,
            'Amount' as amount_type,
            ea.advance_amount as deduction_amount,
            ea.custom_repayment_period_in_months as no_of_installment,
            ea.custom_monthly_repayment_amount as period_deduction_amount,
            ea.custom_total_paid_amount as installments_recovered,
            ea.paid_amount as amount_recovered,
            (ea.custom_total_balance_amount - ea.custom_total_paid_amount) as installments_pending,
            (ea.custom_total_balance_amount - ea.custom_total_paid_amount) as amount_pending,
            ea.status

        FROM `tabEmployee Advance` ea

        LEFT JOIN `tabEmployee` emp
        ON emp.name = ea.employee
    """, as_dict=True)

    return columns, data