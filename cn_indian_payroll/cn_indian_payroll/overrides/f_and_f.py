import frappe


from hrms.hr.doctype.full_and_final_statement.full_and_final_statement import (
    FullandFinalStatement,
)


class CustomFullAndFinalStatement(FullandFinalStatement):
    def get_payable_component(self):
        get_salary_component = frappe.get_all(
            "Salary Component",
            filters={"type": "Earning", "custom_included_in_f_and_f": 1},
            fields=["name"],
        )
        if get_salary_component:
            for i in get_salary_component:
                if i.name not in [d.component for d in self.payables]:
                    self.append(
                        "payables",
                        {"component": i.name, "amount": 0, "status": "Unsettled"},
                    )

    def create_component_row(self, components, component_type):
        pass


# def before_save(self,method):
#     calculated_leave=0
#     if len(self.custom_calculated_amount)>0:
#         for v in self.custom_calculated_amount:
#             calculated_leave+=v.amount

#     locked_leave=0
#     if len(self.custom_locked_leave)>0:
#         for t in self.custom_locked_leave:
#             locked_leave+=t.amount


#     if len(self.payables)>0:
#         for i in self.payables:
#             if i.reference_document_type=="Leave Encashment":
#                 i.amount=round(locked_leave+calculated_leave)


def before_save(self, method):
    calculated_leave = sum(v.amount for v in self.custom_calculated_amount)
    locked_leave = sum(t.amount for t in self.custom_locked_leave)
    for payable in self.payables:
        if payable.component == "Leave Encashment":
            payable.amount = round(locked_leave + calculated_leave)


def on_submit(self, method):
    if self.payables:
        for payable in self.payables:
            additional_salary = frappe.get_doc(
                {
                    "doctype": "Additional Salary",
                    "employee": self.employee,
                    "amount": payable.amount,
                    "salary_component": payable.component,
                    "company": self.company,
                    "payroll_date": self.transaction_date,
                }
            )
            additional_salary.insert()
