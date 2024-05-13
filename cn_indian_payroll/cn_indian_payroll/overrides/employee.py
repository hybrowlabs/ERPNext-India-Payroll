import frappe
from erpnext.setup.doctype.employee.employee import Employee


class CustomEmployee(Employee):
    def before_save(self):

    

        self.set_cpl()

        self.reimbursement_amount()
        



    def set_cpl(self):
        components = ["Car Allowance", "Petrol Reimbursement", "Leave Travel Allowance"]
        array=[]
        
        if self.custom_employee_reimbursements:
            for i in self.custom_employee_reimbursements:
                if i.reimbursements in components:
                    
                    array.append(i.reimbursements)

            
            if len(array)==3:
                self.custom_is_car_petrol_lta=1
               
            else:
                self.custom_is_car_petrol_lta=0



    def reimbursement_amount(self):
        total_amount = 0
        if self.custom_employee_reimbursements:
            for reimbursement in self.custom_employee_reimbursements:
                total_amount += reimbursement.monthly_total_amount

        self.custom_statistical_amount = total_amount
        




                


    
                

                


            
        
        
        

       
                


