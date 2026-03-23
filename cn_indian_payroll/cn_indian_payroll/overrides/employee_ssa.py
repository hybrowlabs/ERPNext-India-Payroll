import frappe


def validate(self, method):
    set_rating_system(self, method)


def set_rating_system(self, method):
    if not self.custom_employee_performance_and_ratings:
        return

    ssa_list = frappe.get_list(
        "Salary Structure Assignment",
        filters={"employee": self.name, "docstatus": 1},
        fields=["name"],
        order_by="from_date desc",
        limit=1,
    )

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
