import frappe


from hrms.hr.doctype.full_and_final_statement.full_and_final_statement import (
    FullandFinalStatement,
)


class CustomFullAndFinalStatement(FullandFinalStatement):
    def get_payable_component(self):
        get_salary_component = frappe.get_all(
            "Salary Component",
            filters={"type": "Earning", "custom_included_in_f_and_f": 1, "disabled": 0},
            fields=["name"],
        )
        if get_salary_component:
            for i in get_salary_component:
                if i.name not in [d.component for d in self.payables]:
                    self.append(
                        "payables",
                        {
                            "component": i.name,
                            "amount": 0,
                            "status": "Unsettled",
                            "custom_reference_component": i.name,
                        },
                    )

    def get_receivable_component(self):
        receivables = []

        # Get deduction-type salary components that are included in F&F and not disabled
        salary_components = frappe.get_all(
            "Salary Component",
            filters={
                "type": "Deduction",
                "custom_included_in_f_and_f": 1,
                "disabled": 0,
            },
            fields=["name"],
        )

        if salary_components:
            for comp in salary_components:
                if comp.name not in [d.component for d in self.payables]:
                    self.append(
                        "receivables",
                        {
                            "component": comp.name,
                            "amount": 0,
                            "status": "Unsettled",
                            "custom_reference_component": comp.name,
                        },
                    )
                    receivables.append(comp.name)

        # Check if "lending" app is installed and add "Loan" if needed
        if "lending" in frappe.get_installed_apps():
            self.append(
                "receivables",
                {
                    "component": "Loan",
                    "amount": 0,
                    "status": "Unsettled",
                    "custom_reference_component": comp.name,
                },
            )
            receivables.append("Loan")

        return receivables

    def create_component_row(self, components, component_type):
        pass

    def on_submit(self):
        if self.payables:
            for payable in self.payables:
                if payable.amount > 0 and payable.custom_reference_component:
                    additional_salary = frappe.get_doc(
                        {
                            "doctype": "Additional Salary",
                            "employee": self.employee,
                            "amount": payable.amount,
                            "salary_component": payable.custom_reference_component,
                            "company": self.company,
                            "payroll_date": self.transaction_date,
                        }
                    )
                    additional_salary.insert()
                    additional_salary.submit()


@frappe.whitelist()
def get_accrued_components(employee, company, relieving_date):
    from frappe.utils import getdate, flt
    from collections import defaultdict

    relieving_date = getdate(relieving_date)
    bonus_list = []
    reimbursement_list = []

    # Fetch bonus accruals
    bonuses = frappe.get_all(
        "Employee Bonus Accrual",
        filters={
            "employee": employee,
            "docstatus": 1,
            "is_paid": 0,
            "company": company,
        },
        fields=[
            "accrual_date",
            "payment_day",
            "salary_slip",
            "salary_component",
            "amount",
        ],
    )

    for b in bonuses:
        bonus_list.append(
            {
                "date": b.accrual_date,
                "payment_days": b.payment_day,
                "salary_slip_id": b.salary_slip,
                "salary_component": b.salary_component,
                "accrued_amount": flt(b.amount),
            }
        )

    # Fetch withheld salary slips
    salary_slips = frappe.get_all(
        "Salary Slip",
        filters={
            "employee": employee,
            "status": "Withheld",
            "docstatus": 0,
        },
        fields=["name"],
    )

    for slip in salary_slips:
        salary_slip_doc = frappe.get_doc("Salary Slip", slip.name)

        # Get accrual-type earnings
        for earning in salary_slip_doc.earnings:
            salary_component_doc = frappe.get_doc(
                "Salary Component", earning.salary_component
            )
            if salary_component_doc.custom_is_accrual == 1:
                bonus_list.append(
                    {
                        "date": salary_slip_doc.start_date,
                        "payment_days": salary_slip_doc.total_working_days,
                        "salary_slip_id": salary_slip_doc.name,
                        "salary_component": earning.salary_component,
                        "accrued_amount": flt(earning.amount),
                    }
                )

        structure_assignment = frappe.get_doc(
            "Salary Structure Assignment",
            salary_slip_doc.custom_salary_structure_assignment,
        )

        payroll_period = structure_assignment.custom_payroll_period

        if payroll_period:
            accruals = frappe.get_all(
                "Employee Benefit Accrual",
                filters={
                    "employee": employee,
                    "docstatus": ["in", [0, 1]],
                    "payroll_period": payroll_period,
                },
                fields=["*"],
            )

            for accrual in accruals:
                reimbursement_list.append(
                    {
                        "date": accrual.benefit_accrual_date,
                        "payment_days": accrual.payment_days,
                        "salary_slip_id": accrual.salary_slip,
                        "salary_component": accrual.salary_component,
                        "accrued_amount": flt(accrual.amount),
                    }
                )

        # Reimbursements from custom_employee_reimbursements
        if structure_assignment.custom_employee_reimbursements:
            for component in structure_assignment.custom_employee_reimbursements:
                if component.reimbursements:
                    daily_amount = 0
                    if salary_slip_doc.total_working_days:
                        daily_amount = (
                            flt(component.monthly_total_amount)
                            / salary_slip_doc.total_working_days
                        )

                    reimbursement_list.append(
                        {
                            "date": salary_slip_doc.posting_date,
                            "payment_days": salary_slip_doc.payment_days,
                            "salary_slip_id": salary_slip_doc.name,
                            "salary_component": component.reimbursements,
                            "accrued_amount": round(flt(daily_amount))
                            * salary_slip_doc.payment_days,
                        }
                    )

    # Aggregate accrued_amount by salary_component
    component_totals = defaultdict(float)
    for item in bonus_list + reimbursement_list:
        component_totals[item["salary_component"]] += item["accrued_amount"]

    # Prepare final array
    final_array = []

    for component, amount in component_totals.items():
        # Get the total claimed amount for this component
        benefit_claims = frappe.get_all(
            "Employee Benefit Claim",
            filters={
                "employee": employee,
                "custom_payroll_period": payroll_period,
                "docstatus": 1,
                "company": company,
                "earning_component": component,
            },
            fields=["custom_paid_amount"],
        )

        # Sum up the claimed amounts
        claimed_amount = sum(flt(claim.custom_paid_amount) for claim in benefit_claims)

        # Append the final result
        final_array.append(
            {
                "component": component,
                "accrued_amount": round(amount, 2),
                "claimed_amount": round(claimed_amount, 2),
                "balance_amount": round(amount - claimed_amount),
            }
        )

    return {
        "bonus_list": bonus_list,
        "reimbursement_list": reimbursement_list,
        "final_array": final_array,
    }


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


# def before_save(self, method):
#     calculated_leave = sum(v.amount for v in self.custom_calculated_amount)
#     locked_leave = sum(t.amount for t in self.custom_locked_leave)
#     for payable in self.payables:
#         if payable.component == "Leave Encashment":
#             payable.amount = round(locked_leave + calculated_leave)
