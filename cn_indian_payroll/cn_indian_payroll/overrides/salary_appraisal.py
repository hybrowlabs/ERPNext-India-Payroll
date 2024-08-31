import frappe

def on_submit(self,method):


    insert_additional_salary(self)
    update_bonus_accrual(self)
    update_reimbursement_accruals(self)


# def on_cancel(self,method):

#     cancel_additional_salary(self)
#     reverse_bonus_accrual(self)
#     reverse_benefit_accrual(self)




def update_bonus_accrual(self):
    if len(self.bonus_components)>0:
        for j in self.bonus_components:
            bonus_accrual = frappe.get_list('Employee Bonus Accrual',
            filters={'employee':self.employee, "salary_slip":j.salary_slip_id},
            fields=['*']
            )
            if bonus_accrual:
                for k in bonus_accrual:
                    get_doc = frappe.get_doc('Employee Bonus Accrual', k.name)
                    if j.difference < 0:
                        difference = 0
                    else:
                        difference = j.difference

                    
                    get_doc.amount += difference
                    get_doc.save()
                    

def update_reimbursement_accruals(self):
    if len(self.reimbursement_components) > 0:
        for accrual in self.reimbursement_components:
            benefit_accrual = frappe.get_list('Employee Benefit Accrual',
                filters={'employee': self.employee, "salary_slip": accrual.salary_slip_id, "salary_component": accrual.salary_component},
                fields=['*']
            )
            if benefit_accrual:
                for each_accrual_doc in benefit_accrual:
                    get_doc = frappe.get_doc('Employee Benefit Accrual', each_accrual_doc.name)
                    
                    
                    if accrual.difference < 0:
                        difference = 0
                    else:
                        difference = accrual.difference

                    
                    get_doc.amount += difference
                    get_doc.save()


def insert_additional_salary(self):
    component_array = []
    
    if len(self.salary_arrear_components) > 0:
        for i in self.salary_arrear_components:
            component_array.append({
                "component": i.salary_component,
                "amount": i.difference
            })

        aggregated_components = {}

        for component in component_array:
            name = component['component']
            amount = component['amount']
            
            
            if name in aggregated_components:
                aggregated_components[name] += amount
            else:
                aggregated_components[name] = amount

        result = [{'component': k, 'amount': v} for k, v in aggregated_components.items()]

        for insert in result:
            salary_component = frappe.get_list('Salary Component',
                        filters={'custom_is_arrear':1, "custom_component":insert['component']},
                        fields=['*']
                    )

            if salary_component:

                for t in salary_component:
                    
                    insert_doc = frappe.get_doc({
                        'doctype': 'Additional Salary',
                        'employee': self.employee,
                        'payroll_date': self.posting_date,
                        'salary_component': t.name,
                        'company': self.company,
                        'currency': "INR",
                        'amount': insert['amount'],
                        'docstatus':1,
                        'custom_salary_appraisal_calculation':self.name,
                        'custom_employee_promotion_id':self.employee_promotion_id,
                        
                    })
                    insert_doc.insert()


def cancel_additional_salary(self):
    get_appraisal_additional = frappe.get_list('Additional Salary',
            filters={'custom_salary_appraisal_calculation':self.name},
            fields=['*']
            )
    if get_appraisal_additional:
        # frappe.msgprint(str(get_appraisal_additional))
        for each_appraisal_doc in get_appraisal_additional:
            get_each_doc = frappe.get_doc('Additional Salary', each_appraisal_doc.name)
            get_each_doc.docstatus=2
            get_each_doc.save()


def reverse_bonus_accrual(self):
    if len(self.bonus_components)>0:
        for j in self.bonus_components:
            bonus_accrual = frappe.get_list('Employee Bonus Accrual',
            filters={'employee':self.employee, "salary_slip":j.salary_slip_id},
            fields=['*']
            )
            if len(bonus_accrual)>0:
                for k in bonus_accrual:
                    get_doc = frappe.get_doc('Employee Bonus Accrual', k.name)
                    if j.difference < 0:
                        difference = 0
                    else:
                        difference = j.difference   
                    get_doc.amount -= difference
                    get_doc.save()


                
                    

def reverse_benefit_accrual(self):
    if len(self.reimbursement_components) > 0:
        for component in self.reimbursement_components:
            benefit_accrual = frappe.get_list('Employee Benefit Accrual',
                filters={'employee': self.employee, "salary_slip": component.salary_slip_id, "salary_component": component.salary_component},
                fields=['*']
            )
            if benefit_accrual:
                for accrual in benefit_accrual:
                    get_accrued_doc = frappe.get_doc('Employee Benefit Accrual', accrual.name)
                    if component.difference < 0:
                        difference = 0
                    else:
                        difference = component.difference

                    
                    get_accrued_doc.amount -= difference
                    get_accrued_doc.save()
                    

                   



