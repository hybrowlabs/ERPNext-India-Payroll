import frappe
from hrms.payroll.doctype.employee_benefit_claim.employee_benefit_claim import EmployeeBenefitClaim


class CustomEmployeeBenefitClaim(EmployeeBenefitClaim):
    
    def validate(self):

        super().validate()

        self.validate_benefit_amount()


        


    def validate_benefit_amount(self):

       

        
        if self.employee:
            accrual_list = frappe.get_list('Employee Benefit Accrual',
                filters={'employee': self.employee,"salary_component":self.earning_component,"docstatus":1},
                fields=['name', 'amount']
            )

            if accrual_list:
                total_amount = sum(accrual['amount'] for accrual in accrual_list)


               

                if self.claimed_amount > total_amount:
                    
                    frappe.throw("Claimed Amount Cannot Exceed Total Accrued Amount")

