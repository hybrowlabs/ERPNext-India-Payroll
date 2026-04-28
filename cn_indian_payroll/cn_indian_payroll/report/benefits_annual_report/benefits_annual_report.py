import frappe

def execute(filters=None):

    columns = [
        {"label": "EMP ID", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 120},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
        {"label": "Location", "fieldname": "branch", "fieldtype": "Data", "width": 150},
        {"label": "Designation", "fieldname": "designation", "fieldtype": "Data", "width": 150},
        {"label": "Department", "fieldname": "department", "fieldtype": "Data", "width": 150},
        {"label": "Component Name", "fieldname": "salary_component", "fieldtype": "Data", "width": 180},
        {"label": "Payout Month", "fieldname": "benefit_accrual_date", "fieldtype": "Data", "width": 120},
        {"label": "Working Days", "fieldname": "working_days", "fieldtype": "Float", "width": 120},
        {"label": "Arrear Days", "fieldname": "arrear_days", "fieldtype": "Float", "width": 120},
        {"label": "LOP Days", "fieldname": "lop_days", "fieldtype": "Float", "width": 120},
        {"label": "Carry Forward Amount", "fieldname": "carry_forward_amount", "fieldtype": "Currency", "width": 160},
        {"label": "Opening Balance", "fieldname": "opening_balance", "fieldtype": "Currency", "width": 150},
        {"label": "Monthly Original Accrual", "fieldname": "monthly_original_accrual", "fieldtype": "Currency", "width": 200},
        {"label": "Monthly Actual Accrual", "fieldname": "monthly_actual_accrual", "fieldtype": "Currency", "width": 200},
        {"label": "Arrear Amount", "fieldname": "arrear_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Claimed Amount", "fieldname": "claimed_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Advance Amount", "fieldname": "advance_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Total Amount", "fieldname": "total_amount", "fieldtype": "Currency", "width": 150},
    ]

    conditions = ""

    if filters.get("employee"):
        conditions += " AND eb.employee = %(employee)s"

    if filters.get("department"):
        conditions += " AND emp.department = %(department)s"

    if filters.get("payout_month"):
       conditions += """
        AND MONTH(eb.benefit_accrual_date) = MONTH(%(payout_month)s)
        AND YEAR(eb.benefit_accrual_date) = YEAR(%(payout_month)s)
    """

    data = frappe.db.sql(f"""
        SELECT
            eb.employee,
            emp.employee_name,
            emp.branch,
            emp.designation,
            emp.department,
            eb.salary_component,
            eb.benefit_accrual_date,
            eb.working_days,
            eb.lop_reversal_days,
            eb.lwp_days,
      
            
          
      
         
            eb.amount

        FROM `tabEmployee Benefit Accrual` eb

        LEFT JOIN `tabEmployee` emp
        ON emp.name = eb.employee

        WHERE 1=1 {conditions}
    """, filters, as_dict=True)

    return columns, data