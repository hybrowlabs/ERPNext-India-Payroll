

import frappe
from frappe import _
from frappe.utils.background_jobs import enqueue
from frappe.model.document import Document
from datetime import datetime

@frappe.whitelist()
def create_salary_structure_assignment(company, payroll_period, income_tax_slab, effective_date):
    enqueue(
        method=create_salary_structure_assignment_worker,
        queue='default',
        timeout=600,
        is_async=True,
        company=company,
        payroll_period=payroll_period,
        income_tax_slab=income_tax_slab,
        effective_date=effective_date
    )
    return "queued"

def create_salary_structure_assignment_worker(company, payroll_period, income_tax_slab, effective_date):
    try:
        effective_date = datetime.strptime(effective_date, "%Y-%m-%d").date()

        employees = frappe.get_all("Employee", filters={"status": "Active"}, fields=["name"])
        total = len(employees)

        for idx, emp in enumerate(employees):
            frappe.publish_realtime("ssa_progress", {"progress": int((idx + 1) / total * 100)})

            if frappe.db.exists("Salary Structure Assignment", {
                "employee": emp.name,
                "from_date": effective_date,
                "docstatus": 1
            }):
                continue

            ssa_list = frappe.get_list(
                "Salary Structure Assignment",
                filters={"employee": emp.name, "docstatus": 1},
                fields=["name"],
                order_by="from_date desc",
                limit=1,
            )

            if not ssa_list:
                continue

            ssa = frappe.get_doc("Salary Structure Assignment", ssa_list[0].name)
            if ssa.from_date <= effective_date:
                new_ssa = frappe.new_doc("Salary Structure Assignment")

                new_ssa.update({
                    "employee": emp.name,
                    "salary_structure": ssa.salary_structure,
                    "from_date": effective_date,
                    "income_tax_slab": income_tax_slab,
                    "company": company,
                    "custom_payroll_period": payroll_period,
                    "currency": ssa.currency,
                    "base": ssa.base,

                    # Custom Fields
                    "custom_is_uniform_allowance": ssa.custom_is_uniform_allowance,
                    "custom_uniform_allowance_value": ssa.custom_uniform_allowance_value,
                    "custom_is_medical_allowance": ssa.custom_is_medical_allowance,
                    "custom_medical_allowance_value": ssa.custom_medical_allowance_value,
                    "custom_is_food_coupon": ssa.custom_is_food_coupon,
                    "custom_is_epf": ssa.custom_is_epf,
                    "custom_is_nps": ssa.custom_is_nps,
                    "custom_is_esic": ssa.custom_is_esic,
                    "custom_state": ssa.custom_state,
                    "custom__car_perquisite": ssa.custom__car_perquisite,
                    "custom_cubic_capacity_of_company": ssa.custom_cubic_capacity_of_company,
                    "custom_car_perquisite_as_per_rules": ssa.custom_car_perquisite_as_per_rules,
                    "custom_driver_provided_by_company": ssa.custom_driver_provided_by_company,
                    "custom_driver_perquisite_as_per_rules": ssa.custom_driver_perquisite_as_per_rules,
                    "custom_nps_percentage": ssa.custom_nps_percentage,
                })

                # Copy child table entries
                for row in ssa.get("custom_employee_reimbursements", []):
                    new_ssa.append("custom_employee_reimbursements", {
                        "reimbursements": row.reimbursements,
                        "monthly_total_amount": row.monthly_total_amount
                    })

                new_ssa.insert()
                new_ssa.submit()

        frappe.publish_realtime("ssa_progress", {"progress": 100})

    except Exception:
        frappe.log_error(frappe.get_traceback(), "Salary Structure Assignment Creation Failed")
        frappe.publish_realtime("ssa_progress", {"progress": 100})
