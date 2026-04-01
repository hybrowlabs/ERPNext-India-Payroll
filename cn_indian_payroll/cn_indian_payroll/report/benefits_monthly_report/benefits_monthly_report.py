import frappe

def execute(filters=None):

    columns = [
        {"label": "EMP ID", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 120},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
        {"label": "Component Name", "fieldname": "salary_component", "fieldtype": "Data", "width": 180},
        {"label": "Payout Month", "fieldname": "benefit_accrual_date", "fieldtype": "Date", "width": 130},
        {"label": "Working Days", "fieldname": "working_days", "fieldtype": "Float", "width": 120},
        {"label": "LOP Days", "fieldname": "lop_days", "fieldtype": "Float", "width": 120},
        {"label": "Opening Balance", "fieldname": "opening_balance", "fieldtype": "Currency", "width": 150},
        {"label": "Monthly Original Accrual", "fieldname": "monthly_original_accrual", "fieldtype": "Currency", "width": 200},
        {"label": "Monthly Actual Accrual", "fieldname": "monthly_actual_accrual", "fieldtype": "Currency", "width": 200},
        {"label": "Claimed Amount", "fieldname": "claimed_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Advance Amount", "fieldname": "advance_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Total Amount", "fieldname": "total_amount", "fieldtype": "Currency", "width": 150},
    ]

    conditions = ""

    if filters.get("employee"):
        conditions += " AND eba.employee = %(employee)s"

    if filters.get("salary_component"):
        conditions += " AND eba.salary_component = %(salary_component)s"

    if filters.get("payout_month"):
        conditions += """
            AND MONTH(eba.benefit_accrual_date) = MONTH(%(payout_month)s)
            AND YEAR(eba.benefit_accrual_date) = YEAR(%(payout_month)s)
        """

    data = frappe.db.sql(f"""
        SELECT
            eba.employee,
            emp.employee_name,
            eba.salary_component,
            eba.benefit_accrual_date,
            eba.working_days,
            eba.lwp_days as lop_days,
            eba.amount as opening_balance,
            IFNULL(bc.custom_max_amount) as custom_max_amount,
            IFNULL(bc.custom_max_amount) as custom_max_amount,
            IFNULL(bc.claimed_amount) as claimed_amount,
            eba.amount,
            IFNULL(bc.claimed_amount) as claimed_amount,
            IFNULL(bc.claimed_amount) as advance_amount,
            (eba.amount 
                - IFNULL(bc.claimed_amount,0) 
                - IFNULL(bc.claimed_amount,0)
            ) as total_amount

        FROM `tabEmployee Benefit Accrual` eba
        LEFT JOIN `tabEmployee` emp
        ON emp.name = eba.employee

        LEFT JOIN `tabEmployee Benefit Claim` bc
        ON bc.employee = eba.employee
        AND bc.earning_component = eba.salary_component

        WHERE 1=1 {conditions}

    """, filters, as_dict=True)

    return columns, data