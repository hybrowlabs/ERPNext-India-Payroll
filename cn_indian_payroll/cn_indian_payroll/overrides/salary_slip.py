import frappe
import datetime



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



class CustomSalarySlip(SalarySlip):



    # def before_insert(self):
    #     self.actual_amount()


    def on_update(self):
        super().on_update()
        self.accrual_update()
        self.insert_lta_reimbursement_lop()
        




    def after_insert(self):
        
        self.employee_accrual_insert()
        
        

    def on_submit(self):
        super().on_submit()
        self.employee_accrual_submit()



    def before_save(self):
        
        
        self.insert_reimbursement()
        
        self.insert_lop_days()
        self.loan_perquisite()
        self.insert_lta_reimbursement()
        self.driver_reimbursement()

        self.calculate_grosspay()

        self.tax_calculation1()

        self.actual_amount()

        self.set_month()

        self.remaining_day()



        


    



    def on_cancel(self):

        get_benefit_accrual=frappe.db.get_list('Employee Benefit Accrual',
                    filters={
                        'salary_slip': self.name,
                        'employee':self.employee,
                    },
                    fields=['*'],
                    
                )

        if len(get_benefit_accrual)>0:
            for j in get_benefit_accrual:
                arrear_doc = frappe.get_doc('Employee Benefit Accrual', j.name)
                arrear_doc.docstatus = 2
                arrear_doc.save()



   
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

            # frappe.msgprint(str(benefit_component_amount1))
            # frappe.msgprint(str(benefit_component_amount))


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

            # frappe.msgprint(str(min_values_list))
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



    def insert_lop_days(self):
        
        benefit_application_days = frappe.get_list(
                'Additional Salary',
                filters={
                    'employee': self.employee,
                    'payroll_date': ['between', [self.start_date, self.end_date]],
                    'docstatus': 1
                },
                fields=['*']
            )


        if len(benefit_application_days)>0:
            self.custom_lop_reversal_days=benefit_application_days[0].custom_lop_reversal_days




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

        # frappe.msgprint(str(driver_reimbursement_component))
        # frappe.msgprint(str(driver_reimbursement_component_amount))

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


        lta_component = frappe.get_list('Company',
            filters={'name': self.company},
            fields=['*']
        )
        if lta_component:
            lta_tax_component.append(lta_component[0].custom_lta_component)

        # frappe.msgprint(str(lta_tax_component))

       
        lta_reimbursement = frappe.get_list('LTA Claim',
            filters={
                'employee': self.employee,
                "docstatus": 1,
                'claim_date': ['between', [self.start_date, self.end_date]]
            },
            fields=['*']
        )
        if lta_reimbursement:
            lta_tax_amount.append(lta_reimbursement[0].taxable_amount*self.payment_days)
            lta_tax_amount.append(lta_reimbursement[0].non_taxable_amount*self.payment_days)
            lta_tax_amount.append(lta_reimbursement[0].amount*self.payment_days)

        

            for earning in self.earnings:
                if earning.salary_component==lta_taxable[0].name:
                    tax_day_amount=earning.amount/self.total_working_days
                    earning.amount=round(tax_day_amount*self.payment_days)
                    


                if earning.salary_component==lta_non_taxable[0].name:
                    non_tax_day_amount=earning.amount/self.total_working_days
                    earning.amount=round(non_tax_day_amount*self.payment_days)
                    


                if earning.salary_component==lta_component[0].custom_lta_component:
                    total_day_amount=earning.amount/self.total_working_days
                    earning.amount=round(total_day_amount*self.payment_days)
                    
        



        # existing_components = {earning.salary_component for earning in self.earnings}

        # if len(lta_tax_amount)>0:

        #     for i in range(len(lta_tax_component)):
        #         if lta_tax_component[i] not in existing_components:
        #             self.append("earnings", {
        #                 "salary_component": lta_tax_component[i],
        #                 "amount": lta_tax_amount[i]
        #             })


                        



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


        lta_component = frappe.get_list('Company',
            filters={'name': self.company},
            fields=['*']
        )
        if lta_component:
            lta_tax_component.append(lta_component[0].custom_lta_component)

        # frappe.msgprint(str(lta_tax_component))

       
        lta_reimbursement = frappe.get_list('LTA Claim',
            filters={
                'employee': self.employee,
                "docstatus": 1,
                'claim_date': ['between', [self.start_date, self.end_date]]
            },
            fields=['*']
        )
        if lta_reimbursement:
            lta_tax_amount.append(lta_reimbursement[0].taxable_amount)
            lta_tax_amount.append(lta_reimbursement[0].non_taxable_amount)
            lta_tax_amount.append(lta_reimbursement[0].amount)

        # frappe.msgprint(str(lta_tax_amount))
        



        existing_components = {earning.salary_component for earning in self.earnings}

        if len(lta_tax_amount)>0:

            for i in range(len(lta_tax_component)):
                if lta_tax_component[i] not in existing_components:
                    self.append("earnings", {
                        "salary_component": lta_tax_component[i],
                        "amount": lta_tax_amount[i]
                    })




    

    # def loan_perquisite(self):
    #     loan_Perquisite_component = []
    #     perquisite_amount_array = []

        
    #     Perquisite_component = frappe.get_list(
    #         'Salary Component',
    #         filters={
    #             'component_type': "Loan Perquisite"
    #         },
    #         fields=['name']
    #     )

    #     if Perquisite_component:
    #         loan_Perquisite_component.append(Perquisite_component[0].name)

        
    #     loan_repayment = frappe.get_list(
    #         'Loan Repayment Schedule',
    #         filters={
    #             'custom_employee': self.employee,
    #             'status': "Active"
    #         },
    #         fields=['name']
    #     )

    #     if loan_repayment:
    #         frappe.msgprint(str(loan_repayment))
        #     for d1 in loan_repayment:
        #         loan_repayment_child = frappe.get_doc('Loan Repayment Schedule', d1.name)
        #         for d2 in loan_repayment_child.custom_loan_perquisite:
        #             if d2.payment_date:
        #                 payment_date = str(d2.payment_date)
        #                 start_date = str(self.start_date)
        #                 end_date = str(self.end_date)

        #                 if start_date <= payment_date <= end_date:
        #                     perquisite_amount_array.append(d2.perquisite_amount)

        # if perquisite_amount_array:
        #     existing_components = {earning.salary_component for earning in self.earnings}

        #     for component in loan_Perquisite_component:
        #         if component not in existing_components:
        #             self.append("earnings", {
        #                 "salary_component": component,
        #                 "amount": sum(perquisite_amount_array)
        #             })


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

                    


        #Pushed the component in array

            # frappe.msgprint(str(benefit_component))

            if len(benefit_component) > 0:
                for component in benefit_component:
                    benefit_accrual = frappe.get_list(
                        'Employee Benefit Accrual',
                        filters={
                            'employee': self.employee,
                            'docstatus': 1,
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
        # frappe.msgprint(str(benefit_component_demo))

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
        if self.employee:


            ss_assignment = frappe.get_list('Salary Structure Assignment',
                        filters={'employee': self.employee,'docstatus':1},
                        fields=['name'],
                        order_by='from_date desc',
                        limit=1
                    )

            if ss_assignment:
             

                child_doc = frappe.get_doc('Salary Structure Assignment',ss_assignment[0].name)

                
           
                for i in child_doc.custom_employee_reimbursements:
                    
                    accrual_insert = frappe.get_doc({
                        'doctype': 'Employee Benefit Accrual',
                        'employee': self.employee,
                        'payroll_entry': self.payroll_entry,
                        'amount': i.monthly_total_amount,
                        'salary_component': i.reimbursements,
                        'benefit_accrual_date': self.posting_date,
                        'salary_slip':self.name,
                        
                        })
                    accrual_insert.insert()



    def employee_accrual_submit(self) :  
        
        if self.employee:

            for i in self.earnings:

                component = frappe.get_doc('Salary Component', i.salary_component)

                
            

                if component.custom_is_reimbursement == 1:
                        get_accrual_data=frappe.db.get_list('Employee Benefit Accrual',
                            filters={
                                'payroll_entry': self.payroll_entry,'salary_component':i.salary_component,"employee":self.employee
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


                if component.custom_is_reimbursement == 1:
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

        # self.custom_gross_earning=gross_earning+gross_pay_sum


        self.custom_total_income=round(total_income)

       
        self.custom_net_pay_amount=round((total_income-self.custom_total_deduction_amount)+reimbursement_sum)

        self.custom_in_words=money_in_words(self.custom_net_pay_amount)

        latest_salary_structure = frappe.get_list('Salary Structure Assignment',
                        filters={'employee': self.employee,'docstatus':1},
                        fields=["*"],
                        order_by='from_date desc',
                        limit=1
                    )
        
        
        self.custom_salary_structure_assignment=latest_salary_structure[0].name
        self.custom_income_tax_slab=latest_salary_structure[0].income_tax_slab
        self.custom_employee_state=latest_salary_structure[0].custom_state
        self.custom_annual_ctc=latest_salary_structure[0].base


        



        

        






    def add_employee_benefits(self):
        pass




    def tax_calculation(self):
        
        latest_salary_structure = frappe.get_list('Salary Structure Assignment',
                        filters={'employee': self.employee,'docstatus':1},
                        fields=["*"],
                        order_by='from_date desc',
                        limit=1
                    )
        
        
        self.custom_taxable_amount=round(self.annual_taxable_amount)
        self.custom_total_income_with_taxable_component=round(self.ctc-self.non_taxable_earnings)

        if latest_salary_structure[0].income_tax_slab:

            
            payroll_period=latest_salary_structure[0].custom_payroll_period
            
            

            income_doc = frappe.get_doc('Income Tax Slab', latest_salary_structure[0].income_tax_slab)

            if income_doc.name=="Old Regime":

                total_value=[]
                from_amount=[]
                to_amount=[]
                percentage=[]

                total_array=[]

                arr=[]
                print_taken=[]

                tax_category=" "

                max_amount=" "

                t1=" "

                tax_category=income_doc.custom_taxable_income_is_less_than
                max_amount=income_doc.custom_maximum_amount

                for i in income_doc.slabs:
                    

                    array_list={
                    'from':i.from_amount,
                        'to':i.to_amount,
                        'percent':i.percent_deduction
                    }
                
                    total_array.append(array_list)

                

                for slab in total_array:
                    
                    if slab['from'] <= self.annual_taxable_amount <= slab['to']:

                        t1=self.annual_taxable_amount-slab['from']
                    
                        t2=slab['percent']
                        t3=(t1*t2)/100
                        

                        remaining_slabs = [s for s in total_array if s['from'] != slab['from'] and s['from'] < slab['from']]

                        for remaining_slab in remaining_slabs:
                            tax_amount = remaining_slab['from'] * remaining_slab["percent"] / 100

                            print_taken.append(remaining_slab['from'])
                            
                            from_amount.append(remaining_slab['from'])
                            to_amount.append(remaining_slab['to'])
                            percentage.append(remaining_slab["percent"])

                            arr.append(tax_amount)

                        arr.append(t3)
                        from_amount.append(slab['from'])
                        to_amount.append(slab['to'])
                        percentage.append(slab['percent'])

                        print_taken.append(t1)

            

                total_sum = sum(arr)



                if self.custom_taxable_amount<tax_category:
                    
                    self.custom_tax_on_total_income=total_sum
                    self.custom_rebate_under_section_87a=total_sum
                    self.custom_total_tax_on_income=0
                else:
                    self.custom_total_tax_on_income=total_sum
                    self.custom_rebate_under_section_87a=0
                    self.custom_tax_on_total_income=total_sum-0
                    


                if self.custom_taxable_amount>5000000:

                    surcharge_m=(self.custom_total_tax_on_income*10)/100
                   
                    self.custom_surcharge=surcharge_m
                    self.custom_education_cess=(surcharge_m+self.custom_total_tax_on_income)*4/100
                else:

                    self.custom_surcharge=0
                    self.custom_education_cess=(self.custom_surcharge+self.custom_total_tax_on_income)*4/100


                self.custom_total_amount=self.custom_surcharge+self.custom_education_cess+self.custom_total_tax_on_income
                
            
                self.custom_tax_slab = []
                for i in range(len(from_amount)):
                    self.append("custom_tax_slab", {
                    "from_amount": from_amount[i],
                    "to_amount": to_amount[i], 
                    "percentage":  percentage[i]   ,
                    "tax_amount":arr[i],
                    "amount":print_taken[i]     
                })



            if income_doc.name=="New Regime":

                total_value=[]
                from_amount=[]
                to_amount=[]
                percentage=[]

                total_array=[]

                arr=[]
                print_taken=[]

                tax_category=" "

                max_amount=" "

                t1=" "

                tax_category=income_doc.custom_taxable_income_is_less_than
                max_amount=income_doc.custom_maximum_amount

                for i in income_doc.slabs:
                    

                    array_list={
                    'from':i.from_amount,
                        'to':i.to_amount,
                        'percent':i.percent_deduction

                    }
                
                    total_array.append(array_list)

                    # frappe.msgprint(str(array_list))

                for slab in total_array:
                    if slab['from'] <= self.custom_taxable_amount <= slab['to']:

                        t1=self.custom_taxable_amount-slab['from']


                        
                        

                        t2=slab['percent']
                        t3=(t1*t2)/100

                        remaining_slabs = [s for s in total_array if s['from'] != slab['from'] and s['from'] < slab['from']]

                        for remaining_slab in remaining_slabs:
                            tax_amount = 300000 * remaining_slab["percent"] / 100

                            print_taken.append(300000)
                            
                            from_amount.append(remaining_slab['from'])
                            to_amount.append(remaining_slab['to'])
                            percentage.append(remaining_slab["percent"])

                            arr.append(tax_amount)

                        arr.append(t3)
                        from_amount.append(slab['from'])
                        to_amount.append(slab['to'])
                        percentage.append(slab['percent'])

                        print_taken.append(t1)


            

                total_sum = sum(arr)



                if self.custom_taxable_amount<tax_category:
                    
                    self.custom_tax_on_total_income=total_sum
                    self.custom_rebate_under_section_87a=total_sum
                    self.custom_total_tax_on_income=0
                else:
                    self.custom_total_tax_on_income=total_sum
                    self.custom_rebate_under_section_87a=0
                    self.custom_tax_on_total_income=total_sum-0
                    


                if self.custom_taxable_amount>5000000:

                    surcharge_m=(self.custom_total_tax_on_income*10)/100
                   
                    self.custom_surcharge=surcharge_m
                    self.custom_education_cess=(surcharge_m+self.custom_total_tax_on_income)*4/100
                else:

                    self.custom_surcharge=0
                    self.custom_education_cess=(self.custom_surcharge+self.custom_total_tax_on_income)*4/100


                self.custom_total_amount=self.custom_surcharge+self.custom_education_cess+self.custom_total_tax_on_income
                
            
                self.custom_tax_slab = []
                for i in range(len(from_amount)):
                    self.append("custom_tax_slab", {
                    "from_amount": from_amount[i],
                    "to_amount": to_amount[i], 
                    "percentage":  percentage[i]   ,
                    "tax_amount":arr[i],
                    "amount":print_taken[i]     
                })

                            








    def tax_calculation1(self):
        
        latest_salary_structure = frappe.get_list('Salary Structure Assignment',
                        filters={'employee': self.employee,'docstatus':1},
                        fields=["*"],
                        order_by='from_date desc',
                        limit=1
                    )
        
        
        self.custom_taxable_amount=round(self.annual_taxable_amount)
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
                        t1=round(self.annual_taxable_amount)-slab['from']
                        t2=slab['percent']
                        t3=round((t1*t2)/100)
                        t4=slab['from']
                        t5=slab['to']
                        remaining_slabs = [s for s in total_array if s['from'] != slab['from'] and s['from'] < slab['from']]
                        for slab in remaining_slabs:
                            from_amount.append(slab['from'])
                            to_amount.append(slab['to'])
                            percentage.append(slab["percent"])
                            difference.append(slab['to']-slab['from'])
                            total_value.append((slab['to']-slab['from'])*slab["percent"]/100)
                        from_amount.append(t4)
                        to_amount.append(t5)
                        percentage.append(t2)
                        difference.append(t1)
                        total_value.append(t3)
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
                        t1=round(self.annual_taxable_amount)-slab['from']
                        t2=slab['percent']
                        t3=(t1*t2)/100
                        t4=slab['from']
                        t5=slab['to']
                        remaining_slabs = [s for s in total_array if s['from'] != slab['from'] and s['from'] < slab['from']]
                        
                        for slab in remaining_slabs:
                            from_amount.append(slab['from'])
                            to_amount.append(slab['to'])
                            percentage.append(slab["percent"])
                            difference.append(slab['to']-slab['from'])
                            total_value.append((slab['to']-slab['from'])*slab["percent"]/100)
                        from_amount.append(t4)
                        to_amount.append(t5)
                        percentage.append(t2)
                        difference.append(t1)
                        total_value.append(t3)

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
                
            


                            











   






   




                

            

            





































# @frappe.whitelist()
# def get_additional_salary(payroll_id):
#     if payroll_id:
#         doc1 = frappe.get_doc('Payroll Entry', payroll_id)
#         employee_bonus_dict = {}  
#         for employee in doc1.employees:
#             employee_bonus = frappe.db.get_list('Employee Bonus Accrual',
#                                                  filters={
#                                                      'employee': employee.employee,
#                                                      'docstatus': 1,
#                                                      'is_paid': 0,
#                                                  },
#                                                  fields=['name', 'amount', 'employee', 'salary_component', 'company']
#                                                  )

#             for bonus in employee_bonus:
#                 employee_id = bonus['employee']
#                 amount = bonus['amount']
#                 salary_component = bonus['salary_component']
#                 document_name = bonus['name']
                
#                 if employee_id in employee_bonus_dict:
#                     employee_bonus_dict[employee_id]['total_amount'] += amount
#                     employee_bonus_dict[employee_id]['components'].add(salary_component)
#                     employee_bonus_dict[employee_id]['documents'].append(document_name)
#                 else:
#                     employee_bonus_dict[employee_id] = {'total_amount': amount, 'components': {salary_component}, 'documents': [document_name]}

        

#         for employee_id, data in employee_bonus_dict.items():
#             total_amount = data['total_amount']
#             components = ', '.join(data['components'])
#             document_names = data['documents']

#             additional_salary_insert = frappe.get_doc({
#                 'doctype': 'Additional Salary',
#                 'employee': employee_id,
#                 'company': doc1.company,
#                 'salary_component': components,
#                 'amount': total_amount,
#                 'payroll_date': doc1.posting_date,
#                 # 'docstatus': 1
#                 'custom_payroll_entry':payroll_id
#             })
            
#             additional_salary_insert.insert()

#             # for doc_name in document_names:
#             #     bonus_doc = frappe.get_doc('Employee Bonus Accrual', doc_name)
#             #     bonus_doc.is_paid = 1
#             #     bonus_doc.save()

#         frappe.msgprint('Additional Salary Created')
#         doc1.custom_additional_salary_created=1
#         doc1.save()

                










# @frappe.whitelist()
# def additional_salary_submit(additional):
#     if additional:
       
#         additional_list=frappe.db.get_list('Additional Salary',
#         filters={
#             'custom_payroll_entry': additional,
#             'docstatus':0
#         },
#         fields=['name','employee','payroll_date'],
        
#         )
        
#         if len(additional_list)>0:

           

#             for i in additional_list:
               

#                 additional_doc = frappe.get_doc('Additional Salary',i.name)

                
#                 additional_doc.docstatus = 1
#                 additional_doc.save()


                
#                 employee_bonus = frappe.db.get_list('Employee Bonus Accrual',
#                                                  filters={
#                                                      'employee': i.employee,
#                                                      'docstatus': 1,
#                                                      'is_paid': 0,
#                                                  },
#                                                  fields=['name', 'amount', 'employee', 'salary_component', 'company']
#                                                  )
                
                
#                 for bonus in employee_bonus:
#                     doc_id = bonus['name']
#                     bonus_doc1 = frappe.get_doc('Employee Bonus Accrual',doc_id)
                

#                     bonus_doc1.is_paid = 1
#                     bonus_doc1.bonus_paid_date=additional_doc.payroll_date
#                     bonus_doc1.save()

                    

                



               

#         frappe.msgprint('Additional Salary Submitted')

#         additional_doc_list= frappe.get_doc('Payroll Entry',additional)

        
#         additional_doc_list.custom_additional_salary_submitted=1
#         additional_doc_list.save()
















# # @frappe.whitelist()
# # def get_submit(payroll_entry):

    
    
# #     if payroll_entry:
# #         bonus_list=frappe.db.get_list('Employee Bonus Accrual',
# #         filters={
# #             'payroll_entry': payroll_entry,
# #             'docstatus':0
# #         },
# #         fields=['name'],
        
# #         )
        
# #         if len(bonus_list)>0:

# #             for i in bonus_list:
               

# #                 bonus_doc = frappe.get_doc('Employee Bonus Accrual',i.name)
                

# #                 bonus_doc.docstatus = 1
# #                 bonus_doc.save()
            
# #             if bonus_doc.name:
# #                 frappe.response['message'] = bonus_doc.name




# # def get_employee_benefit(self,method):
# #     # frappe.msgprint(self.employee)
# #     if self.employee:
# #         employee_data = frappe.get_doc('Employee', self.employee)
# #         if len(employee_data)>0:
# #             for i in employee_data.custom_employee_reimbursements:
# #                 frappe.msgprint(str(i.reimbursements))

        





# def employee_benefit_validate(self, method):
#     if self.employee:
#         accrual_list = frappe.get_list('Employee Benefit Accrual',
#             filters={'employee': self.employee,"salary_component":self.earning_component,"docstatus":1},
#             fields=['name', 'amount']
#         )

#         if accrual_list:
#             total_amount = sum(accrual['amount'] for accrual in accrual_list)

#             if self.claimed_amount > total_amount:
#                 # frappe.throw("Claimed amount cannot exceed total accrued amount."+total_amount)
#                 frappe.throw("Claimed amount cannot exceed total accrued amount: " + str(total_amount))

                
                
                



        
                


            



                    

                







        






