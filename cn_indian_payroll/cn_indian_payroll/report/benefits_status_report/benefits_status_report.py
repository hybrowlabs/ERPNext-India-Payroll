import frappe

def execute(filters=None):

    columns = [
        {"label": "EMP ID", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 120},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
        {"label": "Designation", "fieldname": "designation", "fieldtype": "Data", "width": 160},
        {"label": "Department", "fieldname": "department", "fieldtype": "Data", "width": 160},
        {"label": "Flexi Component", "fieldname": "salary_component", "fieldtype": "Data", "width": 180},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
        {"label": "Expense Claim Date", "fieldname": "expense_claim_date", "fieldtype": "Date", "width": 140},
        {"label": "Currency", "fieldname": "currency", "fieldtype": "Data", "width": 100},
        {"label": "Bill Amount", "fieldname": "bill_amount", "fieldtype": "Currency", "width": 140},
        {"label": "Invoice Number", "fieldname": "invoice_number", "fieldtype": "Data", "width": 160},
        {"label": "User Comments", "fieldname": "user_comments", "fieldtype": "Data", "width": 200},
        {"label": "Attachment", "fieldname": "attachment", "fieldtype": "Attach", "width": 150},
        {"label": "Approved Amount", "fieldname": "approved_amount", "fieldtype": "Currency", "width": 160},
        {"label": "Approver Comments", "fieldname": "approver_comments", "fieldtype": "Data", "width": 200},
        {"label": "Taxable Amount", "fieldname": "taxable_amount", "fieldtype": "Currency", "width": 160},
        {"label": "Non Taxable Amount", "fieldname": "non_taxable_amount", "fieldtype": "Currency", "width": 170},
        {"label": "Payout Month", "fieldname": "benefit_accrual_date", "fieldtype": "Date", "width": 140},
        {"label": "Last Action Date", "fieldname": "modified", "fieldtype": "Datetime", "width": 170},
        {"label": "Approver Name", "fieldname": "approver", "fieldtype": "Data", "width": 180},
        {"label": "Approved On", "fieldname": "approval_date", "fieldtype": "Datetime", "width": 170},
    ]

    conditions = ""

    if filters.get("employee"):
        conditions += " AND bc.employee = %(employee)s"

    if filters.get("department"):
        conditions += " AND emp.department = %(department)s"

    if filters.get("salary_component"):
        conditions += " AND bc.salary_component = %(salary_component)s"

    if filters.get("payout_month"):
        conditions += """
        AND MONTH(eba.benefit_accrual_date) = MONTH(%(payout_month)s)
        AND YEAR(eba.benefit_accrual_date) = YEAR(%(payout_month)s)
        """

    data = frappe.db.sql(f"""
        SELECT
        bc.employee,
        emp.employee_name,
        emp.designation,
        emp.department,
        bc.earning_component as salary_component,
        bc.custom_status as status,

        bc.claim_date as expense_claim_date,
        bc.currency as currency,
        bc.custom_reimbursement_amount_as_per_ctc as bill_amount,

        eba.salary_slip as invoice_number,

        bc.custom_note_by_employee as user_comments,
        bc.attachments as attachment,

        bc.custom_reimbursement_amount_as_per_ctc as approved_amount,
        bc.custom_note_by_employee as approver_comments,

        bc.claimed_amount as taxable_amount,
        bc.custom_reimbursement_amount_as_per_ctc as non_taxable_amount,

        eba.benefit_accrual_date as benefit_accrual_date,

        bc.claim_date as last_action_date

    FROM `tabEmployee Benefit Claim` bc

    LEFT JOIN `tabEmployee` emp
    ON emp.name = bc.employee

    LEFT JOIN `tabEmployee Benefit Accrual` eba
    ON eba.employee = bc.employee
    AND eba.salary_component = bc.earning_component

        WHERE 1=1 {conditions}

    """, filters, as_dict=True)

    return columns, data