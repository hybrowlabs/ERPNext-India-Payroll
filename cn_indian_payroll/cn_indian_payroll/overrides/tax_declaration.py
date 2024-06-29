
import frappe
from hrms.payroll.doctype.employee_tax_exemption_declaration.employee_tax_exemption_declaration import EmployeeTaxExemptionDeclaration


class CustomEmployeeTaxExemptionDeclaration(EmployeeTaxExemptionDeclaration):


    def validate(self):

        self.validate_tax_declaration()

        super().validate()




    

    def validate_tax_declaration(self):
        array=[]
        if len(self.declarations) > 0:
            for i in self.declarations:
                if i.exemption_category == "Section 80C":
                    array.append(i.amount)
        array_sum = sum(array)


        category=frappe.db.get_list('Employee Tax Exemption Category',
            filters={
                'name': 'Section 80C'
            },
            fields=['*'],
            
            
        )

        

        

        if len(category)>0:
           

            if(category[0].max_amount<array_sum):
             
                frappe.throw("You Cant Enter Amount Greater than "+str(category[0].max_amount))

        
           

        

        
           

        