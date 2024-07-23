import frappe
from hrms.payroll.doctype.employee_benefit_claim.employee_benefit_claim import EmployeeBenefitClaim


class CustomEmployeeBenefitClaim(EmployeeBenefitClaim):
    
    # def validate(self):

    #     super().validate()

    def on_submit(self):

        self.insert_future_benefit()


        


    # def validate_benefit_amount(self):

       

        
    #     if self.employee:
    #         accrual_list = frappe.get_list('Employee Benefit Accrual',
    #             filters={'employee': self.employee,"salary_component":self.earning_component,"docstatus":1},
    #             fields=['name', 'amount']
    #         )

    #         if accrual_list:
    #             total_amount = sum(accrual['amount'] for accrual in accrual_list)


               

    #             if self.claimed_amount > total_amount:
                    
    #                 frappe.throw("Claimed Amount Cannot Exceed Total Accrued Amount")



    def insert_future_benefit(self):

        if self.custom_max_amount:
        
        
            if self.claimed_amount>self.custom_max_amount:

                doc1 = frappe.get_doc('Salary Component', self.earning_component)
                if doc1.component_type=="Vehicle Maintenance Reimbursement":
                
                    date_str = self.claim_date       
                    year, month, day = map(int, date_str.split('-'))
                    new_month = month + 1
                    new_year = year
                    if new_month > 12:
                        new_month = 1
                        new_year += 1
                        
                    next_month_date = f"{new_year}-{new_month:02d}-{day:02d}"


                    future_amount=self.claimed_amount-self.custom_max_amount
                    insert_doc = frappe.get_doc({
                        'doctype':'Employee Benefit Claim',
                        'employee':self.employee,
                        'claim_date':next_month_date,
                        'currency':self.currency,
                        'company':self.company,
                        'claimed_amount':future_amount,
                        'earning_component':self.earning_component,
                        'docstatus':1

                    })
                    insert_doc.insert()

