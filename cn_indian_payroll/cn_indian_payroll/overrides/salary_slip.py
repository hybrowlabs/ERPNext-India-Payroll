import frappe

from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip


class CustomSalarySlip(SalarySlip):
    def after_insert(self):
        # super().validate()
        self.employee_accrual_insert()
        


    def on_submit(self):
        super().on_submit()
        self.employee_accrual_submit()



    def before_save(self):
        
        self.calculate_grosspay()

    def compute_ctc(self):
        print(self.previous_taxable_earnings_before_exemption,self.current_structured_taxable_earnings_before_exemption,self.future_structured_taxable_earnings_before_exemption,self.current_additional_earnings,self.other_incomes,self.unclaimed_taxable_benefits,self.non_taxable_earnings)

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
            employee_data = frappe.get_doc('Employee', self.employee)
            if employee_data:
                for i in employee_data.custom_employee_reimbursements:
                    
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

        if self.earnings:
            for i in self.earnings:
                component = frappe.get_doc('Salary Component', i.salary_component)
                if component.custom_is_part_of_gross_pay == 1:
                    gross_pay_sum += i.amount 
                    gross_pay_year_sum +=i.year_to_date
        
        self.custom_statutory_grosspay=gross_pay_sum
        
        self.custom_statutory_year_to_date=gross_pay_year_sum


                

            

            





































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

                
                
                



        
                


            



                    

                







        






