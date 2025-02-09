import frappe

def before_save(self,method):

    if self.loan:
        loan_doc = frappe.get_doc('Loan', self.loan)
        if loan_doc.applicant_type=="Employee":
            

            self.custom_employee=loan_doc.applicant
            self.custom_loan_perquisite_rate_of_interest=loan_doc.custom_loan_perquisite_rate_of_interest
            self.custom_employee_name=loan_doc.applicant_name


            if self.repayment_schedule:
                
                self.custom_loan_perquisite = []
                for i in self.repayment_schedule:

                    
                    t1 = i.payment_date

                    
                    year, month, day = map(int, t1.split('-'))

                    
                    if month in [1, 3, 5, 7, 8, 10, 12]:
                        last_day = 31
                    elif month in [4, 6, 9, 11]:
                        last_day = 30
                    else:  
                        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                            last_day = 29
                        else:
                            last_day = 28

                    
                    t2 = f"{year}-{month:02d}-{last_day:02d}"

                    
                    

                    
                    self.append("custom_loan_perquisite", {
                        "payment_date": i.payment_date,
                        "balance_amount":i.balance_loan_amount,
                        "perquisite_amount":round((i.balance_loan_amount*self.custom_loan_perquisite_rate_of_interest)/1200),
                        "payroll_date":t2

                        
                    })


            