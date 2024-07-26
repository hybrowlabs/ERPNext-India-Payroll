
import frappe
from hrms.payroll.doctype.employee_tax_exemption_declaration.employee_tax_exemption_declaration import EmployeeTaxExemptionDeclaration


class CustomEmployeeTaxExemptionDeclaration(EmployeeTaxExemptionDeclaration):


    def validate(self):

        self.validate_tax_declaration()

        super().validate()


    def on_submit(self):
        self.set_max_amount()




    
    def set_max_amount(self):
        self.total_exemption_amount=self.total_declared_amount


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
             
                frappe.throw("You can't enter amount in Section 80C greater than "+str(round(category[0].max_amount)))

        
           

        

        
           

        