import frappe

def before_submit(self, method):
    if  not self.custom_note_remark:
        frappe.throw("Please add Note/Remarks before Submit")


def validate(self,method):
    if self.applicant_type=="Employee" and self.applicant:
        self.custom_employee=self.applicant
        # frappe.msgprint(str(self.applicant))
