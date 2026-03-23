import frappe
from erpnext.setup.doctype.employee.employee import Employee


class CustomEmployee(Employee):
    def before_save(self):
        self.set_cpl()

        self.reimbursement_amount()

    def validate(self):
        self.set_rating_system()

    def set_rating_system(self):
        if not self.custom_employee_performance_and_ratings:
            return

        ssa_list = frappe.get_list(
            "Salary Structure Assignment",
            filters={"employee": self.name, "docstatus": 1},
            fields=["name"],
            order_by="from_date desc",
            limit=1,
        )

        frappe.msgprint(str(ssa_list))

        if not ssa_list:
            return

        ssa = frappe.get_doc("Salary Structure Assignment", ssa_list[0].name)

        if not ssa.custom_other_extra_payments:
            return

        for k in self.custom_employee_performance_and_ratings:
            for j in ssa.custom_other_extra_payments:
                if j.additional_earning == "Variable Pay":
                    j.rating = k.select_rating

        ssa.save()

    def set_cpl(self):
        components = [
            "Vehicle Maintenance Reimbursement",
            "Petrol Reimbursement",
            "Leave Travel Allowance",
        ]
        array = []

        if self.custom_employee_reimbursements:
            for i in self.custom_employee_reimbursements:
                if i.reimbursements in components:
                    array.append(i.reimbursements)

            if len(array) == 3:
                self.custom_is_car_petrol_lta = 1

            else:
                self.custom_is_car_petrol_lta = 0

    def reimbursement_amount(self):
        total_amount = 0
        if self.custom_employee_reimbursements:
            for reimbursement in self.custom_employee_reimbursements:
                total_amount += reimbursement.monthly_total_amount

        self.custom_statistical_amount = total_amount
