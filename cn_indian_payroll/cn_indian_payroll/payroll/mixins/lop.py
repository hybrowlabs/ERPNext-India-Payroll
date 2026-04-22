"""
LOP / attendance-cycle mixin for CustomSalarySlip.

Handles leave-without-pay, absent days, and the custom attendance-cycle
variant of get_working_days_details().
"""

import frappe
from frappe import _
from frappe.utils import add_days, cint, date_diff, flt, getdate
from dateutil.relativedelta import relativedelta


class LOPMixin:

    def insert_lopreversal_days(self) -> None:
        arrear_days = frappe.get_list(
            "Payroll Correction",
            filters={
                "employee": self.employee,
                "payroll_date": ["between", [self.start_date, self.end_date]],
                "docstatus": 1,
            },
            fields=["days_to_reverse"],
        )
        self.custom_lop_reversal_days = (
            sum(d["days_to_reverse"] for d in arrear_days) if arrear_days else 0
        )

    def update_total_lop(self) -> None:
        self.custom_total_leave_without_pay = (self.absent_days or 0) + self.leave_without_pay

    def get_working_days_details(self, lwp=None, for_preview=0, lwp_days_corrected=None):
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
            add_days(getdate(self.start_date), days=day) for day in range(0, working_days)
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
                actual_lwp, absent = self.calculate_lwp_ppl_and_absent_days_based_on_attendance_cycle(
                    holidays, daily_wages_fraction_for_half_day, consider_marked_attendance_on_holidays
                )
            else:
                actual_lwp, absent = self.calculate_lwp_ppl_and_absent_days_based_on_attendance(
                    holidays, daily_wages_fraction_for_half_day, consider_marked_attendance_on_holidays
                )
            self.absent_days = absent

        if payroll_settings.payroll_based_on == "Leave":
            if not payroll_settings.custom_configure_attendance_cycle:
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

            consider_unmarked_attendance_as = (
                payroll_settings.consider_unmarked_attendance_as or "Present"
            )

            if payroll_settings.payroll_based_on == "Attendance":
                if consider_unmarked_attendance_as == "Absent":
                    unmarked_days = self.get_unmarked_days(
                        payroll_settings.include_holidays_in_total_working_days, holidays
                    )
                    self.absent_days += unmarked_days
                    self.payment_days -= unmarked_days
                half_absent_days = self.get_half_absent_days(
                    consider_marked_attendance_on_holidays, holidays
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

        payroll_setting = frappe.get_doc("Payroll Settings")
        if not (
            payroll_setting.payroll_based_on == "Attendance"
            and payroll_setting.custom_configure_attendance_cycle
        ):
            return lwp, absent

        attendance_start_day = payroll_setting.custom_attendance_start_date
        attendance_end_day = payroll_setting.custom_attendance_end_date
        end_date = getdate(self.end_date)
        attendance_end_date = end_date.replace(day=attendance_end_day)
        attendance_start_date = (attendance_end_date - relativedelta(months=1)).replace(
            day=attendance_start_day
        )

        leave_type_map = self.get_leave_type_map()
        attendance_details = self.get_employee_attendance(
            start_date=attendance_start_date, end_date=attendance_end_date
        )

        for d in attendance_details:
            if (
                d.status in ("Half Day", "On Leave")
                and d.leave_type
                and d.leave_type not in leave_type_map
            ):
                continue

            if (
                not consider_marked_attendance_on_holidays
                and getdate(d.attendance_date) in holidays
            ):
                if d.status in ["Absent", "Half Day"] or (
                    d.leave_type
                    and d.leave_type in leave_type_map
                    and not leave_type_map[d.leave_type]["include_holiday"]
                ):
                    continue

            if d.leave_type:
                fraction_of_daily_salary_per_leave = leave_type_map[d.leave_type][
                    "fraction_of_daily_salary_per_leave"
                ]

            if d.status == "Half Day" and d.leave_type and d.leave_type in leave_type_map:
                equivalent_lwp = 1 - daily_wages_fraction_for_half_day
                if leave_type_map[d.leave_type]["is_ppl"]:
                    equivalent_lwp *= fraction_of_daily_salary_per_leave or 1
                lwp += equivalent_lwp

            elif d.status == "On Leave" and d.leave_type and d.leave_type in leave_type_map:
                equivalent_lwp = 1
                if leave_type_map[d.leave_type]["is_ppl"]:
                    equivalent_lwp *= fraction_of_daily_salary_per_leave or 1
                lwp += equivalent_lwp

            elif d.status == "Absent":
                absent += 1

        return lwp, absent
