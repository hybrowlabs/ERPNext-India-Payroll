import frappe
from frappe.utils.pdf import get_pdf

@frappe.whitelist()
def get_annual_statement_pdf(employee, payroll_period):
    # Define months
    months = [
        "April-2025", "May-2025", "June-2025", "July-2025", "August-2025", "September-2025",
        "October-2025", "November-2025", "December-2025", "January-2026", "February-2026", "March-2026"
    ]

    # Example particulars with dummy data
    particulars = [
        {"name": "Basic Salary", "values": [5000 for _ in months]},
        {"name": "House Rent Allowance", "values": [3000 for _ in months]},
        {"name": "Special Allowance", "values": [2000 for _ in months]},
    ]

    # Add totals per row
    for row in particulars:
        row["total"] = sum(row["values"])

    # Calculate total for each month
    monthly_totals = [sum(row["values"][i] for row in particulars) for i in range(len(months))]

    # Grand total
    grand_total = sum(monthly_totals)

    context = {
        "employee": employee,
        "payroll_period": payroll_period,
        "months": months,
        "particulars": particulars,
        "monthly_totals": monthly_totals,
        "grand_total": grand_total
    }

    html = frappe.render_template("cn_indian_payroll/templates/includes/annual_statement.html", context)

    return {"html": html}
