import frappe
from frappe.utils import formatdate

@frappe.whitelist()
def get_lta_breakup(employee):
    lta_accruals = frappe.get_all(
        "LTA Accrual",
        filters={
            "employee": employee,
        },
        fields=["amount", "date", "year", "lta_exempted"],
        order_by="date asc"
    )

    breakup = []
    for idx, accrual in enumerate(lta_accruals, start=1):
        breakup.append({
            "sl_no": idx,
            "lta_exempted": accrual.lta_exempted,
            "amount": accrual.amount,
            "date": formatdate(accrual.date) if accrual.date else "",
            "year": accrual.year,
        })

    return breakup
