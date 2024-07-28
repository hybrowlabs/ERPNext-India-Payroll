import frappe

def on_submit(self, method):
    
    



   
    if len(self.arrear_breakup)>0:
        for i in self.arrear_breakup:
            

            additional_doc = frappe.get_doc({
                'doctype': 'Additional Salary',
                'employee':self.employee,
                'company':self.company,
                'payroll_date':self.additional_salary_date,
                'custom_payroll_entry':self.payroll_entry,
                'salary_component':i.salary_component,
                'currency':'INR',
                'amount':i.amount,
                'docstatus':1,
                'custom_lop_reversal':self.name,
                'custom_lop_reversal_days':self.number_of_days
            })
            additional_doc.insert()

    if len(self.arrear_deduction_breakup)>0:
        for j in self.arrear_deduction_breakup:
            

            additional_doc = frappe.get_doc({
                'doctype': 'Additional Salary',
                'employee':self.employee,
                'company':self.company,
                'payroll_date':self.additional_salary_date,
                'salary_component':j.salary_component,
                'custom_payroll_entry':self.payroll_entry,
                'currency':'INR',
                'amount':j.amount,
                'docstatus':1,
                'custom_lop_reversal':self.name,
                'custom_lop_reversal_days':self.number_of_days


            })

            additional_doc.insert()


    if self.payroll_entry:


        payroll_entry_doc=frappe.db.get_list('Salary Slip',
                filters={
                    'payroll_entry': self.payroll_entry,
                    'employee':self.employee
                },
                fields=["*"],
                
            )

       
        if len(payroll_entry_doc)>0:
            payroll_entry_doc1 = frappe.get_doc('Salary Slip', payroll_entry_doc[0].name)
            payroll_entry_doc1.custom_lop_updated = 1
            payroll_entry_doc1.save()


    
    reimbursement_accrual_update(self)
    bonus_accrual_update(self)



def reimbursement_accrual_update(self):
        lop_reversal = frappe.get_list('Employee Benefit Accrual',
                        filters={'employee': self.employee,'docstatus':1,"salary_slip":self.salary_slip},
                        fields=['*'],
                       
                    )


        if len(lop_reversal)>0:
            for i in lop_reversal:
                each_doc = frappe.get_doc('Employee Benefit Accrual', i.name)
                lop_reversal_amount=(each_doc.amount/self.working_days)*self.number_of_days
                eligible_amount=each_doc.amount+lop_reversal_amount

                each_doc.amount = round(eligible_amount)
                each_doc.save()




def bonus_accrual_update(self):
    lop_reversal_bonus = frappe.get_list('Employee Bonus Accrual',
                                         filters={'employee': self.employee, 'docstatus': 1, 'salary_slip': self.salary_slip},
                                         fields=['name', 'amount'])

    if lop_reversal_bonus:
        for bonus in lop_reversal_bonus:
            each_doc_bonus = frappe.get_doc('Employee Bonus Accrual', bonus.name)
            lop_reversal_amount_bonus = (each_doc_bonus.amount / self.working_days) * self.number_of_days
            eligible_amount_bonus = each_doc_bonus.amount + lop_reversal_amount_bonus
            each_doc_bonus.amount = round(eligible_amount_bonus)
            each_doc_bonus.save()

        


        




        


def on_cancel(self,method):

    get_additional_arrears=frappe.db.get_list('Additional Salary',
                filters={
                    'custom_payroll_entry': self.payroll_entry
                },
                fields=['*'],
                
            )

    if len(get_additional_arrears)>0:
        for j in get_additional_arrears:
            arrear_doc = frappe.get_doc('Additional Salary', j.name)
            arrear_doc.docstatus = 2
            arrear_doc.save()




    lop_reversal = frappe.get_list('Employee Benefit Accrual',
                        filters={'employee': self.employee,'docstatus':1,"salary_slip":self.salary_slip},
                        fields=['*'],
                       
                    )

    


    if len(lop_reversal)>0:
        for i in lop_reversal:
            each_doc = frappe.get_doc('Employee Benefit Accrual', i.name)
            total_days=self.working_days+self.number_of_days
            lop_reversal_amount=(each_doc.amount/total_days)
            eligible_amount=lop_reversal_amount*self.working_days

            each_doc.amount = round(eligible_amount)
            each_doc.save()



    lop_reversal_bonus = frappe.get_list('Employee Bonus Accrual',
                                         filters={'employee': self.employee, 'docstatus': 1, 'salary_slip': self.salary_slip},
                                         fields=['name', 'amount'])

    if lop_reversal_bonus:
        for bonus in lop_reversal_bonus:
            each_doc_bonus = frappe.get_doc('Employee Bonus Accrual', bonus.name)
            total_days=self.working_days+self.number_of_days
            lop_reversal_amount=(each_doc_bonus.amount/total_days)
            eligible_amount=lop_reversal_amount*self.working_days

            each_doc_bonus.amount = round(eligible_amount)
            each_doc_bonus.save()





    salary_slip=frappe.db.get_list('Salary Slip',
                filters={
                    'name': self.salary_slip
                },
                fields=['*'],
                
            )

    if len(salary_slip)>0:


        salary_slip_doc = frappe.get_doc('Salary Slip',salary_slip[0].name)
        salary_slip_doc.custom_lop_updated = 0
        salary_slip_doc.save()

    








    