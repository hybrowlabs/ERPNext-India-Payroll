from datetime import datetime
import frappe


def validate(self, method):
    effective_from = (
        self.effective_from
        if isinstance(self.effective_from, datetime)
        else datetime.strptime(self.effective_from, "%Y-%m-%d")
    ).date()  # Make it a date object

    active_employees = frappe.get_all(
        "Employee", filters={"status": "Active"}, fields=["name"]
    )

    if active_employees:
        for emp in active_employees:
            ssa_list = frappe.get_list(
                "Salary Structure Assignment",
                filters={"employee": emp.name, "docstatus": 1},
                fields=["name"],
                order_by="from_date desc",
                limit=1,
            )

            if ssa_list:
                ssa = frappe.get_doc("Salary Structure Assignment", ssa_list[0].name)

                if ssa.from_date <= effective_from:
                    new_ssa = frappe.new_doc("Salary Structure Assignment")
                    new_ssa.employee = ssa.employee
                    new_ssa.salary_structure = ssa.salary_structure
                    new_ssa.from_date = self.effective_from
                    new_ssa.income_tax_slab = self.income_tax_slab
                    new_ssa.company = self.company
                    new_ssa.custom_payroll_period = self.payroll_period
                    new_ssa.currency = ssa.currency
                    new_ssa.base = ssa.base
                    new_ssa.custom_is_uniform_allowance = (
                        ssa.custom_is_uniform_allowance
                    )
                    new_ssa.custom_uniform_allowance_value = (
                        ssa.custom_uniform_allowance_value
                    )
                    new_ssa.custom_is_hra = ssa.custom_is_hra
                    new_ssa.custom_hra_value = ssa.custom_hra_value
                    new_ssa.custom_is_educational_allowance = (
                        ssa.custom_is_educational_allowance
                    )
                    new_ssa.custom_educational_allowance_value = (
                        ssa.custom_educational_allowance_value
                    )
                    new_ssa.custom_is_other_allowancegratuity = (
                        ssa.custom_is_other_allowancegratuity
                    )
                    new_ssa.custom_other_allowancegratuity_value = (
                        ssa.custom_other_allowancegratuity_value
                    )
                    new_ssa.custom_is_medical_allowance = (
                        ssa.custom_is_medical_allowance
                    )
                    new_ssa.custom_medical_allowance_value = (
                        ssa.custom_medical_allowance_value
                    )

                    new_ssa.custom_is_hostel_allowance = ssa.custom_is_hostel_allowance
                    new_ssa.custom_hostel_allowance_value = (
                        ssa.custom_hostel_allowance_value
                    )
                    new_ssa.custom_is_twadfi = ssa.custom_is_twadfi
                    new_ssa.custom_twadfi_value = ssa.custom_twadfi_value
                    new_ssa.custom_monthly_driver_reimbursement = (
                        ssa.custom_monthly_driver_reimbursement
                    )
                    new_ssa.custom_monthly_driver_reimbursement_value = (
                        ssa.custom_monthly_driver_reimbursement_value
                    )
                    new_ssa.custom_driver_name = ssa.custom_driver_name
                    new_ssa.custom_vehicle_number = ssa.custom_vehicle_number
                    new_ssa.custom_is_food_coupon = ssa.custom_is_food_coupon
                    new_ssa.custom_is_professional_persuit_allowance = (
                        ssa.custom_is_professional_persuit_allowance
                    )
                    new_ssa.custom_professional_persuit_allowance_value = (
                        ssa.custom_professional_persuit_allowance_value
                    )
                    new_ssa.custom_is_driver_allowancebonus = (
                        ssa.custom_is_driver_allowancebonus
                    )
                    new_ssa.custom_driver_allowancebonus_value = (
                        ssa.custom_driver_allowancebonus_value
                    )
                    new_ssa.custom_is_epf = ssa.custom_is_epf
                    new_ssa.custom_is_nps = ssa.custom_is_nps

                    new_ssa.custom_nps_percentage = ssa.custom_nps_percentage
                    new_ssa.custom_is_esic = ssa.custom_is_esic
                    new_ssa.custom_state = ssa.custom_state
                    new_ssa.custom__car_perquisite = ssa.custom__car_perquisite
                    new_ssa.custom_cubic_capacity_of_company = (
                        ssa.custom_cubic_capacity_of_company
                    )
                    new_ssa.custom_car_perquisite_as_per_rules = (
                        ssa.custom_car_perquisite_as_per_rules
                    )

                    new_ssa.custom_driver_provided_by_company = (
                        ssa.custom_driver_provided_by_company
                    )
                    new_ssa.custom_driver_perquisite_as_per_rules = (
                        ssa.custom_driver_perquisite_as_per_rules
                    )
                    new_ssa.custom_is_special_conveyance = (
                        ssa.custom_is_special_conveyance
                    )
                    new_ssa.custom_special_conveyance_amount_annual = (
                        ssa.custom_special_conveyance_amount_annual
                    )
                    new_ssa.custom_is_car_allowance = ssa.custom_is_car_allowance
                    new_ssa.custom_car_allowance_amount_annual = (
                        ssa.custom_car_allowance_amount_annual
                    )
                    new_ssa.custom_is_extra_driver_salary = (
                        ssa.custom_is_extra_driver_salary
                    )
                    new_ssa.custom_extra_driver_salary_value = (
                        ssa.custom_extra_driver_salary_value
                    )
                    new_ssa.custom_is_incentive = ssa.custom_is_incentive
                    new_ssa.custom_incentive_amount_annual = (
                        ssa.custom_incentive_amount_annual
                    )
                    new_ssa.custom_is_special_hra = ssa.custom_is_special_hra
                    new_ssa.custom_special_hra_amount_annual = (
                        ssa.custom_special_hra_amount_annual
                    )
                    new_ssa.custom_statistical_amount = ssa.custom_statistical_amount
                    new_ssa.custom_is_car_petrol_lta = ssa.custom_is_car_petrol_lta

                    for row in ssa.custom_employee_reimbursements:
                        new_ssa.append(
                            "custom_employee_reimbursements",
                            {
                                "reimbursements": row.reimbursements,
                                "monthly_total_amount": row.monthly_total_amount,
                            },
                        )

                    new_ssa.insert()
                    new_ssa.submit()
