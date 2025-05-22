import frappe

def on_submit(self,method):
    insert_additional_salary(self)
    update_bonus_accrual(self)
    update_reimbursement_accruals(self)
    update_status_completed(self)


def on_cancel(self,method):
    cancel_additional_salary(self)
    reverse_bonus_accrual(self)
    reverse_benefit_accrual(self)



def update_status_completed(self):
    if self.promotion_reference:
        promotion_doc = frappe.get_doc('Employee Promotion', self.promotion_reference)
        promotion_doc.custom_status = "Completed"
        promotion_doc.save()

def update_bonus_accrual(self):
    if not self.bonus_components:
        return

    for bonus_row in self.bonus_components:
        filters = {
            'employee': self.employee,
            'salary_slip': bonus_row.salary_slip_id,
            'salary_component': bonus_row.salary_component,
            'docstatus': 1,
        }

        accrual_list = frappe.get_list(
            'Employee Bonus Accrual',
            filters=filters,
            fields=['name', 'amount']
        )

        if accrual_list:
            for accrual in accrual_list:
                accrual_doc = frappe.get_doc('Employee Bonus Accrual', accrual.name)
                updated_amount = accrual_doc.amount + (bonus_row.difference or 0)
                accrual_doc.amount = max(updated_amount, 0)
                accrual_doc.save()
        else:
            if bonus_row.salary_slip_id:
                salary_slip = frappe.get_doc('Salary Slip', bonus_row.salary_slip_id)

                new_accrual = frappe.get_doc({
                    'doctype': 'Employee Bonus Accrual',
                    'company': self.company,
                    'accrual_date': self.posting_date,
                    'employee': self.employee,
                    'amount': bonus_row.difference or 0,
                    'salary_component': bonus_row.salary_component,
                    'benefit_accrual_date': salary_slip.end_date,
                    'salary_slip': bonus_row.salary_slip_id,
                    'payroll_period': salary_slip.custom_payroll_period,
                    'salary_structure_assignment': salary_slip.custom_salary_structure_assignment,
                    'salary_structure': salary_slip.salary_structure,
                    'docstatus': 1,
                })

                new_accrual.insert()
                new_accrual.submit()






def update_reimbursement_accruals(self):
    if not self.reimbursement_components:
        return

    for row in self.reimbursement_components:
        accruals = frappe.get_list(
            'Employee Benefit Accrual',
            filters={
                'employee': self.employee,
                'salary_slip': row.salary_slip_id,
                'salary_component': row.salary_component,
                'docstatus': 1
            },
            fields=['name', 'amount']
        )

        if accruals:
            for accrual in accruals:
                accrual_doc = frappe.get_doc('Employee Benefit Accrual', accrual.name)
                updated_amount = accrual_doc.amount + (row.difference or 0)
                accrual_doc.amount = max(updated_amount, 0)
                accrual_doc.save()
        else:
            if row.salary_slip_id:
                salary_slip = frappe.get_doc("Salary Slip", row.salary_slip_id)

                new_accrual = frappe.get_doc({
                    'doctype': 'Employee Benefit Accrual',
                    'employee': self.employee,
                    'amount': row.difference or 0,
                    'salary_component': row.salary_component,
                    'benefit_accrual_date': salary_slip.end_date,
                    'salary_slip': row.salary_slip_id,
                    'payroll_period': salary_slip.custom_payroll_period,
                    'docstatus': 1
                })

                new_accrual.insert()
                new_accrual.submit()







def insert_additional_salary(self):
    component_array = []

    if len(self.arrear_breakdown) > 0:
        for i in self.arrear_breakdown:
            component_array.append({
                "component": i.salary_component,
                "amount": i.difference
            })

        aggregated_components = {}

        for component in component_array:
            name = component['component']
            amount = component['amount']


            if name in aggregated_components:
                aggregated_components[name] += amount
            else:
                aggregated_components[name] = amount

        result = [{'component': k, 'amount': v} for k, v in aggregated_components.items()]

        for insert in result:
            salary_component = frappe.get_list('Salary Component',
                        filters={'custom_is_arrear':1, "custom_component":insert['component']},
                        fields=['*']
                    )

            if salary_component:

                for t in salary_component:

                    insert_doc = frappe.get_doc({
                        'doctype': 'Additional Salary',
                        'employee': self.employee,
                        'payroll_date': self.posting_date,
                        'salary_component': t.name,
                        'company': self.company,
                        'currency': "INR",
                        'amount': insert['amount'],
                        'docstatus':1,
                        'ref_doctype':"Salary Appraisal Calculation",
                        'ref_docname':self.name,

                    })
                    insert_doc.insert()


def cancel_additional_salary(self):
    additional_salaries = frappe.get_list(
        'Additional Salary',
        filters={'ref_docname': self.name},
        fields=['name']
    )

    for record in additional_salaries:
        frappe.delete_doc('Additional Salary', record.name, force=True)





def reverse_bonus_accrual(self):
    if not self.bonus_components:
        return

    for component in self.bonus_components:
        bonus_accrual_list = frappe.get_list(
            'Employee Bonus Accrual',
            filters={
                'employee': self.employee,
                'salary_slip': component.salary_slip_id,
                'salary_component': component.salary_component,
                'docstatus': 1
            },
            fields=['name', 'amount']
        )

        for accrual in bonus_accrual_list:
            accrual_doc = frappe.get_doc('Employee Bonus Accrual', accrual.name)

            if accrual_doc.amount == 0:
                accrual_doc.amount = component.old_amount or 0
            else:
                accrual_doc.amount = max(accrual_doc.amount - (component.difference or 0), 0)

            accrual_doc.save()









def reverse_benefit_accrual(self):
    if not self.reimbursement_components:
        return

    for component in self.reimbursement_components:
        benefit_accrual_list = frappe.get_list(
            'Employee Benefit Accrual',
            filters={
                'employee': self.employee,
                'salary_slip': component.salary_slip_id,
                'salary_component': component.salary_component,
                'docstatus': 1
            },
            fields=['name', 'amount']
        )

        for accrual in benefit_accrual_list:
            accrual_doc = frappe.get_doc('Employee Benefit Accrual', accrual.name)

            if accrual_doc.amount == 0:
                accrual_doc.amount = component.old_amount or 0
            else:
                accrual_doc.amount = max(accrual_doc.amount - (component.difference or 0), 0)

            accrual_doc.save()
