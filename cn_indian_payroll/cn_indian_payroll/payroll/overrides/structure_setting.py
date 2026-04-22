from datetime import datetime

import frappe
from frappe.utils.background_jobs import enqueue

_SSA_FIELDS = [
    "name",
    "employee",
    "salary_structure",
    "from_date",
    "currency",
    "base",
    "custom_is_uniform_allowance",
    "custom_uniform_allowance_value",
    "custom_is_medical_allowance",
    "custom_medical_allowance_value",
    "custom_is_food_coupon",
    "custom_is_epf",
    "custom_is_nps",
    "custom_is_esic",
    "custom_state",
    "custom__car_perquisite",
    "custom_cubic_capacity_of_company",
    "custom_car_perquisite_as_per_rules",
    "custom_driver_provided_by_company",
    "custom_driver_perquisite_as_per_rules",
    "custom_nps_percentage",
]


@frappe.whitelist()
def create_salary_structure_assignment(company, payroll_period, income_tax_slab, effective_date):
    frappe.only_for("HR Manager")
    enqueue(
        method=create_salary_structure_assignment_worker,
        queue="default",
        timeout=600,
        is_async=True,
        company=company,
        payroll_period=payroll_period,
        income_tax_slab=income_tax_slab,
        effective_date=effective_date,
        triggered_by=frappe.session.user,
    )
    return "queued"


def create_salary_structure_assignment_worker(
    company, payroll_period, income_tax_slab, effective_date, triggered_by=None
):
    def _publish(progress):
        frappe.publish_realtime("ssa_progress", {"progress": progress}, user=triggered_by)

    try:
        effective_date = datetime.strptime(effective_date, "%Y-%m-%d").date()

        employees = frappe.get_all("Employee", filters={"status": "Active"}, fields=["name"])
        emp_names = [e.name for e in employees]
        total = len(emp_names)

        # Batch: latest submitted SSA per employee — one query instead of N
        all_ssa = frappe.get_all(
            "Salary Structure Assignment",
            filters={"employee": ["in", emp_names], "docstatus": 1},
            fields=_SSA_FIELDS,
            order_by="employee, from_date desc",
        )

        # Keep only the most-recent SSA per employee
        latest_ssa_map = {}
        for ssa in all_ssa:
            if ssa.employee not in latest_ssa_map:
                latest_ssa_map[ssa.employee] = ssa

        # Employees already having an SSA on effective_date — skip them
        existing = frappe.get_all(
            "Salary Structure Assignment",
            filters={"employee": ["in", emp_names], "from_date": effective_date, "docstatus": 1},
            pluck="employee",
        )
        skip_set = set(existing)

        # Benefits for all relevant SSAs — batch fetch
        relevant_ssa_names = [v.name for v in latest_ssa_map.values()]
        benefits_rows = (
            frappe.get_all(
                "Employee Benefit",
                filters={"parent": ["in", relevant_ssa_names]},
                fields=["parent", "salary_component", "amount"],
            )
            if relevant_ssa_names
            else []
        )
        benefits_map = {}
        for b in benefits_rows:
            benefits_map.setdefault(b.parent, []).append(b)

        for idx, emp_name in enumerate(emp_names):
            if idx % max(1, total // 20) == 0:
                _publish(int((idx + 1) / total * 100))

            if emp_name in skip_set:
                continue

            ssa = latest_ssa_map.get(emp_name)
            if not ssa or ssa.from_date > effective_date:
                continue

            new_ssa = frappe.new_doc("Salary Structure Assignment")
            new_ssa.update(
                {
                    "employee": emp_name,
                    "salary_structure": ssa.salary_structure,
                    "from_date": effective_date,
                    "income_tax_slab": income_tax_slab,
                    "company": company,
                    "custom_payroll_period": payroll_period,
                    "currency": ssa.currency,
                    "base": ssa.base,
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
                }
            )

            for row in benefits_map.get(ssa.name, []):
                new_ssa.append(
                    "employee_benefits", {"salary_component": row.salary_component, "amount": row.amount}
                )

            new_ssa.insert()
            new_ssa.submit()

        _publish(100)

    except Exception:
        frappe.log_error(frappe.get_traceback(), "Salary Structure Assignment Creation Failed")
        _publish(100)
