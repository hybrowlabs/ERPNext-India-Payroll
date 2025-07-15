

import frappe
from frappe import _


def validate(self, method):
    validate_days(self)
    insert_breakup_table(self)


def on_submit(self, method):
    insert_additional_salary(self)
    reimbursement_accrual_update(self)
    bonus_accrual_update(self)


def reimbursement_accrual_update(self):
    lop_reversal = frappe.get_all(
        "Employee Benefit Accrual",
        filters={
            "employee": self.employee,
            "docstatus": 1,
            "salary_slip": self.salary_slip,
        },
        fields=["*"],
    )

    for record in lop_reversal:
        each_doc = frappe.get_doc("Employee Benefit Accrual", record.name)
        lop_reversal_amount = (
            each_doc.amount / each_doc.payment_days
        ) * self.number_of_days
        eligible_amount = each_doc.amount + lop_reversal_amount
        each_doc.amount = round(eligible_amount)
        each_doc.save()


def bonus_accrual_update(self):
    lop_reversal_bonus = frappe.get_all(
        "Employee Bonus Accrual",
        filters={
            "employee": self.employee,
            "docstatus": 1,
            "salary_slip": self.salary_slip,
        },
        fields=["*"],
    )

    for bonus in lop_reversal_bonus:
        each_doc_bonus = frappe.get_doc("Employee Bonus Accrual", bonus.name)
        lop_reversal_amount_bonus = (
            each_doc_bonus.amount / each_doc_bonus.payment_day
        ) * self.number_of_days

        eligible_amount_bonus = each_doc_bonus.amount + lop_reversal_amount_bonus
        each_doc_bonus.amount = round(eligible_amount_bonus)
        each_doc_bonus.save()


def validate_days(self):
    if self.number_of_days and self.salary_slip:
        salary_slip = frappe.get_doc("Salary Slip", self.salary_slip)
        self.working_days = salary_slip.total_working_days
        self.absent_days = salary_slip.absent_days or 0
        self.lwp_days = salary_slip.leave_without_pay or 0
        self.total_lwp_applied = self.absent_days + self.lwp_days

        payroll_corrections = frappe.get_all(
            "LOP Reversal",
            filters={
                "docstatus": 1,
                "payroll_period": self.payroll_period,
                "salary_slip": self.salary_slip,
                "employee": self.employee,
            },
            fields=["number_of_days"],
        )

        total_days_reversed = (
            sum(entry["number_of_days"] for entry in payroll_corrections) or 0
        )
        if total_days_reversed + self.number_of_days > self.total_lwp_applied:
            frappe.throw(
                _(
                    "You cannot reverse more than the total LWP days {0}. You have already reversed {1} days for this employee."
                ).format(self.total_lwp_applied, total_days_reversed)
            )


def insert_breakup_table(self):
    salary_slip = frappe.get_doc("Salary Slip", self.salary_slip)
    if not salary_slip:
        frappe.throw(_("Salary Slip not found."))

    self.set("arrear_breakup", [])
    self.set("arrear_deduction_breakup", [])

    total_working_days = max(salary_slip.total_working_days, 1)
    for section, fieldname in [
        ("earnings", "arrear_breakup"),
        ("deductions", "arrear_deduction_breakup"),
    ]:
        for item in getattr(salary_slip, section, []):
            components = frappe.get_all(
                "Salary Component",
                filters={
                    "custom_is_arrear": 1,
                    "custom_component": item.salary_component,
                    "disabled": 0,
                    "type": "Earning" if section == "earnings" else "Deduction",
                },
                fields=["name"],
            )

            if not components:
                continue

            one_day_amount = (item.default_amount or 0) / total_working_days
            arrear_amount = round(one_day_amount * self.number_of_days)

            for component in components:
                self.append(
                    fieldname,
                    {"salary_component": component.name, "amount": arrear_amount},
                )


def insert_additional_salary(self):
    for comp in (self.arrear_breakup or []) + (self.arrear_deduction_breakup or []):
        get_currency=frappe.get_doc("Company",self.company)
        currency=get_currency.default_currency
        additional_salary = frappe.get_doc(
            {
                "doctype": "Additional Salary",
                "employee": self.employee,
                "company": self.company,
                "payroll_date": self.additional_salary_date,
                "salary_component": comp.salary_component,
                "currency": currency,
                "amount": comp.amount,
                "currency":currency,
                "ref_doctype": "LOP Reversal",
                "ref_docname": self.name,
            }
        )
        additional_salary.insert()
        additional_salary.submit()


def on_cancel(self, method):
    additional_arrears = frappe.get_all(
        "Additional Salary", filters={"ref_docname": self.name}, fields=["name"]
    )

    for arrear in additional_arrears:
        frappe.delete_doc("Additional Salary", arrear.get("name"))

    benefit_accruals = frappe.get_all(
        "Employee Benefit Accrual",
        filters={
            "employee": self.employee,
            "docstatus": 1,
            "salary_slip": self.salary_slip,
        },
        fields=["name"],
    )

    for accrual in benefit_accruals:
        accrual_doc = frappe.get_doc("Employee Benefit Accrual", accrual.name)
        total_payment_day = (accrual_doc.payment_days or 0) + self.number_of_days
        if total_payment_day > 0:
            lop_reversal_amount = (
                accrual_doc.amount / total_payment_day
            ) * self.number_of_days
            eligible_amount = accrual_doc.amount - lop_reversal_amount
            accrual_doc.amount = round(eligible_amount)
            accrual_doc.save()

    bonus_accruals = frappe.get_all(
        "Employee Bonus Accrual",
        filters={
            "employee": self.employee,
            "docstatus": 1,
            "salary_slip": self.salary_slip,
        },
        fields=["name"],
    )

    for bonus in bonus_accruals:
        bonus_doc = frappe.get_doc("Employee Bonus Accrual", bonus.name)
        total_payment_day = (bonus_doc.payment_day or 0) + self.number_of_days
        if total_payment_day > 0:
            reversal_amount = (
                bonus_doc.amount / total_payment_day
            ) * self.number_of_days
            eligible_amount = bonus_doc.amount - reversal_amount
            bonus_doc.amount = round(eligible_amount)
            bonus_doc.save()
