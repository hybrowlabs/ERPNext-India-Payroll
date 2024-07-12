import frappe

from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip


class CustomSalarySlip(SalarySlip):


    def on_update(self):
        super().on_update()
        self.accrual_update()
        




    def after_insert(self):
        # super().validate()
        self.employee_accrual_insert()
        # pass
        

    def on_submit(self):
        super().on_submit()
        self.employee_accrual_submit()



    def before_save(self):
        self.calculate_grosspay()

        # self.tax_calculation()



    def accrual_update(self):
        if self.leave_without_pay>0:

            ss_assignment = frappe.get_list('Salary Structure Assignment',
                        filters={'employee': self.employee,'docstatus':1},
                        fields=['name'],
                        order_by='from_date desc',
                        limit=1
                    )

            if ss_assignment:
             

                child_doc = frappe.get_doc('Salary Structure Assignment',ss_assignment[0].name)

                
           
                for i in child_doc.custom_employee_reimbursements:
                    
                    get_benefit_accrual=frappe.db.get_list('Employee Benefit Accrual',
                        filters={
                            'salary_slip': self.name,'salary_component':i.reimbursements
                        },
                        fields=['name'],
                        
                    )

                    if get_benefit_accrual:

                        for j in get_benefit_accrual:
                            accrual_doc = frappe.get_doc('Employee Benefit Accrual', j.name)
                            
                            amount=i.monthly_total_amount/self.total_working_days
                            eligible_amount=amount*self.payment_days
                        
                            accrual_doc.amount =round(eligible_amount)
                            accrual_doc.save()




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



        if self.earnings:
            for i in self.earnings:

                
                # total_income+=i.amount




                component = frappe.get_doc('Salary Component', i.salary_component)
                if component.custom_is_part_of_gross_pay == 1:
                    gross_pay_sum += i.amount 
                    gross_pay_year_sum +=i.year_to_date


                if component.custom_is_reimbursement == 1:
                    reimbursement_sum += i.amount 

                if component.do_not_include_in_total==0 and component.custom_is_reimbursement==0: 
                    total_income+=i.amount
                    
                    
          


        
        self.custom_statutory_grosspay=gross_pay_sum
        
        self.custom_statutory_year_to_date=gross_pay_year_sum


        self.custom_total_income=total_income

       
        self.custom_net_pay_amount=(total_income+gross_pay_sum)-self.total_deduction+reimbursement_sum



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




    def tax_calculation(self):

        total_value=[]

        for component in self.earnings:
            component_check = frappe.get_doc('Salary Component',component.salary_component)
            
            if component_check.custom_is_accrual==0 and component_check.custom_is_reimbursement==0 and component_check.custom_is_food_coupon==0 and component_check.custom_perquisite==0 and component_check.custom_is_allowance==0:
                
                
               
                total_value.append(component.amount*12)


        for component in self.earnings:
            component_check = frappe.get_doc('Salary Component',component.salary_component)
            
            if component_check.custom_perquisite==1:
                
                
                
                total_value.append(component.amount*12)
            
        for component in self.earnings:
            component_check = frappe.get_doc('Salary Component',component.salary_component)
            
            if component_check.custom_is_allowance==1:
                
                
                
                total_value.append(component.amount)



        for component in self.deductions:
            component_check = frappe.get_doc('Salary Component',component.salary_component)
            
            if component_check.custom_is_nps==1:
                
                
                
                total_value.append(component.amount*12)

        # frappe.msgprint(str(total_value))

        


        

        



        






        # self.custom_taxable_amount=5959120
        from_amount=[]
        to_amount=[]
        percentage=[]

        total_array=[]

        arr=[]
        print_taken=[]

        tax_category=" "
        max_amount=" "
        
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

        latest_declaration = frappe.get_list('Employee Tax Exemption Declaration',
                        filters={'employee': self.employee,'docstatus':1,"payroll_period":latest_salary_structure[0].custom_payroll_period},
                        fields=["*"],
                        
                        limit=1
                    )
        if len(latest_declaration)>0:
        
        
            self.custom_total_tax_exemption_declaration=latest_declaration[0].total_declared_amount
            total_tds_ctc=sum(total_value)

            self.custom_taxable_amount=total_tds_ctc-latest_declaration[0].total_declared_amount

        else:
            self.custom_total_tax_exemption_declaration=0
            self.custom_taxable_amount=0


        
        if latest_salary_structure[0].income_tax_slab:

            
            payroll_period=latest_salary_structure[0].custom_payroll_period
            
            

            income_doc = frappe.get_doc('Income Tax Slab', latest_salary_structure[0].income_tax_slab)

            
            

            if income_doc.name=="Old Regime":

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
                    if slab['from'] <= self.custom_taxable_amount <= slab['to']:

                        t1=self.custom_taxable_amount-slab['from']


                        
                        

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
                
                    if slab['from'] <= self.custom_taxable_amount <= slab['to']:

                        t1=self.custom_taxable_amount-slab['from']
                        
                        

                        t2=slab['percent']
                        t3=(t1*t2)/100

                       

                        remaining_slabs = [s for s in total_array if s['from'] != slab['from'] and s['from'] < slab['from']]
                        
                        for remaining_slab in remaining_slabs:
                            from_amount.append(remaining_slab['from'])
                            to_amount.append(remaining_slab['to'])
                            percentage.append(remaining_slab["percent"])
                            tax_amount = remaining_slab['from'] * remaining_slabs[0]['percent'] / 100
                            arr.append(tax_amount)

                        arr.append(t3)
                        from_amount.append(slab['from'])
                        to_amount.append(slab['to'])
                        percentage.append(slab['percent'])

                self.custom_tax_slab = []
                for i in range(len(from_amount)):
                    self.append("custom_tax_slab", {
                    "from_amount": from_amount[i],
                    "to_amount": to_amount[i], 
                    "percentage":  percentage[i]   ,
                    "tax_amount":arr[i]     
                    })




                total_sum = sum(arr)



                if self.custom_taxable_amount<tax_category:
                    
                    self.custom_tax_on_total_income=total_sum
                    self.custom_rebate_under_section_87a=total_sum
                    self.custom_total_tax_on_income=0
                else:
                    self.custom_total_tax_on_income=0+total_sum
                    self.custom_tax_on_total_income=total_sum
                    self.custom_rebate_under_section_87a=0


                if self.custom_taxable_amount>5000000:

                    surcharge_m=(self.custom_total_tax_on_income*10)/100
                   
                    self.custom_surcharge=surcharge_m
                    self.custom_education_cess=(surcharge_m+self.custom_total_tax_on_income)*4/100
                else:

                    self.custom_surcharge=0
                    self.custom_education_cess=(self.custom_surcharge+self.custom_total_tax_on_income)*4/100

                            


















   




                

            

            





































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

                
                
                



        
                


            



                    

                







        






