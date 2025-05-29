# import frappe


# def before_save(self, method):
#     insert_breakup_table(self)


# def on_submit(self, method):
#     if len(self.arrear_breakup) > 0:
#         for i in self.arrear_breakup:
#             additional_doc = frappe.get_doc(
#                 {
#                     "doctype": "Additional Salary",
#                     "employee": self.employee,
#                     "company": self.company,
#                     "payroll_date": self.additional_salary_date,
#                     "custom_payroll_entry": self.payroll_entry,
#                     "salary_component": i.salary_component,
#                     "currency": "INR",
#                     "amount": i.amount,
#                     "docstatus": 1,
#                     "custom_lop_reversal": self.name,
#                     "custom_lop_reversal_days": self.number_of_days,
#                 }
#             )
#             additional_doc.insert()

#     if len(self.arrear_deduction_breakup) > 0:
#         for j in self.arrear_deduction_breakup:
#             additional_doc = frappe.get_doc(
#                 {
#                     "doctype": "Additional Salary",
#                     "employee": self.employee,
#                     "company": self.company,
#                     "payroll_date": self.additional_salary_date,
#                     "salary_component": j.salary_component,
#                     "custom_payroll_entry": self.payroll_entry,
#                     "currency": "INR",
#                     "amount": j.amount,
#                     "docstatus": 1,
#                     "custom_lop_reversal": self.name,
#                     "custom_lop_reversal_days": self.number_of_days,
#                 }
#             )

#             additional_doc.insert()

#     reimbursement_accrual_update(self)
#     bonus_accrual_update(self)


# def reimbursement_accrual_update(self):
#     lop_reversal = frappe.get_list(
#         "Employee Benefit Accrual",
#         filters={
#             "employee": self.employee,
#             "docstatus": 1,
#             "salary_slip": self.salary_slip,
#         },
#         fields=["*"],
#     )

#     if len(lop_reversal) > 0:
#         for i in lop_reversal:
#             each_doc = frappe.get_doc("Employee Benefit Accrual", i.name)
#             lop_reversal_amount = (
#                 each_doc.amount / self.working_days
#             ) * self.number_of_days
#             eligible_amount = each_doc.amount + lop_reversal_amount

#             each_doc.amount = round(eligible_amount)
#             each_doc.save()


# def bonus_accrual_update(self):
#     lop_reversal_bonus = frappe.get_list(
#         "Employee Bonus Accrual",
#         filters={
#             "employee": self.employee,
#             "docstatus": 1,
#             "salary_slip": self.salary_slip,
#         },
#         fields=["name", "amount"],
#     )

#     if lop_reversal_bonus:
#         for bonus in lop_reversal_bonus:
#             each_doc_bonus = frappe.get_doc("Employee Bonus Accrual", bonus.name)
#             lop_reversal_amount_bonus = (
#                 each_doc_bonus.amount / self.working_days
#             ) * self.number_of_days
#             eligible_amount_bonus = each_doc_bonus.amount + lop_reversal_amount_bonus
#             each_doc_bonus.amount = round(eligible_amount_bonus)
#             each_doc_bonus.save()


# def insert_breakup_table(self):
#     if self.number_of_days and self.salary_slip:
#         breakup_component_earning = []
#         breakup_component_deduction = []

#         # Fetch the salary slip
#         get_salary_slip = frappe.get_list(
#             "Salary Slip",
#             filters={
#                 "employee": self.employee,
#                 "docstatus": 1,
#                 "name": self.salary_slip,
#             },
#             fields=["*"],
#         )

#         if get_salary_slip:
#             each_ss_doc = frappe.get_doc("Salary Slip", get_salary_slip[0].name)

#             # Process earnings components
#             for earning_component in each_ss_doc.earnings:
#                 get_salary_component = frappe.get_list(
#                     "Salary Component",
#                     filters={
#                         "custom_is_arrear": 1,
#                         "custom_component": earning_component.salary_component,
#                     },
#                     fields=["*"],
#                 )

#                 for t in get_salary_component:
#                     earning_amount = (
#                         earning_component.amount / self.working_days
#                     ) * self.number_of_days
#                     breakup_component_earning.append(
#                         {"salary_component": t.name, "amount": earning_amount}
#                     )

#             # Process deduction components
#             for deduction_component in each_ss_doc.deductions:
#                 get_deduction_salary_component = frappe.get_list(
#                     "Salary Component",
#                     filters={
#                         "custom_is_arrear": 1,
#                         "custom_component": deduction_component.salary_component,
#                     },
#                     fields=["*"],
#                 )

#                 for k in get_deduction_salary_component:
#                     deduction_amount = (
#                         deduction_component.amount / self.working_days
#                     ) * self.number_of_days
#                     breakup_component_deduction.append(
#                         {"salary_component": k.name, "amount": deduction_amount}
#                     )

#             # Append earnings components to arrear_breakup
#             self.arrear_breakup = []
#             for item in breakup_component_earning:
#                 self.append(
#                     "arrear_breakup",
#                     {
#                         "salary_component": item["salary_component"],
#                         "amount": item["amount"],
#                     },
#                 )

#             # Append deduction components to arrear_deduction_breakup
#             self.arrear_deduction_breakup = []
#             for item in breakup_component_deduction:
#                 self.append(
#                     "arrear_deduction_breakup",
#                     {
#                         "salary_component": item["salary_component"],
#                         "amount": item["amount"],
#                     },
#                 )

#     if self.number_of_days:
#         breakup_component_earning = []
#         breakup_component_deduction = []

#         # Fetch the salary slip
#         get_salary_slip = frappe.get_list(
#             "Salary Slip",
#             filters={
#                 "employee": self.employee,
#                 "docstatus": 1,
#                 "custom_month": self.lop_month_reversal,
#             },
#             fields=["*"],
#         )

#         if get_salary_slip:
#             each_ss_doc = frappe.get_doc("Salary Slip", get_salary_slip[0].name)

#             # Process earnings components
#             for earning_component in each_ss_doc.earnings:
#                 get_salary_component = frappe.get_list(
#                     "Salary Component",
#                     filters={
#                         "custom_is_arrear": 1,
#                         "custom_component": earning_component.salary_component,
#                     },
#                     fields=["*"],
#                 )

#                 for t in get_salary_component:
#                     earning_amount = (
#                         earning_component.amount / each_ss_doc.payment_days
#                     ) * self.number_of_days
#                     breakup_component_earning.append(
#                         {"salary_component": t.name, "amount": earning_amount}
#                     )

#             # Process deduction components
#             for deduction_component in each_ss_doc.deductions:
#                 get_deduction_salary_component = frappe.get_list(
#                     "Salary Component",
#                     filters={
#                         "custom_is_arrear": 1,
#                         "custom_component": deduction_component.salary_component,
#                     },
#                     fields=["*"],
#                 )

#                 for k in get_deduction_salary_component:
#                     deduction_amount = (
#                         deduction_component.amount / each_ss_doc.payment_days
#                     ) * self.number_of_days
#                     breakup_component_deduction.append(
#                         {"salary_component": k.name, "amount": deduction_amount}
#                     )

#             # Append earnings components to arrear_breakup
#             self.arrear_breakup = []
#             for item in breakup_component_earning:
#                 self.append(
#                     "arrear_breakup",
#                     {
#                         "salary_component": item["salary_component"],
#                         "amount": item["amount"],
#                     },
#                 )

#             # Append deduction components to arrear_deduction_breakup
#             self.arrear_deduction_breakup = []
#             for item in breakup_component_deduction:
#                 self.append(
#                     "arrear_deduction_breakup",
#                     {
#                         "salary_component": item["salary_component"],
#                         "amount": item["amount"],
#                     },
#                 )


# def on_cancel(self, method):
#     get_additional_arrears = frappe.db.get_list(
#         "Additional Salary",
#         filters={"custom_lop_reversal": self.name},
#         fields=["*"],
#     )

#     if len(get_additional_arrears) > 0:
#         for j in get_additional_arrears:
#             arrear_doc = frappe.get_doc("Additional Salary", j.name)
#             arrear_doc.docstatus = 2

#             arrear_doc.save()

#             frappe.delete_doc("Additional Salary", j.name)

#     lop_reversal = frappe.get_list(
#         "Employee Benefit Accrual",
#         filters={
#             "employee": self.employee,
#             "docstatus": 1,
#             "salary_slip": self.salary_slip,
#         },
#         fields=["*"],
#     )

#     if len(lop_reversal) > 0:
#         for i in lop_reversal:
#             each_doc = frappe.get_doc("Employee Benefit Accrual", i.name)
#             total_days = self.working_days + self.number_of_days
#             lop_reversal_amount = each_doc.amount / total_days
#             eligible_amount = lop_reversal_amount * self.working_days

#             each_doc.amount = round(eligible_amount)
#             each_doc.save()

#     lop_reversal_bonus = frappe.get_list(
#         "Employee Bonus Accrual",
#         filters={
#             "employee": self.employee,
#             "docstatus": 1,
#             "salary_slip": self.salary_slip,
#         },
#         fields=["name", "amount"],
#     )

#     if lop_reversal_bonus:
#         for bonus in lop_reversal_bonus:
#             each_doc_bonus = frappe.get_doc("Employee Bonus Accrual", bonus.name)
#             total_days = self.working_days + self.number_of_days
#             lop_reversal_amount = each_doc_bonus.amount / total_days
#             eligible_amount = lop_reversal_amount * self.working_days

#             each_doc_bonus.amount = round(eligible_amount)
#             each_doc_bonus.save()


# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

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
        additional_salary = frappe.get_doc(
            {
                "doctype": "Additional Salary",
                "employee": self.employee,
                "company": self.company,
                "payroll_date": self.additional_salary_date,
                "salary_component": comp.salary_component,
                "currency": self.currency,
                "amount": comp.amount,
                "ref_doctype": "LOP Reversal",
                "ref_docname": self.name,
            }
        )
        additional_salary.insert()
        additional_salary.submit()


def on_cancel(self, method):
    # Delete associated Additional Salary records linked by ref_docname
    additional_arrears = frappe.get_all(
        "Additional Salary", filters={"ref_docname": self.name}, fields=["name"]
    )

    for arrear in additional_arrears:
        frappe.delete_doc("Additional Salary", arrear.get("name"))

    # Adjust Employee Benefit Accrual entries using get_doc
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

    # Adjust Employee Bonus Accrual entries using get_doc
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
