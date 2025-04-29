# from datetime import datetime
# import frappe


# def validate(self, method):
#     effective_from = (
#         self.effective_from
#         if isinstance(self.effective_from, datetime)
#         else datetime.strptime(self.effective_from, "%Y-%m-%d")
#     ).date()  # Make it a date object

#     active_employees = frappe.get_all(
#         "Employee", filters={"status": "Active"}, fields=["name"]
#     )

#     if active_employees:
#         for emp in active_employees:
#             ssa_list = frappe.get_list(
#                 "Salary Structure Assignment",
#                 filters={"employee": emp.name, "docstatus": 1},
#                 fields=["name"],
#                 order_by="from_date desc",
#                 limit=1,
#             )

#             if ssa_list:
#                 ssa = frappe.get_doc("Salary Structure Assignment", ssa_list[0].name)

#                 if ssa.from_date <= effective_from:
#                     new_ssa = frappe.new_doc("Salary Structure Assignment")
#                     new_ssa.employee = ssa.employee
#                     new_ssa.salary_structure = ssa.salary_structure
#                     new_ssa.from_date = self.effective_from
#                     new_ssa.income_tax_slab = self.income_tax_slab
#                     new_ssa.company = self.company
#                     new_ssa.custom_payroll_period = self.payroll_period
#                     new_ssa.currency = ssa.currency
#                     new_ssa.base = ssa.base
#                     new_ssa.custom_is_uniform_allowance = (
#                         ssa.custom_is_uniform_allowance
#                     )
#                     new_ssa.custom_uniform_allowance_value = (
#                         ssa.custom_uniform_allowance_value
#                     )
#                     new_ssa.custom_is_hra = ssa.custom_is_hra
#                     new_ssa.custom_hra_value = ssa.custom_hra_value
#                     new_ssa.custom_is_educational_allowance = (
#                         ssa.custom_is_educational_allowance
#                     )
#                     new_ssa.custom_educational_allowance_value = (
#                         ssa.custom_educational_allowance_value
#                     )
#                     new_ssa.custom_is_other_allowancegratuity = (
#                         ssa.custom_is_other_allowancegratuity
#                     )
#                     new_ssa.custom_other_allowancegratuity_value = (
#                         ssa.custom_other_allowancegratuity_value
#                     )
#                     new_ssa.custom_is_medical_allowance = (
#                         ssa.custom_is_medical_allowance
#                     )
#                     new_ssa.custom_medical_allowance_value = (
#                         ssa.custom_medical_allowance_value
#                     )

#                     new_ssa.custom_is_hostel_allowance = ssa.custom_is_hostel_allowance
#                     new_ssa.custom_hostel_allowance_value = (
#                         ssa.custom_hostel_allowance_value
#                     )
#                     new_ssa.custom_is_twadfi = ssa.custom_is_twadfi
#                     new_ssa.custom_twadfi_value = ssa.custom_twadfi_value
#                     new_ssa.custom_monthly_driver_reimbursement = (
#                         ssa.custom_monthly_driver_reimbursement
#                     )
#                     new_ssa.custom_monthly_driver_reimbursement_value = (
#                         ssa.custom_monthly_driver_reimbursement_value
#                     )
#                     new_ssa.custom_driver_name = ssa.custom_driver_name
#                     new_ssa.custom_vehicle_number = ssa.custom_vehicle_number
#                     new_ssa.custom_is_food_coupon = ssa.custom_is_food_coupon
#                     new_ssa.custom_is_professional_persuit_allowance = (
#                         ssa.custom_is_professional_persuit_allowance
#                     )
#                     new_ssa.custom_professional_persuit_allowance_value = (
#                         ssa.custom_professional_persuit_allowance_value
#                     )
#                     new_ssa.custom_is_driver_allowancebonus = (
#                         ssa.custom_is_driver_allowancebonus
#                     )
#                     new_ssa.custom_driver_allowancebonus_value = (
#                         ssa.custom_driver_allowancebonus_value
#                     )
#                     new_ssa.custom_is_epf = ssa.custom_is_epf
#                     new_ssa.custom_is_nps = ssa.custom_is_nps

#                     new_ssa.custom_nps_percentage = ssa.custom_nps_percentage
#                     new_ssa.custom_is_esic = ssa.custom_is_esic
#                     new_ssa.custom_state = ssa.custom_state
#                     new_ssa.custom__car_perquisite = ssa.custom__car_perquisite
#                     new_ssa.custom_cubic_capacity_of_company = (
#                         ssa.custom_cubic_capacity_of_company
#                     )
#                     new_ssa.custom_car_perquisite_as_per_rules = (
#                         ssa.custom_car_perquisite_as_per_rules
#                     )

#                     new_ssa.custom_driver_provided_by_company = (
#                         ssa.custom_driver_provided_by_company
#                     )
#                     new_ssa.custom_driver_perquisite_as_per_rules = (
#                         ssa.custom_driver_perquisite_as_per_rules
#                     )
#                     new_ssa.custom_is_special_conveyance = (
#                         ssa.custom_is_special_conveyance
#                     )
#                     new_ssa.custom_special_conveyance_amount_annual = (
#                         ssa.custom_special_conveyance_amount_annual
#                     )
#                     new_ssa.custom_is_car_allowance = ssa.custom_is_car_allowance
#                     new_ssa.custom_car_allowance_amount_annual = (
#                         ssa.custom_car_allowance_amount_annual
#                     )
#                     new_ssa.custom_is_extra_driver_salary = (
#                         ssa.custom_is_extra_driver_salary
#                     )
#                     new_ssa.custom_extra_driver_salary_value = (
#                         ssa.custom_extra_driver_salary_value
#                     )
#                     new_ssa.custom_is_incentive = ssa.custom_is_incentive
#                     new_ssa.custom_incentive_amount_annual = (
#                         ssa.custom_incentive_amount_annual
#                     )
#                     new_ssa.custom_is_special_hra = ssa.custom_is_special_hra
#                     new_ssa.custom_special_hra_amount_annual = (
#                         ssa.custom_special_hra_amount_annual
#                     )
#                     new_ssa.custom_statistical_amount = ssa.custom_statistical_amount
#                     new_ssa.custom_is_car_petrol_lta = ssa.custom_is_car_petrol_lta

#                     for row in ssa.custom_employee_reimbursements:
#                         new_ssa.append(
#                             "custom_employee_reimbursements",
#                             {
#                                 "reimbursements": row.reimbursements,
#                                 "monthly_total_amount": row.monthly_total_amount,
#                             },
#                         )

#                     new_ssa.insert()
#                     new_ssa.submit()


import frappe
from frappe import _
from frappe.utils.background_jobs import enqueue
from frappe.model.document import Document
from datetime import datetime


@frappe.whitelist()
def create_salary_structure_assignment(
    company, payroll_period, income_tax_slab, effective_date
):
    enqueue(
        method=create_salary_structure_assignment_worker,
        queue="default",
        timeout=600,
        is_async=True,
        company=company,
        payroll_period=payroll_period,
        income_tax_slab=income_tax_slab,
        effective_date=effective_date,
    )
    return "queued"


def create_salary_structure_assignment_worker(
    company, payroll_period, income_tax_slab, effective_date
):
    try:
        effective_date = datetime.strptime(effective_date, "%Y-%m-%d").date()

        employees = frappe.get_all(
            "Employee", filters={"status": "Active"}, fields=["name"]
        )
        total = len(employees)

        for idx, emp in enumerate(employees):
            frappe.publish_realtime(
                "ssa_progress", {"progress": int((idx + 1) / total * 100)}
            )

            # ✅ Skip if SSA with same from_date already exists for employee
            if frappe.db.exists(
                "Salary Structure Assignment",
                {"employee": emp.name, "from_date": effective_date, "docstatus": 1},
            ):
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

                new_ssa.update(
                    {
                        "employee": emp.name,
                        "salary_structure": ssa.salary_structure,
                        "from_date": effective_date,
                        "income_tax_slab": income_tax_slab,
                        "company": company,
                        "custom_payroll_period": payroll_period,
                        "currency": ssa.currency,
                        "base": ssa.base,
                        "custom_is_uniform_allowance": ssa.custom_is_uniform_allowance,
                        "custom_uniform_allowance_value": ssa.custom_uniform_allowance_value,
                        "custom_is_hra": ssa.custom_is_hra,
                        "custom_hra_value": ssa.custom_hra_value,
                        "custom_is_educational_allowance": ssa.custom_is_educational_allowance,
                        "custom_educational_allowance_value": ssa.custom_educational_allowance_value,
                        "custom_is_other_allowancegratuity": ssa.custom_is_other_allowancegratuity,
                        "custom_other_allowancegratuity_value": ssa.custom_other_allowancegratuity_value,
                        "custom_is_medical_allowance": ssa.custom_is_medical_allowance,
                        "custom_medical_allowance_value": ssa.custom_medical_allowance_value,
                        "custom_is_hostel_allowance": ssa.custom_is_hostel_allowance,
                        "custom_hostel_allowance_value": ssa.custom_hostel_allowance_value,
                        "custom_is_twadfi": ssa.custom_is_twadfi,
                        "custom_twadfi_value": ssa.custom_twadfi_value,
                        "custom_monthly_driver_reimbursement": ssa.custom_monthly_driver_reimbursement,
                        "custom_monthly_driver_reimbursement_value": ssa.custom_monthly_driver_reimbursement_value,
                        "custom_driver_name": ssa.custom_driver_name,
                        "custom_vehicle_number": ssa.custom_vehicle_number,
                        "custom_is_food_coupon": ssa.custom_is_food_coupon,
                        "custom_is_professional_persuit_allowance": ssa.custom_is_professional_persuit_allowance,
                        "custom_professional_persuit_allowance_value": ssa.custom_professional_persuit_allowance_value,
                        "custom_is_driver_allowancebonus": ssa.custom_is_driver_allowancebonus,
                        "custom_driver_allowancebonus_value": ssa.custom_driver_allowancebonus_value,
                        "custom_is_epf": ssa.custom_is_epf,
                        "custom_is_nps": ssa.custom_is_nps,
                        "custom_nps_percentage": ssa.custom_nps_percentage,
                        "custom_is_esic": ssa.custom_is_esic,
                        "custom_state": ssa.custom_state,
                        "custom__car_perquisite": ssa.custom__car_perquisite,
                        "custom_cubic_capacity_of_company": ssa.custom_cubic_capacity_of_company,
                        "custom_car_perquisite_as_per_rules": ssa.custom_car_perquisite_as_per_rules,
                        "custom_driver_provided_by_company": ssa.custom_driver_provided_by_company,
                        "custom_driver_perquisite_as_per_rules": ssa.custom_driver_perquisite_as_per_rules,
                        "custom_is_special_conveyance": ssa.custom_is_special_conveyance,
                        "custom_special_conveyance_amount_annual": ssa.custom_special_conveyance_amount_annual,
                        "custom_is_car_allowance": ssa.custom_is_car_allowance,
                        "custom_car_allowance_amount_annual": ssa.custom_car_allowance_amount_annual,
                        "custom_is_extra_driver_salary": ssa.custom_is_extra_driver_salary,
                        "custom_extra_driver_salary_value": ssa.custom_extra_driver_salary_value,
                        "custom_is_incentive": ssa.custom_is_incentive,
                        "custom_incentive_amount_annual": ssa.custom_incentive_amount_annual,
                        "custom_is_special_hra": ssa.custom_is_special_hra,
                        "custom_special_hra_amount_annual": ssa.custom_special_hra_amount_annual,
                        "custom_statistical_amount": ssa.custom_statistical_amount,
                        "custom_is_car_petrol_lta": ssa.custom_is_car_petrol_lta,
                    }
                )

                # Copy child table entries
                for row in ssa.get("custom_employee_reimbursements", []):
                    new_ssa.append(
                        "custom_employee_reimbursements",
                        {
                            "reimbursements": row.reimbursements,
                            "monthly_total_amount": row.monthly_total_amount,
                        },
                    )

                new_ssa.insert()
                new_ssa.submit()

        frappe.publish_realtime("ssa_progress", {"progress": 100})

    except Exception:
        frappe.log_error(
            frappe.get_traceback(), "Salary Structure Assignment Creation Failed"
        )
        frappe.publish_realtime("ssa_progress", {"progress": 100})
