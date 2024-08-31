import frappe



def on_cancel(self,method):

    cancel_additional_salary(self)
    cancel_appraisal_calculation(self)

def on_submit(self,method):
    self.custom_status="Completed"



def cancel_additional_salary(self):
    get_appraisal_additional = frappe.get_list('Additional Salary',
            filters={'custom_employee_promotion_id':self.name},
            fields=['*']
            )
    if get_appraisal_additional:
        
        for each_appraisal_doc in get_appraisal_additional:
            get_each_doc = frappe.get_doc('Additional Salary', each_appraisal_doc.name)
            get_each_doc.docstatus=2
            get_each_doc.save()

            frappe.delete_doc('Additional Salary', each_appraisal_doc.name)

def cancel_appraisal_calculation(self):
    get_appraisal_calculation = frappe.get_list('Salary Appraisal Calculation',
            filters={'employee_promotion_id':self.name},
            fields=['*']
            )
    if get_appraisal_calculation:
        
        for each_appraisal_doc in get_appraisal_calculation:
            get_each_doc = frappe.get_doc('Salary Appraisal Calculation', each_appraisal_doc.name)
            get_each_doc.docstatus=2
            get_each_doc.save()

            frappe.delete_doc('Salary Appraisal Calculation', each_appraisal_doc.name)

