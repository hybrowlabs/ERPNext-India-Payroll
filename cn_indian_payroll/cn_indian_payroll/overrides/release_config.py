import frappe
from frappe.utils import getdate, add_months
from calendar import monthrange
import datetime

@frappe.whitelist()
def get_date_format(start_date, end_date, payroll_period, docname):
    if not (start_date and end_date and payroll_period and docname):
        frappe.throw("Missing required inputs.")

    start_date = getdate(start_date)
    end_date = getdate(end_date)

    period = frappe.get_doc("Payroll Period", payroll_period)
    doc = frappe.get_doc("Release Config", docname)


    end_day = min(end_date.day, 28)

    current_date = start_date
    doc.set("locking_period_months", [])

    while current_date <= period.end_date:

        formatted_month = current_date.strftime("%b-%Y")


        month_start = current_date

        try:
            month_end = current_date.replace(day=end_day)
        except ValueError:
            last_day = monthrange(current_date.year, current_date.month)[1]
            month_end = current_date.replace(day=last_day)


        doc.append("locking_period_months", {
            "month": formatted_month,
            "start_date": month_start,
            "end_date": month_end,
            "enable": 1
        })


        current_date = add_months(current_date, 1)


    doc.save(ignore_permissions=True)

    return {"status": "success", "added_months": len(doc.locking_period_months)}
