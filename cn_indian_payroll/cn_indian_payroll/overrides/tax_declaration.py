
import frappe
from hrms.payroll.doctype.employee_tax_exemption_declaration.employee_tax_exemption_declaration import EmployeeTaxExemptionDeclaration


class CustomEmployeeTaxExemptionDeclaration(EmployeeTaxExemptionDeclaration):


    # def validate(self):

    #     # self.validate_tax_declaration()
        

    #     super().validate()


    def on_submit(self):
        self.insert_declaration_history()


    


    def before_update_after_submit(self):
        
        self.calculate_hra_breakup()
        self.update_hra_breakup()
        self.update_tax_declaration()
        
        self.set_total_declared_amount()
        self.set_total_exemption_amount()
        self.calculate_hra_exemption()

    def on_cancel(self):
        self.cancel_declaration_history()
        





    def cancel_declaration_history(self):
        history_data=frappe.db.get_list('Tax Declaration History',
            filters={
                'tax_exemption':self.name,
            },
            fields=['*'],
            
        )

        if len(history_data)>0:
            data_doc=frappe.get_doc('Tax Declaration History',history_data[0].name)
            frappe.delete_doc('Tax Declaration History', data_doc.name)






    def update_hra_breakup(self):
        if self.monthly_house_rent:
            array = []
            for t1 in self.custom_hra_breakup:
                array.append({
                    "month": t1.month,
                    "rent_paid": t1.rent_paid,
                    "basic": t1.earned_basic,
                    "hra": t1.hra_received,
                    "basic_excess": t1.exemption_amount,
                    "exception_amount": t1.exemption_amount
                })

            # Fetch the latest Tax Declaration History for the employee
            get_latest_history = frappe.get_list(
                'Tax Declaration History',
                filters={'employee': self.employee},
                fields=['*'],
                order_by='posting_date desc',
                limit=1  

            )

            if len(get_latest_history) > 0:
                each_doc = frappe.get_doc("Tax Declaration History", get_latest_history[0].name)

                each_doc.monthly_house_rent=self.monthly_house_rent
                each_doc.rented_in_metro_city=self.rented_in_metro_city
                each_doc.hra_as_per_salary_structure=self.salary_structure_hra
                each_doc.annual_hra_exemption=self.annual_hra_exemption
                each_doc.monthly_hra_exemption=self.monthly_hra_exemption

                
                
                each_doc.hra_breakup = []

                for entry in array:
                    each_doc.append("hra_breakup", {
                        "month": entry["month"],
                        "rent_paid": entry["rent_paid"],
                        "earned_basic": entry["basic"],
                        "hra_received": entry["hra"],
                        "excess_of_rent_paid": entry["basic_excess"],
                        "exemption_amount": entry["exception_amount"]
                    })

                each_doc.save()
                frappe.db.commit()

    def update_tax_declaration(self):

        if len(self.declarations) > 0:
            tax_component = []
            for component in self.declarations:
                tax_component.append({
                    "sub_category": component.exemption_sub_category,
                    "category": component.exemption_category,
                    "max_amount": component.max_amount,
                    "amount": component.amount
                })

            hra_component = []
            for hra in self.custom_hra_breakup:
                hra_component.append({
                    "month": hra.month,
                    "rent_paid": hra.rent_paid,
                    "earned_basic": hra.earned_basic,
                    "hra_received": hra.hra_received,
                    "excess_of_rent_paid": hra.excess_of_rent_paid,
                    "exemption_amount": hra.exemption_amount
                })

            get_latest_history = frappe.get_list(
                'Tax Declaration History',
                filters={'employee': self.employee, "posting_date": self.custom_posting_date},
                fields=['*'],
                limit=1
            )

            if len(get_latest_history) > 0:
                each_doc = frappe.get_doc("Tax Declaration History", get_latest_history[0].name)

                each_doc.rented_in_metro_city = self.rented_in_metro_city
                each_doc.hra_as_per_salary_structure = self.salary_structure_hra
                each_doc.annual_hra_exemption = self.annual_hra_exemption
                each_doc.monthly_hra_exemption = self.monthly_hra_exemption
                each_doc.total_declared_amount = self.total_declared_amount
                each_doc.total_exemption_amount = self.total_exemption_amount

                each_doc.declaration_details = []
                for entry in tax_component:
                    each_doc.append("declaration_details", {
                        "exemption_sub_category": entry["sub_category"],
                        "exemption_category": entry["category"],
                        "maximum_exempted_amount": entry["max_amount"],
                        "declared_amount": entry["amount"],
                    })

                each_doc.hra_breakup = []
                for hra_entry in hra_component:
                    each_doc.append("hra_breakup", {
                        "month": hra_entry["month"],
                        "rent_paid": hra_entry["rent_paid"],
                        "earned_basic": hra_entry["earned_basic"],
                        "hra_received": hra_entry["hra_received"],
                        "excess_of_rent_paid": hra_entry["excess_of_rent_paid"],
                        "exemption_amount": hra_entry["exemption_amount"],
                    })

                each_doc.save()
                frappe.db.commit()

            else:
                insert_history = frappe.get_doc({
                    'doctype': 'Tax Declaration History',
                    'employee': self.employee,
                    'employee_name': self.employee_name,
                    'income_tax': self.custom_income_tax,
                    'company': self.company,
                    'posting_date': self.custom_posting_date,
                    'payroll_period': self.payroll_period,
                    'tax_exemption': self.name,
                    'total_declared_amount': self.total_declared_amount,
                    'total_exemption_amount': self.total_exemption_amount,
                    'monthly_house_rent': self.monthly_house_rent,
                    'rented_in_metro_city': self.rented_in_metro_city,
                    'hra_as_per_salary_structure': self.salary_structure_hra,
                    'annual_hra_exemption': self.annual_hra_exemption,
                    'monthly_hra_exemption': self.monthly_hra_exemption,
                    'declaration_details': [
                        {
                            "exemption_sub_category": entry["sub_category"],
                            "exemption_category": entry["category"],
                            "maximum_exempted_amount": entry["max_amount"],
                            "declared_amount": entry["amount"],
                        } for entry in tax_component
                    ],
                    'hra_breakup': [
                        {
                            "month": hra_entry["month"],
                            "rent_paid": hra_entry["rent_paid"],
                            "earned_basic": hra_entry["earned_basic"],
                            "hra_received": hra_entry["hra_received"],
                            "excess_of_rent_paid": hra_entry["excess_of_rent_paid"],
                            "exemption_amount": hra_entry["exemption_amount"],
                        } for hra_entry in hra_component
                    ]
                })

                insert_history.insert()
                frappe.db.commit()










    
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

        
    def insert_declaration_history(self):
        if self.employee:
            declaration_details = []
            hra_breakup=[]

            for i in self.declarations:
                declaration_details.append({
                    'exemption_sub_category': i.exemption_sub_category,
                    'exemption_category': i.exemption_category,
                    'maximum_exempted_amount': i.max_amount,
                    'declared_amount': i.amount
                })

            for j in self.custom_hra_breakup:
                hra_breakup.append({
                    'month': j.month,
                    'rent_paid': j.rent_paid,
                    'earned_basic': j.earned_basic,
                    'hra_received': j.hra_received,
                    'excess_of_rent_paid':j.excess_of_rent_paid,
                    'exemption_amount':j.exemption_amount
                })


            insert_doc = frappe.get_doc({
                'doctype': 'Tax Declaration History',
                'employee': self.employee,
                'employee_name':self.employee_name,
                'income_tax': self.custom_income_tax, 
                'company': self.company,
                'posting_date': frappe.utils.nowdate(),
                'payroll_period': self.payroll_period,
                'monthly_house_rent': self.monthly_house_rent,
                'rented_in_metro_city': self.rented_in_metro_city,
                'hra_as_per_salary_structure': self.salary_structure_hra,  
                'total_declared_amount': self.total_declared_amount,
                'annual_hra_exemption': self.annual_hra_exemption,
                'monthly_hra_exemption': self.monthly_hra_exemption,
                'total_exemption_amount': self.total_exemption_amount,
                'tax_exemption':self.name,
                'declaration_details': declaration_details,
                'hra_breakup': hra_breakup
            })

            insert_doc.insert()
            

    def calculate_hra_breakup(self):
        
        if self.monthly_house_rent:

            months = ["April", "May", "June", "July", "August", "September", "October", "November", "December","January", "February", "March"]
            basic_salary=(self.monthly_house_rent-self.monthly_hra_exemption)/0.1
            earned_basic = 0
            if self.rented_in_metro_city==1:
                earned_basic=(basic_salary*50)/100
            else:
                earned_basic=(basic_salary*40)/100
            

            self.custom_hra_breakup=[]
            for i in range(len(months)):
                self.append("custom_hra_breakup", {
                    "month": months[i],
                    "rent_paid": self.monthly_house_rent,
                    "hra_received": self.salary_structure_hra / 12,
                    "excess_of_rent_paid":round(self.monthly_hra_exemption),
                    "exemption_amount":round(self.monthly_hra_exemption),
                    "earned_basic":round(earned_basic)
                })

        else:
            self.custom_hra_breakup=[]

   



        

        
           

        