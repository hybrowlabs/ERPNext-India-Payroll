import frappe
from hrms.payroll.doctype.salary_structure_assignment.salary_structure_assignment import SalaryStructureAssignment


class CustomSalaryStructureAssignment(SalaryStructureAssignment):
    def before_save(self):

        

    

        self.set_cpl()

        self.reimbursement_amount()


    def on_submit(self):
        self.insert_tax_declaration()
       




    def insert_tax_declaration(self):
        array=[]
        if self.employee:
            if self.custom_is_uniform_allowance and self.custom_uniform_allowance_value:
                component = frappe.get_list('Employee Tax Exemption Sub Category',
                        filters={'custom_is_uniform':1},
                        fields=['name'],
                       
                    )

                if component:
                    for i in component:
                        array.append(i.name)

            if self.custom_is_medical_allowance and self.custom_medical_allowance_value:
                component = frappe.get_list('Employee Tax Exemption Sub Category',
                        filters={'custom_is_medical':1},
                        fields=['name'],
                       
                    )

                if component:
                    for i in component:
                        array.append(i.name)

            if self.custom_is_epf:
                component = frappe.get_list('Employee Tax Exemption Sub Category',
                        filters={'custom_is_epf':1},
                        fields=['name'],
                       
                    )

                if component:
                    for i in component:
                        array.append(i.name)


            if self.custom_is_nps:
                component = frappe.get_list('Employee Tax Exemption Sub Category',
                        filters={'custom_is_nps':1},
                        fields=['name'],
                       
                    )

                if component:
                    for i in component:
                        array.append(i.name)

            if self.custom_state:
                component = frappe.get_list('Employee Tax Exemption Sub Category',
                        filters={'custom_is_pt':1},
                        fields=['name'],
                       
                    )

                if component:
                    for i in component:
                        array.append(i.name)





        
            doc1 = frappe.get_doc({'doctype': 'Employee Tax Exemption Declaration'})
                
            doc1.employee= self.employee,
            doc1.company= self.company,
            doc1.payroll_period= self.custom_payroll_period,
            doc1.currency= self.currency,

            for x in range(len(array)):
               
                
                doc2_child1 = doc1.append("declarations", {})
                doc2_child1.exemption_sub_category = array[x]
                
                doc2_child1. amount= 0
                
                
            
            doc1.insert()

           
                    

        



    def set_cpl(self):
        # components = ["Vehicle Maintenance Reimbursement", "Petrol Reimbursement", "Leave Travel Allowance"]
        array=[]
        
        if self.custom_employee_reimbursements:
            for i in self.custom_employee_reimbursements:
                doc1 = frappe.get_doc('Salary Component', i.reimbursements)
                if(doc1.custom_is_reimbursement==1):
                   
                    array.append(doc1.name)



            
            if len(array)==3:
                self.custom_is_car_petrol_lta=1
               
            else:
                self.custom_is_car_petrol_lta=0



    def reimbursement_amount(self):
        total_amount = 0
        if self.custom_employee_reimbursements:
            for reimbursement in self.custom_employee_reimbursements:
                total_amount += reimbursement.monthly_total_amount

        self.custom_statistical_amount = total_amount
        




                


    
                

                


            
        
        
        

       
                


