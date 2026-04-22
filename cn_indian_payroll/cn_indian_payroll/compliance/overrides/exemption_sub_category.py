import frappe
from frappe import _

def validate(self, method):
    if not self.custom_component_type:
        return

    validate_doc = frappe.get_list(
        "Employee Tax Exemption Sub Category",
        filters={
            "custom_component_type": self.custom_component_type,
            "is_active": 1,
            "name": ["!=", self.name]
        },
        fields=["name"]
    )

    if validate_doc:
        frappe.throw(
            _("An active Exemption Sub Category with component type '{0}' already exists.").format(self.custom_component_type)
        )
