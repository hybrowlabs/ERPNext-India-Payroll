import frappe



def validate(self,method):
    amount=0

    if self.employee:
        component=[]


        company_data=frappe.db.get_list('Company',
            filters={
                'name': self.company,
            },
            fields=['*'],
            
            )
        if company_data[0].custom_lta_component:
            
            get_salary_assignment = frappe.db.get_list('Salary Structure Assignment',
                filters={
                    'docstatus': 1,
                    'employee': self.employee,
                },
                fields=['*'],
                order_by='from_date desc'
            )
            

            if get_salary_assignment[0].name:
               

                employee_doc = frappe.get_doc('Salary Structure Assignment', get_salary_assignment[0].name)

                
                if len(employee_doc.custom_employee_reimbursements)>0:
                    for j in employee_doc.custom_employee_reimbursements:
                        
                        component.append(j.reimbursements)

        

        if company_data[0].custom_lta_component not in component:
            frappe.throw("you are not eligible for claim LTA")
            
            

        
                        








    if self.non_taxable_amount!=None:
        amount+=self.non_taxable_amount

    if self.non_taxable_amount!=None:
        amount+=self.taxable_amount
        

    if self.amount>amount and amount!=0:
        frappe.throw("Cannot enter the amount greater than the sum of taxable and non-taxable amounts")

    