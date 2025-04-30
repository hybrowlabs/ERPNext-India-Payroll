

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

            # ✅ Skip if SSA with same from_date already exists for employee
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

                    # Existing fields
                    "custom_is_uniform_allowance": ssa.custom_is_uniform_allowance,
                    "custom_uniform_allowance_value": ssa.custom_uniform_allowance_value,
                    "custom_is_medical_allowance": ssa.custom_is_medical_allowance,
                    "custom_medical_allowance_value": ssa.custom_medical_allowance_value,
                    "custom_is_food_coupon": ssa.custom_is_food_coupon,
                    "custom_is_epf": ssa.custom_is_epf,
                    "custom_is_nps": ssa.custom_is_nps,
                    "custom_state": ssa.custom_state,
                    "custom__car_perquisite": ssa.custom__car_perquisite,
                    "custom_cubic_capacity_of_company": ssa.custom_cubic_capacity_of_company,
                    "custom_car_perquisite_as_per_rules": ssa.custom_car_perquisite_as_per_rules,
                    "custom_driver_provided_by_company": ssa.custom_driver_provided_by_company,
                    "custom_driver_perquisite_as_per_rules": ssa.custom_driver_perquisite_as_per_rules,
                    "custom_nps_percentage": ssa.custom_nps_percentage,

                    # ✅ Newly added fields
                    "custom_is_educational_allowance": ssa.custom_is_educational_allowance,
                    "custom_educational_allowance_value": ssa.custom_educational_allowance_value,
                    "custom_is_hra": ssa.custom_is_hra,
                    "custom_hra_value": ssa.custom_hra_value,
                    "custom_is_other_allowancegratuity": ssa.custom_is_other_allowancegratuity,
                    "custom_other_allowancegratuity_value": ssa.custom_other_allowancegratuity_value,
                    "custom_canteen_allowance": ssa.custom_canteen_allowance,
                    "custom_canteen_allowance_value": ssa.custom_canteen_allowance_value,
                    "custom_is_hostel_allowance": ssa.custom_is_hostel_allowance,
                    "custom_is_twadfi": ssa.custom_is_twadfi,
                    "custom_monthly_driver_reimbursement": ssa.custom_monthly_driver_reimbursement,
                    "custom_hostel_allowance_value": ssa.custom_hostel_allowance_value,
                    "custom_twadfi_value": ssa.custom_twadfi_value,
                    "custom_monthly_driver_reimbursement_value": ssa.custom_monthly_driver_reimbursement_value,
                    "custom_is_conveyance_allowance": ssa.custom_is_conveyance_allowance,
                    "custom_conveyance_allowance": ssa.custom_conveyance_allowance,
                    "custom_is_custom_basic": ssa.custom_is_custom_basic,
                    "custom_basic_amount": ssa.custom_basic_amount,
                    "custom_is_professional_persuit_allowance": ssa.custom_is_professional_persuit_allowance,
                    "custom_professional_persuit_allowance_value": ssa.custom_professional_persuit_allowance_value,
                    "custom_is_driver_allowancebonus": ssa.custom_is_driver_allowancebonus,
                    "custom_driver_allowancebonus_value": ssa.custom_driver_allowancebonus_value,
                    "custom_is_adhoc": ssa.custom_is_adhoc,
                    "custom_adhoc_amount": ssa.custom_adhoc_amount,
                    "custom_is_city_compensation": ssa.custom_is_city_compensation,
                    "custom_city_compensation_value": ssa.custom_city_compensation_value,
                    "custom_is_special_hra": ssa.custom_is_special_hra,
                    "custom_special_hra_amount_annual": ssa.custom_special_hra_amount_annual,
                    "custom_is_extra_driver_salary": ssa.custom_is_extra_driver_salary,
                    "custom_extra_driver_salary_value": ssa.custom_extra_driver_salary_value,
                    "custom_is_performance_allowance": ssa.custom_is_performance_allowance,
                    "custom_performance_allowance_value": ssa.custom_performance_allowance_value,
                    "custom_apna_bank": ssa.custom_apna_bank,
                    "custom_apna_bank_monthly": ssa.custom_apna_bank_monthly,
                    "custom_is_special_conveyance": ssa.custom_is_special_conveyance,
                    "custom_special_conveyance_amount_annual": ssa.custom_special_conveyance_amount_annual,
                    "custom_is_bus_deduction": ssa.custom_is_bus_deduction,
                    "custom_bus_deduction_value": ssa.custom_bus_deduction_value,
                    "custom_is_accomdation_allowance": ssa.custom_is_accomdation_allowance,
                    "custom_accomdation_allowance_value": ssa.custom_accomdation_allowance_value,
                    "custom_is_incentive": ssa.custom_is_incentive,
                    "custom_incentive_amount_annual": ssa.custom_incentive_amount_annual,
                    "custom_is_car_allowance": ssa.custom_is_car_allowance,
                    "custom_car_allowance_amount_annual": ssa.custom_car_allowance_amount_annual,
                    "custom_lic_premium": ssa.custom_lic_premium,
                    "custom_lic_premium_value": ssa.custom_lic_premium_value,
                    "custom_is_special_allowance": ssa.custom_is_special_allowance,
                    "custom_special_allowance": ssa.custom_special_allowance,
                    "custom_is_gratuity": ssa.custom_is_gratuity,
                    "custom_gratuity_value": ssa.custom_gratuity_value,
                    "custom_lwf_ee": ssa.custom_lwf_ee,
                    "custom_lwf_ee_value": ssa.custom_lwf_ee_value,
                    "custom_is_special_project_allowace": ssa.custom_is_special_project_allowace,
                    "custom_special_project_allowace": ssa.custom_special_project_allowace,
                    "custom_superannuation": ssa.custom_superannuation,
                    "custom_superannuation_value": ssa.custom_superannuation_value,
                    "custom_is_books_and_periodicals": ssa.custom_is_books_and_periodicals,
                    "custom_books_and_periodicals": ssa.custom_books_and_periodicals,
                    "custom_motor_car_reimbursement": ssa.custom_motor_car_reimbursement,
                    "custom_motor_car_reimbursement_amount": ssa.custom_motor_car_reimbursement_amount,
                    "custom_car_maintenance": ssa.custom_car_maintenance,
                    "custom_maintenance_amountyearly": ssa.custom_maintenance_amountyearly
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
