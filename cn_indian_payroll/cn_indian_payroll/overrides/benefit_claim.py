import frappe
from hrms.payroll.doctype.employee_benefit_claim.employee_benefit_claim import (
    EmployeeBenefitClaim,validate_active_employee,
    get_max_benefits,
    get_payroll_period,
)
from frappe.utils import getdate

from frappe.utils import add_months



class CustomEmployeeBenefitClaim(EmployeeBenefitClaim):
    def on_submit(self):
        # self.insert_future_benefit()
        self.insert_additional_salary()


    def validate(self):
        super().validate()
        self.set_taxable_or_non_taxable()


    def set_taxable_or_non_taxable(self):
        if self.earning_component and self.claimed_amount:
            component=frappe.get_doc("Salary Component",self.earning_component)
            if component.is_tax_applicable==1:
                self.custom_is_taxable=1
                self.custom_taxable_amount=self.claimed_amount
            else:
                self.custom_is_non_taxable=1
                self.custom_non_taxable_amount=self.claimed_amount






    def insert_future_benefit(self):
        if self.custom_max_amount:
            if self.claimed_amount > self.custom_max_amount:
                doc1 = frappe.get_doc("Salary Component", self.earning_component)
                if doc1.component_type == "Vehicle Maintenance Reimbursement":
                    date_str = self.claim_date
                    year, month, day = map(int, date_str.split("-"))
                    new_month = month + 1
                    new_year = year
                    if new_month > 12:
                        new_month = 1
                        new_year += 1

                    next_month_date = f"{new_year}-{new_month:02d}-{day:02d}"

                    future_amount = self.claimed_amount - self.custom_max_amount
                    insert_doc = frappe.get_doc(
                        {
                            "doctype": "Employee Benefit Claim",
                            "employee": self.employee,
                            "claim_date": next_month_date,
                            "currency": self.currency,
                            "company": self.company,
                            "claimed_amount": future_amount,
                            "earning_component": self.earning_component,
                            "docstatus": 1,
                        }
                    )
                    insert_doc.insert()

    def insert_additional_salary(self):
        if self.employee and self.claimed_amount and self.earning_component:
            insert_doc = frappe.get_doc(
                {
                    "doctype": "Additional Salary",
                    "employee": self.employee,
                    "salary_component": self.earning_component,
                    "amount": self.claimed_amount,
                    "company": self.company,
                    "currency": self.currency,
                    "payroll_date": self.claim_date,
                    "overwrite_salary_structure_amount": 0,
                    "ref_doctype": self.doctype,
                    "ref_docname": self.name,
                }
            )

            insert_doc.insert()
            insert_doc.submit()



    def before_submit(self):
        if self.custom_status=="Pending":
            frappe.throw("Please Select the Status Approved or Rejected")
