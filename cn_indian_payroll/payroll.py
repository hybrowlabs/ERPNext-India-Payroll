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
                
                if employee_id in employee_bonus_dict:
                    employee_bonus_dict[employee_id]['total_amount'] += amount
                    employee_bonus_dict[employee_id]['components'].add(salary_component)
                else:
                    employee_bonus_dict[employee_id] = {'total_amount': amount, 'components': {salary_component}}

        
        for employee_id, data in employee_bonus_dict.items():
            total_amount = data['total_amount']
            components = ', '.join(data['components'])
            
            additional_salary_insert = frappe.get_doc({
                'doctype': 'Additional Salary',
                'employee': employee_id,
                'company': doc1.company,
                'salary_component': components,
                'amount': total_amount,
                'payroll_date': doc1.posting_date,
                'docstatus': 1
            })
            
            additional_salary_insert.insert()














# @frappe.whitelist()
# def get_additional_salary(payroll_id):
#     if payroll_id:
#         doc1 = frappe.get_doc('Payroll Entry', payroll_id)
#         for i in doc1.employees:
#             employee_bonus = frappe.db.get_list('Employee Bonus Accrual',
#                                                  filters={
#                                                      'employee': i.employee,
#                                                      'docstatus': 1,
#                                                      'is_paid': 0,
#                                                  },
#                                                  fields=['name', 'amount', 'employee','salary_component','company']
#                                                  )
#             bonus_sum = sum(bonus['amount'] for bonus in employee_bonus)  # Calculate sum of employee amounts
#             frappe.msgprint("Employee: {}, Total Bonus Amount: {}".format(i.employee, bonus_sum))  # Print employee and total bonus amount
            

#             additional_salary_insert = frappe.get_doc({
#             'doctype': 'Additional Salary',
#             'employee': i.employee,
#             'company': i.employee_bonus,
#             'salary_component': i.salary_component,
#             'amount': bonus_sum,
#             'payroll_date': doc1.posting_date

#             })
#             additional_salary_insert.insert()













@frappe.whitelist()
def get_submit(payroll_entry):
    # frappe.msgprint(str(payroll_entry))
    if payroll_entry:
        bonus_list=frappe.db.get_list('Employee Bonus Accrual',
        filters={
            'payroll_entry': payroll_entry,
            'docstatus':0
        },
        fields=['name'],
        
        )
        # frappe.msgprint(str(bonus_list))

        if len(bonus_list)>0:

            for i in bonus_list:
               

                bonus_doc = frappe.get_doc('Employee Bonus Accrual',i.name)
                

                bonus_doc.docstatus = 1
                bonus_doc.save()
            
            if bonus_doc.name:
                frappe.response['message'] = bonus_doc.name


                


            



                    

                







        






