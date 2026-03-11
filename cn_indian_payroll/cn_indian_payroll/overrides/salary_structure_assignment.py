import frappe
from hrms.payroll.doctype.salary_structure_assignment.salary_structure_assignment import (
    SalaryStructureAssignment,
)

from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip
from frappe.utils import getdate
import datetime
from frappe.utils import get_last_day, getdate
import frappe
from frappe.utils import getdate, add_months, flt
from dateutil.relativedelta import relativedelta
from frappe.utils import flt


class CustomSalaryStructureAssignment(SalaryStructureAssignment):
    def before_save(self):
        self.set_cpl()
        self.reimbursement_amount()
        self.update_employee_promotion_from_date()

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

    def insert_tax_declaration(self):
        if not self.employee:
            return

        sub_categories = []
        payroll_period = frappe.get_doc("Payroll Period", self.custom_payroll_period)
        from_date = getdate(self.from_date)
        payroll_start_date = getdate(payroll_period.start_date)
        payroll_end_date = getdate(payroll_period.end_date)

        declaration_start_date = max(from_date, payroll_start_date)
        start = (
            declaration_start_date
            if not isinstance(declaration_start_date, str)
            else datetime.strptime(declaration_start_date, "%Y-%m-%d").date()
        )
        end = (
            payroll_end_date
            if not isinstance(payroll_end_date, str)
            else datetime.strptime(payroll_end_date, "%Y-%m-%d").date()
        )

        num_months = (end.year - start.year) * 12 + (end.month - start.month) + 1

        salary_slip = make_salary_slip(
            source_name=self.salary_structure,
            employee=self.employee,
            print_format="Salary Slip Standard",
            posting_date=self.from_date,
            for_preview=1,
        )

        def add_exemption(component_type, monthly_amount):
            total_amount = monthly_amount * num_months
            exemption_components = frappe.get_all(
                "Employee Tax Exemption Sub Category",
                filters={"custom_component_type": component_type},
                fields=["name", "max_amount"],
            )
            for comp in exemption_components:
                allowed_amount = min(total_amount, comp.max_amount or total_amount)
                sub_categories.append(
                    {
                        "sub_category": comp.name,
                        "max_amount": comp.max_amount,
                        "amount": allowed_amount,
                    }
                )

        if (
            self.custom_tax_regime == "New Regime"
            or self.custom_tax_regime == "Old Regime"
        ):
            for earning in salary_slip.earnings:
                comp_doc = frappe.get_doc("Salary Component", earning.salary_component)
                if comp_doc.component_type == "NPS":
                    add_exemption("NPS", earning.amount)

            if self.custom_tax_regime == "Old Regime":
                for deduction in salary_slip.deductions:
                    comp_doc = frappe.get_doc(
                        "Salary Component", deduction.salary_component
                    )
                    if comp_doc.component_type in ["EPF", "Professional Tax"]:
                        add_exemption(comp_doc.component_type, deduction.amount)

        existing_declaration = frappe.get_list(
            "Employee Tax Exemption Declaration",
            filters={
                "employee": self.employee,
                "payroll_period": self.custom_payroll_period,
                "docstatus": ["in", [0, 1]],
            },
            fields=["name"],
        )

        if existing_declaration:
            return

        new_declaration = frappe.get_doc(
            {
                "doctype": "Employee Tax Exemption Declaration",
                "employee": self.employee,
                "company": self.company,
                "payroll_period": self.custom_payroll_period,
                "currency": self.currency,
                "custom_income_tax": self.income_tax_slab,
                "custom_salary_structure_assignment": self.name,
                "custom_posting_date": self.from_date,
            }
        )

        for category in sub_categories:
            new_declaration.append(
                "declarations",
                {
                    "exemption_sub_category": category["sub_category"],
                    "max_amount": category["max_amount"],
                    "amount": category["amount"],
                },
            )

        new_declaration.insert()
        new_declaration.submit()
        frappe.db.commit()
        # frappe.msgprint("Tax Exemption declaration is created")

    def set_variable_pay_amount(self):
        for row in self.custom_other_extra_payments:
            if row.additional_earning == "Variable Pay" and getattr(
                row, "rating", None
            ):
                payroll_setting = frappe.get_doc("Payroll Settings")

                if getattr(payroll_setting, "custom_varible_pay_config", None):
                    for config in payroll_setting.custom_varible_pay_config:
                        if getattr(config, "rating", None) == getattr(
                            row, "rating", None
                        ):
                            amount = flt(row.amount)
                            percentage = flt(config.percentage)

                            self.custom_variable_pay_amount = (
                                amount * percentage
                            ) / 100

                            break

    def insert_joining_bonus(self):
        company = frappe.get_doc("Company", self.company)

        if not company.custom_joining_bonus:
            return

        joining_bonus_component = company.custom_joining_bonus

        # Check Joining Bonus in child table
        joining_bonus_row = None
        for row in self.custom_other_extra_payments or []:
            if row.additional_earning == "Joining Bonus":
                joining_bonus_row = row
                break

        # Check existing Additional Salary
        additional_salary = frappe.get_list(
            "Additional Salary",
            filters={
                "employee": self.employee,
                "salary_component": joining_bonus_component,
                "docstatus": ["!=", 2],
            },
            fields=["name", "amount"],
            limit=1,
        )

        # --------------------------------------------------
        # Case 1: Child table has Joining Bonus → Create/Update
        # --------------------------------------------------
        if joining_bonus_row:
            amount = flt(joining_bonus_row.amount)

            if additional_salary:
                add_sal_doc = frappe.get_doc(
                    "Additional Salary", additional_salary[0].name
                )

                # Update if amount mismatch
                if flt(add_sal_doc.amount) != amount:
                    add_sal_doc.amount = amount
                    add_sal_doc.save()

            else:
                last_day = get_last_day(getdate(self.from_date))
                next_year_day = getdate(self.from_date) + relativedelta(years=1)

                doc = frappe.get_doc(
                    {
                        "doctype": "Additional Salary",
                        "employee": self.employee,
                        "salary_component": joining_bonus_component,
                        "payroll_date": last_day,
                        "company": self.company,
                        "currency": frappe.db.get_value(
                            "Company", self.company, "default_currency"
                        ),
                        "amount": amount,
                        "custom_clawback_date": next_year_day,
                    }
                )

                doc.insert()
                doc.submit()

        # --------------------------------------------------
        # Case 2: No Joining Bonus in child table → Delete Additional Salary
        # --------------------------------------------------
        else:
            if additional_salary:
                add_sal_doc = frappe.get_doc(
                    "Additional Salary", additional_salary[0].name
                )

                if add_sal_doc.docstatus == 1:
                    add_sal_doc.cancel()

                add_sal_doc.delete()
