# Copyright (c) 2025, Hybrowlabs technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip


class JoiningSalaryArrear(Document):
    def before_save(self):
        frappe.msgprint("Before Save")
        # if self.employee:
        # 	salary_structure_assignment = frappe.get_list(
        #     "Salary Structure Assignment",
        #     filters={"employee": self.employee, "company": self.company, "docstatus": 1},
        #     fields=["*"],
        #     order_by="from_date desc",
        #     limit=1,
        # 	)

        # 	if not salary_structure_assignment:
        # 		new_salary_slip = make_salary_slip(
        # 			source_name=salary_structure_assignment[0].salary_structure,
        # 			employee=self.employee,
        # 			print_format="Salary Slip Standard",
        # 			posting_date=salary_structure_assignment[0].from_date,
        # 			for_preview=1,
        # 		)

        # 		processed_components = set()

        # 		# Collect new amounts from earnings and deductions
        # 		for new_earning in new_salary_slip.earnings:
        # 	part_of_ctc = frappe.get_doc(
        # 		"Salary Component", new_earning.salary_component
        # 	)

        # 	if part_of_ctc.name in processed_components:
        # 		continue

        # 	if part_of_ctc.custom_is_arrear == 1 and part_of_ctc.custom_component==:
        # 		component = new_earning.salary_component
        # 		new_amounts[component] = new_earning.amount

        # 	if part_of_ctc.custom_is_accrual == 1:
        # 		component = new_earning.salary_component
        # 		new_bonus[component] = new_earning.amount

        # 	processed_components.add(part_of_ctc.name)

        # for new_deduction in new_salary_slip.deductions:
        # 	part_of_ctc = frappe.get_doc(
        # 		"Salary Component", new_deduction.salary_component
        # 	)
        # 	if part_of_ctc.name in processed_components:
        # 		continue

        # 	if part_of_ctc.custom_is_part_of_appraisal == 1:
        # 		component = new_deduction.salary_component
        # 		new_amounts[component] = new_deduction.amount

        # 	processed_components.add(part_of_ctc.name)
