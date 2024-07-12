import frappe

@frappe.whitelist()
def accrual_created(payroll_entry_doc_id, company_name):
    if company_name:
        company_doc = frappe.get_doc('Company', company_name)
        if company_doc:
            salary_slips = frappe.get_list('Salary Slip', 
                filters={'payroll_entry': payroll_entry_doc_id},
                fields=['name', 'employee', 'payroll_entry', 'salary_structure','posting_date']
            )
            # frappe.msgprint(str(salary_slips))
            for salary_slip in salary_slips:
                salary_slip_doc = frappe.get_doc('Salary Slip', salary_slip.name)
                bonus_component_amount = None
                for earning in salary_slip_doc.earnings:
                    if earning.salary_component == company_doc.custom_bonus_salary_component:
                        bonus_component_amount = earning.amount
                        break
                if bonus_component_amount is not None:
                    ss_assignment = frappe.get_list('Salary Structure Assignment',
                        filters={'employee': salary_slip.employee,'docstatus':1},
                        fields=['name'],
                        order_by='from_date desc',
                        limit=1
                    )

                    if ss_assignment:

                        
                        for ssa_id in ss_assignment:
                           
                            
                            insert_bonus_accrual= frappe.get_doc({
                                
                                "doctype": "Employee Bonus Accrual",

                                "employee": salary_slip.employee,
                                "company":  company_name,
                                "accrual_date": salary_slip.posting_date,
                                "salary_component": company_doc.custom_bonus_salary_component,
                                "salary_structure":salary_slip.salary_structure,
                                "salary_structure_assignment": ssa_id.name,
                               
                                "payroll_entry":salary_slip.payroll_entry,
                                                                                            
                                "amount": bonus_component_amount


                            })
                            insert_bonus_accrual.insert()

                            if insert_bonus_accrual.name:
                                frappe.response['message'] = insert_bonus_accrual.name

                        

                    
@frappe.whitelist()
def get_submit(payroll_entry):

    
    
    if payroll_entry:
        bonus_list=frappe.db.get_list('Employee Bonus Accrual',
        filters={
            'payroll_entry': payroll_entry,
            'docstatus':0
        },
        fields=['name'],
        
        )
        
        if len(bonus_list)>0:

            for i in bonus_list:
               

                bonus_doc = frappe.get_doc('Employee Bonus Accrual',i.name)
                

                bonus_doc.docstatus = 1
                bonus_doc.save()
            
            if bonus_doc.name:
                frappe.response['message'] = bonus_doc.name

