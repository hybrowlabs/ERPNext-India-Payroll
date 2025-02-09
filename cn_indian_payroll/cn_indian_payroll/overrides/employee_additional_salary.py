import frappe
from hrms.payroll.doctype.additional_salary.additional_salary import AdditionalSalary

class CustomAdditionalSalary(AdditionalSalary):
    def validate(self):
        
        self.validate_dates()
        self.validate_salary_structure()
        self.validate_recurring_additional_salary_overlap()
        self.validate_employee_referral()
        self.validate_duplicate_additional_salary()
        self.validate_tax_component_overwrite()
