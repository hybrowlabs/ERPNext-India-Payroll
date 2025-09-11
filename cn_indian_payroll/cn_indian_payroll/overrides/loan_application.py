import frappe

def before_submit(self, method):
    if  not self.custom_note_remark:
        frappe.throw("Please add Note/Remarks before Submit")
