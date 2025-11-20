import frappe
import datetime
from frappe.query_builder.functions import Count, Sum
import json
from frappe.query_builder import Order
from frappe import _
import math
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
from datetime import datetime, timedelta,date
from hrms.payroll.doctype.payroll_period.payroll_period import get_period_factor
from hrms.payroll.doctype.salary_slip.salary_slip import eval_tax_slab_condition
from collections import defaultdict

class CustomSalarySlip(SalarySlip):


    def before_save(self):

        self.esic_amount_roundup()
        self.update_declaration_component()
        self.tax_calculation()


    def validate(self):
        super().validate()
        self.set_month()
        self.set_sub_period()
        self.update_total_lop()
        self.set_taxale_regime()
        self.insert_lopreversal_days()


    def insert_lopreversal_days(self):
        total_lop_days=0
        arrear_days = frappe.get_list(
            'Payroll Correction',
            filters={
                'employee': self.employee,
                'payroll_date': ['between', [self.start_date, self.end_date]],
                'docstatus': 1
            },
            fields=['days_to_reverse']
        )

        if arrear_days:

            total_lop_days = sum(days['days_to_reverse'] for days in arrear_days)
            self.custom_lop_reversal_days = total_lop_days
        else:
            self.custom_lop_reversal_days = 0




    def calculate_variable_tax(self, tax_component):
        self.previous_total_paid_taxes = self.get_tax_paid_in_period(
            self.payroll_period.start_date, self.start_date, tax_component
        )

        # Structured tax amount
        eval_locals, default_data = self.get_data_for_eval()
        self.total_structured_tax_amount, __ = override_calculate_tax_by_tax_slab(
            self,
            self.total_taxable_earnings_without_full_tax_addl_components,
            self.tax_slab,
            self.whitelisted_globals,
            eval_locals,
        )

        self.current_structured_tax_amount = (
            self.total_structured_tax_amount - self.previous_total_paid_taxes
        ) / self.remaining_sub_periods

        # Total taxable earnings with additional earnings with full tax
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



    def get_working_days_details(self, lwp=None, for_preview=0, lwp_days_corrected=None):
        actual_lwp=0
        absent=0
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

        daily_wages_fraction_for_half_day = flt(payroll_settings.daily_wages_fraction_for_half_day) or 0.5

        working_days = date_diff(self.end_date, self.start_date) + 1
        if for_preview:
            self.total_working_days = working_days
            self.payment_days = working_days
            return

        holidays = self.get_holidays_for_employee(self.start_date, self.end_date)
        working_days_list = [add_days(getdate(self.start_date), days=day) for day in range(0, working_days)]

        if not cint(payroll_settings.include_holidays_in_total_working_days):
            working_days_list = [i for i in working_days_list if i not in holidays]

            working_days -= len(holidays)
            if working_days < 0:
                frappe.throw(_("There are more holidays than working days this month."))

        if not payroll_settings.payroll_based_on:
            frappe.throw(_("Please set Payroll based on in Payroll settings"))

        if payroll_settings.payroll_based_on == "Attendance":
            if payroll_settings.custom_configure_attendance_cycle:
                actual_lwp, absent = self.calculate_lwp_ppl_and_absent_days_based_on_attendance_cycle(
                    holidays, daily_wages_fraction_for_half_day, consider_marked_attendance_on_holidays
                )
                self.absent_days = absent
            else:
                actual_lwp, absent = self.calculate_lwp_ppl_and_absent_days_based_on_attendance(
                    holidays, daily_wages_fraction_for_half_day, consider_marked_attendance_on_holidays
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

        payment_days = self.get_payment_days(payroll_settings.include_holidays_in_total_working_days)

        if flt(payment_days) > flt(lwp):
            self.payment_days = flt(payment_days) - flt(lwp)

            if payroll_settings.payroll_based_on == "Attendance":
                self.payment_days -= flt(absent)

            consider_unmarked_attendance_as = payroll_settings.consider_unmarked_attendance_as or "Present"

            if payroll_settings.payroll_based_on == "Attendance":
                if consider_unmarked_attendance_as == "Absent":
                    unmarked_days = self.get_unmarked_days(
                        payroll_settings.include_holidays_in_total_working_days, holidays
                    )
                    self.absent_days += unmarked_days  # will be treated as absent
                    self.payment_days -= unmarked_days
                half_absent_days = self.get_half_absent_days(
                    consider_marked_attendance_on_holidays,
                    holidays,
                )
                self.absent_days += half_absent_days * daily_wages_fraction_for_half_day
                self.payment_days -= half_absent_days * daily_wages_fraction_for_half_day
        else:
            self.payment_days = 0

        if lwp_days_corrected and lwp_days_corrected > 0:
            if verify_lwp_days_corrected(self.employee, self.start_date, self.end_date, lwp_days_corrected):
                self.payment_days += lwp_days_corrected


    def calculate_lwp_ppl_and_absent_days_based_on_attendance_cycle(
        self, holidays, daily_wages_fraction_for_half_day, consider_marked_attendance_on_holidays
        ):
        lwp = 0
        absent = 0

        payroll_setting=frappe.get_doc("Payroll Settings")
        if payroll_setting.payroll_based_on=="Attendance" and payroll_setting.custom_configure_attendance_cycle:
            attendance_start_day=payroll_setting.custom_attendance_start_date
            attendance_end_day=payroll_setting.custom_attendance_end_date
            start_date=getdate(self.start_date)
            end_date=getdate(self.end_date)
            attendance_end_date = end_date.replace(day=attendance_end_day)
            attendance_start_date = (attendance_end_date - relativedelta(months=1)).replace(day=attendance_start_day)

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


                if not consider_marked_attendance_on_holidays and getdate(d.attendance_date) in holidays:
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

                if d.status == "Half Day" and d.leave_type and d.leave_type in leave_type_map.keys():
                    equivalent_lwp = 1 - daily_wages_fraction_for_half_day

                    if leave_type_map[d.leave_type]["is_ppl"]:
                        equivalent_lwp *= (
                            fraction_of_daily_salary_per_leave if fraction_of_daily_salary_per_leave else 1
                        )
                    lwp += equivalent_lwp

                elif d.status == "On Leave" and d.leave_type and d.leave_type in leave_type_map.keys():
                    equivalent_lwp = 1
                    if leave_type_map[d.leave_type]["is_ppl"]:
                        equivalent_lwp *= (
                            fraction_of_daily_salary_per_leave if fraction_of_daily_salary_per_leave else 1
                        )
                    lwp += equivalent_lwp

                elif d.status == "Absent":
                    absent += 1

        return lwp, absent


    def eval_condition_and_formula(self, struct_row, data):
        try:
            condition, formula, amount = struct_row.condition, struct_row.formula, struct_row.amount
            if condition and not _safe_eval(condition, self.whitelisted_globals, data):
                return None
            if struct_row.amount_based_on_formula and formula:
                amount = flt(
                    _safe_eval(formula, self.whitelisted_globals, data), struct_row.precision("amount")
                )
            if amount:
                data[struct_row.abbr] = amount

            return amount

        except NameError as ne:
            throw_error_message(
                struct_row,
                ne,
                title=_("Name error"),
                description=_("This error can be due to missing or deleted field."),
            )
        except SyntaxError as se:
            throw_error_message(
                struct_row,
                se,
                title=_("Syntax error"),
                description=_("This error can be due to invalid syntax."),
            )
        except Exception as exc:
            throw_error_message(
                struct_row,
                exc,
                title=_("Error in formula or condition"),
                description=_("This error can be due to invalid formula or condition."),
            )
            raise






    def update_benefit_claim_amount(self):
        if not self.earnings:
            return

        for earning in self.earnings:
            additional_salary_name = earning.get("additional_salary")
            if not additional_salary_name:
                continue

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







    def set_sub_period(self):
        sub_period=get_period_factor(
                    self.employee,
                    self.start_date,
                    self.end_date,
                    self.payroll_frequency,
                    self.payroll_period,
                    joining_date=self.joining_date,
                    relieving_date=self.relieving_date,
                )[1]


        self.custom_month_count=sub_period-1


    def compute_income_tax_breakup(self):
        self.standard_tax_exemption_amount = 0
        self.tax_exemption_declaration = 0
        self.deductions_before_tax_calculation = 0
        self.custom_perquisite_amount = 0

        self.non_taxable_earnings = self.compute_non_taxable_earnings()
        self.ctc = self.compute_ctc()
        self.income_from_other_sources = self.get_income_form_other_sources()
        self.total_earnings = self.ctc + self.income_from_other_sources

        payroll_period = frappe.get_value(
            'Payroll Period',
            {'company': self.company, 'name': self.payroll_period.name},
            ['name', 'start_date', 'end_date'],
            as_dict=True
        )

        if not payroll_period:
            return

        start_date = frappe.utils.getdate(payroll_period["start_date"])
        end_date = frappe.utils.getdate(payroll_period["end_date"])
        fiscal_year = payroll_period["name"]

        loan_repayments = frappe.get_list(
            'Loan Repayment Schedule',
            filters={
                'custom_employee': self.employee,
                'status': 'Active',
                'docstatus': 1
            },
            fields=['name']
        )

        total_perq = 0
        for repayment in loan_repayments:
            repayment_doc = frappe.get_doc("Loan Repayment Schedule", repayment.name)
            for entry in repayment_doc.custom_loan_perquisite:
                if entry.payment_date and start_date <= frappe.utils.getdate(entry.payment_date) <= end_date:
                    total_perq += entry.perquisite_amount
        self.custom_perquisite_amount = total_perq

        if hasattr(self, "tax_slab") and self.tax_slab:
            if self.tax_slab.allow_tax_exemption:
                self.standard_tax_exemption_amount = self.tax_slab.standard_tax_exemption_amount
                self.deductions_before_tax_calculation = (
                    self.compute_annual_deductions_before_tax_calculation()
                )

            self.tax_exemption_declaration = (
                self.get_total_exemption_amount() - self.standard_tax_exemption_amount
            )

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
                ssa.custom_tax_regime
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
            self.custom_salary_structure_assignment=st_name[0][2]
            self.custom_income_tax_slab=st_name[0][3]
            self.custom_tax_regime=st_name[0][4]


            return self.salary_structure

        else:
            self.salary_structure = None
            frappe.msgprint(
                _("No active or default Salary Structure found for employee {0} for the given dates").format(
                    self.employee
                ),
                title=_("Salary Structure Missing"),
            )




    def update_total_lop(self):
        self.custom_total_leave_without_pay = (self.absent_days or 0) + self.leave_without_pay




    def get_taxable_earnings(self, allow_tax_exemption=False, based_on_payment_days=0):
        taxable_earnings = 0
        additional_income = 0
        additional_income_with_full_tax = 0
        flexi_benefits = 0
        amount_exempted_from_income_tax = 0

        tax_component = None

        latest_salary_structure = frappe.get_list('Salary Structure Assignment',
                    filters={'employee': self.employee,'docstatus':1},
                    fields=["*"],
                    order_by='from_date desc',
                    limit=1
                )

        if len(latest_salary_structure)>0:
            tax_component=latest_salary_structure[0].custom_tax_regime

        for earning in self.earnings:

            get_tax=frappe.get_doc("Salary Component",earning.salary_component)


            if get_tax.is_tax_applicable==1 and get_tax.custom_tax_exemption_applicable_based_on_regime==1:
                if get_tax.custom_regime=="All":
                    earning.is_tax_applicable=get_tax.is_tax_applicable
                    earning.custom_regime=get_tax.custom_regime
                    earning.custom_tax_exemption_applicable_based_on_regime=get_tax.custom_tax_exemption_applicable_based_on_regime

                elif get_tax.custom_regime==tax_component:
                    earning.is_tax_applicable=get_tax.is_tax_applicable
                    earning.custom_regime=get_tax.custom_regime
                    earning.custom_tax_exemption_applicable_based_on_regime=get_tax.custom_tax_exemption_applicable_based_on_regime
                elif get_tax.custom_regime!=tax_component:
                    earning.is_tax_applicable=0
                    earning.custom_regime=get_tax.custom_regime
                    earning.custom_tax_exemption_applicable_based_on_regime=get_tax.custom_tax_exemption_applicable_based_on_regime

            elif get_tax.is_tax_applicable==0 and get_tax.custom_tax_exemption_applicable_based_on_regime==0:
                earning.is_tax_applicable=0
                earning.custom_regime=get_tax.custom_regime
                earning.custom_tax_exemption_applicable_based_on_regime=get_tax.custom_tax_exemption_applicable_based_on_regime
            elif get_tax.is_tax_applicable==1 and get_tax.custom_tax_exemption_applicable_based_on_regime==0:
                earning.is_tax_applicable=1
                earning.custom_regime=get_tax.custom_regime
                earning.custom_tax_exemption_applicable_based_on_regime=get_tax.custom_tax_exemption_applicable_based_on_regime


            if based_on_payment_days:
                amount, additional_amount = self.get_amount_based_on_payment_days(earning)
            else:
                if earning.additional_amount:
                    amount, additional_amount = earning.amount, earning.additional_amount
                else:
                    amount, additional_amount = earning.default_amount, earning.additional_amount
            if earning.is_tax_applicable:
                if earning.is_flexible_benefit:
                    flexi_benefits += amount
                else:

                    taxable_earnings += amount - additional_amount
                    additional_income += additional_amount

                    if additional_amount and earning.is_recurring_additional_salary:
                        additional_income += self.get_future_recurring_additional_amount(
                            earning.additional_salary, earning.additional_amount
                        )

                    if earning.deduct_full_tax_on_selected_payroll_date:
                        additional_income_with_full_tax += additional_amount

        if allow_tax_exemption:
            for ded in self.deductions:
                if ded.exempted_from_income_tax:
                    amount, additional_amount = ded.amount, ded.additional_amount
                    if based_on_payment_days:
                        amount, additional_amount = self.get_amount_based_on_payment_days(ded)

                    taxable_earnings -= flt(amount - additional_amount)
                    additional_income -= additional_amount
                    amount_exempted_from_income_tax = flt(amount - additional_amount)

                    if additional_amount and ded.is_recurring_additional_salary:
                        additional_income -= self.get_future_recurring_additional_amount(
                            ded.additional_salary, ded.additional_amount
                        )

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

        regime_matched = any(
            earning.custom_regime == custom_tax_regime or earning.custom_regime == "All"
            for earning in self.earnings
        )

        if regime_matched:
            taxable_earnings = self.get_salary_slip_details(
                start_date,
                end_date,
                parentfield="earnings",
                is_tax_applicable=1,
                custom_tax_exemption_applicable_based_on_regime=1,
                custom_regime=custom_tax_regime,
            ) + self.get_salary_slip_details(
                start_date,
                end_date,
                parentfield="earnings",
                is_tax_applicable=1,
                custom_tax_exemption_applicable_based_on_regime=1,
                custom_regime="All",
            )
        else:
            taxable_earnings = self.get_salary_slip_details(
                start_date,
                end_date,
                parentfield="earnings",
                is_tax_applicable=1,
                custom_regime="All",
            )


        if allow_tax_exemption:
            exempted_amount = self.get_salary_slip_details(
                start_date,
                end_date,
                parentfield="deductions",
                exempted_from_income_tax=1,
            )

        opening_taxable_earning = self.get_opening_for(
            "taxable_earnings_till_date", start_date, end_date
        )

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
        custom_tax_regime=None
    ):
        ss = frappe.qb.DocType("Salary Slip")
        sd = frappe.qb.DocType("Salary Detail")


        if field_to_select == "amount":
            field = sd.amount
        else:
            field = sd.additional_amount


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

        if is_tax_applicable is not None:
            query = query.where(sd.is_tax_applicable == is_tax_applicable)

        if exempted_from_income_tax:
            query = query.where(sd.exempted_from_income_tax == exempted_from_income_tax)

        if variable_based_on_taxable_salary:
            query = query.where(sd.variable_based_on_taxable_salary == variable_based_on_taxable_salary)

        if salary_component:
            query = query.where(sd.salary_component == salary_component)

        if custom_tax_exemption_applicable_based_on_regime:
            query = query.where(sd.custom_tax_exemption_applicable_based_on_regime == custom_tax_exemption_applicable_based_on_regime)

        if custom_regime:
            query = query.where(sd.custom_regime == custom_regime)


        if custom_tax_regime:
            query = query.where(ss.custom_tax_regime == custom_tax_regime)

        result = query.run()

        return flt(result[0][0]) if result else 0.0








    def update_declaration_component(self):
        if not self.employee:
            return

        current_basic=current_hra=None

        current_basic_value = current_hra_value = current_nps_value = current_epf_value = current_pt_value = 0
        previous_basic_value = previous_hra_value = previous_nps_value = previous_epf_value = previous_pt_value = 0
        future_basic_value = future_hra_value = future_nps_value = future_epf_value = future_pt_value = 0

        get_company = frappe.get_doc("Company", self.company)
        if get_company.basic_component:
            current_basic = get_company.basic_component
        if get_company.hra_component:
            current_hra = get_company.hra_component



        if self.earnings:
            for earning in self.earnings:
                earning_component_data = frappe.get_doc(
                    "Salary Component", earning.salary_component
                )
                if earning_component_data.component_type == "NPS":
                    current_nps_value += earning.amount or 0
                    if earning_component_data.custom_component_sub_type=="Fixed":
                        future_nps_value = (
                            earning.default_amount or 0
                        ) * self.custom_month_count


                if earning.salary_component == current_basic:
                    current_basic_value += earning.amount
                    if  earning_component_data.custom_component_sub_type=="Fixed":
                        future_basic_value = (earning.default_amount) * (
                            self.custom_month_count
                        )
                if earning.salary_component == current_hra:
                    current_hra_value += earning.amount
                    if earning_component_data.custom_component_sub_type=="Fixed":
                        future_hra_value = (earning.default_amount) * (
                            self.custom_month_count
                        )



        if self.deductions:
            for deduction in self.deductions:
                deduction_component_data = frappe.get_doc(
                    "Salary Component", deduction.salary_component
                )
                if deduction_component_data.component_type == "Provident Fund":
                    current_epf_value += deduction.amount
                    if deduction_component_data.custom_component_sub_type=="Fixed":
                        future_epf_value = (deduction.default_amount) * (
                            self.custom_month_count
                        )
                if deduction_component_data.component_type == "Professional Tax":
                    current_pt_value += deduction.amount

                    if deduction_component_data.custom_component_sub_type=="Fixed":
                        future_pt_value = (deduction.default_amount) * (
                            self.custom_month_count
                        )




        get_previous_salary_slip = frappe.get_list(
            'Salary Slip',
            filters={
                'employee': self.employee,
                'custom_payroll_period': self.custom_payroll_period,
                'docstatus': 1,
                'name': ['!=', self.name]
            },
            fields=['name',"custom_payroll_period"]
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
                        if component_data.component_type == "Provident Fund":
                            previous_epf_value += deduction.amount
                        if component_data.component_type == "Professional Tax":
                            previous_pt_value += deduction.amount


        if self.custom_tax_regime == "Old Regime":
            declaration = frappe.get_list(
                'Employee Tax Exemption Declaration',
                filters={
                    'employee': self.employee,
                    'payroll_period': self.custom_payroll_period,
                    'docstatus': 1,
                    'company': self.company
                },
                fields=['*']
            )

            if declaration:
                get_each_doc = frappe.get_doc("Employee Tax Exemption Declaration", declaration[0].name)

                form_data = json.loads(declaration[0].custom_declaration_form_data or '[]')

                total_nps = round(previous_nps_value + future_nps_value + current_nps_value)
                total_pf = min(round(previous_epf_value + future_epf_value + current_epf_value), 150000)
                total_pt = round(previous_pt_value + future_pt_value + current_pt_value)

                for subcategory in get_each_doc.declarations:
                    check_component = frappe.get_doc("Employee Tax Exemption Sub Category", subcategory.exemption_sub_category)

                    if check_component.custom_component_type == "NPS":
                        subcategory.amount = total_nps

                    elif check_component.custom_component_type == "Provident Fund":
                        subcategory.amount = total_pf

                    elif check_component.custom_component_type == "Professional Tax":
                        subcategory.amount = total_pt

                for entry in form_data:
                    subcat = entry.get("sub_category") or entry.get("id")
                    component = frappe.get_all(
                        "Employee Tax Exemption Sub Category",
                        filters={"name": subcat},
                        fields=["custom_component_type"],
                        limit=1
                    )
                    if component:
                        ctype = component[0].custom_component_type
                        if ctype == "NPS":
                            entry["amount"] = total_nps
                            entry["value"] = total_nps
                        elif ctype == "Provident Fund":
                            entry["amount"] = total_pf
                            entry["value"] = total_pf
                        elif ctype == "Professional Tax":
                            entry["amount"] = total_pt
                            entry["value"] = total_pt

                get_each_doc.custom_posting_date = self.posting_date
                get_each_doc.custom_declaration_form_data = json.dumps(form_data)



                if get_each_doc.monthly_house_rent>0:
                    ss_assignment = frappe.get_list(
                    "Salary Structure Assignment",
                    filters={
                        "employee": self.employee,
                        "docstatus": 1,
                        "company": self.company,
                        "custom_payroll_period": self.custom_payroll_period,
                        "from_date": ("<=", self.end_date),
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
                        first_assignment_structure = first_assignment.get("salary_structure")

                        start_date = ss_assignment[-1].from_date
                        if ss_assignment[-1].custom_payroll_period:
                            payroll_period = frappe.get_doc(
                                "Payroll Period", ss_assignment[-1].custom_payroll_period
                            )
                            end_date = payroll_period.end_date
                            month_count = (
                                (end_date.year - start_date.year) * 12
                                + end_date.month
                                - start_date.month
                                + 1
                            )

                            percentage=(previous_basic_value+future_basic_value+current_basic_value)*10/100
                            get_each_doc.custom_check=1
                            get_each_doc.custom_basic_as_per_salary_structure=round(percentage)
                            get_each_doc.salary_structure_hra=round(previous_hra_value+future_hra_value+current_hra_value)
                            get_each_doc.custom_basic=round(previous_basic_value+future_basic_value+current_basic_value)

                            total_basic_amount= round(previous_basic_value + future_basic_value + current_basic_value)
                            total_hra_amount = round(previous_hra_value + future_hra_value + current_hra_value)

                            annual_hra_amount = get_each_doc.monthly_house_rent * month_count

                            basic_rule2 = round(annual_hra_amount - percentage)
                            if get_each_doc.rented_in_metro_city == 0:
                                non_metro_or_metro = (total_basic_amount * 40) / 100
                            elif get_each_doc.rented_in_metro_city == 1:
                                non_metro_or_metro = (total_basic_amount * 50) / 100

                            final_hra_exemption = round(
                                min(basic_rule2, annual_hra_amount, non_metro_or_metro)
                            )


                            get_each_doc.annual_hra_exemption = round(final_hra_exemption)
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
                                    (get_each_doc.custom_basic_as_per_salary_structure * 10) * 50 / 100
                                )
                            else:
                                earned_basic = (
                                    (get_each_doc.custom_basic_as_per_salary_structure * 10) * 40 / 100
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


                get_each_doc.custom_status="Approved"

                get_each_doc.save()
                frappe.db.commit()
                self.tax_exemption_declaration=get_each_doc.total_exemption_amount


        if self.custom_tax_regime=="New Regime":
            declaration = frappe.get_list(
                'Employee Tax Exemption Declaration',
                filters={
                    'employee': self.employee,
                    'payroll_period': self.custom_payroll_period,
                    'docstatus': 1,
                    'company': self.company
                },
                fields=['*']
            )

            if declaration:
                get_each_doc = frappe.get_doc("Employee Tax Exemption Declaration", declaration[0].name)

                form_data = json.loads(declaration[0].custom_declaration_form_data or '[]')

                total_nps = round(previous_nps_value + future_nps_value + current_nps_value)

                for subcategory in get_each_doc.declarations:
                    check_component = frappe.get_doc("Employee Tax Exemption Sub Category", subcategory.exemption_sub_category)

                    if check_component.custom_component_type == "NPS":
                        subcategory.amount = total_nps


                for entry in form_data:
                    subcat = entry.get("sub_category") or entry.get("id")
                    component = frappe.get_all(
                        "Employee Tax Exemption Sub Category",
                        filters={"name": subcat},
                        fields=["custom_component_type"],
                        limit=1
                    )
                    if component:
                        ctype = component[0].custom_component_type
                        if ctype == "NPS":
                            entry["amount"] = total_nps
                            entry["value"] = total_nps

                get_each_doc.custom_posting_date = self.posting_date
                get_each_doc.custom_declaration_form_data = json.dumps(form_data)

                get_each_doc.custom_status="Approved"

                get_each_doc.save()
                frappe.db.commit()
                self.tax_exemption_declaration=get_each_doc.total_exemption_amount



    def set_month(self):
        date_str = str(self.start_date)
        month_str = date_str[5:7]
        month_number = int(month_str)
        month_names = ["", "January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"]

        month_name = month_names[month_number]
        self.custom_month=month_name




    def esic_amount_roundup(self):
        if self.deductions:
            for deduction in self.deductions:
                component_doc = frappe.get_doc("Salary Component", deduction.salary_component)
                original_amount = float(deduction.amount or 0)

        if self.total_deduction or self.total_loan_repayment:
            self.custom_total_deduction_amount = (self.total_deduction or 0) + (self.total_loan_repayment or 0)
        else:
            self.custom_total_deduction_amount = 0




    def compute_ctc(self):
        if hasattr(self, "previous_taxable_earnings"):
            return (
				self.previous_taxable_earnings_before_exemption
				+ self.current_structured_taxable_earnings_before_exemption
				+ self.future_structured_taxable_earnings_before_exemption
				+ self.current_additional_earnings
				+ self.other_incomes
				+ self.unclaimed_taxable_benefits
				+ self.non_taxable_earnings
			)
        return 0
















    def set_taxale_regime(self):
        for earning in self.earnings:
            get_tax_component=frappe.get_doc("Salary Component",earning.salary_component)
            earning.custom_tax_exemption_applicable_based_on_regime=get_tax_component.custom_tax_exemption_applicable_based_on_regime
            earning.custom_regime=get_tax_component.custom_regime






    def tax_calculation(self):
        latest_salary_structure = frappe.get_list(
            'Salary Structure Assignment',
            filters={'employee': self.employee, 'docstatus': 1,"from_date": ("<=", self.end_date)},
            fields=["*"],
            order_by='from_date desc',
            limit=1
        )


        if self.annual_taxable_amount:
            self.custom_taxable_amount = round(self.annual_taxable_amount)

        if self.ctc and self.non_taxable_earnings:
            self.custom_total_income_with_taxable_component = round(self.ctc - self.non_taxable_earnings)


        if latest_salary_structure and latest_salary_structure[0].income_tax_slab:
            income_doc = frappe.get_doc('Income Tax Slab', latest_salary_structure[0].income_tax_slab)
            total_array = []
            from_amount, to_amount, percentage, difference, total_value = [], [], [], [], []

            rebate = income_doc.custom_taxable_income_is_less_than
            max_amount = income_doc.custom_maximum_amount


            for i in income_doc.slabs:
                total_array.append({
                    'from': i.from_amount,
                    'to': i.to_amount,
                    'percent': i.percent_deduction
                })

            self.custom_tax_slab = []

            for slab in total_array:
                taxable = round(self.annual_taxable_amount)

                if slab['to'] == 0.0:

                    if taxable >= slab['from']:
                        taxable_diff = taxable - slab['from']
                        tax_percent = slab['percent']
                        tax_amount = round((taxable_diff * tax_percent) / 100)


                        remaining_slabs = [s for s in total_array if s['from'] < slab['from']]
                        for s in remaining_slabs:
                            from_amount.append(s['from'])
                            to_amount.append(s['to'])
                            percentage.append(s["percent"])
                            difference.append(s['to'] - s['from'])
                            total_value.append((s['to'] - s['from']) * s["percent"] / 100)


                        from_amount.append(slab['from'])
                        to_amount.append(slab['to'])
                        percentage.append(tax_percent)
                        difference.append(taxable_diff)
                        total_value.append(tax_amount)
                        break

                else:

                    if slab['from'] <= taxable <= slab['to']:
                        taxable_diff = taxable - slab['from']
                        tax_percent = slab['percent']
                        tax_amount = (taxable_diff * tax_percent) / 100


                        remaining_slabs = [s for s in total_array if s['from'] < slab['from']]
                        for s in remaining_slabs:
                            from_amount.append(s['from'])
                            to_amount.append(s['to'])
                            percentage.append(s["percent"])
                            difference.append(s['to'] - s['from'])
                            total_value.append((s['to'] - s['from']) * s["percent"] / 100)


                        from_amount.append(slab['from'])
                        to_amount.append(slab['to'])
                        percentage.append(tax_percent)
                        difference.append(taxable_diff)
                        total_value.append(tax_amount)
                        break


            for i in range(len(from_amount)):
                self.append("custom_tax_slab", {
                    "from_amount": from_amount[i],
                    "to_amount": to_amount[i],
                    "percentage": percentage[i],
                    "tax_amount": total_value[i],
                    "amount": difference[i]
                })


            total_sum = sum(total_value)


            if self.custom_taxable_amount < rebate:
                self.custom_tax_on_total_income = total_sum
                self.custom_rebate_under_section_87a = total_sum
                self.custom_total_tax_on_income = 0
            else:
                self.custom_rebate_under_section_87a = 0
                self.custom_tax_on_total_income = total_sum
                self.custom_total_tax_on_income = total_sum


            if self.custom_taxable_amount > 5000000:
                surcharge = (self.custom_total_tax_on_income * 10) / 100
                self.custom_surcharge = round(surcharge)
            else:
                self.custom_surcharge = 0

            self.custom_education_cess = round((self.custom_total_tax_on_income + self.custom_surcharge) * 4 / 100)


            self.custom_total_amount = round(
                self.custom_total_tax_on_income + self.custom_surcharge + self.custom_education_cess
            )


def _safe_eval(code: str, eval_globals: dict | None = None, eval_locals: dict | None = None):
	import unicodedata
	code = unicodedata.normalize("NFKC", code)

	_check_attributes(code)


	whitelisted_globals = {
		"int": int,
		"float": float,
		"long": int,
		"round": round,
		"sum": sum,
		"min": min,
		"max": max,
		"next": next,
		"len": len,
	}

	if not eval_globals:
		eval_globals = {}

	eval_globals["__builtins__"] = {}
	eval_globals.update(whitelisted_globals)

	return eval(code, eval_globals, eval_locals)  # nosemgrep


def _check_attributes(code: str) -> None:
	import ast

	from frappe.utils.safe_exec import UNSAFE_ATTRIBUTES

	unsafe_attrs = set(UNSAFE_ATTRIBUTES).union(["__"]) - {"format"}

	for attribute in unsafe_attrs:
		if attribute in code:
			raise SyntaxError(f'Illegal rule {frappe.bold(code)}. Cannot use "{attribute}"')

	BLOCKED_NODES = (ast.NamedExpr,)

	tree = ast.parse(code, mode="eval")
	for node in ast.walk(tree):
		if isinstance(node, BLOCKED_NODES):
			raise SyntaxError(f"Operation not allowed: line {node.lineno} column {node.col_offset}")
		if isinstance(node, ast.Attribute) and isinstance(node.attr, str) and node.attr in UNSAFE_ATTRIBUTES:
			raise SyntaxError(f'Illegal rule {frappe.bold(code)}. Cannot use "{node.attr}"')

def throw_error_message(row, error, title, description=None):
	data = frappe._dict(
		{
			"doctype": row.parenttype,
			"name": row.parent,
			"doclink": get_link_to_form(row.parenttype, row.parent),
			"row_id": row.idx,
			"error": error,
			"title": title,
			"description": description or "",
		}
	)

	message = _(
		"Error while evaluating the {doctype} {doclink} at row {row_id}. <br><br> <b>Error:</b> {error} <br><br> <b>Hint:</b> {description}"
	).format(**data)

	frappe.throw(message, title=title)


def override_calculate_tax_by_tax_slab(
    self, annual_taxable_earning, tax_slab, eval_globals=None, eval_locals=None
):
    eval_locals.update({"annual_taxable_earning": annual_taxable_earning})
    base_tax = 0
    rebate = 0
    other_taxes_and_charges = 0


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
        if (
            flt(d.min_taxable_income)
            and flt(d.min_taxable_income) > annual_taxable_earning
        ):
            continue
        if (
            flt(d.max_taxable_income)
            and flt(d.max_taxable_income) < annual_taxable_earning
        ):
            continue

        charge_percent = flt(d.percent)
        charge = base_tax * charge_percent / 100.0
        other_taxes_and_charges += charge



    final_tax = (
        base_tax + other_taxes_and_charges
    )

    return round(final_tax, 2), round(other_taxes_and_charges, 2)
