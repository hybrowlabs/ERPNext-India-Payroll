import frappe



def validate(self,method):
    amount=0

    if self.non_taxable_amount!=None:
        amount+=self.non_taxable_amount

    if self.non_taxable_amount!=None:
        amount+=self.taxable_amount

    if self.amount>amount and amount!=0:
        frappe.throw("Cannot enter the amount greater than the sum of taxable and non-taxable amounts")

    