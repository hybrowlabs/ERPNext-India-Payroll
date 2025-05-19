import frappe


def on_submit(self, method):
    insert_additional_salary(self)


def validate(self, method):
    amount = 0

    if self.employee:
        component = []

        lta_data = frappe.db.get_list(
            "Salary Component",
            filters={
                "component_type": "LTA Reimbursement",
            },
            fields=["*"],
        )

        if lta_data and lta_data[0].name:
            get_salary_assignment = frappe.db.get_list(
                "Salary Structure Assignment",
                filters={
                    "docstatus": 1,
                    "employee": self.employee,
                },
                fields=["*"],
                order_by="from_date desc",
                limit=1,
            )

            if get_salary_assignment and get_salary_assignment[0].name:
                employee_doc = frappe.get_doc(
                    "Salary Structure Assignment", get_salary_assignment[0].name
                )

                if len(employee_doc.custom_employee_reimbursements) > 0:
                    for reimbursement in employee_doc.custom_employee_reimbursements:
                        component.append(reimbursement.reimbursements)

        if lta_data and lta_data[0].name not in component:
            frappe.throw("you are not eligible for claim LTA")
    # if self.non_taxable_amount:
    #     amount += self.non_taxable_amount

    # if self.taxable_amount:
    #     amount += self.taxable_amount

    # if self.amount > amount and amount != 0:
    #     frappe.throw("Cannot enter the amount greater than the sum of taxable and non-taxable amounts")


def insert_additional_salary(self):
    if not self.employee or not self.claim_date:
        return

    component = []

    if self.income_tax_regime == "New Regime":
        lta_tax_data = frappe.db.get_list(
            "Salary Component",
            filters={"component_type": "LTA Taxable"},
            fields=["name"],
            limit=1,
        )
        if lta_tax_data and self.taxable_amount:
            component.append(
                {"component": lta_tax_data[0].name, "amount": self.taxable_amount}
            )

    elif self.income_tax_regime == "Old Regime":
        # LTA Non-Taxable
        lta_non_taxable = frappe.db.get_list(
            "Salary Component",
            filters={"component_type": "LTA Non Taxable"},
            fields=["name"],
            limit=1,
        )
        if lta_non_taxable and self.non_taxable_amount:
            component.append(
                {
                    "component": lta_non_taxable[0].name,
                    "amount": self.non_taxable_amount,
                }
            )

        # LTA Taxable
        lta_taxable = frappe.db.get_list(
            "Salary Component",
            filters={"component_type": "LTA Taxable"},
            fields=["name"],
            limit=1,
        )
        if lta_taxable and self.taxable_amount:
            component.append(
                {"component": lta_taxable[0].name, "amount": self.taxable_amount}
            )
    for item in component:
        additional_salary = frappe.new_doc("Additional Salary")
        additional_salary.employee = self.employee
        additional_salary.salary_component = item["component"]
        additional_salary.amount = item["amount"]
        additional_salary.payroll_date = self.claim_date
        additional_salary.currency = "INR"
        additional_salary.ref_doctype = "LTA Claim"
        additional_salary.ref_docname = self.name
        additional_salary.insert()
        additional_salary.submit()
