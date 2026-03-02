import frappe
from hrms.payroll.doctype.salary_structure_assignment.salary_structure_assignment import (
    SalaryStructureAssignment,
)

from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip
from frappe.utils import getdate
from frappe.utils import get_last_day, getdate


class CustomSalaryStructureAssignment(SalaryStructureAssignment):
    def before_save(self):
        self.set_cpl()
        self.reimbursement_amount()
        self.update_employee_promotion_from_date()

        # self.insert_tax_declaration()

    def on_submit(self):
        self.insert_tax_declaration()
        self.update_employee_promotion()
        self.insert_joining_bonus()
        self.set_variable_pay_amount()

    def before_update_after_submit(self):
        self.reimbursement_amount()
        self.update_employee_promotion_from_date()
        self.insert_joining_bonus()
        self.set_variable_pay_amount()

    def update_employee_promotion_from_date(self):
        if self.custom_is_increment:
            promotions = frappe.get_all(
                "Employee Promotion",
                filters={
                    "employee": self.employee,
                    "company": self.company,
                    "promotion_date": self.from_date,
                    "docstatus": 0,
                },
                fields=["name"],
            )

            if promotions:
                self.custom_promotion_id = promotions[0].name

    def on_cancel(self):
        self.cancel_declaration()

    def cancel_declaration(self):
        data = frappe.db.get_list(
            "Employee Tax Exemption Declaration",
            filters={
                "payroll_period": self.custom_payroll_period,
                "docstatus": ["in", [0, 1]],
                "employee": self.employee,
                "custom_salary_structure_assignment": self.name,
            },
            fields=["*"],
        )

        if len(data) > 0:
            data_doc = frappe.get_doc(
                "Employee Tax Exemption Declaration", data[0].name
            )

            if data_doc.docstatus == 0:
                frappe.delete_doc("Employee Tax Exemption Declaration", data_doc.name)

            if data_doc.docstatus == 1:
                data_doc.docstatus = 2

                data_doc.save()
                frappe.delete_doc("Employee Tax Exemption Declaration", data_doc.name)

    def update_employee_promotion(self):
        if self.custom_promotion_id:
            get_promotion_doc = frappe.get_doc(
                "Employee Promotion", self.custom_promotion_id
            )
            get_promotion_doc.custom_new_salary_structure_assignment_id = self.name
            get_promotion_doc.custom_new_effective_from = self.from_date
            get_promotion_doc.revised_ctc = self.base
            get_promotion_doc.custom_status = "Payroll Configured"
            get_promotion_doc.save()

            # get_promotion_doc.reload()

            # frappe.db.commit()

    def insert_tax_declaration(self):
        if self.employee:
            array = []
            amount = []
            max_amount_category = []
            get_payroll_period = frappe.get_doc(
                "Payroll Period", self.custom_payroll_period
            )

            from_date = getdate(self.from_date)
            payroll_start_date = getdate(get_payroll_period.start_date)
            payroll_end_date = getdate(get_payroll_period.end_date)
            declaration_date = max(from_date, payroll_start_date)
            start_date = declaration_date
            end_date = payroll_end_date

            if isinstance(start_date, str):
                start = datetime.strptime(start_date, "%Y-%m-%d").date()
            else:
                start = start_date

            if isinstance(end_date, str):
                end = datetime.strptime(end_date, "%Y-%m-%d").date()
            else:
                end = end_date

            num_months = (end.year - start.year) * 12 + (end.month - start.month) + 1

            if self.custom_tax_regime == "Old Regime":
                # find Uniform
                if (
                    self.custom_is_uniform_allowance
                    and self.custom_uniform_allowance_value
                ):
                    uniform_component = frappe.get_list(
                        "Employee Tax Exemption Sub Category",
                        filters={"custom_component_type": "Uniform"},
                        fields=["*"],
                    )
                    if len(uniform_component) > 0:
                        for i in uniform_component:
                            array.append(i.name)
                            amount.append(0)

                            max_amount_category.append(i.max_amount)

                # find epf

                if self.custom_is_epf:
                    new_salary_slip = make_salary_slip(
                        source_name=self.salary_structure,
                        employee=self.employee,
                        print_format="Salary Slip Standard for CTC",
                        posting_date=self.from_date,
                        for_preview=1,
                    )
                    for new_earning in new_salary_slip.deductions:
                        epf_component = frappe.get_doc(
                            "Salary Component", new_earning.salary_component
                        )
                        if epf_component.component_type == "EPF":
                            epf_amount_year = new_earning.amount * num_months

                            epf_component_subcategory = frappe.get_list(
                                "Employee Tax Exemption Sub Category",
                                filters={"custom_component_type": "EPF"},
                                fields=["*"],
                            )
                            if len(epf_component_subcategory) > 0:
                                for i in epf_component_subcategory:
                                    array.append(i.name)

                                    max_amount_category.append(i.max_amount)

                                    if epf_amount_year > i.max_amount:
                                        amount.append(i.max_amount)
                                    else:
                                        amount.append(epf_amount_year)

                # find nps
                if self.custom_is_nps:
                    new_salary_slip = make_salary_slip(
                        source_name=self.salary_structure,
                        employee=self.employee,
                        print_format="Salary Slip Standard for CTC",
                        posting_date=self.from_date,
                        for_preview=1,
                    )
                    for new_earning in new_salary_slip.earnings:
                        nps_component = frappe.get_doc(
                            "Salary Component", new_earning.salary_component
                        )
                        if nps_component.component_type == "NPS":
                            nps_amount_year = new_earning.amount * num_months
                            nps_component = frappe.get_list(
                                "Employee Tax Exemption Sub Category",
                                filters={"custom_component_type": "NPS"},
                                fields=["*"],
                            )

                            if len(nps_component) > 0:
                                for i in nps_component:
                                    array.append(i.name)
                                    max_amount_category.append(nps_amount_year)

                                    amount.append(nps_amount_year)

                if self.custom_state:
                    pt_component = frappe.get_list(
                        "Employee Tax Exemption Sub Category",
                        filters={"custom_component_type": "Professional Tax"},
                        fields=["*"],
                    )

                    if len(pt_component) > 0:
                        for i in pt_component:
                            array.append(i.name)
                            max_amount_category.append(i.max_amount)

                            amount.append(i.max_amount)

            if self.custom_tax_regime == "New Regime":
                if self.custom_is_nps:
                    new_salary_slip = make_salary_slip(
                        source_name=self.salary_structure,
                        employee=self.employee,
                        print_format="Salary Slip Standard for CTC",
                        posting_date=self.from_date,
                        for_preview=1,
                    )
                    for new_earning in new_salary_slip.earnings:
                        nps_component = frappe.get_doc(
                            "Salary Component", new_earning.salary_component
                        )
                        if nps_component.component_type == "NPS":
                            nps_amount_year = new_earning.amount * num_months
                            nps_component = frappe.get_list(
                                "Employee Tax Exemption Sub Category",
                                filters={"custom_component_type": "NPS"},
                                fields=["*"],
                            )

                            if len(nps_component) > 0:
                                for i in nps_component:
                                    array.append(i.name)
                                    max_amount_category.append(nps_amount_year)

                                    amount.append(nps_amount_year)

            get_all_declaration = frappe.get_list(
                "Employee Tax Exemption Declaration",
                filters={
                    "employee": self.employee,
                    "payroll_period": self.custom_payroll_period,
                    "docstatus": ["in", [0, 1]],
                },
                fields=["*"],
            )

            if len(get_all_declaration) == 0:
                insert_declaration = frappe.get_doc(
                    {"doctype": "Employee Tax Exemption Declaration"}
                )
                insert_declaration.employee = (self.employee,)
                insert_declaration.company = (self.company,)
                insert_declaration.payroll_period = (self.custom_payroll_period,)
                insert_declaration.currency = (self.currency,)
                insert_declaration.custom_income_tax = (self.income_tax_slab,)
                insert_declaration.custom_salary_structure_assignment = (self.name,)
                # insert_declaration.custom_posting_date = frappe.utils.nowdate(),
                insert_declaration.custom_posting_date = declaration_date

                for x in range(len(array)):
                    doc2_child1 = insert_declaration.append("declarations", {})
                    doc2_child1.exemption_sub_category = array[x]
                    doc2_child1.amount = amount[x]
                    doc2_child1.max_amount = max_amount_category[x]

                insert_declaration.insert()
                insert_declaration.submit()
                frappe.db.commit()

    def set_cpl(self):
        components = [
            "Vehicle Maintenance Reimbursement",
            "Petrol Reimbursement",
            "Leave Travel Allowance",
        ]
        array = []

        if self.custom_employee_reimbursements:
            for i in self.custom_employee_reimbursements:
                if i.reimbursements in components:
                    array.append(i.reimbursements)

            if len(array) == 3:
                self.custom_is_car_petrol_lta = 1

            else:
                self.custom_is_car_petrol_lta = 0

    def reimbursement_amount(self):
        total_amount = 0
        if len(self.custom_employee_reimbursements) > 0:
            for reimbursement in self.custom_employee_reimbursements:
                total_amount += reimbursement.monthly_total_amount

        self.custom_statistical_amount = total_amount

    def set_variable_pay_amount(self):
        # Now calculate Variable Pay based on rating
        for row in self.custom_other_extra_payments:
            if row.additional_earning == "Variable Pay" and getattr(
                row, "rating", None
            ):
                payroll_setting = frappe.get_doc("Payroll Settings")
                if getattr(payroll_setting, "custom_varible_pay_config", None):
                    for config in payroll_setting.custom_varible_pay_config:
                        # Match the rating from config and row
                        if getattr(config, "rating", None) == getattr(
                            row, "rating", None
                        ):
                            # Calculate variable pay
                            self.custom_variable_pay_amount = (
                                row.amount * config.percentage
                            ) / 100
                            break  # Stop after first match for this row

    def insert_joining_bonus(self):
        if not self.custom_other_extra_payments:
            return

        for row in self.custom_other_extra_payments:
            if row.additional_earning == "Joining Bonus":
                company = frappe.get_doc("Company", self.company)

                if not company.custom_joining_bonus:
                    return

                # Check if already submitted Additional Salary exists
                additional_salary = frappe.get_list(
                    "Additional Salary",
                    filters={
                        "employee": self.employee,
                        "salary_component": company.custom_joining_bonus,
                        "docstatus": 1,
                    },
                    limit=1,
                )

                if not additional_salary:
                    last_day = get_last_day(getdate(self.from_date))

                    doc = frappe.get_doc(
                        {
                            "doctype": "Additional Salary",
                            "employee": self.employee,
                            "salary_component": company.custom_joining_bonus,
                            "payroll_date": last_day,
                            "company": self.company,
                            "currency": frappe.db.get_value(
                                "Company", self.company, "default_currency"
                            ),
                            "amount": row.amount,  # assuming amount is in child table
                        }
                    )

                    doc.insert()
                    doc.submit()
