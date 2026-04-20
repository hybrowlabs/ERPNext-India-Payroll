import frappe


def validate(self, method):
    if self.is_tax_applicable and self.custom_tax_exemption_applicable_based_on_regime and not self.custom_regime:
        frappe.throw(
            "Please select the tax regime for this salary component as it is marked as tax applicable."
        )
    