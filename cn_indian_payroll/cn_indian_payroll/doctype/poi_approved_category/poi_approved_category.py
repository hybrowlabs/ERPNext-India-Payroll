



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