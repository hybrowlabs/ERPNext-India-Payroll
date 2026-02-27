


import frappe
from frappe.model.document import Document


class DeclarationApprovedCategory(Document):

    def validate(self):

        if self.status in ["Approved", "Rejected"] and self.declaration_id:

            declaration = frappe.get_doc(
                "Employee Tax Exemption Declaration",
                self.declaration_id
            )

            for row in declaration.declarations:

                if row.exemption_sub_category == self.exemption_sub_category:

                    frappe.db.set_value(
                        row.doctype,   # Child DocType
                        row.name,      # Row ID
                        {
                            "custom_status": self.status,
                            "custom_note": self.note
                        }
                    )