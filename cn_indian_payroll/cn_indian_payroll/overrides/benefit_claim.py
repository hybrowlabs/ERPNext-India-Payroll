import frappe
from hrms.payroll.doctype.employee_benefit_claim.employee_benefit_claim import EmployeeBenefitClaim


class CustomEmployeeBenefitClaim(EmployeeBenefitClaim):
    
    def validate(self):

        super().validate()

        self.validate_employee()

    def on_submit(self):

        self.insert_future_benefit()


    def validate_employee(self):
        get_component = frappe.get_doc("Salary Component", self.earning_component)
        
        if get_component.component_type == "Vehicle Maintenance Reimbursement":
            get_salary_assignment = frappe.db.get_list(
                'Salary Structure Assignment',
                filters={
                    'docstatus': 1,
                    'employee': self.employee,
                },
                fields=['custom_car_maintenance'],
                order_by='from_date desc',
                limit=1
            )
            
            # Check if a salary assignment exists
            if get_salary_assignment:
                # Validate custom_car_maintenance value
                if get_salary_assignment[0].get('custom_car_maintenance', 0) == 0:
                    frappe.throw("You are not eligible to claim Vehicle Maintenance Reimbursement")
            else:
                # If no salary assignment is found, raise an error
                frappe.throw("No valid Salary Structure Assignment found for the employee.")








    def insert_future_benefit(self):

        if self.custom_max_amount:
        
        
            if self.claimed_amount>self.custom_max_amount:

                doc1 = frappe.get_doc('Salary Component', self.earning_component)
                if doc1.component_type=="Vehicle Maintenance Reimbursement":
                
                    date_str = self.claim_date       
                    year, month, day = map(int, date_str.split('-'))
                    new_month = month + 1
                    new_year = year
                    if new_month > 12:
                        new_month = 1
                        new_year += 1
                        
                    next_month_date = f"{new_year}-{new_month:02d}-{day:02d}"


                    future_amount=self.claimed_amount-self.custom_max_amount
                    insert_doc = frappe.get_doc({
                        'doctype':'Employee Benefit Claim',
                        'employee':self.employee,
                        'claim_date':next_month_date,
                        'currency':self.currency,
                        'company':self.company,
                        'claimed_amount':future_amount,
                        'earning_component':self.earning_component,
                        'docstatus':1

                    })
                    insert_doc.insert()

