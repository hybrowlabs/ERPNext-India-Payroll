import frappe
from hrms.payroll.doctype.salary_structure_assignment.salary_structure_assignment import SalaryStructureAssignment


class CustomSalaryStructureAssignment(SalaryStructureAssignment):
    def before_save(self):

        self.set_cpl()
        self.reimbursement_amount()

        

    # def validate(self):
    #     self.insert_tax_declaration()
        


    def on_submit(self):
        self.insert_tax_declaration()
        # self.update_lta_in_employee()
       


    def on_cancel(self):
        self.cancel_declaration()



    def cancel_declaration(self):
        data=frappe.db.get_list('Employee Tax Exemption Declaration',
            filters={
                'payroll_period': self.custom_payroll_period,
                'docstatus': ['in', [0, 1]],
                'employee':self.employee,
                'custom_salary_structure_assignment':self.name,

            },
            fields=['*'],
            
        )

        

        if len(data)>0:

        

            data_doc=frappe.get_doc('Employee Tax Exemption Declaration',data[0].name)
        

            if data_doc.docstatus==0:
                frappe.delete_doc('Employee Tax Exemption Declaration', data_doc.name)

            if data_doc.docstatus==1:
                data_doc.docstatus=2

                data_doc.save()
                frappe.delete_doc('Employee Tax Exemption Declaration', data_doc.name)




    def insert_tax_declaration(self):
        array=[]
        amount=[]
        max_amount_category=[]
        if self.employee:
            if self.income_tax_slab=="Old Regime":

                if self.custom_is_uniform_allowance and self.custom_uniform_allowance_value:
                    uniform_component = frappe.get_list('Employee Tax Exemption Sub Category',
                            filters={'custom_salary_component':"Uniform"},
                            fields=['*'],
                        
                        )

                    if len(uniform_component)>0:
                        for i in uniform_component:
                            array.append(i.name)
                            amount.append(0)
                            
                            max_amount_category.append(i.max_amount)

                

                
                


                if self.custom_is_epf:

                    epf_amount=round((self.base * 0.35)/12 * .12)
                    epf_amount_year=round(epf_amount*12)

                    epf_component = frappe.get_list('Employee Tax Exemption Sub Category',
                            filters={'custom_salary_component':"Employee Provident Fund"},
                            fields=['*'],
                        
                        )

                    

                    if len(epf_component)>0:
                        for i in epf_component:
                            
                            array.append(i.name)
                            
                            max_amount_category.append(i.max_amount)

                            if epf_amount_year>i.max_amount:
                                amount.append(round(i.max_amount))

                            else:
                                amount.append(round(epf_amount_year))

                
                if self.custom_is_nps:
                    nps_amount=round(((self.base * 0.35)/12))
                    nps_amount_percentage=round((nps_amount*self.custom_nps_percentage)/100)
                    nps_amount_year=round(nps_amount_percentage*12)


                    nps_component = frappe.get_list('Employee Tax Exemption Sub Category',
                            filters={'custom_salary_component':"NPS"},
                            fields=['*'],
                        
                        )

                    if len(nps_component)>0:
                        for i in nps_component:
                            array.append(i.name)
                            max_amount_category.append(nps_amount_year)

                            amount.append(nps_amount_year)



                            
                   

                    
                if self.custom_state:
                    pt_component = frappe.get_list('Employee Tax Exemption Sub Category',
                            filters={'custom_salary_component':"Professional Tax (Gujarat)"},
                            fields=['*'],
                        
                        )

                    if len(pt_component)>0:
                        for i in pt_component:
                            array.append(i.name)
                            max_amount_category.append(i.max_amount)
                           
                            amount.append(2400)

               



            if self.income_tax_slab=="New Regime":

                if self.custom_is_nps:
                    nps_amount=round(((self.base * 0.35)/12 * self.custom_nps_percentage)/100)
                    nps_amount_year=round(nps_amount*12)


                    nps_component = frappe.get_list('Employee Tax Exemption Sub Category',
                            filters={'custom_salary_component':"NPS"},
                            fields=['*'],
                        
                        )

                    if len(nps_component)>0:
                        for i in nps_component:
                            array.append(i.name)
                            max_amount_category.append(nps_amount_year)

                            amount.append(nps_amount_year)


                

                


            doc1=frappe.get_list('Employee Tax Exemption Declaration',
                            filters={'employee':self.employee,'payroll_period':self.custom_payroll_period,'docstatus': ['in', [0, 1]]},
                            fields=['*'],
                        
                        )

            if len(doc1)==0:

                doc1 = frappe.get_doc({'doctype': 'Employee Tax Exemption Declaration'})
                doc1.employee= self.employee,
                doc1.company= self.company,
                doc1.payroll_period= self.custom_payroll_period,
                doc1.currency= self.currency,
                doc1.custom_income_tax=self.income_tax_slab,
                doc1.custom_salary_structure_assignment=self.name,
                doc1.custom_posting_date = frappe.utils.nowdate(),
                
                for x in range(len(array)):
                    
                        
                    doc2_child1 = doc1.append("declarations", {})
                    doc2_child1.exemption_sub_category = array[x]
                    doc2_child1.amount = amount[x]
                    doc2_child1.max_amount = max_amount_category[x]
                
                        
                doc1.insert()
                doc1.submit()  
                frappe.db.commit() 

           
                    

        



    def set_cpl(self):
        components = ["Vehicle Maintenance Reimbursement", "Petrol Reimbursement", "Leave Travel Allowance"]
        array=[]
        
        if self.custom_employee_reimbursements:
            for i in self.custom_employee_reimbursements:
                if i.reimbursements in components:
                    
                    array.append(i.reimbursements)

            
            if len(array)==3:
                self.custom_is_car_petrol_lta=1
               
            else:
                self.custom_is_car_petrol_lta=0



    def reimbursement_amount(self):
        total_amount = 0
        if len(self.custom_employee_reimbursements)>0:
            for reimbursement in self.custom_employee_reimbursements:
                total_amount += reimbursement.monthly_total_amount

        self.custom_statistical_amount = total_amount
        




                


    
                

                


            
        
        
        

       
                


