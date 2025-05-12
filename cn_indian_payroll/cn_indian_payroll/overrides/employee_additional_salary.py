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
        # Find all Salary Slips where the additional_salary_date falls within start and end date
        salary_slips = frappe.get_list(
            'Salary Slip',
            filters={
                'docstatus': 0,
                'start_date': ['<=', self.payroll_date],
                'end_date': ['>=', self.payroll_date]
            },
            fields=['name']
        )

        for slip in salary_slips:
            ss_doc = frappe.get_doc('Salary Slip', slip.name)

            # Filter out the rows where additional_salary == self.name
            updated_details = [
                d for d in ss_doc.earnings
                if d.additional_salary != self.name
            ]

            # Assign filtered list back to the earnings child table
            ss_doc.set('earnings', updated_details)

            # Save the updated Salary Slip
            ss_doc.save()
