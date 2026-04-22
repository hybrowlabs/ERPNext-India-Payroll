"""
Tax calculation mixin for CustomSalarySlip.

Covers variable tax, income-tax breakup, taxable-earnings queries,
regime-aware component flagging, and the custom tax-slab child table.
"""

import frappe
from frappe.query_builder.functions import Sum
from frappe.utils import cstr, flt
from hrms.payroll.doctype.salary_slip.salary_slip import eval_tax_slab_condition

# ---------------------------------------------------------------------------
# Module-level helpers (used by the mixin and by CustomSalarySlip directly)
# ---------------------------------------------------------------------------


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
        and tax_slab.custom_minmum_value < annual_taxable_earning < tax_slab.custom_maximun_value
    ):
        excess_income = annual_taxable_earning - tax_slab.custom_minmum_value
        if base_tax > excess_income:
            rebate = base_tax - excess_income
            base_tax -= rebate

    for d in tax_slab.other_taxes_and_charges:
        if flt(d.min_taxable_income) and flt(d.min_taxable_income) > annual_taxable_earning:
            continue
        if flt(d.max_taxable_income) and flt(d.max_taxable_income) < annual_taxable_earning:
            continue
        other_taxes_and_charges += base_tax * flt(d.percent) / 100.0

    return round(base_tax + other_taxes_and_charges, 2), round(other_taxes_and_charges, 2)


# ---------------------------------------------------------------------------
# Mixin
# ---------------------------------------------------------------------------


class TaxMixin:
    def set_taxable_regime(self) -> None:
        """Stamp each earning row with the regime flags from its Salary Component."""
        for earning in self.earnings:
            sc = frappe.get_cached_doc("Salary Component", earning.salary_component)
            earning.custom_tax_exemption_applicable_based_on_regime = (
                sc.custom_tax_exemption_applicable_based_on_regime
            )
            earning.custom_regime = sc.custom_regime

    # kept the original misspelled name as an alias so existing calls don't break
    set_taxale_regime = set_taxable_regime

    def calculate_variable_tax(self, tax_component: str) -> float:
        self.previous_total_paid_taxes = self.get_tax_paid_in_period(
            self.payroll_period.start_date, self.start_date, tax_component
        )

        eval_locals, _ = self.get_data_for_eval()
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

        self.full_tax_on_additional_earnings = 0.0
        if self.current_additional_earnings_with_full_tax:
            self.total_tax_amount, __ = override_calculate_tax_by_tax_slab(
                self,
                self.total_taxable_earnings,
                self.tax_slab,
                self.whitelisted_globals,
                eval_locals,
            )
            self.full_tax_on_additional_earnings = self.total_tax_amount - self.total_structured_tax_amount

        current_tax_amount = max(
            0.0,
            self.current_structured_tax_amount + self.full_tax_on_additional_earnings,
        )

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

    def get_taxable_earnings(self, allow_tax_exemption=False, based_on_payment_days=0):
        taxable_earnings = 0
        additional_income = 0
        additional_income_with_full_tax = 0
        flexi_benefits = 0
        amount_exempted_from_income_tax = 0

        latest_ssa = frappe.get_list(
            "Salary Structure Assignment",
            filters={"employee": self.employee, "docstatus": 1},
            fields=["custom_tax_regime"],
            order_by="from_date desc",
            limit=1,
        )
        tax_component = latest_ssa[0].custom_tax_regime if latest_ssa else None

        for earning in self.earnings:
            sc = frappe.get_cached_doc("Salary Component", earning.salary_component)

            if sc.is_tax_applicable and sc.custom_tax_exemption_applicable_based_on_regime:
                regime_match = sc.custom_regime in ("All", tax_component)
                earning.is_tax_applicable = 1 if regime_match else 0
            elif sc.is_tax_applicable and not sc.custom_tax_exemption_applicable_based_on_regime:
                earning.is_tax_applicable = 1
            else:
                earning.is_tax_applicable = 0

            earning.custom_regime = sc.custom_regime
            earning.custom_tax_exemption_applicable_based_on_regime = (
                sc.custom_tax_exemption_applicable_based_on_regime
            )

            if based_on_payment_days:
                amount, additional_amount = self.get_amount_based_on_payment_days(earning)
            else:
                amount = earning.amount
                additional_amount = earning.additional_amount or 0
                if not additional_amount:
                    amount = earning.default_amount

            if not earning.is_tax_applicable:
                continue

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
                if not ded.exempted_from_income_tax:
                    continue
                if based_on_payment_days:
                    amount, additional_amount = self.get_amount_based_on_payment_days(ded)
                else:
                    amount, additional_amount = ded.amount, ded.additional_amount

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

    def get_taxable_earnings_for_prev_period(self, start_date, end_date, allow_tax_exemption=False):
        exempted_amount = 0

        latest_ssa = frappe.get_list(
            "Salary Structure Assignment",
            filters={"employee": self.employee, "docstatus": 1},
            fields=["custom_tax_regime"],
            order_by="from_date desc",
            limit=1,
        )
        custom_tax_regime = latest_ssa[0].custom_tax_regime if latest_ssa else None

        regime_matched = any(e.custom_regime in (custom_tax_regime, "All") for e in self.earnings)

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

        opening_taxable_earning = self.get_opening_for("taxable_earnings_till_date", start_date, end_date)

        return (taxable_earnings + opening_taxable_earning) - exempted_amount, exempted_amount

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
        custom_tax_regime=None,
    ) -> float:
        ss = frappe.qb.DocType("Salary Slip")
        sd = frappe.qb.DocType("Salary Detail")

        field = sd.amount if field_to_select == "amount" else sd.additional_amount

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
        if custom_tax_exemption_applicable_based_on_regime is not None:
            query = query.where(
                sd.custom_tax_exemption_applicable_based_on_regime
                == custom_tax_exemption_applicable_based_on_regime
            )
        if custom_regime:
            query = query.where(sd.custom_regime == custom_regime)
        if custom_tax_regime:
            query = query.where(ss.custom_tax_regime == custom_tax_regime)

        result = query.run()
        return flt(result[0][0]) if result else 0.0

    def compute_income_tax_breakup(self) -> None:
        self.standard_tax_exemption_amount = 0
        self.tax_exemption_declaration = 0
        self.deductions_before_tax_calculation = 0
        self.custom_perquisite_amount = 0

        self.non_taxable_earnings = self.compute_non_taxable_earnings()
        self.ctc = self.compute_ctc()
        self.income_from_other_sources = self.get_income_form_other_sources()
        self.total_earnings = self.ctc + self.income_from_other_sources

        payroll_period = frappe.get_value(
            "Payroll Period",
            {"company": self.company, "name": self.payroll_period.name},
            ["name", "start_date", "end_date"],
            as_dict=True,
        )
        if not payroll_period:
            return

        start_date = frappe.utils.getdate(payroll_period["start_date"])
        end_date = frappe.utils.getdate(payroll_period["end_date"])

        loan_repayments = frappe.get_list(
            "Loan Repayment Schedule",
            filters={"custom_employee": self.employee, "status": "Active", "docstatus": 1},
            fields=["name"],
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

        if hasattr(self, "total_structured_tax_amount") and hasattr(self, "current_structured_tax_amount"):
            self.future_income_tax_deductions = (
                self.total_structured_tax_amount
                + self.get("full_tax_on_additional_earnings", 0)
                - self.income_tax_deducted_till_date
            )
            self.current_month_income_tax = self.current_structured_tax_amount + self.get(
                "full_tax_on_additional_earnings", 0
            )
            self.total_income_tax = self.income_tax_deducted_till_date + self.future_income_tax_deductions

    def tax_calculation(self) -> None:
        if self.annual_taxable_amount:
            self.custom_taxable_amount = round(self.annual_taxable_amount)

        if self.ctc and self.non_taxable_earnings:
            self.custom_total_income_with_taxable_component = round(self.ctc - self.non_taxable_earnings)

        latest_ssa = frappe.get_list(
            "Salary Structure Assignment",
            filters={
                "employee": self.employee,
                "docstatus": 1,
                "from_date": ("<=", self.end_date),
            },
            fields=["income_tax_slab"],
            order_by="from_date desc",
            limit=1,
        )

        if not (latest_ssa and latest_ssa[0].income_tax_slab):
            return

        income_doc = frappe.get_doc("Income Tax Slab", latest_ssa[0].income_tax_slab)
        rebate = income_doc.custom_taxable_income_is_less_than

        total_array = [
            {"from": s.from_amount, "to": s.to_amount, "percent": s.percent_deduction}
            for s in income_doc.slabs
        ]

        self.custom_tax_slab = []
        from_amount, to_amount, percentage, difference, total_value = [], [], [], [], []

        taxable = round(self.annual_taxable_amount)

        for slab in total_array:
            if slab["to"] == 0.0:
                if taxable < slab["from"]:
                    continue
                taxable_diff = taxable - slab["from"]
                tax_amount = round((taxable_diff * slab["percent"]) / 100)
            else:
                if not (slab["from"] <= taxable <= slab["to"]):
                    continue
                taxable_diff = taxable - slab["from"]
                tax_amount = (taxable_diff * slab["percent"]) / 100

            for s in [s for s in total_array if s["from"] < slab["from"]]:
                from_amount.append(s["from"])
                to_amount.append(s["to"])
                percentage.append(s["percent"])
                difference.append(s["to"] - s["from"])
                total_value.append((s["to"] - s["from"]) * s["percent"] / 100)

            from_amount.append(slab["from"])
            to_amount.append(slab["to"])
            percentage.append(slab["percent"])
            difference.append(taxable_diff)
            total_value.append(tax_amount)
            break

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

        total_sum = sum(total_value)

        if self.custom_taxable_amount < rebate:
            self.custom_tax_on_total_income = total_sum
            self.custom_rebate_under_section_87a = total_sum
            self.custom_total_tax_on_income = 0
        else:
            self.custom_rebate_under_section_87a = 0
            self.custom_tax_on_total_income = total_sum
            self.custom_total_tax_on_income = total_sum

        if self.custom_taxable_amount > 5_000_000:
            self.custom_surcharge = round(self.custom_total_tax_on_income * 10 / 100)
        else:
            self.custom_surcharge = 0

        self.custom_education_cess = round(
            (self.custom_total_tax_on_income + self.custom_surcharge) * 4 / 100
        )
        self.custom_total_amount = round(
            self.custom_total_tax_on_income + self.custom_surcharge + self.custom_education_cess
        )
