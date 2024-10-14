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


                

            

            





