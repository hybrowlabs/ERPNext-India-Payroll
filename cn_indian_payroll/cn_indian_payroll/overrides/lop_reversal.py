import frappe

def on_submit(self,method):
   
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
                'docstatus':1
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
                'docstatus':1
            })

            additional_doc.insert()

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


    