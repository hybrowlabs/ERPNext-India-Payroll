import frappe
import datetime
from frappe.query_builder.functions import Count, Sum
import json
from frappe.query_builder import Order
from frappe import _
import math




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
from datetime import datetime, timedelta
from hrms.payroll.doctype.payroll_period.payroll_period import get_period_factor
from collections import defaultdict

class CustomSalarySlip(SalarySlip):
    def on_submit(self):
        super().on_submit()
        self.insert_bonus_accruals()
        self.employee_accrual_insert()
        self.update_benefit_claim_amount()


    def before_save(self):

        self.actual_amount_ctc()
        self.update_declaration_component()
        self.arrear_ytd()
        self.food_coupon_tax()
        self.tax_calculation()
        self.calculate_grosspay()



    def validate(self):
        super().validate()
        self.set_month()
        self.set_sub_period()
        self.apply_lop_amount_in_reimbursement_component()
        self.insert_lopreversal_days()
        self.update_total_lop()
        self.set_taxale_regime()

    def on_cancel(self):
        super().on_cancel()
        self.delete_bonus_accruals()
        self.delete_benefit_accruals()



    def delete_bonus_accruals(self):
        bonus_accruals = frappe.get_list(
            'Employee Bonus Accrual',
            filters={
                'salary_slip': self.name,
                'payroll_entry': self.payroll_entry,
                'payroll_period': self.custom_payroll_period,
            },
            fields=['name']
        )

        if bonus_accruals:
            for accrual in bonus_accruals:
                bonus_doc = frappe.get_doc('Employee Bonus Accrual', accrual.name)
                bonus_doc.delete()

    def delete_benefit_accruals(self):
        benefit_accruals = frappe.get_list(
            'Employee Benefit Accrual',
            filters={
                'salary_slip': self.name,
                'payroll_entry': self.payroll_entry,
                'payroll_period': self.custom_payroll_period,
            },
            fields=['name']
        )
        if benefit_accruals:
            for accrual in benefit_accruals:
                benefit_doc = frappe.get_doc('Employee Benefit Accrual', accrual.name)
                benefit_doc.delete()


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










    def insert_bonus_accruals(self):
        for bonus in self.earnings:
            bonus_component = frappe.get_doc("Salary Component", bonus.salary_component)

            if bonus_component.custom_is_accrual == 1:
                existing_accruals = frappe.get_list(
                    'Employee Bonus Accrual',
                    filters={
                        'salary_slip': self.name,
                        'salary_component': bonus_component.name,
                        'payroll_entry': self.payroll_entry,
                        'payroll_period': self.custom_payroll_period
                    },
                    limit=1
                )

                if not existing_accruals:
                    accrual_doc = frappe.new_doc("Employee Bonus Accrual")
                    accrual_doc.amount = bonus.amount
                    accrual_doc.employee = self.employee
                    accrual_doc.accrual_date = self.posting_date
                    accrual_doc.salary_structure = self.salary_structure
                    accrual_doc.salary_structure_assignment = self.custom_salary_structure_assignment
                    accrual_doc.salary_component = bonus.salary_component
                    accrual_doc.payroll_entry = self.payroll_entry
                    accrual_doc.salary_slip = self.name
                    accrual_doc.payroll_period = self.custom_payroll_period

                    accrual_doc.insert()
                    accrual_doc.submit()



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




    def insert_loan_perquisite(self):
        if self.custom_payroll_period:

            get_payroll_period = frappe.get_list(
            'Payroll Period',
            filters={
                'company': self.company,
                'name': self.custom_payroll_period
            },
            fields=['*']
            )


            if get_payroll_period:
                start_date = frappe.utils.getdate(get_payroll_period[0].start_date)
                end_date = frappe.utils.getdate(get_payroll_period[0].end_date)



                loan_repayments = frappe.get_list(
                    'Loan Repayment Schedule',
                    filters={
                        'custom_employee': self.employee,
                        'status': 'Active',
                        'docstatus':1
                    },
                    fields=['*']
                )
                if loan_repayments:
                    sum=0
                    for repayment in loan_repayments:
                        get_each_perquisite=frappe.get_doc("Loan Repayment Schedule",repayment.name)
                        if len(get_each_perquisite.custom_loan_perquisite)>0:
                            for date in get_each_perquisite.custom_loan_perquisite:

                                payment_date = frappe.utils.getdate(date.payment_date)
                                if start_date <= payment_date <= end_date:
                                    sum=sum+date.perquisite_amount

                    self.custom_perquisite_amount=sum



    def insert_other_perquisites(self):
        latest_salary_structure = frappe.get_list(
            'Salary Structure Assignment',
            filters={'employee': self.employee, 'docstatus': 1},
            fields=["name"],
            order_by='from_date desc',
            limit=1
        )

        if latest_salary_structure:
            salary_structure_doc = frappe.get_doc("Salary Structure Assignment", latest_salary_structure[0].name)

            existing_components = [earning.salary_component for earning in self.earnings]

            for perquisite in salary_structure_doc.custom_other_perquisites:
                get_tax=frappe.get_doc("Salary Component",perquisite.title)

                if get_tax.is_tax_applicable==1 and get_tax.custom_tax_exemption_applicable_based_on_regime==1:
                    if get_tax.custom_regime=="All":
                        is_tax_applicable=get_tax.is_tax_applicable
                        custom_regime=get_tax.custom_regime
                        custom_tax_exemption_applicable_based_on_regime=get_tax.custom_tax_exemption_applicable_based_on_regime

                    elif get_tax.custom_regime==tax_component:
                        is_tax_applicable=get_tax.is_tax_applicable
                        custom_regime=get_tax.custom_regime
                        custom_tax_exemption_applicable_based_on_regime=get_tax.custom_tax_exemption_applicable_based_on_regime
                    elif get_tax.custom_regime!=tax_component:
                        is_tax_applicable=0
                        custom_regime=get_tax.custom_regime
                        custom_tax_exemption_applicable_based_on_regime=get_tax.custom_tax_exemption_applicable_based_on_regime

                elif get_tax.is_tax_applicable==0 and get_tax.custom_tax_exemption_applicable_based_on_regime==0:
                    is_tax_applicable=0
                    custom_regime=get_tax.custom_regime
                    custom_tax_exemption_applicable_based_on_regime=get_tax.custom_tax_exemption_applicable_based_on_regime
                elif get_tax.is_tax_applicable==1 and get_tax.custom_tax_exemption_applicable_based_on_regime==0:
                    is_tax_applicable=1
                    custom_regime=get_tax.custom_regime
                    custom_tax_exemption_applicable_based_on_regime=get_tax.custom_tax_exemption_applicable_based_on_regime


                if perquisite.title not in existing_components:
                    self.append("earnings", {
                        "salary_component": perquisite.title,
                        "amount": perquisite.amount/12,
                        "is_tax_applicable":is_tax_applicable,
                        "custom_regime":custom_regime,
                        "custom_tax_exemption_applicable_based_on_regime":custom_tax_exemption_applicable_based_on_regime

                    })







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

    def food_coupon_tax(self):
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
                if earning.is_tax_applicable == 0 and earning.custom_regime == "New Regime":
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
        arrear_ytd_sum = defaultdict(float)
        for slip in arrear_slips:
            doc = frappe.get_doc("Salary Slip", slip.name)

            for section in ["earnings", "deductions"]:
                for row in doc.get(section):
                    component_doc = frappe.get_doc("Salary Component", row.salary_component)

                    if component_doc.custom_component:
                        arrear_ytd_sum[component_doc.custom_component] += row.amount

        for row in self.earnings:
            if row.salary_component in arrear_ytd_sum:
                row.custom_arrear_ytd = arrear_ytd_sum[row.salary_component]

        for row in self.deductions:
            if row.salary_component in arrear_ytd_sum:
                row.custom_arrear_ytd = arrear_ytd_sum[row.salary_component]



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



                    if earning_component_data.custom_is_arrear == 0:
                        future_nps_value = (
                            earning.custom_actual_amount or 0
                        ) * self.custom_month_count




                if earning.salary_component == current_basic:
                    current_basic_value += earning.amount
                    if earning_component_data.custom_is_arrear == 0:
                        future_basic_value = (earning.custom_actual_amount) * (
                            self.custom_month_count
                        )
                if earning.salary_component == current_hra:
                    current_hra_value += earning.amount
                    if earning_component_data.custom_is_arrear == 0:
                        future_hra_value = (earning.custom_actual_amount) * (
                            self.custom_month_count
                        )



        if self.deductions:
            for deduction in self.deductions:
                deduction_component_data = frappe.get_doc(
                    "Salary Component", deduction.salary_component
                )
                if deduction_component_data.component_type == "Provident Fund":
                    current_epf_value += deduction.amount
                    if deduction_component_data.custom_is_arrear == 0:
                        future_epf_value = (deduction.custom_actual_amount) * (
                            self.custom_month_count
                        )
                if deduction_component_data.component_type == "Professional Tax":
                    current_pt_value += deduction.amount

                    if deduction_component_data.custom_is_arrear == 0:
                        future_pt_value = (deduction.custom_actual_amount) * (
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
                form_data = json.loads(declaration[0].custom_declaration_form_data or '{}')
                get_each_doc = frappe.get_doc("Employee Tax Exemption Declaration", declaration[0].name)

                total_nps = round(previous_nps_value + future_nps_value + current_nps_value)
                form_data['nineNumber'] = total_nps
                total_pf = min(round(previous_epf_value + future_epf_value + current_epf_value), 150000)
                form_data['pfValue'] = total_pf
                total_pt=round(previous_pt_value + future_pt_value + current_pt_value)
                form_data['nineteenNumber'] = total_pt

                for subcategory in get_each_doc.declarations:
                    check_component=frappe.get_doc("Employee Tax Exemption Sub Category",subcategory.exemption_sub_category)
                    if check_component.custom_component_type=="NPS":
                        subcategory.amount=total_nps
                    if check_component.custom_component_type=="Provident Fund":
                        subcategory.amount=total_pf
                    if check_component.custom_component_type=="Professional Tax":
                        subcategory.amount=total_pt

                get_each_doc.custom_posting_date = self.posting_date
                get_each_doc.custom_declaration_form_data = json.dumps(form_data)
                get_each_doc.save()


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
                            filters={'employee': self.employee, 'payroll_period': self.custom_payroll_period,"docstatus":1,'company':self.company},
                            fields=['*'],
                        )
            if declaration:
                form_data = json.loads(declaration[0].custom_declaration_form_data or '{}')
                get_each_doc = frappe.get_doc("Employee Tax Exemption Declaration", declaration[0].name)

                form_data['nineNumber'] = round(previous_nps_value+future_nps_value+current_nps_value)


                get_each_doc.custom_posting_date=self.posting_date
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




    def actual_amount_ctc(self):
        if self.earnings:
            for earning in self.earnings:
                if earning.depends_on_payment_days == 1:
                    if self.payment_days and self.payment_days > 0:
                        earning.custom_actual_amount = (earning.amount * self.total_working_days) / self.payment_days
                    else:
                        earning.custom_actual_amount = 0
                else:
                    earning.custom_actual_amount = earning.amount


        if self.deductions:
            for deduction in self.deductions:
                component_doc = frappe.get_doc("Salary Component", deduction.salary_component)
                original_amount = float(deduction.amount or 0)

                if deduction.depends_on_payment_days == 1:
                    if self.payment_days and self.payment_days > 0:
                        deduction.custom_actual_amount = (original_amount * self.total_working_days) / self.payment_days
                    else:
                        deduction.custom_actual_amount = 0

                    if component_doc.component_type == "ESIC":
                        deduction.amount = math.ceil(original_amount)
                else:
                    deduction.custom_actual_amount = original_amount


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


    @frappe.whitelist()
    def insert_lopreversal_days(self):
        benefit_application_days = frappe.get_list(
            'LOP Reversal',
            filters={
                'employee': self.employee,
                'additional_salary_date': ['between', [self.start_date, self.end_date]],
                'docstatus': 1
            },
            fields=['number_of_days']
        )

        if benefit_application_days:
            total_lop_days = sum(days['number_of_days'] for days in benefit_application_days)
            self.custom_lop_reversal_days = total_lop_days
        else:
            self.custom_lop_reversal_days = 0








    def loan_perquisite(self):
        loan_perquisite_component = frappe.get_value(
            'Salary Component',
            filters={'component_type': 'Loan Perquisite'},
            fieldname='name'
        )

        if not loan_perquisite_component:
            return

        loan_repayments = frappe.get_list(
            'Loan Repayment Schedule',
            filters={
                'custom_employee': self.employee,
                'status': 'Active',
                'docstatus':1
            },
            fields=['name']
        )

        if not loan_repayments:
            return

        self.start_date = frappe.utils.getdate(self.start_date)
        self.end_date = frappe.utils.getdate(self.end_date)

        perquisite_amount_array = []
        for repayment in loan_repayments:
            loan_repayment_doc = frappe.get_doc('Loan Repayment Schedule', repayment.name)
            for perquisite in loan_repayment_doc.custom_loan_perquisite:
                payment_date = frappe.utils.getdate(perquisite.payment_date)
                if self.start_date <= payment_date <= self.end_date:
                    perquisite_amount_array.append(perquisite.perquisite_amount)

        if perquisite_amount_array:
            existing_components = {earning.salary_component for earning in self.earnings}

            if loan_perquisite_component not in existing_components:
                self.append("earnings", {
                    "salary_component": loan_perquisite_component,
                    "amount": sum(perquisite_amount_array)
                })






    def employee_accrual_insert(self) :
        if self.custom_salary_structure_assignment:
            child_doc = frappe.get_doc('Salary Structure Assignment',self.custom_salary_structure_assignment)
            if child_doc.custom_employee_reimbursements:
                for i in child_doc.custom_employee_reimbursements:
                    accrual_insert = frappe.get_doc({
                        'doctype': 'Employee Benefit Accrual',
                        'employee': self.employee,
                        'payroll_entry': self.payroll_entry,
                        'amount': round((i.monthly_total_amount/self.total_working_days)*self.payment_days),
                        'salary_component': i.reimbursements,
                        'benefit_accrual_date': self.posting_date,
                        'salary_slip':self.name,
                        'payroll_period':child_doc.custom_payroll_period

                        })
                    accrual_insert.insert()
                    accrual_insert.submit()


    def calculate_grosspay(self):
        gross_pay_sum = 0
        gross_pay_year_sum = 0

        if self.earnings:
            for gross_pay in self.earnings:
                if not gross_pay.salary_component:
                    continue

                component = frappe.get_doc('Salary Component', gross_pay.salary_component)

                if component.custom_is_part_of_gross_pay == 1:
                    gross_pay_sum += gross_pay.amount or 0
                    gross_pay_year_sum += (gross_pay.year_to_date or 0) + (gross_pay.custom_arrear_ytd or 0)

        self.custom_statutory_grosspay = round(gross_pay_sum)
        self.custom_statutory_year_to_date = round(gross_pay_year_sum)





    def set_taxale_regime(self):
        for earning in self.earnings:
            get_tax_component=frappe.get_doc("Salary Component",earning.salary_component)
            earning.custom_tax_exemption_applicable_based_on_regime=get_tax_component.custom_tax_exemption_applicable_based_on_regime
            earning.custom_regime=get_tax_component.custom_regime





    # def add_employee_benefits(self):
    #     pass



    # def tax_calculation(self):

    #     frappe.msgprint(str(self.employee))


    #     latest_salary_structure = frappe.get_list('Salary Structure Assignment',
    #                     filters={'employee': self.employee,'docstatus':1},
    #                     fields=["*"],
    #                     order_by='from_date desc',
    #                     limit=1
    #                 )

    #     if self.annual_taxable_amount:
    #         self.custom_taxable_amount=round(self.annual_taxable_amount)

    #     if self.ctc and self.non_taxable_earnings:
    #         self.custom_total_income_with_taxable_component=round(self.ctc-self.non_taxable_earnings)

    #     if latest_salary_structure[0].income_tax_slab:
    #         payroll_period=latest_salary_structure[0].custom_payroll_period
    #         income_doc = frappe.get_doc('Income Tax Slab', latest_salary_structure[0].income_tax_slab)
    #         total_value=[]
    #         from_amount=[]
    #         to_amount=[]
    #         percentage=[]
    #         total_array=[]
    #         difference=[]

    #         rebate=income_doc.custom_taxable_income_is_less_than
    #         max_amount=income_doc.custom_maximum_amount

    #         for i in income_doc.slabs:

    #             array_list={
    #                 'from':i.from_amount,
    #                 'to':i.to_amount,
    #                 'percent':i.percent_deduction
    #                 }

    #             total_array.append(array_list)
    #         for slab in total_array:

    #             if slab['to'] == 0.0:
    #                 if round(self.annual_taxable_amount) >= slab['from']:
    #                     tt1=round(self.annual_taxable_amount)-slab['from']
    #                     tt2=slab['percent']
    #                     tt3=round((tt1*tt2)/100)

    #                     tt4=slab['from']
    #                     tt5=slab['to']

    #                     remaining_slabs = [s for s in total_array if s['from'] != slab['from'] and s['from'] < slab['from']]
    #                     for slab in remaining_slabs:
    #                         from_amount.append(slab['from'])
    #                         to_amount.append(slab['to'])
    #                         percentage.append(slab["percent"])
    #                         difference.append(slab['to']-slab['from'])
    #                         total_value.append((slab['to']-slab['from'])*slab["percent"]/100)
    #                     from_amount.append(tt4)
    #                     to_amount.append(tt5)
    #                     percentage.append(tt2)
    #                     difference.append(tt1)
    #                     total_value.append(tt3)
    #                 self.custom_tax_slab = []
    #                 for i in range(len(from_amount)):
    #                         self.append("custom_tax_slab", {
    #                         "from_amount": from_amount[i],
    #                         "to_amount": to_amount[i],
    #                         "percentage":  percentage[i]   ,
    #                         "tax_amount":total_value[i],
    #                         "amount":difference[i]
    #                     })

    #             else:
    #                 if slab['from'] <= round(self.annual_taxable_amount) <= slab['to']:
    #                     tt1=round(self.annual_taxable_amount)-slab['from']
    #                     tt2=slab['percent']
    #                     tt3=(tt1*tt2)/100
    #                     tt4=slab['from']
    #                     tt5=slab['to']
    #                     remaining_slabs = [s for s in total_array if s['from'] != slab['from'] and s['from'] < slab['from']]

    #                     for slab in remaining_slabs:
    #                         from_amount.append(slab['from'])
    #                         to_amount.append(slab['to'])
    #                         percentage.append(slab["percent"])
    #                         difference.append(slab['to']-slab['from'])
    #                         total_value.append((slab['to']-slab['from'])*slab["percent"]/100)
    #                     from_amount.append(tt4)
    #                     to_amount.append(tt5)
    #                     percentage.append(tt2)
    #                     difference.append(tt1)
    #                     total_value.append(tt3)

    #                 self.custom_tax_slab = []
    #                 for i in range(len(from_amount)):
    #                         self.append("custom_tax_slab", {
    #                         "from_amount": from_amount[i],
    #                         "to_amount": to_amount[i],
    #                         "percentage":  percentage[i]   ,
    #                         "tax_amount":total_value[i],
    #                         "amount":difference[i]
    #                     })



    #         total_sum = sum(total_value)

    #         if self.custom_taxable_amount<rebate:

    #             self.custom_tax_on_total_income=total_sum
    #             self.custom_rebate_under_section_87a=total_sum
    #             self.custom_total_tax_on_income=0
    #         else:
    #             self.custom_total_tax_on_income=total_sum
    #             self.custom_rebate_under_section_87a=0
    #             self.custom_tax_on_total_income=total_sum-0

    #         if self.custom_taxable_amount>5000000:

    #             surcharge_m=(self.custom_total_tax_on_income*10)/100

    #             self.custom_surcharge=round(surcharge_m)
    #             self.custom_education_cess=round((surcharge_m+self.custom_total_tax_on_income)*4/100)
    #         else:

    #             self.custom_surcharge=0
    #             self.custom_education_cess=(self.custom_surcharge+self.custom_total_tax_on_income)*4/100


    #         self.custom_total_amount=round(self.custom_surcharge+self.custom_education_cess+self.custom_total_tax_on_income)


    def tax_calculation(self):
        latest_salary_structure = frappe.get_list(
            'Salary Structure Assignment',
            filters={'employee': self.employee, 'docstatus': 1,"from_date": ("<=", self.end_date)},
            fields=["*"],
            order_by='from_date desc',
            limit=1
        )

        # Set taxable amount and total income with taxable components
        if self.annual_taxable_amount:
            self.custom_taxable_amount = round(self.annual_taxable_amount)

        if self.ctc and self.non_taxable_earnings:
            self.custom_total_income_with_taxable_component = round(self.ctc - self.non_taxable_earnings)

        # Proceed only if Income Tax Slab is defined
        if latest_salary_structure and latest_salary_structure[0].income_tax_slab:
            income_doc = frappe.get_doc('Income Tax Slab', latest_salary_structure[0].income_tax_slab)
            total_array = []
            from_amount, to_amount, percentage, difference, total_value = [], [], [], [], []

            rebate = income_doc.custom_taxable_income_is_less_than
            max_amount = income_doc.custom_maximum_amount

            # Prepare slab ranges
            for i in income_doc.slabs:
                total_array.append({
                    'from': i.from_amount,
                    'to': i.to_amount,
                    'percent': i.percent_deduction
                })

            self.custom_tax_slab = []  # Clear any existing entries

            for slab in total_array:
                taxable = round(self.annual_taxable_amount)

                if slab['to'] == 0.0:
                    # For open-ended upper slab
                    if taxable >= slab['from']:
                        taxable_diff = taxable - slab['from']
                        tax_percent = slab['percent']
                        tax_amount = round((taxable_diff * tax_percent) / 100)

                        # Add previous slabs
                        remaining_slabs = [s for s in total_array if s['from'] < slab['from']]
                        for s in remaining_slabs:
                            from_amount.append(s['from'])
                            to_amount.append(s['to'])
                            percentage.append(s["percent"])
                            difference.append(s['to'] - s['from'])
                            total_value.append((s['to'] - s['from']) * s["percent"] / 100)

                        # Current slab
                        from_amount.append(slab['from'])
                        to_amount.append(slab['to'])
                        percentage.append(tax_percent)
                        difference.append(taxable_diff)
                        total_value.append(tax_amount)
                        break  # Since it covers the remaining amount

                else:
                    # Slab with upper limit
                    if slab['from'] <= taxable <= slab['to']:
                        taxable_diff = taxable - slab['from']
                        tax_percent = slab['percent']
                        tax_amount = (taxable_diff * tax_percent) / 100

                        # Add previous slabs
                        remaining_slabs = [s for s in total_array if s['from'] < slab['from']]
                        for s in remaining_slabs:
                            from_amount.append(s['from'])
                            to_amount.append(s['to'])
                            percentage.append(s["percent"])
                            difference.append(s['to'] - s['from'])
                            total_value.append((s['to'] - s['from']) * s["percent"] / 100)

                        # Current slab
                        from_amount.append(slab['from'])
                        to_amount.append(slab['to'])
                        percentage.append(tax_percent)
                        difference.append(taxable_diff)
                        total_value.append(tax_amount)
                        break

            # Populate tax slab child table
            for i in range(len(from_amount)):
                self.append("custom_tax_slab", {
                    "from_amount": from_amount[i],
                    "to_amount": to_amount[i],
                    "percentage": percentage[i],
                    "tax_amount": total_value[i],
                    "amount": difference[i]
                })

            # Total tax amount
            total_sum = sum(total_value)

            # Section 87A rebate logic
            if self.custom_taxable_amount < rebate:
                self.custom_tax_on_total_income = total_sum
                self.custom_rebate_under_section_87a = total_sum
                self.custom_total_tax_on_income = 0
            else:
                self.custom_rebate_under_section_87a = 0
                self.custom_tax_on_total_income = total_sum
                self.custom_total_tax_on_income = total_sum

            # Surcharge and cess logic
            if self.custom_taxable_amount > 5000000:
                surcharge = (self.custom_total_tax_on_income * 10) / 100
                self.custom_surcharge = round(surcharge)
            else:
                self.custom_surcharge = 0

            self.custom_education_cess = round((self.custom_total_tax_on_income + self.custom_surcharge) * 4 / 100)

            # Final total tax payable
            self.custom_total_amount = round(
                self.custom_total_tax_on_income + self.custom_surcharge + self.custom_education_cess
            )
