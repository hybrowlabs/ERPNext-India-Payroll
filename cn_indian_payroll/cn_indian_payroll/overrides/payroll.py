import frappe
from hrms.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry


class CustomPayrollEntry(PayrollEntry):
    # @frappe.whitelist()
    # def custpayroll(self, value):
    #     frappe.msgprint(value)

    # def before_save(self):
    #     frappe.msgprint(str(self.company))
    @frappe.whitelist()
    def payrollset(self,value1):
        frappe.msgprint(str(value1))




