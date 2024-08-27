import frappe

def validate(self, method):
    amount = 0

    if self.employee:
        component = []

        lta_data = frappe.db.get_list('Salary Component',
            filters={
                'component_type': "LTA Reimbursement",
            },
            fields=['*']
        )

        if lta_data and lta_data[0].name:

            get_salary_assignment = frappe.db.get_list('Salary Structure Assignment',
                filters={
                    'docstatus': 1,
                    'employee': self.employee,
                },
                fields=['*'],
                order_by='from_date desc',
                limit=1  # Fetch only the latest record
            )

            if get_salary_assignment and get_salary_assignment[0].name:
                employee_doc = frappe.get_doc('Salary Structure Assignment', get_salary_assignment[0].name)

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
