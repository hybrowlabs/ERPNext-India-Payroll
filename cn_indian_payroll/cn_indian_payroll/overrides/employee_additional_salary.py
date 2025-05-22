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

    def on_cancel(self):
    # Find all draft Salary Slips where payroll_date falls between start_date and end_date
        salary_slips = frappe.get_list(
            'Salary Slip',
            filters={
                'docstatus': 0,
                'start_date': ['<=', self.payroll_date],
                'end_date': ['>=', self.payroll_date],
                'employee': self.employee,
            },
            fields=['name']
        )

        for slip in salary_slips:
            ss_doc = frappe.get_doc('Salary Slip', slip.name)

            # Filter out earnings and deductions linked to this additional salary
            updated_earnings = [
                d for d in ss_doc.earnings
                if d.additional_salary != self.name
            ]
            updated_deductions = [
                d for d in ss_doc.deductions
                if d.additional_salary != self.name
            ]

            # Update the child tables
            ss_doc.set('earnings', updated_earnings)
            ss_doc.set('deductions', updated_deductions)

            # Save the updated Salary Slip
            ss_doc.save()
