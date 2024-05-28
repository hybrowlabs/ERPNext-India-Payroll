
import frappe



@frappe.whitelist()
def get_additional_salary(payroll_id):
    if payroll_id:
        doc1 = frappe.get_doc('Payroll Entry', payroll_id)
        employee_bonus_dict = {}  
        for employee in doc1.employees:
            employee_bonus = frappe.db.get_list('Employee Bonus Accrual',
                                                 filters={
                                                     'employee': employee.employee,
                                                     'docstatus': 1,
                                                     'is_paid': 0,
                                                 },
                                                 fields=['name', 'amount', 'employee', 'salary_component', 'company']
                                                 )

            for bonus in employee_bonus:
                employee_id = bonus['employee']
                amount = bonus['amount']
                salary_component = bonus['salary_component']
                document_name = bonus['name']
                
                if employee_id in employee_bonus_dict:
                    employee_bonus_dict[employee_id]['total_amount'] += amount
                    employee_bonus_dict[employee_id]['components'].add(salary_component)
                    employee_bonus_dict[employee_id]['documents'].append(document_name)
                else:
                    employee_bonus_dict[employee_id] = {'total_amount': amount, 'components': {salary_component}, 'documents': [document_name]}

        

        for employee_id, data in employee_bonus_dict.items():
            total_amount = data['total_amount']
            components = ', '.join(data['components'])
            document_names = data['documents']

            additional_salary_insert = frappe.get_doc({
                'doctype': 'Additional Salary',
                'employee': employee_id,
                'company': doc1.company,
                'salary_component': components,
                'amount': total_amount,
                'payroll_date': doc1.posting_date,
                
                'custom_payroll_entry':payroll_id
            })
            
            additional_salary_insert.insert()

            # for doc_name in document_names:
            #     bonus_doc = frappe.get_doc('Employee Bonus Accrual', doc_name)
            #     bonus_doc.is_paid = 1
            #     bonus_doc.save()

        frappe.msgprint('Additional Salary Created')
        doc1.custom_additional_salary_created=1
        doc1.save()

                










@frappe.whitelist()
def additional_salary_submit(additional):
    if additional:
       
        additional_list=frappe.db.get_list('Additional Salary',
        filters={
            'custom_payroll_entry': additional,
            'docstatus':0
        },
        fields=['name','employee','payroll_date'],
        
        )
        
        if len(additional_list)>0:

           

            for i in additional_list:
               

                additional_doc = frappe.get_doc('Additional Salary',i.name)

                
                additional_doc.docstatus = 1
                additional_doc.save()


                
                employee_bonus = frappe.db.get_list('Employee Bonus Accrual',
                                                 filters={
                                                     'employee': i.employee,
                                                     'docstatus': 1,
                                                     'is_paid': 0,
                                                 },
                                                 fields=['name', 'amount', 'employee', 'salary_component', 'company']
                                                 )
                
                
                for bonus in employee_bonus:
                    doc_id = bonus['name']
                    bonus_doc1 = frappe.get_doc('Employee Bonus Accrual',doc_id)
                

                    bonus_doc1.is_paid = 1
                    bonus_doc1.bonus_paid_date=additional_doc.payroll_date
                    bonus_doc1.save()

                    

                



               

        frappe.msgprint('Additional Salary Submitted')

        additional_doc_list= frappe.get_doc('Payroll Entry',additional)

        
        additional_doc_list.custom_additional_salary_submitted=1
        additional_doc_list.save()




















def employee_benefit_validate(self, method):
    if self.employee:
        accrual_list = frappe.get_list('Employee Benefit Accrual',
            filters={'employee': self.employee,"salary_component":self.earning_component,"docstatus":1},
            fields=['name', 'amount']
        )

        if accrual_list:
            total_amount = sum(accrual['amount'] for accrual in accrual_list)

            if self.claimed_amount > total_amount:
                # frappe.throw("Claimed amount cannot exceed total accrued amount."+total_amount)
                frappe.throw("Claimed amount cannot exceed total accrued amount: " + str(total_amount))

                
                
                



        
                