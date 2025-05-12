import frappe
import datetime
from frappe.query_builder.functions import Count, Sum
import json
from frappe.query_builder import Order
from frappe import _




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






class CustomSalarySlip(SalarySlip):

    def validate(self):
        super().validate()
        self.set_sub_period()

    def on_submit(self):
        super().on_submit()
        self.insert_bonus_accruals()
        self.employee_accrual_insert()


    def before_save(self):

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

        # Fetch payroll period once
        payroll_period = frappe.get_value(
            'Payroll Period',
            {'company': self.company, 'name': self.payroll_period.name},
            ['name', 'start_date', 'end_date'],
            as_dict=True
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

        # Tax slab logic
        if hasattr(self, "tax_slab") and self.tax_slab:
            if self.tax_slab.allow_tax_exemption:
                self.standard_tax_exemption_amount = self.tax_slab.standard_tax_exemption_amount
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
            # Get the Salary Structure Assignment document
            salary_structure_doc = frappe.get_doc("Salary Structure Assignment", latest_salary_structure[0].name)

            # Get the list of existing salary components in earnings
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
                #condition for current tax  component
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
            # print(taxable_earnings,"taxable_earnings------")

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














    def get_taxable_earnings_for_prev_period(self, start_date, end_date, allow_tax_exemption=False):
        exempted_amount = 0
        taxable_earnings = 0


        latest_salary_structure = frappe.get_list('Salary Structure Assignment',
                        filters={'employee': self.employee,'docstatus':1},
                        fields=["*"],
                        order_by='from_date desc',
                        limit=1
                    )



        custom_tax_regime=latest_salary_structure[0].custom_tax_regime

        for earning in self.earnings:
            if custom_tax_regime==earning.custom_regime:

                taxable_earnings = self.get_salary_slip_details(
                        start_date, end_date, parentfield="earnings",
                        is_tax_applicable=1,
                        custom_tax_exemption_applicable_based_on_regime=1,

                    )

            else:

                taxable_earnings = self.get_salary_slip_details(
                        start_date, end_date, parentfield="earnings",
                        is_tax_applicable=1,
                        custom_regime="All"
                    )


        # Check if tax exemption is allowed and get exempted amount
        if allow_tax_exemption:
            exempted_amount = self.get_salary_slip_details(
                start_date, end_date, parentfield="deductions", exempted_from_income_tax=1
            )

        # Get opening taxable earnings for the period
        opening_taxable_earning = self.get_opening_for("taxable_earnings_till_date", start_date, end_date)

        # Calculate and return the final taxable earnings
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
        custom_taxable=None,
        custom_tax_regime=None
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
            query = query.where(sd.variable_based_on_taxable_salary == variable_based_on_taxable_salary)

        if salary_component:
            query = query.where(sd.salary_component == salary_component)

        if custom_tax_exemption_applicable_based_on_regime:
            query = query.where(sd.custom_tax_exemption_applicable_based_on_regime == custom_tax_exemption_applicable_based_on_regime)

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
        food_coupon_array = []

        for food_coupon_component in self.earnings:
            if food_coupon_component.is_tax_applicable==1 and food_coupon_component.custom_regime == "New Regime":

                get_fd_component = frappe.get_list(
                    'Salary Slip',
                    filters={
                        'employee': self.employee,
                        'custom_payroll_period': self.custom_payroll_period,
                        'docstatus': 1
                    },
                    fields=['name']
                )


                if len(get_fd_component) > 0:
                    for k in get_fd_component:
                        get_slip=frappe.get_doc("Salary Slip",k.name)
                        for m in get_slip.earnings:
                            if m.is_tax_applicable==0 and m.custom_regime == "New Regime":
                                food_coupon_array.append(m.amount)


            g1=sum(food_coupon_array)

            food_coupon_component.custom_total_ytd=g1




    def arrear_ytd(self):

        get_arrear_component = frappe.db.get_list('Salary Slip',
            filters={
                'employee': self.employee,
                'custom_payroll_period': self.custom_payroll_period,
                'docstatus': 1
            },
            fields=['name']
        )


        if get_arrear_component:

            arrear_ytd_sum = {}


            for arrear in get_arrear_component:

                if self.name != arrear.name:

                    get_arrear_doc = frappe.get_doc("Salary Slip", arrear.name)


                    if get_arrear_doc.earnings:
                        for earning in get_arrear_doc.earnings:

                            get_arrear = frappe.get_doc("Salary Component", earning.salary_component)


                            if get_arrear.custom_component:
                                arrear_component = get_arrear.custom_component

                                if arrear_component not in arrear_ytd_sum:
                                    arrear_ytd_sum[arrear_component] = 0

                                arrear_ytd_sum[arrear_component] += earning.amount

            for current_earning in self.earnings:
                if current_earning.salary_component in arrear_ytd_sum:
                    current_earning.custom_arrear_ytd = arrear_ytd_sum[current_earning.salary_component]





    # def new_joinee(self):
    #     if self.employee:
    #         employee_doc = frappe.get_doc("Employee", self.employee)

    #         start_date = frappe.utils.getdate(self.start_date)
    #         end_date = frappe.utils.getdate(self.end_date)

    #         if start_date <= employee_doc.date_of_joining <= end_date:
    #             self.custom_new_joinee="New Joinee"
    #         else:
    #             self.custom_new_joinee="-"


    def add_reimbursement_taxable_new_doc(self):
        if len(self.earnings)>0:
            for lta_component in self.earnings:
                get_lta=frappe.get_doc("Salary Component",lta_component.salary_component)
                if get_lta.component_type=="LTA Taxable":
                    if self.annual_taxable_amount:
                        self.annual_taxable_amount=self.annual_taxable_amount+lta_component.amount


    def update_declaration_component(self):
        if not self.employee:
            return

        current_basic=current_hra=None

        current_basic_value = current_hra_value = current_nps_value = current_epf_value = current_pt_value = 0
        previous_basic_value = previous_hra_value = previous_nps_value = previous_epf_value = previous_pt_value = 0
        future_basic_value = future_hra_value = future_nps_value = future_epf_value = future_pt_value = 0

        # basic_rule2=non_metro_or_metro=final_hra_exemption=0

        get_company = frappe.get_doc("Company", self.company)
        if get_company.basic_component:
            current_basic = get_company.basic_component
        if get_company.hra_component:
            current_hra = get_company.hra_component


        salary_components = {d.name: d.component_type for d in frappe.get_list('Salary Component', fields=['name', 'component_type'])}

        if self.earnings:
            for earning in self.earnings:
                component_type = salary_components.get(earning.salary_component)
                if component_type == "NPS":
                    current_nps_value = earning.amount
                    future_nps_value = (earning.custom_actual_amount) * (self.custom_month_count)
                if earning.salary_component == current_basic:
                    current_basic_value = earning.amount
                    future_basic_value = (earning.custom_actual_amount) * (self.custom_month_count)
                if earning.salary_component == current_hra:
                    current_hra_value = earning.amount
                    future_hra_value = (earning.custom_actual_amount) * (self.custom_month_count)




        if self.deductions:
            for deduction in self.deductions:
                component_type = salary_components.get(deduction.salary_component)
                if component_type == "Provident Fund":
                    current_epf_value = deduction.amount
                    future_epf_value = (deduction.default_amount)*(self.custom_month_count)
                elif component_type == "Professional Tax":
                    current_pt_value = deduction.amount
                    future_pt_value = (deduction.default_amount)*(self.custom_month_count)

        get_previous_salary_slip = frappe.get_list(
            'Salary Slip',
            filters={
                'employee': self.employee,
                'custom_payroll_period': self.custom_payroll_period,
                'docstatus': 1,
                'name': ['!=', self.name]
            },
            fields=['name']
        )
        if get_previous_salary_slip:
                for slip in get_previous_salary_slip:
                    previous_salary_slip = frappe.get_doc("Salary Slip", slip.name)
                    if previous_salary_slip.earnings:
                        for earning in previous_salary_slip.earnings:
                            component_type = salary_components.get(earning.salary_component)
                            if component_type == "NPS":
                                previous_nps_value = earning.amount
                            if earning.salary_component == current_basic:
                                previous_basic_value = earning.amount
                            if earning.salary_component == current_hra:
                                previous_hra_value = earning.amount

                    if previous_salary_slip.deductions:
                        for deduction in previous_salary_slip.deductions:
                            component_type = salary_components.get(deduction.salary_component)
                            if component_type == "Provident Fund":
                                previous_epf_value = deduction.amount
                            elif component_type == "Professional Tax":
                                previous_pt_value = deduction.amount


        if self.custom_tax_regime=="Old Regime":
            declaration = frappe.get_list(
                            'Employee Tax Exemption Declaration',
                            filters={'employee': self.employee, 'payroll_period': self.custom_payroll_period,"docstatus":1,'company':self.company},
                            fields=['*'],
                        )
            if declaration:
                form_data = json.loads(declaration[0].custom_declaration_form_data or '{}')
                get_each_doc = frappe.get_doc("Employee Tax Exemption Declaration", declaration[0].name)


                form_data['nineNumber'] = round(previous_nps_value+future_nps_value+current_nps_value)
                form_data['pfValue'] = min(round(previous_epf_value + future_epf_value + current_epf_value), 150000)
                form_data['nineteenNumber'] = round(previous_pt_value+future_pt_value+current_pt_value)




                get_each_doc.custom_posting_date=self.posting_date
                get_each_doc.custom_declaration_form_data = json.dumps(form_data)

                if get_each_doc.monthly_house_rent>0:

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


                            # HRA Exemption rule
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

                get_each_doc.save()
                frappe.db.commit()
                self.tax_exemption_declaration=get_each_doc.total_exemption_amount


    def tax_declartion_insert(self):
        tax_declaration_doc=frappe.db.get_list('Employee Tax Exemption Declaration',
                    filters={

                        'employee':self.employee,
                        'docstatus':1,
                        'payroll_period':self.custom_payroll_period,

                    },
                    fields=['*'],

                )
        if tax_declaration_doc:
            declaration_child_doc = frappe.get_doc('Employee Tax Exemption Declaration', tax_declaration_doc[0].name)
            self.custom_declaration=[]
            for k in declaration_child_doc.declarations:
                self.append("custom_declaration", {
                    "exemption_sub_category": k.exemption_sub_category,
                    "exemption_category":k.exemption_category,
                    "maximum_exempted_amount":k.max_amount,
                    "declared_amount":k.amount
                })



    def update_bonus_accrual(self):
        for bonus in self.earnings:
            bonus_component=frappe.get_doc("Salary Component",bonus.salary_component)
            if bonus_component.custom_is_accrual==1:
                # frappe.msgprint(str(bonus_component.name))

                bonus_accrual= frappe.get_list(
                        'Employee Bonus Accrual',
                        filters={'salary_slip': self.name},
                        fields=['*'],

                    )

                if len(bonus_accrual)>0:
                    # frappe.msgprint(str(bonus_accrual[0].name))
                    accrual_each_doc=frappe.get_doc("Employee Bonus Accrual",bonus_accrual[0].name)
                    accrual_each_doc.amount=bonus.amount
                    accrual_each_doc.save()








    def remaining_day(self):
        fiscal_year = frappe.get_list(
        'Payroll Period',
        fields=['*'],
        order_by='end_date desc',
        limit=1
        )

        if fiscal_year:
            t1 = fiscal_year[0].end_date
            t2 = self.end_date


            if not isinstance(t1, str):
                t1 = str(t1)
            if not isinstance(t2, str):
                t2 = str(t2)

            t1_parts = t1.split('-')
            t2_parts = t2.split('-')

            t1_year = int(t1_parts[0])
            t1_month = int(t1_parts[1])
            t1_day = int(t1_parts[2])

            t2_year = int(t2_parts[0])
            t2_month = int(t2_parts[1])
            t2_day = int(t2_parts[2])


            months_t2_to_t1 = (t1_year - t2_year) * 12 + (t1_month - t2_month)
            self.custom_month_count=months_t2_to_t1





    def set_month(self):



        date_str = str(self.start_date)


        month_str = date_str[5:7]


        month_number = int(month_str)


        month_names = ["", "January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"]

        month_name = month_names[month_number]

        self.custom_month=month_name










    def actual_amount(self):
        if self.leave_without_pay==0:
            if len(self.earnings)>0:
                for k in self.earnings:
                    k.custom_actual_amount=k.amount



    def actual_amount_ctc(self):
        if self.earnings:
            for k in self.earnings:
                salary_component_doc = frappe.get_doc("Salary Component", k.salary_component)

                if salary_component_doc.custom_is_arrear == 0:
                    if self.payment_days and self.payment_days > 0:
                        k.custom_actual_amount = (k.amount * self.total_working_days) / self.payment_days
                    else:
                        k.custom_actual_amount = 0
                else:
                    k.custom_actual_amount = 0











    def accrual_update(self):
        if self.leave_without_pay > 0:
            ss_assignment = frappe.get_list(
                'Salary Structure Assignment',
                filters={'employee': self.employee, 'docstatus': 1},
                fields=['name'],
                order_by='from_date desc',
                limit=1
            )

            if ss_assignment:
                child_doc = frappe.get_doc('Salary Structure Assignment', ss_assignment[0].name)

                for i in child_doc.custom_employee_reimbursements:
                    get_benefit_accrual = frappe.db.get_list(
                        'Employee Benefit Accrual',
                        filters={
                            'salary_slip': self.name,
                            'salary_component': i.reimbursements
                        },
                        fields=['name']
                    )

                    if get_benefit_accrual:
                        amount = i.monthly_total_amount / self.total_working_days
                        eligible_amount = amount * self.payment_days

                        for j in get_benefit_accrual:
                            accrual_doc = frappe.get_doc('Employee Benefit Accrual', j.name)
                            accrual_doc.amount = round(eligible_amount)
                            accrual_doc.save()

            if len(self.earnings) > 0:
                benefit_component = []
                component_amount_dict = {}

                benefit_component_demo=[]



                benefit_application = frappe.get_list(
                    'Employee Benefit Claim',
                    filters={
                        'employee': self.employee,
                        'claim_date': ['between', [self.start_date, self.end_date]],
                        'docstatus': 1
                    },
                    fields=['*']
                )

                if benefit_application:
                    for k in benefit_application:
                        benefit_component.append(k.earning_component)

                        benefit_component_demo.append({
                            "component":k.earning_component,
                            "amount":k.claimed_amount,
                            "settlement":0
                        })

            if len(benefit_component) > 0:
                for component in benefit_component:
                    benefit_accrual = frappe.get_list(
                        'Employee Benefit Accrual',
                        filters={
                            'employee': self.employee,
                            # 'docstatus': 1,
                            'salary_component': component
                        },
                        fields=['*']
                    )

                    if benefit_accrual:
                        for j in benefit_accrual:
                            if j.salary_component in component_amount_dict:
                                component_amount_dict[j.salary_component]['amount'] += j.amount
                                component_amount_dict[j.salary_component]['settlement'] += j.total_settlement

                            else:
                                component_amount_dict[j.salary_component] = {
                                    'amount': j.amount,
                                    'settlement': j.total_settlement
                                }

                            for demo in benefit_component_demo:
                                if demo['component'] == j.salary_component:
                                    demo['settlement'] += j.total_settlement
                                    demo['amount']+=j.total_settlement
            # frappe.msgprint(str(benefit_component_demo))

            benefit_component_amount1 = []
            for data in benefit_component_demo:
                total_amount = data['amount'] - data['settlement']
                benefit_component_amount1.append({
                    'component': data['component'],
                    'total_amount': total_amount
                })

            benefit_component_amount = []
            for component, data in component_amount_dict.items():
                total_amount = data['amount'] - data['settlement']
                benefit_component_amount.append({
                    'component': component,
                    'total_amount': total_amount
                })




            min_values = {}


            for item in benefit_component_amount1:
                component = item['component']
                total_amount = item['total_amount']
                min_values[component] = total_amount

            for item in benefit_component_amount:
                component = item['component']
                total_amount = item['total_amount']
                if component in min_values:
                    min_values[component] = min(min_values[component], total_amount)
                else:
                    min_values[component] = total_amount


            min_values_list = [{'component': component, 'total_amount': total_amount} for component, total_amount in min_values.items()]


            for component_data in min_values_list:
                for earnings in self.earnings:
                    if earnings.salary_component == component_data['component']:
                        earnings.amount = component_data['total_amount']








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
    def insert_lop_days(self):
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




    def driver_reimbursement_lop(self):

        driver_reimbursement_component_lop=[]
        driver_reimbursement_component_amount_lop=[]

        driver_reimbursement_application= frappe.get_list(
                'Employee Benefit Claim',
                filters={
                    'employee': self.employee,
                    'claim_date': ['between', [self.start_date, self.end_date]],
                    'docstatus': 1
                },
                fields=['*']
            )
        if driver_reimbursement_application:
            for k in driver_reimbursement_application:
                component_check = frappe.get_doc('Salary Component', k.earning_component)
                if component_check.component_type=="Vehicle Maintenance Reimbursement":
                    driver_reimbursement_component_lop.append(k.earning_component)

                    ss_assignment_doc = frappe.get_list(
                    'Salary Structure Assignment',
                    filters={'employee': self.employee, 'docstatus': 1},
                    fields=['name'],
                    order_by='from_date desc',
                    limit=1
                    )

                    if ss_assignment_doc:

                        record = frappe.get_doc('Salary Structure Assignment', ss_assignment_doc[0].name)
                        for i in record.custom_employee_reimbursements:
                            if i.reimbursements ==driver_reimbursement_component_lop[0]:
                                one_day_amount=round((i.monthly_total_amount/self.total_working_days)*self.payment_days)
                                monthly_reimbursement=round(i.monthly_total_amount-one_day_amount)
                                total_amount=round(k.claimed_amount-monthly_reimbursement)

                                driver_reimbursement_component_amount_lop.append(total_amount)


        if len(driver_reimbursement_component_amount_lop)>0:

            for earning in self.earnings:
                if earning.salary_component==driver_reimbursement_component_lop[0]:

                    earning.amount=driver_reimbursement_component_amount_lop[0]


    def driver_reimbursement(self):

        driver_reimbursement_component=[]
        driver_reimbursement_component_amount=[]

        driver_reimbursement_application= frappe.get_list(
                'Employee Benefit Claim',
                filters={
                    'employee': self.employee,
                    'claim_date': ['between', [self.start_date, self.end_date]],
                    'docstatus': 1
                },
                fields=['*']
            )
        if driver_reimbursement_application:
            for k in driver_reimbursement_application:
                component_check = frappe.get_doc('Salary Component', k.earning_component)
                if component_check.component_type=="Vehicle Maintenance Reimbursement":
                    driver_reimbursement_component.append(k.earning_component)
                    driver_reimbursement_component_amount.append(k.claimed_amount)


        existing_components = {earning.salary_component for earning in self.earnings}

        for i in range(len(driver_reimbursement_component)):
            if driver_reimbursement_component[i] not in existing_components:
                self.append("earnings", {
                    "salary_component": driver_reimbursement_component[i],
                    "amount": driver_reimbursement_component_amount[i]
                })





    def insert_lta_reimbursement_lop(self):
        lta_tax_component = []
        lta_tax_amount = []


        lta_taxable = frappe.get_list('Salary Component',
            filters={'component_type': "LTA Taxable"},
            fields=['name']
        )
        if lta_taxable:
            lta_tax_component.append(lta_taxable[0].name)


        lta_non_taxable = frappe.get_list('Salary Component',
            filters={'component_type': "LTA Non Taxable"},
            fields=['name']
        )
        if lta_non_taxable:
            lta_tax_component.append(lta_non_taxable[0].name)


        lta_component = frappe.get_list('Salary Component',
            filters={'component_type': "LTA Reimbursement"},
            fields=['name']
        )
        if lta_component:
            reimbursement_component=lta_component[0].name




        lta_reimbursement = frappe.get_list('LTA Claim',
            filters={
                'employee': self.employee,
                "docstatus": 1,
                'claim_date': ['between', [self.start_date, self.end_date]]
            },
            fields=['*']
        )
        if lta_reimbursement:
            taxable_sum=0
            non_taxable_sum=0
            for lta in lta_reimbursement:
                if lta.income_tax_regime=="Old Regime":
                    taxable_sum=taxable_sum+lta.taxable_amount
                    non_taxable_sum=non_taxable_sum+lta.non_taxable_amount
                    # lta_tax_amount.append(taxable_sum)
                    # lta_tax_amount.append(non_taxable_sum)
                else:
                    taxable_sum=taxable_sum+lta.taxable_amount
                    # lta_tax_amount.append(taxable_sum)


            if taxable_sum>0:
                ss_assignment = frappe.get_list(
                    'Salary Structure Assignment',
                    filters={'employee': self.employee, 'docstatus': 1},
                    fields=['name'],
                    order_by='from_date desc',
                    limit=1
                )

                if ss_assignment:

                    record = frappe.get_doc('Salary Structure Assignment', ss_assignment[0].name)
                    for i in record.custom_employee_reimbursements:
                        if i.reimbursements ==reimbursement_component:
                            if record.custom_tax_regime=="Old Regime":
                                one_day_amount=round((i.monthly_total_amount/self.total_working_days)*self.payment_days)
                                total_amount_taxable=round(taxable_sum-one_day_amount)
                                total_amount_non_taxable=round(non_taxable_sum-one_day_amount)
                                lta_tax_amount.append(total_amount_taxable)
                                lta_tax_amount.append(total_amount_non_taxable)
                            else:
                                one_day_amount=round((i.monthly_total_amount/self.total_working_days)*self.payment_days)
                                total_amount_taxable=round(taxable_sum-one_day_amount)
                                lta_tax_amount.append(total_amount_taxable)



        if len(lta_tax_amount)>0:



            for earning in self.earnings:
                # if earning.salary_component==lta_component[0].custom_lta_component:

                #     earning.amount=lta_tax_amount[0]
                if earning.salary_component==lta_tax_component[0]:
                    earning.amount=lta_tax_amount[0]

                if earning.salary_component==lta_tax_component[1]:
                    earning.amount=lta_tax_amount[1]



    def insert_lta_reimbursement(self):
        lta_tax_component = []
        lta_tax_amount = []

        lta_taxable = frappe.get_list('Salary Component',
            filters={'component_type': "LTA Taxable"},
            fields=['name']
        )
        if lta_taxable:
            lta_tax_component.append(lta_taxable[0].name)


        lta_non_taxable = frappe.get_list('Salary Component',
            filters={'component_type': "LTA Non Taxable"},
            fields=['name']
        )
        if lta_non_taxable:
            lta_tax_component.append(lta_non_taxable[0].name)


        lta_reimbursement = frappe.get_list('LTA Claim',
            filters={
                'employee': self.employee,
                "docstatus": 1,
                'claim_date': ['between', [self.start_date, self.end_date]]
            },
            fields=['*']
        )




        if lta_reimbursement:
            taxable_sum=0
            non_taxable_sum=0
            for lta in lta_reimbursement:
                if lta.income_tax_regime=="Old Regime":
                    taxable_sum=taxable_sum+lta.taxable_amount
                    non_taxable_sum=non_taxable_sum+lta.non_taxable_amount
                    lta_tax_amount.append(taxable_sum)
                    lta_tax_amount.append(non_taxable_sum)
                else:
                    taxable_sum=taxable_sum+lta.taxable_amount
                    lta_tax_amount.append(taxable_sum)




        existing_components = {earning.salary_component for earning in self.earnings}

        if len(lta_tax_amount)>0:

            for i in range(len(lta_tax_amount)):
                if lta_tax_component[i] not in existing_components:
                    self.append("earnings", {
                        "salary_component": lta_tax_component[i],
                        "amount": lta_tax_amount[i]
                    })

















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









    def insert_reimbursement(self):
        if self.employee:
            benefit_component = []
            component_amount_dict = {}
            benefit_component_demo=[]
            benefit_component_vehicle=[]

            benefit_application = frappe.get_list(
                'Employee Benefit Claim',
                filters={
                    'employee': self.employee,
                    'claim_date': ['between', [self.start_date, self.end_date]],
                    'docstatus': 1
                },
                fields=['*']
            )
            if benefit_application:
                for k in benefit_application:
                    component_check = frappe.get_doc('Salary Component', k.earning_component)
                    if component_check.component_type!="Vehicle Maintenance Reimbursement":

                        benefit_component.append(k.earning_component)
                        benefit_component_demo.append({
                            "component":k.earning_component,
                            "amount":k.claimed_amount,
                            "settlement":0
                        })
            # frappe.msgprint(str(benefit_component))
            # frappe.msgprint(str(benefit_component_demo))

            if len(benefit_component) > 0:
                for component in benefit_component:
                    benefit_accrual = frappe.get_list(
                        'Employee Benefit Accrual',
                        filters={
                            'employee': self.employee,
                            'docstatus': 1,
                            'salary_component': component,
                            'payroll_period':self.custom_payroll_period,
                        },
                        fields=['*']
                    )

                    if benefit_accrual:
                        for j in benefit_accrual:
                            if j.salary_component in component_amount_dict:
                                component_amount_dict[j.salary_component]['amount'] += j.amount
                                component_amount_dict[j.salary_component]['settlement'] += j.total_settlement

                            else:
                                component_amount_dict[j.salary_component] = {
                                    'amount': j.amount,
                                    'settlement': j.total_settlement
                                }
                            # frappe.msgprint(str(component_amount_dict))

                            for demo in benefit_component_demo:
                                if demo['component'] == j.salary_component:
                                    demo['settlement'] += j.total_settlement
                                    demo['amount']+=j.total_settlement

        benefit_component_amount1 = []
        for data in benefit_component_demo:
            total_amount = max(0, data['amount'] - data['settlement'])

            benefit_component_amount1.append({
                'component': data['component'],
                'total_amount': total_amount
            })

        # # frappe.msgprint(str(benefit_component_amount1))

        if self.employee:
            ss_assignment = frappe.get_list(
                'Salary Structure Assignment',
                filters={'employee': self.employee, 'docstatus': 1},
                fields=['name'],
                order_by='from_date desc',
                limit=1
            )

            if ss_assignment:
                child_doc = frappe.get_doc('Salary Structure Assignment', ss_assignment[0].name)

                for i in child_doc.custom_employee_reimbursements:
                    if i.reimbursements in benefit_component:
                        if i.reimbursements in component_amount_dict:
                            component_amount_dict[i.reimbursements]['amount'] += i.monthly_total_amount
                        else:
                            component_amount_dict[i.reimbursements] = {
                                'amount': i.monthly_total_amount,
                                'settlement': 0.0
                            }

        # frappe.msgprint(str(component_amount_dict))


        benefit_component_amount = []
        for component, data in component_amount_dict.items():
            total_amount = data['amount'] - data['settlement']
            benefit_component_amount.append({
                'component': component,
                'total_amount': total_amount
            })

        # frappe.msgprint(str(benefit_component_amount))
        # frappe.msgprint(str(benefit_component_amount1))

        min_values = {}


        for item in benefit_component_amount1:
            component = item['component']
            total_amount = item['total_amount']
            min_values[component] = total_amount

        for item in benefit_component_amount:
            component = item['component']
            total_amount = item['total_amount']
            if component in min_values:
                min_values[component] = min(min_values[component], total_amount)
            else:
                min_values[component] = total_amount


        min_values_list = [{'component': component, 'total_amount': total_amount} for component, total_amount in min_values.items()]
        existing_components = {earning.salary_component for earning in self.earnings}
        for component_data in min_values_list:
            if component_data['component'] not in existing_components:
                self.append("earnings", {
                    "salary_component": component_data['component'],
                    "amount": component_data['total_amount']
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



    def employee_accrual_submit(self) :

        if self.employee:

            for i in self.earnings:

                component = frappe.get_doc('Salary Component', i.salary_component)




                if component.custom_is_reimbursement == 1:
                        get_accrual_data=frappe.db.get_list('Employee Benefit Accrual',
                            filters={
                                'salary_slip': self.name,'salary_component':i.salary_component,"employee":self.employee
                            },
                            fields=['*'],

                        )


                        for j in get_accrual_data:
                            accrual_doc = frappe.get_doc('Employee Benefit Accrual', j.name)
                            accrual_doc.total_settlement = i.amount
                            accrual_doc.save()


            get_accrual=frappe.db.get_list('Employee Benefit Accrual',
                filters={
                    'salary_slip': self.name
                },
                fields=['name'],

            )

            for j in get_accrual:
                accrual_doc = frappe.get_doc('Employee Benefit Accrual', j.name)
                accrual_doc.docstatus = 1
                accrual_doc.save()



    def calculate_grosspay(self):
        gross_pay_sum = 0

        gross_pay_year_sum=0

        reimbursement_sum=0

        total_income=0

        gross_earning=0



        if self.earnings:
            for i in self.earnings:
                component = frappe.get_doc('Salary Component', i.salary_component)
                if component.custom_is_part_of_gross_pay == 1:
                    gross_pay_sum += i.amount
                    gross_pay_year_sum +=i.year_to_date


                if component.custom_is_reimbursement == 1 or component.component_type=="LTA Taxable" or component.component_type=="LTA Non Taxable":
                    reimbursement_sum += i.amount

                if component.do_not_include_in_total==0 and component.custom_is_reimbursement==0:
                    total_income+=i.amount


                # if component.custom_is_gross_earning == 1:
                #     gross_earning += i.amount


        total_loan_amount=0
        if len(self.loans)>0:
            for ji in self.loans:
                total_loan_amount+=ji.total_payment



        self.custom_total_deduction_amount=total_loan_amount+self.total_deduction

        self.custom_statutory_grosspay=round(gross_pay_sum)

        self.custom_statutory_year_to_date=round(gross_pay_year_sum)

        self.custom_total_income=round(total_income)

        self.custom_net_pay_amount=round((total_income-self.custom_total_deduction_amount)+reimbursement_sum)

        self.custom_in_words=money_in_words(self.custom_net_pay_amount)

        if self.total_loan_repayment:
            self.custom_loan_amount=self.total_loan_repayment




    def set_taxale(self):

        for earning in self.earnings:
            get_tax=frappe.get_doc("Salary Component",earning.salary_component)

            earning.custom_tax_exemption_applicable_based_on_regime=get_tax.custom_tax_exemption_applicable_based_on_regime
            earning.custom_regime=get_tax.custom_regime







    # def set_payroll_period(self):

    #     latest_salary_structure = frappe.get_list(
    #     'Salary Structure Assignment',
    #     filters={
    #         'employee': self.employee,
    #         'docstatus': 1,
    #         'from_date': ['<', self.end_date]
    #     },
    #     fields=["*"],
    #     limit=1
    #     )


    #     self.custom_salary_structure_assignment=latest_salary_structure[0].name
    #     self.custom_income_tax_slab=latest_salary_structure[0].income_tax_slab
    #     self.custom_tax_regime=latest_salary_structure[0].custom_tax_regime
    #     self.custom_employee_state=latest_salary_structure[0].custom_state
    #     self.custom_annual_ctc=latest_salary_structure[0].base

    #     # latest_payroll_period = frappe.get_list('Payroll Period',
    #     #     filters={'start_date': ('<', self.end_date),'company':self.company},
    #     #     fields=["*"],
    #     #     order_by='start_date desc',
    #     #     limit=1
    #     # )
    #     # if latest_payroll_period:
    #     self.custom_payroll_period=self.payroll_period.name

















    def add_employee_benefits(self):
        pass









    def tax_calculation(self):

        latest_salary_structure = frappe.get_list('Salary Structure Assignment',
                        filters={'employee': self.employee,'docstatus':1},
                        fields=["*"],
                        order_by='from_date desc',
                        limit=1
                    )

        if self.annual_taxable_amount:
            self.custom_taxable_amount=round(self.annual_taxable_amount)

        if self.ctc and self.non_taxable_earnings:
            self.custom_total_income_with_taxable_component=round(self.ctc-self.non_taxable_earnings)

        if latest_salary_structure[0].income_tax_slab:
            payroll_period=latest_salary_structure[0].custom_payroll_period
            income_doc = frappe.get_doc('Income Tax Slab', latest_salary_structure[0].income_tax_slab)
            total_value=[]
            from_amount=[]
            to_amount=[]
            percentage=[]

            total_array=[]
            difference=[]

            rebate=income_doc.custom_taxable_income_is_less_than
            max_amount=income_doc.custom_maximum_amount

            for i in income_doc.slabs:


                array_list={
                    'from':i.from_amount,
                    'to':i.to_amount,
                    'percent':i.percent_deduction
                    }

                total_array.append(array_list)
            for slab in total_array:

                if slab['to'] == 0.0:
                    if round(self.annual_taxable_amount) >= slab['from']:
                        tt1=round(self.annual_taxable_amount)-slab['from']
                        tt2=slab['percent']
                        tt3=round((tt1*tt2)/100)

                        tt4=slab['from']
                        tt5=slab['to']

                        remaining_slabs = [s for s in total_array if s['from'] != slab['from'] and s['from'] < slab['from']]
                        for slab in remaining_slabs:
                            from_amount.append(slab['from'])
                            to_amount.append(slab['to'])
                            percentage.append(slab["percent"])
                            difference.append(slab['to']-slab['from'])
                            total_value.append((slab['to']-slab['from'])*slab["percent"]/100)
                        from_amount.append(tt4)
                        to_amount.append(tt5)
                        percentage.append(tt2)
                        difference.append(tt1)
                        total_value.append(tt3)
                    self.custom_tax_slab = []
                    for i in range(len(from_amount)):
                            self.append("custom_tax_slab", {
                            "from_amount": from_amount[i],
                            "to_amount": to_amount[i],
                            "percentage":  percentage[i]   ,
                            "tax_amount":total_value[i],
                            "amount":difference[i]
                        })

                else:
                    if slab['from'] <= round(self.annual_taxable_amount) <= slab['to']:
                        tt1=round(self.annual_taxable_amount)-slab['from']
                        tt2=slab['percent']
                        tt3=(tt1*tt2)/100
                        tt4=slab['from']
                        tt5=slab['to']
                        remaining_slabs = [s for s in total_array if s['from'] != slab['from'] and s['from'] < slab['from']]

                        for slab in remaining_slabs:
                            from_amount.append(slab['from'])
                            to_amount.append(slab['to'])
                            percentage.append(slab["percent"])
                            difference.append(slab['to']-slab['from'])
                            total_value.append((slab['to']-slab['from'])*slab["percent"]/100)
                        from_amount.append(tt4)
                        to_amount.append(tt5)
                        percentage.append(tt2)
                        difference.append(tt1)
                        total_value.append(tt3)

                    self.custom_tax_slab = []
                    for i in range(len(from_amount)):
                            self.append("custom_tax_slab", {
                            "from_amount": from_amount[i],
                            "to_amount": to_amount[i],
                            "percentage":  percentage[i]   ,
                            "tax_amount":total_value[i],
                            "amount":difference[i]
                        })



            total_sum = sum(total_value)



            if self.custom_taxable_amount<rebate:

                self.custom_tax_on_total_income=total_sum
                self.custom_rebate_under_section_87a=total_sum
                self.custom_total_tax_on_income=0
            else:
                self.custom_total_tax_on_income=total_sum
                self.custom_rebate_under_section_87a=0
                self.custom_tax_on_total_income=total_sum-0

            if self.custom_taxable_amount>5000000:

                surcharge_m=(self.custom_total_tax_on_income*10)/100

                self.custom_surcharge=round(surcharge_m)
                self.custom_education_cess=round((surcharge_m+self.custom_total_tax_on_income)*4/100)
            else:

                self.custom_surcharge=0
                self.custom_education_cess=(self.custom_surcharge+self.custom_total_tax_on_income)*4/100


            self.custom_total_amount=round(self.custom_surcharge+self.custom_education_cess+self.custom_total_tax_on_income)
