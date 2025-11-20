# Copyright (c) 2025, Hybrowlabs technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip
from datetime import datetime
import calendar


class NewJoiningArrear(Document):
	def before_save(self):
		self.insert_breakup_table()


	def on_submit(self):
		self.insert_additional_salary()
		self.insert_benefit_ledger()


	def insert_benefit_ledger(self):
		if self.reimbursement_component:
			for row in self.reimbursement_component:
				component=frappe.get_doc("Salary Component",row.salary_component)
				if component.is_flexible_benefit==1:
					benefit_ledger = frappe.new_doc("Employee Benefit Ledger")
					benefit_ledger.posting_date = self.posting_date
					benefit_ledger.employee = self.employee
					benefit_ledger.salary_component = row.salary_component
					benefit_ledger.amount = row.amount
					benefit_ledger.company = self.company
					benefit_ledger.payroll_period=self.payroll_period

					benefit_ledger.transaction_type = "Accrual"
					benefit_ledger.yearly_benefit = row.custom_actual_amount*12
					benefit_ledger.remarks = "Pro rata flexible benefit accrual"
					benefit_ledger.flexible_benefit = 1

					benefit_ledger.insert()
					benefit_ledger.submit()
				else:
					benefit_ledger = frappe.new_doc("Employee Benefit Ledger")
					benefit_ledger.posting_date = self.posting_date
					benefit_ledger.employee = self.employee
					benefit_ledger.salary_component = row.salary_component
					benefit_ledger.amount = row.amount
					benefit_ledger.company = self.company
					benefit_ledger.payroll_period=self.payroll_period

					benefit_ledger.transaction_type = "Accrual"
					benefit_ledger.yearly_benefit = 0
					benefit_ledger.remarks = "Accrual Component assigned via salary structure"
					benefit_ledger.flexible_benefit = 0

					benefit_ledger.insert()
					benefit_ledger.submit()


	def insert_additional_salary(self):
		if not (self.earning_component or self.deduction_component):
			return

		for row in self.earning_component:
			additional_salary = frappe.new_doc("Additional Salary")
			additional_salary.employee = self.employee
			additional_salary.salary_component = row.salary_component
			additional_salary.amount = row.amount
			additional_salary.company = self.company
			additional_salary.payroll_date = self.payout_date
			additional_salary.currency = "INR"
			additional_salary.ref_doctype = "New Joining Arrear"
			additional_salary.ref_docname = self.name
			additional_salary.insert()
			additional_salary.submit()

		for row in self.deduction_component:
			additional_salary = frappe.new_doc("Additional Salary")
			additional_salary.employee = self.employee
			additional_salary.salary_component = row.salary_component
			additional_salary.amount = row.amount
			additional_salary.company = self.company
			additional_salary.payroll_date = self.payout_date
			additional_salary.currency = "INR"
			additional_salary.ref_doctype = "New Joining Arrear"
			additional_salary.ref_docname = self.name
			additional_salary.insert()
			additional_salary.submit()

	def insert_breakup_table(self):
		if not self.employee:
			return

		payout_date = self.payout_date

		salary_structure_assignment = frappe.get_list(
			"Salary Structure Assignment",
			filters={
				"employee": self.employee,
				"company": self.company,
				"docstatus": 1,
			},
			fields=["*"],
			order_by="from_date desc",
			limit=1,
		)

		if not salary_structure_assignment:
			return

		salary_structure = salary_structure_assignment[0].salary_structure
		from_date = salary_structure_assignment[0].from_date
		self.payroll_period=salary_structure_assignment[0].custom_payroll_period


		ssa=frappe.get_doc("Salary Structure Assignment",salary_structure_assignment[0].name)


		new_salary_slip = make_salary_slip(
			source_name=salary_structure,
			employee=self.employee,
			print_format="Salary Slip Standard",
			posting_date=from_date,
			for_preview=1,
		)

		processed_components = []
		earning_components = []
		deduction_components = []
		reimbursement_components = []

		for accrued_benefit in new_salary_slip.accrued_benefits:
			salary_component_doc = frappe.get_doc("Salary Component", accrued_benefit.salary_component)

			if salary_component_doc.arrear_component == 1 and not salary_component_doc.is_flexible_benefit == 1:
				reimbursement_components.append({
					"salary_component": accrued_benefit.salary_component,
					"amount": round(
						(accrued_benefit.amount / new_salary_slip.total_working_days) * self.number_of_present_days
					),
					"custom_actual_amount":round(accrued_benefit.amount)
				})

			if salary_component_doc.arrear_component == 1 and salary_component_doc.is_flexible_benefit == 1:
				reimbursement_components.append({
					"salary_component": accrued_benefit.salary_component,
					"amount": round(
						((accrued_benefit.amount / 12) / new_salary_slip.total_working_days) * self.number_of_present_days
					),
					"custom_actual_amount":round(accrued_benefit.amount)
				})





		for new_earning in new_salary_slip.earnings:
			component_doc = frappe.get_value(
				"Salary Component",
				filters={
					"name": new_earning.salary_component,
					"disabled": 0,
				},
				fieldname=["name", "arrear_component"],
				as_dict=True,
			)

			if not component_doc or component_doc.name in processed_components:
				continue

			if component_doc.arrear_component == 1:
				earning_components.append(
					{
						"salary_component": component_doc.name,
						"amount": round(
							(new_earning.amount / new_salary_slip.total_working_days)
							* self.number_of_present_days
						),
						"custom_actual_amount":round(accrued_benefit.amount)
					}
				)
				processed_components.append(component_doc.name)

		for new_deduction in new_salary_slip.deductions:
			component_doc = frappe.get_value(
				"Salary Component",
				filters={
					"name": new_deduction.salary_component,
					"disabled": 0,
				},
				fieldname=["name", "arrear_component"],
				as_dict=True,
			)

			if not component_doc or component_doc.name in processed_components:
				continue

			if component_doc.arrear_component == 1:
				deduction_components.append(
					{
						"salary_component": component_doc.name,
						"amount": round(
							(new_deduction.amount / new_salary_slip.total_working_days)
							* self.number_of_present_days
						),
						"custom_actual_amount":round(accrued_benefit.amount)
					}
				)
				processed_components.append(component_doc.name)

		self.set("earning_component", [])
		self.set("deduction_component", [])
		self.set("reimbursement_component",[])

		for row in earning_components:
			self.append("earning_component", row)

		for row in deduction_components:
			self.append("deduction_component", row)

		for row in reimbursement_components:
			self.append("reimbursement_component", row)
