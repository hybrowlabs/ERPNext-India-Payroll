# Copyright (c) 2026, Hybrowlabs technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class POIApprovedCategory(Document):
	def validate(self):
		if self.proof_id and self.status == "Approved":
			existing_approved_category = frappe.get_doc(
				"Employee Tax Exemption Proof Submission",self.proof_id
				
			)
			if existing_approved_category.tax_exemption_proofs:
				for category in existing_approved_category.tax_exemption_proofs:
					if category.exemption_sub_category == self.exemption_sub_category:
						category.custom_proof_status = "Approved"
						category.custom_note=self.command
			existing_approved_category.save()

		if self.proof_id and self.status == "Rejected":
			existing_approved_category = frappe.get_doc(
				"Employee Tax Exemption Proof Submission",self.proof_id
				
			)
			if existing_approved_category.tax_exemption_proofs:
				for category in existing_approved_category.tax_exemption_proofs:
					if category.exemption_sub_category == self.exemption_sub_category:
						category.custom_proof_status = "Rejected"
						category.custom_note=self.command
			existing_approved_category.save()
						