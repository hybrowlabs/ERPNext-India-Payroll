import frappe
import datetime
from frappe.query_builder.functions import Count, Sum
import json
from frappe.utils import flt
from frappe.query_builder import Order
from frappe import _
import math

from collections import defaultdict
from dateutil.relativedelta import relativedelta


from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip
from frappe.utils import (
    add_days,
    ceil,
    cint,
    cstr,
    date_diff,
    floor,
    flt,
    formatdate,
    get_first_day,
    get_link_to_form,
    getdate,
    money_in_words,
    rounded,
)
from datetime import datetime

from frappe.utils import flt
from hrms.payroll.doctype.salary_slip.salary_slip import eval_tax_slab_condition
from hrms.payroll.doctype.payroll_period.payroll_period import get_period_factor
from datetime import datetime, timedelta


class CustomSalarySlip(SalarySlip):
    # def before_update_after_submit(self):
    # self.tax_calculation()

    def on_submit(self):
        super().on_submit()
        self.insert_bonus_accruals()
        self.employee_accrual_insert()
        self.update_benefit_claim_amount()

    def validate(self):
        super().validate()
        self.set_sub_period()
        self.apply_lop_amount_in_reimbursement_component()

        self.custom_previous_taxable_earnings = (
            self.previous_taxable_earnings_before_exemption
            if self.previous_taxable_earnings_before_exemption
            else 0
        )

        # Set current taxable earnings
        self.custom_current_taxable_earnings = (
            self.current_structured_taxable_earnings_before_exemption
            if self.current_structured_taxable_earnings_before_exemption
            else 0
        )

        # Set future taxable earnings
        self.custom_future_taxable_earnings = (
            self.future_structured_taxable_earnings_before_exemption
            if self.future_structured_taxable_earnings_before_exemption
            else 0
        )

        # Calculate annual taxable earnings
        self.custom_annual_taxable_earnings = (
            self.ctc - self.non_taxable_earnings if self.ctc else 0
        )

        # Calculate total taxable earnings from CTC
        self.custom_ctc_taxable_earnings = 0
        if self.earnings:
            total_ctc_taxable_amount = 0
            for earning in self.earnings:
                if earning.is_tax_applicable == 1:
                    total_ctc_taxable_amount += earning.default_amount or 0
            self.custom_ctc_taxable_earnings = total_ctc_taxable_amount

        # self.insert_other_perquisites()

    def before_save(self):
        self.new_joinee()
        self.insert_lop_days()
        self.set_taxale()
        self.actual_amount_ctc()
        self.set_month()
        self.update_declaration_component()
        self.update_total_lop()
        self.arrear_ytd()
        self.food_coupon()
        self.tax_calculation()

        self.calculate_grosspay()

    def on_cancel(self):
        super().on_cancel()
        self.delete_bonus_accruals()
        self.delete_benefit_accruals()

    def set_sub_period(self):
        sub_period = get_period_factor(
            self.employee,
            self.start_date,
            self.end_date,
            self.payroll_frequency,
            self.payroll_period,
            joining_date=self.joining_date,
            relieving_date=self.relieving_date,
        )[1]

        self.custom_month_count = sub_period - 1

    def update_benefit_claim_amount(self):
        if not self.earnings:
            return

        for earning in self.earnings:
            additional_salary_name = earning.get("additional_salary")
            if not additional_salary_name:
                continue

            # Fetch the Additional Salary document safely
            additional_salary = frappe.get_value(
                "Additional Salary",
                additional_salary_name,
                ["ref_doctype", "ref_docname"],
            )

            if not additional_salary:
                frappe.log_error(
                    f"Additional Salary '{additional_salary_name}' not found.",
                    "update_benefit_claim_amount",
                )
                continue

            ref_doctype, ref_docname = additional_salary

            # Check if it's linked to an Employee Benefit Claim
            if ref_doctype == "Employee Benefit Claim" and ref_docname:
                try:
                    benefit_claim = frappe.get_doc(
                        "Employee Benefit Claim", ref_docname
                    )
                    benefit_claim.custom_is_paid = 1
                    benefit_claim.custom_paid_amount = earning.amount
                    benefit_claim.save(ignore_permissions=True)
                except frappe.DoesNotExistError:
                    frappe.log_error(
                        f"Employee Benefit Claim '{ref_docname}' not found.",
                        "update_benefit_claim_amount",
                    )

    def get_working_days_details(
        self, lwp=None, for_preview=0, lwp_days_corrected=None
    ):
        actual_lwp = 0
        absent = 0
        payroll_settings = frappe.get_cached_value(
            "Payroll Settings",
            None,
            (
                "payroll_based_on",
                "include_holidays_in_total_working_days",
                "consider_marked_attendance_on_holidays",
                "daily_wages_fraction_for_half_day",
                "consider_unmarked_attendance_as",
                "custom_configure_attendance_cycle",
            ),
            as_dict=1,
        )

        consider_marked_attendance_on_holidays = (
            payroll_settings.include_holidays_in_total_working_days
            and payroll_settings.consider_marked_attendance_on_holidays
        )

        daily_wages_fraction_for_half_day = (
            flt(payroll_settings.daily_wages_fraction_for_half_day) or 0.5
        )

        working_days = date_diff(self.end_date, self.start_date) + 1
        if for_preview:
            self.total_working_days = working_days
            self.payment_days = working_days
            return

        holidays = self.get_holidays_for_employee(self.start_date, self.end_date)
        working_days_list = [
            add_days(getdate(self.start_date), days=day)
            for day in range(0, working_days)
        ]

        if not cint(payroll_settings.include_holidays_in_total_working_days):
            working_days_list = [i for i in working_days_list if i not in holidays]

            working_days -= len(holidays)
            if working_days < 0:
                frappe.throw(_("There are more holidays than working days this month."))

        if not payroll_settings.payroll_based_on:
            frappe.throw(_("Please set Payroll based on in Payroll settings"))

        if payroll_settings.payroll_based_on == "Attendance":
            if payroll_settings.custom_configure_attendance_cycle:
                (
                    actual_lwp,
                    absent,
                ) = self.calculate_lwp_ppl_and_absent_days_based_on_attendance_cycle(
                    holidays,
                    daily_wages_fraction_for_half_day,
                    consider_marked_attendance_on_holidays,
                )
                self.absent_days = absent
            else:
                (
                    actual_lwp,
                    absent,
                ) = self.calculate_lwp_ppl_and_absent_days_based_on_attendance(
                    holidays,
                    daily_wages_fraction_for_half_day,
                    consider_marked_attendance_on_holidays,
                )
                self.absent_days = absent

        if payroll_settings.payroll_based_on == "Leave":
            if payroll_settings.custom_configure_attendance_cycle:
                actual_lwp = 0
            else:
                actual_lwp = self.calculate_lwp_or_ppl_based_on_leave_application(
                    holidays, working_days_list, daily_wages_fraction_for_half_day
                )

        if not lwp:
            lwp = actual_lwp
        elif lwp != actual_lwp:
            frappe.msgprint(
                _("Leave Without Pay does not match with approved {} records").format(
                    payroll_settings.payroll_based_on
                )
            )

        self.leave_without_pay = lwp
        self.total_working_days = working_days

        payment_days = self.get_payment_days(
            payroll_settings.include_holidays_in_total_working_days
        )

        if flt(payment_days) > flt(lwp):
            self.payment_days = flt(payment_days) - flt(lwp)

            if payroll_settings.payroll_based_on == "Attendance":
                self.payment_days -= flt(absent)

            consider_unmarked_attendance_as = (
                payroll_settings.consider_unmarked_attendance_as or "Present"
            )

            if payroll_settings.payroll_based_on == "Attendance":
                if consider_unmarked_attendance_as == "Absent":
                    unmarked_days = self.get_unmarked_days(
                        payroll_settings.include_holidays_in_total_working_days,
                        holidays,
                    )
                    self.absent_days += unmarked_days  # will be treated as absent
                    self.payment_days -= unmarked_days
                half_absent_days = self.get_half_absent_days(
                    consider_marked_attendance_on_holidays,
                    holidays,
                )
                self.absent_days += half_absent_days * daily_wages_fraction_for_half_day
                self.payment_days -= (
                    half_absent_days * daily_wages_fraction_for_half_day
                )
        else:
            self.payment_days = 0

        if lwp_days_corrected and lwp_days_corrected > 0:
            if verify_lwp_days_corrected(
                self.employee, self.start_date, self.end_date, lwp_days_corrected
            ):
                self.payment_days += lwp_days_corrected

    def calculate_lwp_ppl_and_absent_days_based_on_attendance_cycle(
        self,
        holidays,
        daily_wages_fraction_for_half_day,
        consider_marked_attendance_on_holidays,
    ):
        lwp = 0
        absent = 0

        payroll_setting = frappe.get_doc("Payroll Settings")
        if (
            payroll_setting.payroll_based_on == "Attendance"
            and payroll_setting.custom_configure_attendance_cycle
        ):
            attendance_start_day = payroll_setting.custom_attendance_start_date
            attendance_end_day = payroll_setting.custom_attendance_end_date
            start_date = getdate(self.start_date)
            end_date = getdate(self.end_date)
            attendance_end_date = end_date.replace(day=attendance_end_day)
            attendance_start_date = (
                attendance_end_date - relativedelta(months=1)
            ).replace(day=attendance_start_day)

            leave_type_map = self.get_leave_type_map()
            attendance_details = self.get_employee_attendance(
                start_date=attendance_start_date, end_date=attendance_end_date
            )

            for d in attendance_details:
                if (
                    d.status in ("Half Day", "On Leave")
                    and d.leave_type
                    and d.leave_type not in leave_type_map.keys()
                ):
                    continue

                if (
                    not consider_marked_attendance_on_holidays
                    and getdate(d.attendance_date) in holidays
                ):
                    if d.status in ["Absent", "Half Day"] or (
                        d.leave_type
                        and d.leave_type in leave_type_map.keys()
                        and not leave_type_map[d.leave_type]["include_holiday"]
                    ):
                        continue

                if d.leave_type:
                    fraction_of_daily_salary_per_leave = leave_type_map[d.leave_type][
                        "fraction_of_daily_salary_per_leave"
                    ]

                if (
                    d.status == "Half Day"
                    and d.leave_type
                    and d.leave_type in leave_type_map.keys()
                ):
                    equivalent_lwp = 1 - daily_wages_fraction_for_half_day

                    if leave_type_map[d.leave_type]["is_ppl"]:
                        equivalent_lwp *= (
                            fraction_of_daily_salary_per_leave
                            if fraction_of_daily_salary_per_leave
                            else 1
                        )
                    lwp += equivalent_lwp

                elif (
                    d.status == "On Leave"
                    and d.leave_type
                    and d.leave_type in leave_type_map.keys()
                ):
                    equivalent_lwp = 1
                    if leave_type_map[d.leave_type]["is_ppl"]:
                        equivalent_lwp *= (
                            fraction_of_daily_salary_per_leave
                            if fraction_of_daily_salary_per_leave
                            else 1
                        )
                    lwp += equivalent_lwp

                elif d.status == "Absent":
                    absent += 1

        return lwp, absent

    def apply_lop_amount_in_reimbursement_component(self):
        if not self.custom_salary_structure_assignment:
            frappe.throw("Salary Structure Assignment not linked.")

        ssa_doc = frappe.get_doc(
            "Salary Structure Assignment", self.custom_salary_structure_assignment
        )

        if not self.earnings:
            return

        if not self.salary_withholding:
            for earning in self.earnings:
                component = frappe.get_doc("Salary Component", earning.salary_component)

                # Step 1: Standard reimbursement-based LOP adjustment
                for reimbursement in ssa_doc.custom_employee_reimbursements or []:
                    if reimbursement.reimbursements == earning.salary_component:
                        if self.total_working_days and self.payment_days:
                            prorated_amount = round(
                                (reimbursement.monthly_total_amount or 0)
                                / self.total_working_days
                                * (self.total_working_days - self.payment_days),
                                2,
                            )

                            earning.amount -= prorated_amount

                # Step 2: Handle special case for LTA reimbursement → apply to taxable/non-taxable LTA
                for reimbursement in ssa_doc.custom_employee_reimbursements or []:
                    lta_component = frappe.get_doc(
                        "Salary Component", reimbursement.reimbursements
                    )
                    if lta_component.component_type == "LTA Reimbursement":
                        if component.component_type in [
                            "LTA Taxable",
                            "LTA Non Taxable",
                        ]:
                            if self.total_working_days and self.payment_days:
                                prorated_amount = round(
                                    (reimbursement.monthly_total_amount or 0)
                                    / self.total_working_days
                                    * (self.total_working_days - self.payment_days),
                                    2,
                                )
                                earning.amount -= prorated_amount
                        break

    def compute_income_tax_breakup(self):
        self.standard_tax_exemption_amount = 0
        self.tax_exemption_declaration = 0
        self.deductions_before_tax_calculation = 0
        self.custom_perquisite_amount = 0

        self.non_taxable_earnings = self.compute_non_taxable_earnings()
        self.ctc = self.compute_ctc()
        self.income_from_other_sources = self.get_income_form_other_sources()
        self.total_earnings = self.ctc + self.income_from_other_sources

        # Fetch payroll period once
        payroll_period = frappe.get_value(
            "Payroll Period",
            {"company": self.company, "name": self.payroll_period.name},
            ["name", "start_date", "end_date"],
            as_dict=True,
        )

        # If payroll period is not found, return without further processing
        if not payroll_period:
            return

        # If payroll period is found, process further
        start_date = frappe.utils.getdate(payroll_period["start_date"])
        end_date = frappe.utils.getdate(payroll_period["end_date"])
        fiscal_year = payroll_period["name"]

        # Calculate loan perquisites within the fiscal year
        loan_repayments = frappe.get_list(
            "Loan Repayment Schedule",
            filters={
                "custom_employee": self.employee,
                "status": "Active",
                "docstatus": 1,
            },
            fields=["name"],
        )

        total_perq = 0
        for repayment in loan_repayments:
            repayment_doc = frappe.get_doc("Loan Repayment Schedule", repayment.name)
            for entry in repayment_doc.custom_loan_perquisite:
                if (
                    entry.payment_date
                    and start_date
                    <= frappe.utils.getdate(entry.payment_date)
                    <= end_date
                ):
                    total_perq += entry.perquisite_amount
        self.custom_perquisite_amount = total_perq

        # Tax slab logic
        if hasattr(self, "tax_slab") and self.tax_slab:
            if self.tax_slab.allow_tax_exemption:
                self.standard_tax_exemption_amount = (
                    self.tax_slab.standard_tax_exemption_amount
                )
                self.deductions_before_tax_calculation = (
                    self.compute_annual_deductions_before_tax_calculation()
                )

            self.tax_exemption_declaration = (
                self.get_total_exemption_amount() - self.standard_tax_exemption_amount
            )

        # Final Taxable Income Calculation
        self.annual_taxable_amount = (
            self.total_earnings
            + self.custom_perquisite_amount
            - (
                self.non_taxable_earnings
                + self.deductions_before_tax_calculation
                + self.tax_exemption_declaration
                + self.standard_tax_exemption_amount
            )
        )

        self.income_tax_deducted_till_date = self.get_income_tax_deducted_till_date()

        if hasattr(self, "total_structured_tax_amount") and hasattr(
            self, "current_structured_tax_amount"
        ):
            self.future_income_tax_deductions = (
                self.total_structured_tax_amount
                + self.get("full_tax_on_additional_earnings", 0)
                - self.income_tax_deducted_till_date
            )

            self.current_month_income_tax = (
                self.current_structured_tax_amount
                + self.get("full_tax_on_additional_earnings", 0)
            )

            self.total_income_tax = (
                self.income_tax_deducted_till_date + self.future_income_tax_deductions
            )

    def check_sal_struct(self):
        ss = frappe.qb.DocType("Salary Structure")
        ssa = frappe.qb.DocType("Salary Structure Assignment")

        query = (
            frappe.qb.from_(ssa)
            .join(ss)
            .on(ssa.salary_structure == ss.name)
            .select(
                ssa.salary_structure,
                ssa.custom_payroll_period,
                ssa.name,
                ssa.income_tax_slab,
                ssa.custom_tax_regime,
                ssa.custom_state,
                ssa.base,
            )
            .where(
                (ssa.docstatus == 1)
                & (ss.docstatus == 1)
                & (ss.is_active == "Yes")
                & (ssa.employee == self.employee)
                & (
                    (ssa.from_date <= self.start_date)
                    | (ssa.from_date <= self.end_date)
                    | (ssa.from_date <= self.joining_date)
                )
            )
            .orderby(ssa.from_date, order=Order.desc)
            .limit(1)
        )

        if not self.salary_slip_based_on_timesheet and self.payroll_frequency:
            query = query.where(ss.payroll_frequency == self.payroll_frequency)

        st_name = query.run()

        if st_name:
            self.salary_structure = st_name[0][0]
            self.custom_payroll_period = st_name[0][1]
            self.custom_salary_structure_assignment = st_name[0][2]
            self.custom_income_tax_slab = st_name[0][3]
            self.custom_tax_regime = st_name[0][4]
            self.custom_employee_state = st_name[0][5]
            self.custom_annual_ctc = st_name[0][6]

            return self.salary_structure

        else:
            self.salary_structure = None
            frappe.msgprint(
                _(
                    "No active or default Salary Structure found for employee {0} for the given dates"
                ).format(self.employee),
                title=_("Salary Structure Missing"),
            )

    def delete_bonus_accruals(self):
        bonus_accruals = frappe.get_list(
            "Employee Bonus Accrual",
            filters={
                "salary_slip": self.name,
                "payroll_entry": self.payroll_entry,
                "payroll_period": self.custom_payroll_period,
            },
            fields=["name"],
        )

        if bonus_accruals:
            for accrual in bonus_accruals:
                bonus_doc = frappe.get_doc("Employee Bonus Accrual", accrual.name)
                bonus_doc.delete()

    def delete_benefit_accruals(self):
        benefit_accruals = frappe.get_list(
            "Employee Benefit Accrual",
            filters={
                "salary_slip": self.name,
                "payroll_entry": self.payroll_entry,
                "payroll_period": self.custom_payroll_period,
            },
            fields=["name"],
        )
        if benefit_accruals:
            for accrual in benefit_accruals:
                benefit_doc = frappe.get_doc("Employee Benefit Accrual", accrual.name)
                benefit_doc.delete()

    def employee_accrual_insert(self):
        if self.custom_salary_structure_assignment:
            child_doc = frappe.get_doc(
                "Salary Structure Assignment", self.custom_salary_structure_assignment
            )
            if child_doc.custom_employee_reimbursements:
                for i in child_doc.custom_employee_reimbursements:
                    accrual_insert = frappe.get_doc(
                        {
                            "doctype": "Employee Benefit Accrual",
                            "employee": self.employee,
                            "payroll_entry": self.payroll_entry,
                            "amount": round(
                                (i.monthly_total_amount / self.total_working_days)
                                * self.payment_days
                            ),
                            "salary_component": i.reimbursements,
                            "benefit_accrual_date": self.posting_date,
                            "salary_slip": self.name,
                            "payroll_period": child_doc.custom_payroll_period,
                        }
                    )
                    accrual_insert.insert()
                    accrual_insert.submit()

    def insert_bonus_accruals(self):
        for bonus in self.earnings:
            bonus_component = frappe.get_doc("Salary Component", bonus.salary_component)

            if bonus_component.custom_is_accrual == 1:
                existing_accruals = frappe.get_list(
                    "Employee Bonus Accrual",
                    filters={
                        "salary_slip": self.name,
                        "salary_component": bonus_component.name,
                        "payroll_entry": self.payroll_entry,
                        "payroll_period": self.custom_payroll_period,
                    },
                    limit=1,
                )

                if not existing_accruals:
                    accrual_doc = frappe.new_doc("Employee Bonus Accrual")
                    accrual_doc.amount = bonus.amount
                    accrual_doc.employee = self.employee
                    accrual_doc.accrual_date = self.posting_date
                    accrual_doc.salary_structure = self.salary_structure
                    accrual_doc.salary_structure_assignment = (
                        self.custom_salary_structure_assignment
                    )
                    accrual_doc.salary_component = bonus.salary_component
                    accrual_doc.payroll_entry = self.payroll_entry
                    accrual_doc.salary_slip = self.name
                    accrual_doc.payroll_period = self.custom_payroll_period

                    accrual_doc.insert()
                    accrual_doc.submit()

    def calculate_variable_tax(self, tax_component):
        employee_request_additional_tds = 0

        declaration = frappe.db.get_value(
            "Employee Tax Exemption Declaration",
            {
                "employee": self.employee,
                "payroll_period": self.payroll_period.name,
                "docstatus": 1,
            },
            "custom_employee_request_additional_tds",
            as_dict=True,
            cache=True,
        )
        if declaration:
            employee_request_additional_tds = (
                declaration.custom_employee_request_additional_tds or 0.0
            )

        self.previous_total_paid_taxes = self.get_tax_paid_in_period(
            self.payroll_period.start_date, self.start_date, tax_component
        )

        eval_locals, default_data = self.get_data_for_eval()
        self.total_structured_tax_amount, __ = override_calculate_tax_by_tax_slab(
            self,
            self.total_taxable_earnings_without_full_tax_addl_components,
            self.tax_slab,
            self.whitelisted_globals,
            eval_locals,
        )

        self.current_structured_tax_amount = (
            (self.total_structured_tax_amount - self.previous_total_paid_taxes)
            / self.remaining_sub_periods
        ) + employee_request_additional_tds

        self.full_tax_on_additional_earnings = 0.0
        if self.current_additional_earnings_with_full_tax:
            self.total_tax_amount, __ = override_calculate_tax_by_tax_slab(
                self,
                self.total_taxable_earnings,
                self.tax_slab,
                self.whitelisted_globals,
                eval_locals,
            )
            self.full_tax_on_additional_earnings = (
                self.total_tax_amount - self.total_structured_tax_amount
            )

        current_tax_amount = (
            self.current_structured_tax_amount + self.full_tax_on_additional_earnings
        )
        if flt(current_tax_amount) < 0:
            current_tax_amount = 0

        self._component_based_variable_tax[tax_component].update(
            {
                "previous_total_paid_taxes": self.previous_total_paid_taxes,
                "total_structured_tax_amount": self.total_structured_tax_amount,
                "current_structured_tax_amount": self.current_structured_tax_amount,
                "full_tax_on_additional_earnings": self.full_tax_on_additional_earnings,
                "current_tax_amount": current_tax_amount,
            }
        )

        return current_tax_amount

    def insert_other_perquisites(self):
        latest_salary_structure = frappe.get_list(
            "Salary Structure Assignment",
            filters={
                "employee": self.employee,
                "docstatus": 1,
                "from_date": ["<=", self.end_date],
            },
            fields=["name"],
            order_by="from_date desc",
            limit=1,
        )

        if latest_salary_structure:
            salary_structure_doc = frappe.get_doc(
                "Salary Structure Assignment", latest_salary_structure[0].name
            )

            existing_components = [
                earning.salary_component for earning in self.earnings
            ]

            for perquisite in salary_structure_doc.custom_other_perquisites:
                get_tax = frappe.get_doc("Salary Component", perquisite.title)

                if (
                    get_tax.is_tax_applicable == 1
                    and get_tax.custom_tax_exemption_applicable_based_on_regime == 1
                ):
                    if get_tax.custom_regime == "All":
                        is_tax_applicable = get_tax.is_tax_applicable
                        custom_regime = get_tax.custom_regime
                        custom_tax_exemption_applicable_based_on_regime = (
                            get_tax.custom_tax_exemption_applicable_based_on_regime
                        )

                    elif get_tax.custom_regime == tax_component:
                        is_tax_applicable = get_tax.is_tax_applicable
                        custom_regime = get_tax.custom_regime
                        custom_tax_exemption_applicable_based_on_regime = (
                            get_tax.custom_tax_exemption_applicable_based_on_regime
                        )
                    elif get_tax.custom_regime != tax_component:
                        is_tax_applicable = 0
                        custom_regime = get_tax.custom_regime
                        custom_tax_exemption_applicable_based_on_regime = (
                            get_tax.custom_tax_exemption_applicable_based_on_regime
                        )

                elif (
                    get_tax.is_tax_applicable == 0
                    and get_tax.custom_tax_exemption_applicable_based_on_regime == 0
                ):
                    is_tax_applicable = 0
                    custom_regime = get_tax.custom_regime
                    custom_tax_exemption_applicable_based_on_regime = (
                        get_tax.custom_tax_exemption_applicable_based_on_regime
                    )
                elif (
                    get_tax.is_tax_applicable == 1
                    and get_tax.custom_tax_exemption_applicable_based_on_regime == 0
                ):
                    is_tax_applicable = 1
                    custom_regime = get_tax.custom_regime
                    custom_tax_exemption_applicable_based_on_regime = (
                        get_tax.custom_tax_exemption_applicable_based_on_regime
                    )

                if perquisite.title not in existing_components:
                    self.append(
                        "earnings",
                        {
                            "salary_component": perquisite.title,
                            "amount": perquisite.amount,
                            "is_tax_applicable": is_tax_applicable,
                            "custom_regime": custom_regime,
                            "custom_tax_exemption_applicable_based_on_regime": custom_tax_exemption_applicable_based_on_regime,
                        },
                    )

    def update_total_lop(self):
        self.custom_total_leave_without_pay = (
            self.absent_days or 0
        ) + self.leave_without_pay

    def get_taxable_earnings(self, allow_tax_exemption=False, based_on_payment_days=0):
        taxable_earnings = 0
        additional_income = 0
        additional_income_with_full_tax = 0
        flexi_benefits = 0
        amount_exempted_from_income_tax = 0

        tax_component = None

        latest_salary_structure = frappe.get_list(
            "Salary Structure Assignment",
            filters={
                "employee": self.employee,
                "docstatus": 1,
                "from_date": ["<=", self.end_date],
            },
            fields=["*"],
            order_by="from_date desc",
            limit=1,
        )

        if len(latest_salary_structure) > 0:
            tax_component = latest_salary_structure[0].custom_tax_regime

        for earning in self.earnings:
            get_tax = frappe.get_doc("Salary Component", earning.salary_component)

            if (
                get_tax.is_tax_applicable == 1
                and get_tax.custom_tax_exemption_applicable_based_on_regime == 1
            ):
                if get_tax.custom_regime == "All":
                    earning.is_tax_applicable = get_tax.is_tax_applicable
                    earning.custom_regime = get_tax.custom_regime
                    earning.custom_tax_exemption_applicable_based_on_regime = (
                        get_tax.custom_tax_exemption_applicable_based_on_regime
                    )

                elif get_tax.custom_regime == tax_component:
                    earning.is_tax_applicable = get_tax.is_tax_applicable
                    earning.custom_regime = get_tax.custom_regime
                    earning.custom_tax_exemption_applicable_based_on_regime = (
                        get_tax.custom_tax_exemption_applicable_based_on_regime
                    )
                elif get_tax.custom_regime != tax_component:
                    earning.is_tax_applicable = 0
                    earning.custom_regime = get_tax.custom_regime
                    earning.custom_tax_exemption_applicable_based_on_regime = (
                        get_tax.custom_tax_exemption_applicable_based_on_regime
                    )

            elif (
                get_tax.is_tax_applicable == 0
                and get_tax.custom_tax_exemption_applicable_based_on_regime == 0
            ):
                earning.is_tax_applicable = 0
                earning.custom_regime = get_tax.custom_regime
                earning.custom_tax_exemption_applicable_based_on_regime = (
                    get_tax.custom_tax_exemption_applicable_based_on_regime
                )
            elif (
                get_tax.is_tax_applicable == 1
                and get_tax.custom_tax_exemption_applicable_based_on_regime == 0
            ):
                earning.is_tax_applicable = 1
                earning.custom_regime = get_tax.custom_regime
                earning.custom_tax_exemption_applicable_based_on_regime = (
                    get_tax.custom_tax_exemption_applicable_based_on_regime
                )

            if based_on_payment_days:
                amount, additional_amount = self.get_amount_based_on_payment_days(
                    earning
                )
            else:
                if earning.additional_amount:
                    amount, additional_amount = (
                        earning.amount,
                        earning.additional_amount,
                    )
                else:
                    amount, additional_amount = (
                        earning.default_amount,
                        earning.additional_amount,
                    )
            # condition for current tax  component
            if earning.is_tax_applicable:
                if earning.is_flexible_benefit:
                    flexi_benefits += amount
                else:
                    taxable_earnings += amount - additional_amount
                    additional_income += additional_amount

                    # Get additional amount based on future recurring additional salary
                    if additional_amount and earning.is_recurring_additional_salary:
                        additional_income += self.get_future_recurring_additional_amount(
                            earning.additional_salary, earning.additional_amount
                        )  # Used earning.additional_amount to consider the amount for the full month

                    if earning.deduct_full_tax_on_selected_payroll_date:
                        additional_income_with_full_tax += additional_amount

        if allow_tax_exemption:
            for ded in self.deductions:
                if ded.exempted_from_income_tax:
                    amount, additional_amount = ded.amount, ded.additional_amount
                    if based_on_payment_days:
                        (
                            amount,
                            additional_amount,
                        ) = self.get_amount_based_on_payment_days(ded)

                    taxable_earnings -= flt(amount - additional_amount)
                    additional_income -= additional_amount
                    amount_exempted_from_income_tax = flt(amount - additional_amount)

                    if additional_amount and ded.is_recurring_additional_salary:
                        additional_income -= self.get_future_recurring_additional_amount(
                            ded.additional_salary, ded.additional_amount
                        )  # Used ded.additional_amount to consider the amount for the full month

        return frappe._dict(
            {
                "taxable_earnings": taxable_earnings,
                "additional_income": additional_income,
                "amount_exempted_from_income_tax": amount_exempted_from_income_tax,
                "additional_income_with_full_tax": additional_income_with_full_tax,
                "flexi_benefits": flexi_benefits,
            }
        )

    def get_taxable_earnings_for_prev_period(
        self, start_date, end_date, allow_tax_exemption=False
    ):
        exempted_amount = 0
        taxable_earnings = 0

        latest_salary_structure = frappe.get_list(
            "Salary Structure Assignment",
            filters={"employee": self.employee, "docstatus": 1},
            fields=["custom_tax_regime"],
            order_by="from_date desc",
            limit=1,
        )

        custom_tax_regime = latest_salary_structure[0].custom_tax_regime

        # Check if any earnings are assigned with the current regime
        regime_matched = any(
            earning.custom_regime == custom_tax_regime or earning.custom_regime == "All"
            for earning in self.earnings
        )

        # Build the filters
        if regime_matched:
            # Get both matching regime and "All"
            taxable_earnings = self.get_salary_slip_details(
                start_date,
                end_date,
                parentfield="earnings",
                is_tax_applicable=1,
                custom_tax_exemption_applicable_based_on_regime=1,
                custom_regime=custom_tax_regime,  # match specific regime
            ) + self.get_salary_slip_details(
                start_date,
                end_date,
                parentfield="earnings",
                is_tax_applicable=1,
                custom_tax_exemption_applicable_based_on_regime=1,
                custom_regime="All",  # include "All"
            )
        else:
            # Use only regime "All"
            taxable_earnings = self.get_salary_slip_details(
                start_date,
                end_date,
                parentfield="earnings",
                is_tax_applicable=1,
                custom_regime="All",
            )

        # latest_salary_structure = frappe.get_list(
        #     "Salary Structure Assignment",
        #     filters={"employee": self.employee, "docstatus": 1},
        #     fields=["*"],
        #     order_by="from_date desc",
        #     limit=1,
        # )

        # custom_tax_regime = latest_salary_structure[0].custom_tax_regime

        # for earning in self.earnings:
        #     if custom_tax_regime == earning.custom_regime:

        #         taxable_earnings = self.get_salary_slip_details(
        #             start_date,
        #             end_date,
        #             parentfield="earnings",
        #             is_tax_applicable=1,
        #             custom_tax_exemption_applicable_based_on_regime=1,
        #         )

        #         print("\n\n\n\n\n\n\n\n\n\n==================",taxable_earnings, "\n\n\n\n\n\n\n\n\n\n")
        #     # else:
        #     #     print("\n\n\n\n\n\n\n\n\n\n+++++++++++++++++",taxable_earnings, "\n\n\n\n\n\n\n\n\n\n")
        #     #     taxable_earnings = self.get_salary_slip_details(
        #     #         start_date,
        #     #         end_date,
        #     #         parentfield="earnings",
        #     #         is_tax_applicable=1,
        #     #         custom_regime="All",
        #     #     )

        # print("\n\n\n\n\n\n\n\n\n\ntaxable earning",taxable_earnings, "\n\n\n\n\n\n\n\n\n\n")

        # Check if tax exemption is allowed and get exempted amount
        if allow_tax_exemption:
            exempted_amount = self.get_salary_slip_details(
                start_date,
                end_date,
                parentfield="deductions",
                exempted_from_income_tax=1,
            )

        # Get opening taxable earnings for the period
        opening_taxable_earning = self.get_opening_for(
            "taxable_earnings_till_date", start_date, end_date
        )

        # Calculate and return the final taxable earnings
        return (
            taxable_earnings + opening_taxable_earning
        ) - exempted_amount, exempted_amount

    def get_salary_slip_details(
        self,
        start_date,
        end_date,
        parentfield,
        salary_component=None,
        is_tax_applicable=None,
        is_flexible_benefit=0,
        exempted_from_income_tax=0,
        variable_based_on_taxable_salary=0,
        field_to_select="amount",
        custom_tax_exemption_applicable_based_on_regime=None,
        custom_regime=None,
        custom_taxable=None,
        custom_tax_regime=None,
    ):
        ss = frappe.qb.DocType("Salary Slip")
        sd = frappe.qb.DocType("Salary Detail")

        # Select the field based on the input
        if field_to_select == "amount":
            field = sd.amount
        else:
            field = sd.additional_amount

        # Build the base query
        query = (
            frappe.qb.from_(ss)
            .join(sd)
            .on(sd.parent == ss.name)
            .select(Sum(field))
            .where(sd.parentfield == parentfield)
            .where(sd.is_flexible_benefit == is_flexible_benefit)
            .where(ss.docstatus == 1)
            .where(ss.employee == self.employee)
            .where(ss.start_date.between(start_date, end_date))
            .where(ss.end_date.between(start_date, end_date))
        )

        # Add conditions if they are provided
        if is_tax_applicable is not None:
            query = query.where(sd.is_tax_applicable == is_tax_applicable)

        if exempted_from_income_tax:
            query = query.where(sd.exempted_from_income_tax == exempted_from_income_tax)

        if variable_based_on_taxable_salary:
            query = query.where(
                sd.variable_based_on_taxable_salary == variable_based_on_taxable_salary
            )

        if salary_component:
            query = query.where(sd.salary_component == salary_component)

        if custom_tax_exemption_applicable_based_on_regime:
            query = query.where(
                sd.custom_tax_exemption_applicable_based_on_regime
                == custom_tax_exemption_applicable_based_on_regime
            )

        if custom_regime:
            query = query.where(sd.custom_regime == custom_regime)

        if custom_taxable:
            query = query.where(sd.custom_taxable == custom_taxable)

        if custom_tax_regime:
            query = query.where(ss.custom_tax_regime == custom_tax_regime)

        # Run the query and return the result
        result = query.run()

        return flt(result[0][0]) if result else 0.0

    def food_coupon(self):
        past_salary_slips = frappe.db.get_list(
            "Salary Slip",
            filters={
                "employee": self.employee,
                "custom_payroll_period": self.custom_payroll_period,
                "docstatus": 1,
            },
            fields=["name"],
        )

        food_coupon_array = []

        for slip in past_salary_slips:
            slip_doc = frappe.get_doc("Salary Slip", slip.name)
            for earning in slip_doc.earnings:
                if (
                    earning.is_tax_applicable == 0
                    and earning.custom_regime == "New Regime"
                ):
                    food_coupon_array.append(earning.amount)

        total_food_coupon_ytd = sum(food_coupon_array)

        for earning in self.earnings:
            if earning.is_tax_applicable == 1 and earning.custom_regime == "New Regime":
                earning.custom_total_ytd = total_food_coupon_ytd

    def arrear_ytd(self):
        arrear_slips = frappe.db.get_list(
            "Salary Slip",
            filters={
                "employee": self.employee,
                "custom_payroll_period": self.custom_payroll_period,
                "docstatus": 1,
                "name": ("!=", self.name),
            },
            fields=["name"],
        )

        if not arrear_slips:
            return

        # Store YTD arrears component-wise
        arrear_ytd_sum = defaultdict(float)

        for slip in arrear_slips:
            doc = frappe.get_doc("Salary Slip", slip.name)

            for section in ["earnings", "deductions"]:
                for row in doc.get(section):
                    component_doc = frappe.get_doc(
                        "Salary Component", row.salary_component
                    )

                    if component_doc.custom_component:
                        arrear_ytd_sum[component_doc.custom_component] += row.amount

        # Update current slip's earnings and deductions with YTD arrear value
        for row in self.earnings:
            if row.salary_component in arrear_ytd_sum:
                row.custom_arrear_ytd = arrear_ytd_sum[row.salary_component]

        for row in self.deductions:
            if row.salary_component in arrear_ytd_sum:
                row.custom_arrear_ytd = arrear_ytd_sum[row.salary_component]

    def new_joinee(self):
        if self.employee:
            employee_doc = frappe.get_doc("Employee", self.employee)

            start_date = frappe.utils.getdate(self.start_date)
            end_date = frappe.utils.getdate(self.end_date)

            if start_date <= employee_doc.date_of_joining <= end_date:
                self.custom_new_joinee = "New Joinee"
            else:
                self.custom_new_joinee = "-"

    def add_reimbursement_taxable_new_doc(self):
        if len(self.earnings) > 0:
            for lta_component in self.earnings:
                get_lta = frappe.get_doc(
                    "Salary Component", lta_component.salary_component
                )
                if get_lta.component_type == "LTA Taxable":
                    if self.annual_taxable_amount:
                        self.annual_taxable_amount = (
                            self.annual_taxable_amount + lta_component.amount
                        )

    def update_declaration_component(self):
        if not self.employee:
            return

        current_basic = current_hra = None

        current_basic_value = (
            current_hra_value
        ) = current_nps_value = current_epf_value = current_pt_value = 0
        previous_basic_value = (
            previous_hra_value
        ) = previous_nps_value = previous_epf_value = previous_pt_value = 0
        future_basic_value = (
            future_hra_value
        ) = future_nps_value = future_epf_value = future_pt_value = 0

        get_company = frappe.get_doc("Company", self.company)
        if get_company.basic_component:
            current_basic = get_company.basic_component
        if get_company.hra_component:
            current_hra = get_company.hra_component

        if self.earnings:
            for earning in self.earnings:
                component_data = frappe.get_doc(
                    "Salary Component", earning.salary_component
                )
                if component_data.component_type == "NPS":
                    current_nps_value += earning.amount or 0
                    if component_data.custom_is_arrear == 0:
                        future_nps_value = (
                            earning.custom_actual_amount or 0
                        ) * self.custom_month_count

                if earning.salary_component == current_basic:
                    current_basic_value += earning.amount
                    if component_data.custom_is_arrear == 0:
                        future_basic_value = (earning.custom_actual_amount) * (
                            self.custom_month_count
                        )
                if earning.salary_component == current_hra:
                    current_hra_value += earning.amount
                    if component_data.custom_is_arrear == 0:
                        future_hra_value = (earning.custom_actual_amount) * (
                            self.custom_month_count
                        )

        if self.deductions:
            for deduction in self.deductions:
                component_data = frappe.get_doc(
                    "Salary Component", deduction.salary_component
                )
                if component_data.component_type == "EPF":
                    current_epf_value += deduction.amount
                    if component_data.custom_is_arrear == 0:
                        future_epf_value = (deduction.custom_actual_amount) * (
                            self.custom_month_count
                        )
                if component_data.component_type == "Professional Tax":
                    current_pt_value += deduction.amount

                    if component_data.custom_is_arrear == 0:
                        future_pt_value = (deduction.custom_actual_amount) * (
                            self.custom_month_count
                        )
        get_previous_salary_slip = frappe.get_list(
            "Salary Slip",
            filters={
                "employee": self.employee,
                "custom_payroll_period": self.custom_payroll_period,
                "docstatus": 1,
                "name": ["!=", self.name],
            },
            fields=["name", "custom_payroll_period"],
        )
        if get_previous_salary_slip:
            for slip in get_previous_salary_slip:
                previous_salary_slip = frappe.get_doc("Salary Slip", slip.name)
                if previous_salary_slip.earnings:
                    for earning in previous_salary_slip.earnings:
                        component_data = frappe.get_doc(
                            "Salary Component", earning.salary_component
                        )
                        if component_data.component_type == "NPS":
                            previous_nps_value += earning.amount
                        if earning.salary_component == current_basic:
                            previous_basic_value += earning.amount
                        if earning.salary_component == current_hra:
                            previous_hra_value += earning.amount

                if previous_salary_slip.deductions:
                    for deduction in previous_salary_slip.deductions:
                        component_data = frappe.get_doc(
                            "Salary Component", deduction.salary_component
                        )
                        if component_data.component_type == "EPF":
                            previous_epf_value += deduction.amount
                        if component_data.component_type == "Professional Tax":
                            previous_pt_value += deduction.amount

        if self.custom_tax_regime == "Old Regime":
            declaration = frappe.get_list(
                "Employee Tax Exemption Declaration",
                filters={
                    "employee": self.employee,
                    "payroll_period": self.custom_payroll_period,
                    "docstatus": 1,
                    "company": self.company,
                },
                fields=["*"],
            )
            if declaration:
                form_data = json.loads(
                    declaration[0].custom_declaration_form_data or "{}"
                )
                get_each_doc = frappe.get_doc(
                    "Employee Tax Exemption Declaration", declaration[0].name
                )

                form_data["nineNumber"] = round(
                    previous_nps_value + future_nps_value + current_nps_value
                )
                form_data["pfValue"] = min(
                    round(previous_epf_value + future_epf_value + current_epf_value),
                    150000,
                )
                form_data["nineteenNumber"] = round(
                    previous_pt_value + future_pt_value + current_pt_value
                )

                get_each_doc.custom_posting_date = self.posting_date
                get_each_doc.custom_declaration_form_data = json.dumps(form_data)

                if get_each_doc.monthly_house_rent > 0:
                    ss_assignment = frappe.get_list(
                        "Salary Structure Assignment",
                        filters={
                            "employee": self.employee,
                            "docstatus": 1,
                            "company": self.company,
                            "custom_payroll_period": self.custom_payroll_period,
                        },
                        fields=[
                            "name",
                            "from_date",
                            "custom_payroll_period",
                            "salary_structure",
                        ],
                        order_by="from_date desc",
                    )

                    if ss_assignment:
                        first_assignment = next(iter(ss_assignment))
                        first_assignment_date = first_assignment.get("from_date")
                        first_assignment_structure = first_assignment.get(
                            "salary_structure"
                        )

                        start_date = ss_assignment[-1].from_date
                        if ss_assignment[-1].custom_payroll_period:
                            payroll_period = frappe.get_doc(
                                "Payroll Period",
                                ss_assignment[-1].custom_payroll_period,
                            )
                            end_date = payroll_period.end_date
                            month_count = (
                                (end_date.year - start_date.year) * 12
                                + end_date.month
                                - start_date.month
                                + 1
                            )

                            percentage = (
                                (
                                    previous_basic_value
                                    + future_basic_value
                                    + current_basic_value
                                )
                                * 10
                                / 100
                            )
                            get_each_doc.custom_check = 1
                            get_each_doc.custom_basic_as_per_salary_structure = round(
                                percentage
                            )
                            get_each_doc.salary_structure_hra = round(
                                previous_hra_value
                                + future_hra_value
                                + current_hra_value
                            )
                            get_each_doc.custom_basic = round(
                                previous_basic_value
                                + future_basic_value
                                + current_basic_value
                            )

                            total_basic_amount = round(
                                previous_basic_value
                                + future_basic_value
                                + current_basic_value
                            )
                            total_hra_amount = round(
                                previous_hra_value
                                + future_hra_value
                                + current_hra_value
                            )

                            annual_hra_amount = (
                                get_each_doc.monthly_house_rent * month_count
                            )

                            basic_rule2 = round(annual_hra_amount - percentage)

                            if get_each_doc.rented_in_metro_city == 0:
                                non_metro_or_metro = (total_basic_amount * 40) / 100
                            elif get_each_doc.rented_in_metro_city == 1:
                                non_metro_or_metro = (total_basic_amount * 50) / 100

                            # HRA Exemption rule
                            final_hra_exemption = round(
                                min(basic_rule2, annual_hra_amount, non_metro_or_metro)
                            )

                            get_each_doc.annual_hra_exemption = round(
                                final_hra_exemption
                            )
                            get_each_doc.monthly_hra_exemption = round(
                                final_hra_exemption / month_count
                            )

                            months = []
                            current_date = start_date

                            while current_date <= end_date:
                                month_name = current_date.strftime("%B")
                                if month_name not in months:
                                    months.append(month_name)
                                current_date = (
                                    current_date.replace(day=28) + timedelta(days=4)
                                ).replace(day=1)

                            earned_basic = 0
                            if get_each_doc.rented_in_metro_city == 1:
                                earned_basic = (
                                    (
                                        get_each_doc.custom_basic_as_per_salary_structure
                                        * 10
                                    )
                                    * 50
                                    / 100
                                )
                            else:
                                earned_basic = (
                                    (
                                        get_each_doc.custom_basic_as_per_salary_structure
                                        * 10
                                    )
                                    * 40
                                    / 100
                                )

                            get_each_doc.custom_hra_breakup = []
                            for i in range(len(months)):
                                get_each_doc.append(
                                    "custom_hra_breakup",
                                    {
                                        "month": months[i],
                                        "rent_paid": round(annual_hra_amount),
                                        "hra_received": round(total_hra_amount),
                                        "earned_basic": round(earned_basic),
                                        "excess_of_rent_paid": round(basic_rule2),
                                        "exemption_amount": final_hra_exemption,
                                    },
                                )
                get_each_doc.workflow_state = "Approved"

                get_each_doc.save()
                frappe.db.commit()
                self.tax_exemption_declaration = get_each_doc.total_exemption_amount

        if self.custom_tax_regime == "New Regime":
            declaration = frappe.get_list(
                "Employee Tax Exemption Declaration",
                filters={
                    "employee": self.employee,
                    "payroll_period": self.custom_payroll_period,
                    "docstatus": 1,
                    "company": self.company,
                },
                fields=["*"],
            )
            if declaration:
                form_data = json.loads(
                    declaration[0].custom_declaration_form_data or "{}"
                )
                get_each_doc = frappe.get_doc(
                    "Employee Tax Exemption Declaration", declaration[0].name
                )

                form_data["nineNumber"] = round(
                    previous_nps_value + future_nps_value + current_nps_value
                )

                get_each_doc.custom_posting_date = self.posting_date
                get_each_doc.custom_declaration_form_data = json.dumps(form_data)
                get_each_doc.workflow_state = "Approved"

                get_each_doc.save()
                frappe.db.commit()
                self.tax_exemption_declaration = get_each_doc.total_exemption_amount

    def update_nps(self):
        if self.earnings:
            update_component_array = []
            if self.custom_tax_regime == "Old Regime":
                # Process earnings
                for earning in self.earnings:
                    components = frappe.get_list(
                        "Employee Tax Exemption Sub Category",
                        filters={"custom_salary_component": earning.salary_component},
                        fields=["*"],
                    )
                    if components:
                        for component in components:
                            update_component_array.append(
                                {
                                    "component": component.name,
                                    "amount": earning.amount * 12,
                                }
                            )

                # Process deductions
                for deduction in self.deductions:
                    component_deductions = frappe.get_list(
                        "Employee Tax Exemption Sub Category",
                        filters={"custom_salary_component": deduction.salary_component},
                        fields=["*"],
                    )
                    if component_deductions:
                        for component_deduction in component_deductions:
                            if deduction.amount * 12 > 150000:
                                update_component_array.append(
                                    {
                                        "component": component_deduction.name,
                                        "amount": 150000,
                                    }
                                )

                            else:
                                update_component_array.append(
                                    {
                                        "component": component_deduction.name,
                                        "amount": deduction.amount * 12,
                                    }
                                )

            if self.custom_tax_regime == "New Regime":
                for earning in self.earnings:
                    components = frappe.get_list(
                        "Employee Tax Exemption Sub Category",
                        filters={"custom_salary_component": earning.salary_component},
                        fields=["*"],
                    )
                    if components:
                        for component in components:
                            update_component_array.append(
                                {
                                    "component": component.name,
                                    "amount": earning.amount * 12,
                                    "max_amount": earning.amount * 12,
                                }
                            )

            if update_component_array:
                declaration = frappe.get_list(
                    "Employee Tax Exemption Declaration",
                    filters={
                        "employee": self.employee,
                        "payroll_period": self.custom_payroll_period,
                        "docstatus": 1,
                    },
                    fields=["name"],
                )
                if declaration:
                    get_each_doc = frappe.get_doc(
                        "Employee Tax Exemption Declaration", declaration[0].name
                    )
                    for each_component in get_each_doc.declarations:
                        for ki in update_component_array:
                            if each_component.exemption_sub_category == ki["component"]:
                                each_component.amount = ki["amount"]
                                each_component.max_amount = ki["max_amount"]

                    get_each_doc.save()
                    frappe.db.commit()

    def tax_declartion_insert(self):
        tax_declaration_doc = frappe.db.get_list(
            "Employee Tax Exemption Declaration",
            filters={
                "employee": self.employee,
                "docstatus": 1,
                "payroll_period": self.custom_payroll_period,
            },
            fields=["*"],
        )
        if tax_declaration_doc:
            declaration_child_doc = frappe.get_doc(
                "Employee Tax Exemption Declaration", tax_declaration_doc[0].name
            )
            self.custom_declaration = []
            for k in declaration_child_doc.declarations:
                self.append(
                    "custom_declaration",
                    {
                        "exemption_sub_category": k.exemption_sub_category,
                        "exemption_category": k.exemption_category,
                        "maximum_exempted_amount": k.max_amount,
                        "declared_amount": k.amount,
                    },
                )

    def update_bonus_accrual(self):
        for bonus in self.earnings:
            bonus_component = frappe.get_doc("Salary Component", bonus.salary_component)
            if bonus_component.custom_is_accrual == 1:
                # frappe.msgprint(str(bonus_component.name))

                bonus_accrual = frappe.get_list(
                    "Employee Bonus Accrual",
                    filters={"salary_slip": self.name},
                    fields=["*"],
                )

                if len(bonus_accrual) > 0:
                    # frappe.msgprint(str(bonus_accrual[0].name))
                    accrual_each_doc = frappe.get_doc(
                        "Employee Bonus Accrual", bonus_accrual[0].name
                    )
                    accrual_each_doc.amount = bonus.amount
                    accrual_each_doc.save()

    def remaining_day(self):
        fiscal_year = frappe.get_list(
            "Payroll Period", fields=["*"], order_by="end_date desc", limit=1
        )

        if fiscal_year:
            t1 = fiscal_year[0].end_date
            t2 = self.end_date

            if not isinstance(t1, str):
                t1 = str(t1)
            if not isinstance(t2, str):
                t2 = str(t2)

            t1_parts = t1.split("-")
            t2_parts = t2.split("-")

            t1_year = int(t1_parts[0])
            t1_month = int(t1_parts[1])
            t1_day = int(t1_parts[2])

            t2_year = int(t2_parts[0])
            t2_month = int(t2_parts[1])
            t2_day = int(t2_parts[2])

            months_t2_to_t1 = (t1_year - t2_year) * 12 + (t1_month - t2_month)
            self.custom_month_count = months_t2_to_t1

    def set_month(self):
        date_str = str(self.start_date)

        month_str = date_str[5:7]

        month_number = int(month_str)

        month_names = [
            "",
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]

        month_name = month_names[month_number]

        self.custom_month = month_name

    def actual_amount(self):
        if self.leave_without_pay == 0:
            if len(self.earnings) > 0:
                for k in self.earnings:
                    k.custom_actual_amount = k.amount

    # def actual_amount_ctc(self):
    #     total_deduction = 0

    #     if self.earnings:
    #         for earning in self.earnings:
    #             if earning.depends_on_payment_days == 1:
    #                 if self.payment_days and self.payment_days > 0:
    #                     earning.custom_actual_amount = round(
    #                         (earning.amount * self.total_working_days)
    #                         / self.payment_days
    #                     )
    #                 else:
    #                     earning.custom_actual_amount = 0
    #             else:
    #                 earning.custom_actual_amount = earning.amount

    #     if self.deductions:
    #         for deduction in self.deductions:
    #             component_doc = frappe.get_doc(
    #                 "Salary Component", deduction.salary_component
    #             )
    #             original_amount = float(deduction.amount or 0)

    #             if deduction.depends_on_payment_days == 1:
    #                 if self.payment_days and self.payment_days > 0:
    #                     deduction.custom_actual_amount = round(
    #                         (original_amount * self.total_working_days)
    #                         / self.payment_days
    #                     )
    #                 else:
    #                     deduction.custom_actual_amount = 0

    #                 # ESIC → use ROUND UP
    #                 if component_doc.component_type == "ESIC":
    #                     deduction.amount = math.ceil(original_amount)
    #                 else:
    #                     deduction.amount = round(original_amount)

    #                 if not component_doc.do_not_include_in_total:

    #                     total_deduction += deduction.amount

    #             else:
    #                 deduction.custom_actual_amount = original_amount
    #                 if not component_doc.do_not_include_in_total:
    #                     total_deduction += deduction.amount or 0

    #     loan = self.total_loan_repayment or 0
    #     self.custom_total_deduction_amount = round(total_deduction + loan)

    def actual_amount_ctc(self):
        total_deduction = 0
        for earning in self.earnings or []:
            if earning.depends_on_payment_days == 1:
                if self.payment_days and self.payment_days > 0:
                    earning.custom_actual_amount = round(
                        (earning.amount * self.total_working_days) / self.payment_days
                    )
                else:
                    earning.custom_actual_amount = 0
            else:
                earning.custom_actual_amount = earning.amount

        for deduction in self.deductions or []:
            component_doc = frappe.get_doc(
                "Salary Component", deduction.salary_component
            )
            original_amount = flt(deduction.amount)

            if deduction.depends_on_payment_days == 1:
                if self.payment_days and self.payment_days > 0:
                    deduction.custom_actual_amount = round(
                        (original_amount * self.total_working_days) / self.payment_days
                    )
                else:
                    deduction.custom_actual_amount = 0
            else:
                deduction.custom_actual_amount = original_amount

            if component_doc.component_type == "ESIC":
                deduction.amount = math.ceil(original_amount)
            else:
                deduction.amount = round(original_amount)

            if not component_doc.do_not_include_in_total:
                total_deduction += deduction.amount

        loan = self.total_loan_repayment or 0

        self.custom_total_deduction_amount = round(total_deduction + loan)

    def accrual_update(self):
        if self.leave_without_pay > 0:
            ss_assignment = frappe.get_list(
                "Salary Structure Assignment",
                filters={"employee": self.employee, "docstatus": 1},
                fields=["name"],
                order_by="from_date desc",
                limit=1,
            )

            if ss_assignment:
                child_doc = frappe.get_doc(
                    "Salary Structure Assignment", ss_assignment[0].name
                )

                for i in child_doc.custom_employee_reimbursements:
                    get_benefit_accrual = frappe.db.get_list(
                        "Employee Benefit Accrual",
                        filters={
                            "salary_slip": self.name,
                            "salary_component": i.reimbursements,
                        },
                        fields=["name"],
                    )

                    if get_benefit_accrual:
                        amount = i.monthly_total_amount / self.total_working_days
                        eligible_amount = amount * self.payment_days

                        for j in get_benefit_accrual:
                            accrual_doc = frappe.get_doc(
                                "Employee Benefit Accrual", j.name
                            )
                            accrual_doc.amount = round(eligible_amount)
                            accrual_doc.save()

            if len(self.earnings) > 0:
                benefit_component = []
                component_amount_dict = {}

                benefit_component_demo = []

                benefit_application = frappe.get_list(
                    "Employee Benefit Claim",
                    filters={
                        "employee": self.employee,
                        "claim_date": ["between", [self.start_date, self.end_date]],
                        "docstatus": 1,
                    },
                    fields=["*"],
                )

                if benefit_application:
                    for k in benefit_application:
                        benefit_component.append(k.earning_component)

                        benefit_component_demo.append(
                            {
                                "component": k.earning_component,
                                "amount": k.claimed_amount,
                                "settlement": 0,
                            }
                        )

            if len(benefit_component) > 0:
                for component in benefit_component:
                    benefit_accrual = frappe.get_list(
                        "Employee Benefit Accrual",
                        filters={
                            "employee": self.employee,
                            # 'docstatus': 1,
                            "salary_component": component,
                        },
                        fields=["*"],
                    )

                    if benefit_accrual:
                        for j in benefit_accrual:
                            if j.salary_component in component_amount_dict:
                                component_amount_dict[j.salary_component][
                                    "amount"
                                ] += j.amount
                                component_amount_dict[j.salary_component][
                                    "settlement"
                                ] += j.total_settlement

                            else:
                                component_amount_dict[j.salary_component] = {
                                    "amount": j.amount,
                                    "settlement": j.total_settlement,
                                }

                            for demo in benefit_component_demo:
                                if demo["component"] == j.salary_component:
                                    demo["settlement"] += j.total_settlement
                                    demo["amount"] += j.total_settlement
            # frappe.msgprint(str(benefit_component_demo))

            benefit_component_amount1 = []
            for data in benefit_component_demo:
                total_amount = data["amount"] - data["settlement"]
                benefit_component_amount1.append(
                    {"component": data["component"], "total_amount": total_amount}
                )

            benefit_component_amount = []
            for component, data in component_amount_dict.items():
                total_amount = data["amount"] - data["settlement"]
                benefit_component_amount.append(
                    {"component": component, "total_amount": total_amount}
                )

            min_values = {}

            for item in benefit_component_amount1:
                component = item["component"]
                total_amount = item["total_amount"]
                min_values[component] = total_amount

            for item in benefit_component_amount:
                component = item["component"]
                total_amount = item["total_amount"]
                if component in min_values:
                    min_values[component] = min(min_values[component], total_amount)
                else:
                    min_values[component] = total_amount

            min_values_list = [
                {"component": component, "total_amount": total_amount}
                for component, total_amount in min_values.items()
            ]

            for component_data in min_values_list:
                for earnings in self.earnings:
                    if earnings.salary_component == component_data["component"]:
                        earnings.amount = component_data["total_amount"]

    # def compute_ctc(self):
    #     if hasattr(self, "previous_taxable_earnings"):
    #         return (
    #             self.previous_taxable_earnings_before_exemption
    #             + self.current_structured_taxable_earnings_before_exemption
    #             + self.future_structured_taxable_earnings_before_exemption
    #             + self.current_additional_earnings
    #             + self.other_incomes
    #             + self.unclaimed_taxable_benefits
    #             + self.non_taxable_earnings
    #         )
    #     return 0

    def insert_lop_days(self):
        """Calculate total LOP reversal + arrear present days and store in custom field."""
        import frappe

        # Always initialize first at top level
        total_lop_days = 0.0

        # --- LOP Reversal Days ---
        benefit_application_days = frappe.get_list(
            "LOP Reversal",
            filters={
                "employee": self.employee,
                "additional_salary_date": ["between", [self.start_date, self.end_date]],
                "docstatus": 1,
            },
            fields=["number_of_days"],
        )

        if benefit_application_days:
            total_lop_days += sum(
                float(d.get("number_of_days") or 0) for d in benefit_application_days
            )

        # --- Joining Salary Arrear (Present Days) ---
        arrear_days = frappe.get_list(
            "Joining Salary Arrear",
            filters={
                "employee": self.employee,
                "additional_salary_date": ["between", [self.start_date, self.end_date]],
                "docstatus": 1,
            },
            fields=["number_of_present_days"],
        )

        if arrear_days:
            total_lop_days += sum(
                float(d.get("number_of_present_days") or 0) for d in arrear_days
            )

        # --- Assign to custom field (always defined) ---
        self.custom_lop_reversal_days = total_lop_days

    def driver_reimbursement_lop(self):
        driver_reimbursement_component_lop = []
        driver_reimbursement_component_amount_lop = []

        driver_reimbursement_application = frappe.get_list(
            "Employee Benefit Claim",
            filters={
                "employee": self.employee,
                "claim_date": ["between", [self.start_date, self.end_date]],
                "docstatus": 1,
            },
            fields=["*"],
        )
        if driver_reimbursement_application:
            for k in driver_reimbursement_application:
                component_check = frappe.get_doc(
                    "Salary Component", k.earning_component
                )
                if (
                    component_check.component_type
                    == "Vehicle Maintenance Reimbursement"
                ):
                    driver_reimbursement_component_lop.append(k.earning_component)

                    ss_assignment_doc = frappe.get_list(
                        "Salary Structure Assignment",
                        filters={"employee": self.employee, "docstatus": 1},
                        fields=["name"],
                        order_by="from_date desc",
                        limit=1,
                    )

                    if ss_assignment_doc:
                        record = frappe.get_doc(
                            "Salary Structure Assignment", ss_assignment_doc[0].name
                        )
                        for i in record.custom_employee_reimbursements:
                            if (
                                i.reimbursements
                                == driver_reimbursement_component_lop[0]
                            ):
                                one_day_amount = round(
                                    (i.monthly_total_amount / self.total_working_days)
                                    * self.payment_days
                                )
                                monthly_reimbursement = round(
                                    i.monthly_total_amount - one_day_amount
                                )
                                total_amount = round(
                                    k.claimed_amount - monthly_reimbursement
                                )

                                driver_reimbursement_component_amount_lop.append(
                                    total_amount
                                )

        if len(driver_reimbursement_component_amount_lop) > 0:
            for earning in self.earnings:
                if earning.salary_component == driver_reimbursement_component_lop[0]:
                    earning.amount = driver_reimbursement_component_amount_lop[0]

    def driver_reimbursement(self):
        driver_reimbursement_component = []
        driver_reimbursement_component_amount = []

        driver_reimbursement_application = frappe.get_list(
            "Employee Benefit Claim",
            filters={
                "employee": self.employee,
                "claim_date": ["between", [self.start_date, self.end_date]],
                "docstatus": 1,
            },
            fields=["*"],
        )
        if driver_reimbursement_application:
            for k in driver_reimbursement_application:
                component_check = frappe.get_doc(
                    "Salary Component", k.earning_component
                )
                if (
                    component_check.component_type
                    == "Vehicle Maintenance Reimbursement"
                ):
                    driver_reimbursement_component.append(k.earning_component)
                    driver_reimbursement_component_amount.append(k.claimed_amount)

        existing_components = {earning.salary_component for earning in self.earnings}

        for i in range(len(driver_reimbursement_component)):
            if driver_reimbursement_component[i] not in existing_components:
                self.append(
                    "earnings",
                    {
                        "salary_component": driver_reimbursement_component[i],
                        "amount": driver_reimbursement_component_amount[i],
                    },
                )

    def insert_lta_reimbursement_lop(self):
        lta_tax_component = []
        lta_tax_amount = []

        lta_taxable = frappe.get_list(
            "Salary Component",
            filters={"component_type": "LTA Taxable"},
            fields=["name"],
        )
        if lta_taxable:
            lta_tax_component.append(lta_taxable[0].name)

        lta_non_taxable = frappe.get_list(
            "Salary Component",
            filters={"component_type": "LTA Non Taxable"},
            fields=["name"],
        )
        if lta_non_taxable:
            lta_tax_component.append(lta_non_taxable[0].name)

        lta_component = frappe.get_list(
            "Salary Component",
            filters={"component_type": "LTA Reimbursement"},
            fields=["name"],
        )
        if lta_component:
            reimbursement_component = lta_component[0].name

        lta_reimbursement = frappe.get_list(
            "LTA Claim",
            filters={
                "employee": self.employee,
                "docstatus": 1,
                "claim_date": ["between", [self.start_date, self.end_date]],
            },
            fields=["*"],
        )
        if lta_reimbursement:
            taxable_sum = 0
            non_taxable_sum = 0
            for lta in lta_reimbursement:
                if lta.income_tax_regime == "Old Regime":
                    taxable_sum = taxable_sum + lta.taxable_amount
                    non_taxable_sum = non_taxable_sum + lta.non_taxable_amount
                    # lta_tax_amount.append(taxable_sum)
                    # lta_tax_amount.append(non_taxable_sum)
                else:
                    taxable_sum = taxable_sum + lta.taxable_amount
                    # lta_tax_amount.append(taxable_sum)

            if taxable_sum > 0:
                ss_assignment = frappe.get_list(
                    "Salary Structure Assignment",
                    filters={"employee": self.employee, "docstatus": 1},
                    fields=["name"],
                    order_by="from_date desc",
                    limit=1,
                )

                if ss_assignment:
                    record = frappe.get_doc(
                        "Salary Structure Assignment", ss_assignment[0].name
                    )
                    for i in record.custom_employee_reimbursements:
                        if i.reimbursements == reimbursement_component:
                            if record.custom_tax_regime == "Old Regime":
                                one_day_amount = round(
                                    (i.monthly_total_amount / self.total_working_days)
                                    * self.payment_days
                                )
                                total_amount_taxable = round(
                                    taxable_sum - one_day_amount
                                )
                                total_amount_non_taxable = round(
                                    non_taxable_sum - one_day_amount
                                )
                                lta_tax_amount.append(total_amount_taxable)
                                lta_tax_amount.append(total_amount_non_taxable)
                            else:
                                one_day_amount = round(
                                    (i.monthly_total_amount / self.total_working_days)
                                    * self.payment_days
                                )
                                total_amount_taxable = round(
                                    taxable_sum - one_day_amount
                                )
                                lta_tax_amount.append(total_amount_taxable)

        if len(lta_tax_amount) > 0:
            for earning in self.earnings:
                # if earning.salary_component==lta_component[0].custom_lta_component:

                #     earning.amount=lta_tax_amount[0]
                if earning.salary_component == lta_tax_component[0]:
                    earning.amount = lta_tax_amount[0]

                if earning.salary_component == lta_tax_component[1]:
                    earning.amount = lta_tax_amount[1]

    def insert_lta_reimbursement(self):
        lta_tax_component = []
        lta_tax_amount = []

        lta_taxable = frappe.get_list(
            "Salary Component",
            filters={"component_type": "LTA Taxable"},
            fields=["name"],
        )
        if lta_taxable:
            lta_tax_component.append(lta_taxable[0].name)

        lta_non_taxable = frappe.get_list(
            "Salary Component",
            filters={"component_type": "LTA Non Taxable"},
            fields=["name"],
        )
        if lta_non_taxable:
            lta_tax_component.append(lta_non_taxable[0].name)

        lta_reimbursement = frappe.get_list(
            "LTA Claim",
            filters={
                "employee": self.employee,
                "docstatus": 1,
                "claim_date": ["between", [self.start_date, self.end_date]],
            },
            fields=["*"],
        )

        if lta_reimbursement:
            taxable_sum = 0
            non_taxable_sum = 0
            for lta in lta_reimbursement:
                if lta.income_tax_regime == "Old Regime":
                    taxable_sum = taxable_sum + lta.taxable_amount
                    non_taxable_sum = non_taxable_sum + lta.non_taxable_amount
                    lta_tax_amount.append(taxable_sum)
                    lta_tax_amount.append(non_taxable_sum)
                else:
                    taxable_sum = taxable_sum + lta.taxable_amount
                    lta_tax_amount.append(taxable_sum)

        existing_components = {earning.salary_component for earning in self.earnings}

        if len(lta_tax_amount) > 0:
            for i in range(len(lta_tax_amount)):
                if lta_tax_component[i] not in existing_components:
                    self.append(
                        "earnings",
                        {
                            "salary_component": lta_tax_component[i],
                            "amount": lta_tax_amount[i],
                        },
                    )

    def insert_loan_perquisite(self):
        if self.custom_payroll_period:
            get_payroll_period = frappe.get_list(
                "Payroll Period",
                filters={"company": self.company, "name": self.custom_payroll_period},
                fields=["*"],
            )

            if get_payroll_period:
                start_date = frappe.utils.getdate(get_payroll_period[0].start_date)
                end_date = frappe.utils.getdate(get_payroll_period[0].end_date)

                loan_repayments = frappe.get_list(
                    "Loan Repayment Schedule",
                    filters={
                        "custom_employee": self.employee,
                        "status": "Active",
                        "docstatus": 1,
                    },
                    fields=["*"],
                )
                if loan_repayments:
                    sum = 0
                    for repayment in loan_repayments:
                        get_each_perquisite = frappe.get_doc(
                            "Loan Repayment Schedule", repayment.name
                        )
                        if len(get_each_perquisite.custom_loan_perquisite) > 0:
                            for date in get_each_perquisite.custom_loan_perquisite:
                                payment_date = frappe.utils.getdate(date.payment_date)
                                if start_date <= payment_date <= end_date:
                                    sum = sum + date.perquisite_amount

                    self.custom_perquisite_amount = sum

    def loan_perquisite(self):
        loan_perquisite_component = frappe.get_value(
            "Salary Component",
            filters={"component_type": "Loan Perquisite"},
            fieldname="name",
        )

        if not loan_perquisite_component:
            return

        loan_repayments = frappe.get_list(
            "Loan Repayment Schedule",
            filters={
                "custom_employee": self.employee,
                "status": "Active",
                "docstatus": 1,
            },
            fields=["name"],
        )

        if not loan_repayments:
            return

        self.start_date = frappe.utils.getdate(self.start_date)
        self.end_date = frappe.utils.getdate(self.end_date)

        perquisite_amount_array = []
        for repayment in loan_repayments:
            loan_repayment_doc = frappe.get_doc(
                "Loan Repayment Schedule", repayment.name
            )
            for perquisite in loan_repayment_doc.custom_loan_perquisite:
                payment_date = frappe.utils.getdate(perquisite.payment_date)
                if self.start_date <= payment_date <= self.end_date:
                    perquisite_amount_array.append(perquisite.perquisite_amount)

        if perquisite_amount_array:
            existing_components = {
                earning.salary_component for earning in self.earnings
            }

            if loan_perquisite_component not in existing_components:
                self.append(
                    "earnings",
                    {
                        "salary_component": loan_perquisite_component,
                        "amount": sum(perquisite_amount_array),
                    },
                )

    def insert_reimbursement(self):
        if self.employee:
            benefit_component = []
            component_amount_dict = {}
            benefit_component_demo = []
            benefit_component_vehicle = []

            benefit_application = frappe.get_list(
                "Employee Benefit Claim",
                filters={
                    "employee": self.employee,
                    "claim_date": ["between", [self.start_date, self.end_date]],
                    "docstatus": 1,
                },
                fields=["*"],
            )
            if benefit_application:
                for k in benefit_application:
                    component_check = frappe.get_doc(
                        "Salary Component", k.earning_component
                    )
                    if (
                        component_check.component_type
                        != "Vehicle Maintenance Reimbursement"
                    ):
                        benefit_component.append(k.earning_component)
                        benefit_component_demo.append(
                            {
                                "component": k.earning_component,
                                "amount": k.claimed_amount,
                                "settlement": 0,
                            }
                        )
            # frappe.msgprint(str(benefit_component))
            # frappe.msgprint(str(benefit_component_demo))

            if len(benefit_component) > 0:
                for component in benefit_component:
                    benefit_accrual = frappe.get_list(
                        "Employee Benefit Accrual",
                        filters={
                            "employee": self.employee,
                            "docstatus": 1,
                            "salary_component": component,
                            "payroll_period": self.custom_payroll_period,
                        },
                        fields=["*"],
                    )

                    if benefit_accrual:
                        for j in benefit_accrual:
                            if j.salary_component in component_amount_dict:
                                component_amount_dict[j.salary_component][
                                    "amount"
                                ] += j.amount
                                component_amount_dict[j.salary_component][
                                    "settlement"
                                ] += j.total_settlement

                            else:
                                component_amount_dict[j.salary_component] = {
                                    "amount": j.amount,
                                    "settlement": j.total_settlement,
                                }
                            # frappe.msgprint(str(component_amount_dict))

                            for demo in benefit_component_demo:
                                if demo["component"] == j.salary_component:
                                    demo["settlement"] += j.total_settlement
                                    demo["amount"] += j.total_settlement

        benefit_component_amount1 = []
        for data in benefit_component_demo:
            total_amount = max(0, data["amount"] - data["settlement"])

            benefit_component_amount1.append(
                {"component": data["component"], "total_amount": total_amount}
            )

        # # frappe.msgprint(str(benefit_component_amount1))

        if self.employee:
            ss_assignment = frappe.get_list(
                "Salary Structure Assignment",
                filters={"employee": self.employee, "docstatus": 1},
                fields=["name"],
                order_by="from_date desc",
                limit=1,
            )

            if ss_assignment:
                child_doc = frappe.get_doc(
                    "Salary Structure Assignment", ss_assignment[0].name
                )

                for i in child_doc.custom_employee_reimbursements:
                    if i.reimbursements in benefit_component:
                        if i.reimbursements in component_amount_dict:
                            component_amount_dict[i.reimbursements][
                                "amount"
                            ] += i.monthly_total_amount
                        else:
                            component_amount_dict[i.reimbursements] = {
                                "amount": i.monthly_total_amount,
                                "settlement": 0.0,
                            }

        # frappe.msgprint(str(component_amount_dict))

        benefit_component_amount = []
        for component, data in component_amount_dict.items():
            total_amount = data["amount"] - data["settlement"]
            benefit_component_amount.append(
                {"component": component, "total_amount": total_amount}
            )

        # frappe.msgprint(str(benefit_component_amount))
        # frappe.msgprint(str(benefit_component_amount1))

        min_values = {}

        for item in benefit_component_amount1:
            component = item["component"]
            total_amount = item["total_amount"]
            min_values[component] = total_amount

        for item in benefit_component_amount:
            component = item["component"]
            total_amount = item["total_amount"]
            if component in min_values:
                min_values[component] = min(min_values[component], total_amount)
            else:
                min_values[component] = total_amount

        min_values_list = [
            {"component": component, "total_amount": total_amount}
            for component, total_amount in min_values.items()
        ]
        existing_components = {earning.salary_component for earning in self.earnings}
        for component_data in min_values_list:
            if component_data["component"] not in existing_components:
                self.append(
                    "earnings",
                    {
                        "salary_component": component_data["component"],
                        "amount": component_data["total_amount"],
                    },
                )

    # def employee_accrual_insert(self):
    #     if self.employee:
    #         ss_assignment = frappe.get_list(
    #             "Salary Structure Assignment",
    #             filters={"employee": self.employee, "docstatus": 1},
    #             fields=["name"],
    #             order_by="from_date desc",
    #             limit=1,
    #         )

    #         if ss_assignment:
    #             child_doc = frappe.get_doc(
    #                 "Salary Structure Assignment", ss_assignment[0].name
    #             )

    #             for i in child_doc.custom_employee_reimbursements:
    #                 accrual_insert = frappe.get_doc(
    #                     {
    #                         "doctype": "Employee Benefit Accrual",
    #                         "employee": self.employee,
    #                         "payroll_entry": self.payroll_entry,
    #                         "amount": round(
    #                             (i.monthly_total_amount / self.total_working_days)
    #                             * self.payment_days
    #                         ),
    #                         "salary_component": i.reimbursements,
    #                         "benefit_accrual_date": self.posting_date,
    #                         "salary_slip": self.name,
    #                         "payroll_period": child_doc.custom_payroll_period,
    #                     }
    #                 )
    #                 accrual_insert.insert()

    def employee_accrual_submit(self):
        if self.employee:
            for i in self.earnings:
                component = frappe.get_doc("Salary Component", i.salary_component)

                if component.custom_is_reimbursement == 1:
                    get_accrual_data = frappe.db.get_list(
                        "Employee Benefit Accrual",
                        filters={
                            "salary_slip": self.name,
                            "salary_component": i.salary_component,
                            "employee": self.employee,
                        },
                        fields=["*"],
                    )

                    for j in get_accrual_data:
                        accrual_doc = frappe.get_doc("Employee Benefit Accrual", j.name)
                        accrual_doc.total_settlement = i.amount
                        accrual_doc.save()

            get_accrual = frappe.db.get_list(
                "Employee Benefit Accrual",
                filters={"salary_slip": self.name},
                fields=["name"],
            )

            for j in get_accrual:
                accrual_doc = frappe.get_doc("Employee Benefit Accrual", j.name)
                accrual_doc.docstatus = 1
                accrual_doc.save()

    def calculate_grosspay(self):
        gross_pay_sum = 0

        # gross_pay_year_sum = 0

        reimbursement_sum = 0

        total_income = 0

        gross_earning = 0

        if self.earnings:
            for i in self.earnings:
                component = frappe.get_doc("Salary Component", i.salary_component)
                if component.custom_is_part_of_gross_pay == 1:
                    gross_pay_sum += i.amount
                    # gross_pay_year_sum += i.year_to_date

                if (
                    component.custom_is_reimbursement == 1
                    or component.component_type == "LTA Taxable"
                    or component.component_type == "LTA Non Taxable"
                ):
                    reimbursement_sum += i.amount

                if (
                    component.do_not_include_in_total == 0
                    and component.custom_is_reimbursement == 0
                ):
                    total_income += i.amount

        if self.total_loan_repayment:
            self.custom_loan_amount = self.total_loan_repayment
        else:
            self.custom_loan_amount = 0

        # self.custom_total_deduction_amount = (
        #     self.custom_loan_amount + self.total_deduction
        # )

        self.custom_statutory_grosspay = round(gross_pay_sum)

        # self.custom_statutory_year_to_date = round(gross_pay_year_sum)

        self.custom_total_income = round(total_income)

        self.custom_net_pay_amount = round(
            (total_income - self.custom_total_deduction_amount) + reimbursement_sum
        )

        self.custom_in_words = money_in_words(self.custom_net_pay_amount)

    def set_taxale(self):
        for earning in self.earnings:
            get_tax = frappe.get_doc("Salary Component", earning.salary_component)

            earning.custom_tax_exemption_applicable_based_on_regime = (
                get_tax.custom_tax_exemption_applicable_based_on_regime
            )
            earning.custom_regime = get_tax.custom_regime

    def set_payroll_period(self):
        latest_salary_structure = frappe.get_list(
            "Salary Structure Assignment",
            filters={"employee": self.employee, "docstatus": 1},
            fields=["*"],
            order_by="from_date desc",
            limit=1,
        )

        self.custom_salary_structure_assignment = latest_salary_structure[0].name
        self.custom_income_tax_slab = latest_salary_structure[0].income_tax_slab
        self.custom_tax_regime = latest_salary_structure[0].custom_tax_regime
        self.custom_employee_state = latest_salary_structure[0].custom_state
        self.custom_annual_ctc = latest_salary_structure[0].base
        # self.custom_payroll_period=latest_salary_structure[0].custom_payroll_period

        latest_payroll_period = frappe.get_list(
            "Payroll Period",
            filters={"start_date": ("<", self.end_date), "company": self.company},
            fields=["*"],
            order_by="start_date desc",
            limit=1,
        )
        if latest_payroll_period:
            self.custom_payroll_period = latest_payroll_period[0].name

    # def add_employee_benefits(self):
    #     pass

    def tax_calculation(self):
        latest_salary_structure = frappe.get_list(
            "Salary Structure Assignment",
            filters={"employee": self.employee, "docstatus": 1},
            fields=["*"],
            order_by="from_date desc",
            limit=1,
        )

        if self.annual_taxable_amount:
            self.custom_taxable_amount = round(self.annual_taxable_amount)
        else:
            self.custom_taxable_amount = 0

        if self.ctc and self.non_taxable_earnings:
            self.custom_total_income_with_taxable_component = round(
                self.ctc - self.non_taxable_earnings
            )

        if latest_salary_structure[0].income_tax_slab:
            payroll_period = latest_salary_structure[0].custom_payroll_period
            income_doc = frappe.get_doc(
                "Income Tax Slab", latest_salary_structure[0].income_tax_slab
            )

            total_value = []
            from_amount = []
            to_amount = []
            percentage = []

            total_array = []
            difference = []

            rebate = income_doc.custom_taxable_income_is_less_than
            max_amount = income_doc.custom_maximum_amount

            if (
                income_doc.custom_marginal_relief_applicable
                and income_doc.custom_minmum_value
                and income_doc.custom_maximun_value
            ):
                marginal_relief_min_value = income_doc.custom_minmum_value
                marginal_relief_max_value = income_doc.custom_maximun_value

            # if self.annual_taxable_amount > rebate:
            for i in income_doc.slabs:
                array_list = {
                    "from": i.from_amount,
                    "to": i.to_amount,
                    "percent": i.percent_deduction,
                }

                total_array.append(array_list)
            for slab in total_array:
                if slab["to"] == 0.0:
                    if round(self.annual_taxable_amount) >= slab["from"]:
                        tt1 = round(self.annual_taxable_amount) - slab["from"]
                        tt2 = slab["percent"]
                        tt3 = round((tt1 * tt2) / 100)

                        tt4 = slab["from"]
                        tt5 = slab["to"]

                        remaining_slabs = [
                            s
                            for s in total_array
                            if s["from"] != slab["from"] and s["from"] < slab["from"]
                        ]
                        for slab in remaining_slabs:
                            from_amount.append(slab["from"])
                            to_amount.append(slab["to"])
                            percentage.append(slab["percent"])
                            difference.append(slab["to"] - slab["from"])
                            total_value.append(
                                (slab["to"] - slab["from"]) * slab["percent"] / 100
                            )
                        from_amount.append(tt4)
                        to_amount.append(tt5)
                        percentage.append(tt2)
                        difference.append(tt1)
                        total_value.append(tt3)
                    self.custom_tax_slab = []
                    for i in range(len(from_amount)):
                        self.append(
                            "custom_tax_slab",
                            {
                                "from_amount": from_amount[i],
                                "to_amount": to_amount[i],
                                "percentage": percentage[i],
                                "tax_amount": total_value[i],
                                "amount": difference[i],
                            },
                        )

                else:
                    if slab["from"] <= round(self.annual_taxable_amount) <= slab["to"]:
                        tt1 = round(self.annual_taxable_amount) - slab["from"]
                        tt2 = slab["percent"]
                        tt3 = (tt1 * tt2) / 100
                        tt4 = slab["from"]
                        tt5 = slab["to"]
                        remaining_slabs = [
                            s
                            for s in total_array
                            if s["from"] != slab["from"] and s["from"] < slab["from"]
                        ]

                        for slab in remaining_slabs:
                            from_amount.append(slab["from"])
                            to_amount.append(slab["to"])
                            percentage.append(slab["percent"])
                            difference.append(slab["to"] - slab["from"])
                            total_value.append(
                                (slab["to"] - slab["from"]) * slab["percent"] / 100
                            )
                        from_amount.append(tt4)
                        to_amount.append(tt5)
                        percentage.append(tt2)
                        difference.append(tt1)
                        total_value.append(tt3)

                    self.custom_tax_slab = []
                    for i in range(len(from_amount)):
                        self.append(
                            "custom_tax_slab",
                            {
                                "from_amount": from_amount[i],
                                "to_amount": to_amount[i],
                                "percentage": percentage[i],
                                "tax_amount": round(total_value[i]),
                                "amount": difference[i],
                            },
                        )


def override_calculate_tax_by_tax_slab(
    self, annual_taxable_earning, tax_slab, eval_globals=None, eval_locals=None
):
    eval_locals.update({"annual_taxable_earning": annual_taxable_earning})
    base_tax = 0
    rebate = 0
    other_taxes_and_charges = 0
    custom_tds_already_deducted_amount = 0
    surcharge = 0
    charge_percent = 0
    education_cess_amount = 0
    total_tax_payable = 0

    for slab in tax_slab.slabs:
        cond = cstr(slab.condition).strip()
        if cond and not eval_tax_slab_condition(cond, eval_globals, eval_locals):
            continue

        from_amt = slab.from_amount
        to_amt = slab.to_amount or annual_taxable_earning
        rate = slab.percent_deduction * 0.01

        if annual_taxable_earning > from_amt:
            taxable_range = min(annual_taxable_earning, to_amt) - from_amt

            base_tax += taxable_range * rate

    if (
        tax_slab.custom_marginal_relief_applicable
        and tax_slab.custom_minmum_value
        and tax_slab.custom_maximun_value
    ):
        if (
            tax_slab.custom_minmum_value
            < annual_taxable_earning
            < tax_slab.custom_maximun_value
        ):
            excess_income = annual_taxable_earning - tax_slab.custom_minmum_value

            if base_tax > excess_income:
                rebate = base_tax - excess_income
                base_tax -= rebate

    for d in tax_slab.other_taxes_and_charges:
        if d.custom_is_education_cess == 0:
            min_value = flt(d.min_taxable_income) or 0
            max_value = flt(d.max_taxable_income) or None

            if annual_taxable_earning >= min_value and (
                not max_value or annual_taxable_earning < max_value
            ):
                charge_percent = flt(d.percent)
                surcharge = (base_tax * charge_percent) / 100.0

    for d in tax_slab.other_taxes_and_charges:
        if d.custom_is_education_cess == 1:
            total_tax_before_cess = base_tax + surcharge

            education_cess_amount = (total_tax_before_cess * flt(d.percent)) / 100.0

    total_tax_payable = round(education_cess_amount + surcharge + base_tax)

    self.custom_tax_on_total_income = base_tax

    if annual_taxable_earning <= tax_slab.custom_taxable_income_is_less_than:
        self.custom_rebate_under_section_87a = base_tax
    else:
        self.custom_rebate_under_section_87a = 0

    self.custom_total_tax_on_income = (
        self.custom_tax_on_total_income + self.custom_rebate_under_section_87a
    )
    self.custom_surcharge = surcharge
    self.custom_education_cess = education_cess_amount
    self.custom_total_amount = total_tax_payable

    declaration = frappe.db.get_value(
        "Employee Tax Exemption Declaration",
        {
            "employee": self.employee,
            "payroll_period": self.payroll_period.name,
            "docstatus": 1,
        },
        "custom_tds_already_deducted_amount",
        as_dict=True,
        cache=True,
    )
    if declaration:
        custom_tds_already_deducted_amount = (
            declaration.custom_tds_already_deducted_amount or 0.0
        )

    final_tax = (total_tax_payable) - custom_tds_already_deducted_amount

    print("\n\n\n\n\final_tax", final_tax)

    return round(final_tax, 2), round(total_tax_payable, 2)
