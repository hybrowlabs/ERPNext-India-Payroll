# # Copyright (c) 2026, Hybrowlabs technologies and contributors
# # For license information, please see license.txt

# import frappe
# from frappe.model.document import Document


# class POIApprovedCategory(Document):
# 	def validate(self):
# 		if self.proof_id and self.status == "Approved":
# 			if self.category=="HRA":
# 				existing_approved_category = frappe.get_doc(
# 					"Employee Tax Exemption Proof Submission",self.proof_id
					
# 				)
# 				existing_approved_category.custom_hra_approval_status="Approved"
# 				existing_approved_category.save(ignore_permissions=True)

# 			else:

# 				existing_approved_category = frappe.get_doc(
# 					"Employee Tax Exemption Proof Submission",self.proof_id
					
# 				)
# 				if existing_approved_category.tax_exemption_proofs:
# 					for category in existing_approved_category.tax_exemption_proofs:
# 						if category.exemption_sub_category == self.exemption_sub_category and category.custom_proof_status!=self.status:
# 							category.custom_proof_status = "Approved"
# 							category.custom_note=self.command
# 				existing_approved_category.save()
# 				frappe.db.commit()

# 		if self.proof_id and self.status == "Rejected":
# 			if self.category=="HRA":
# 				existing_approved_category = frappe.get_doc(
# 					"Employee Tax Exemption Proof Submission",self.proof_id
					
# 				)
# 				existing_approved_category.custom_hra_approval_status="Rejected"
# 				existing_approved_category.save()
# 			else:
# 				existing_approved_category = frappe.get_doc(
# 					"Employee Tax Exemption Proof Submission",self.proof_id
					
# 				)
# 				if existing_approved_category.tax_exemption_proofs:
# 					for category in existing_approved_category.tax_exemption_proofs :
# 						if category.exemption_sub_category == self.exemption_sub_category and category.custom_proof_status!=self.status:
# 							category.custom_proof_status = "Rejected"
# 							category.custom_note=self.command
# 				existing_approved_category.save()
# 				frappe.db.commit()

# 		if self.proof_id and self.status == "Pending":
# 			if self.category=="HRA":
# 				existing_approved_category = frappe.get_doc(
# 					"Employee Tax Exemption Proof Submission",self.proof_id
					
# 				)
# 				existing_approved_category.custom_hra_approval_status="Pending"
# 				existing_approved_category.save()

# 			else:

# 				existing_approved_category = frappe.get_doc(
# 					"Employee Tax Exemption Proof Submission",self.proof_id
					
# 				)
# 				if existing_approved_category.tax_exemption_proofs:
# 					for category in existing_approved_category.tax_exemption_proofs:
# 						if category.exemption_sub_category == self.exemption_sub_category:
# 							category.custom_proof_status = "Pending"
# 							category.custom_note=self.command
# 				existing_approved_category.save()
# 				frappe.db.commit()



import frappe
from frappe.model.document import Document


class POIApprovedCategory(Document):

    def validate(self):

        if not self.proof_id:
            return

        # Handle HRA separately
        if self.category == "HRA":
            frappe.db.set_value(
                "Employee Tax Exemption Proof Submission",
                self.proof_id,
                "custom_hra_approval_status",
                self.status
            )
            return

        # For non-HRA categories (child table update)

        submission = frappe.get_doc(
            "Employee Tax Exemption Proof Submission",
            self.proof_id
        )

        if not submission.tax_exemption_proofs:
            return

        for row in submission.tax_exemption_proofs:
            if row.exemption_sub_category == self.exemption_sub_category:
                if row.custom_proof_status != self.status:
                    row.custom_proof_status = self.status
                    row.custom_note = self.command
                row.custom_note = self.command

        # Save child table changes without triggering recursion
        submission.flags.ignore_validate = True
        submission.save(ignore_permissions=True)