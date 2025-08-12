import frappe

def validate(self, method):
    validate_custom_variable_name(self)

def validate_custom_variable_name(self):
    if self.custom_variable_name:
        if frappe.db.exists("Salary Component", {"custom_variable_name": self.custom_variable_name,"name": ["!=", self.name]}):
            frappe.throw(f"Custom Variable '{self.custom_variable_name}' already exists in another component")
