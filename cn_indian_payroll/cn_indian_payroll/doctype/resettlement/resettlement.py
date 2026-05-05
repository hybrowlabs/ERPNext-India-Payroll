import frappe
from frappe.model.document import Document

class Resettlement(Document):
	def on_submit(self):
		if self.payable_earnings:
			for earning in self.payable_earnings:
				additional_salary = frappe.get_doc({
					"doctype": "Additional Salary",
					"employee": self.employee,
					"company": self.company,
					"payroll_date": self.transaction_date,
					"salary_component": earning.salary_component,
					"currency": "INR",
					"amount": earning.amount,
					"ref_doctype":"Resettlement",
					"ref_docname":self.name,


					})
				additional_salary.insert()
				additional_salary.submit()
		if self.receivable_deductions:
			for earning in self.receivable_deductions:
				additional_salary = frappe.get_doc({
					"doctype": "Additional Salary",
					"employee": self.employee,
					"company": self.company,
					"payroll_date": self.transaction_date,
					"salary_component": earning.salary_component,
					"currency": "INR",
					"amount": earning.amount,
					"ref_doctype":"Resettlement",
					"ref_docname":self.name,


				})
				additional_salary.insert()
				additional_salary.submit()

		if self.salary_slip_detail:
			for slip in self.salary_slip_detail:
				salary_slip=frappe.get_doc("Salary Slip",slip.salary_slip)
				salary_slip.custom_resettlement_updated=1
				salary_slip.save()
