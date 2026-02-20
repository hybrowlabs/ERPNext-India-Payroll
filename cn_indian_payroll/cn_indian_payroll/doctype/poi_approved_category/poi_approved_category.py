# Copyright (c) 2026, Hybrowlabs technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class POIApprovedCategory(Document):
	def validate(self):
		if self.proof_id and self.status == "Approved":
			if self.category=="HRA":
				existing_approved_category = frappe.get_doc(
					"Employee Tax Exemption Proof Submission",self.proof_id
					
				)
				existing_approved_category.custom_hra_approval_status="Approved"
				existing_approved_category.save(ignore_permissions=True)

			else:

				existing_approved_category = frappe.get_doc(
					"Employee Tax Exemption Proof Submission",self.proof_id
					
				)
				if existing_approved_category.tax_exemption_proofs:
					for category in existing_approved_category.tax_exemption_proofs:
						if category.exemption_sub_category == self.exemption_sub_category and category.custom_proof_status!=self.status:
							category.custom_proof_status = "Approved"
							category.custom_note=self.command
				existing_approved_category.save()
				frappe.db.commit()

		if self.proof_id and self.status == "Rejected":
			if self.category=="HRA":
				existing_approved_category = frappe.get_doc(
					"Employee Tax Exemption Proof Submission",self.proof_id
					
				)
				existing_approved_category.custom_hra_approval_status="Rejected"
				existing_approved_category.save()
			else:
				existing_approved_category = frappe.get_doc(
					"Employee Tax Exemption Proof Submission",self.proof_id
					
				)
				if existing_approved_category.tax_exemption_proofs:
					for category in existing_approved_category.tax_exemption_proofs :
						if category.exemption_sub_category == self.exemption_sub_category and category.custom_proof_status!=self.status:
							category.custom_proof_status = "Rejected"
							category.custom_note=self.command
				existing_approved_category.save()
				frappe.db.commit()

		if self.proof_id and self.status == "Pending":
			if self.category=="HRA":
				existing_approved_category = frappe.get_doc(
					"Employee Tax Exemption Proof Submission",self.proof_id
					
				)
				existing_approved_category.custom_hra_approval_status="Pending"
				existing_approved_category.save()

			else:

				existing_approved_category = frappe.get_doc(
					"Employee Tax Exemption Proof Submission",self.proof_id
					
				)
				if existing_approved_category.tax_exemption_proofs:
					for category in existing_approved_category.tax_exemption_proofs:
						if category.exemption_sub_category == self.exemption_sub_category:
							category.custom_proof_status = "Pending"
							category.custom_note=self.command
				existing_approved_category.save()
				frappe.db.commit()



						