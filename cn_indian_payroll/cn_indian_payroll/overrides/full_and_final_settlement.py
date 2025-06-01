import frappe


from hrms.hr.doctype.full_and_final_statement.full_and_final_statement import (
    FullandFinalStatement,
)

from datetime import datetime


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
                    # "custom_reference_component": comp.name,
                },
            )
            receivables.append("Loan")

        return receivables

    def create_component_row(self, components, component_type):
        pass

    def on_submit(self):
        transaction_date = datetime.strptime(
            str(self.transaction_date), "%Y-%m-%d"
        ).date()
        original_payable_component = []
        original_receivable_component = []

        if self.payables:
            for payable in self.payables:
                if payable.reference_document_type != "Salary Slip":
                    component = payable.custom_reference_component
                    amount = payable.amount or 0

                    if amount > 0 and component:
                        additional_salary = frappe.get_doc(
                            {
                                "doctype": "Additional Salary",
                                "employee": self.employee,
                                "amount": amount,
                                "salary_component": component,
                                "company": self.company,
                                "payroll_date": self.transaction_date,
                                "ref_doctype": "Full and Final Statement",
                                "ref_docname": self.name,
                            }
                        )
                        additional_salary.insert()
                        additional_salary.submit()

                        original_payable_component.append(
                            {"salary_component": component, "amount": amount}
                        )

        if self.receivables:
            for receivable in self.receivables:
                component = receivable.custom_reference_component
                amount = receivable.amount or 0

                if amount > 0 and component:
                    additional_salary = frappe.get_doc(
                        {
                            "doctype": "Additional Salary",
                            "employee": self.employee,
                            "amount": amount,
                            "salary_component": component,
                            "company": self.company,
                            "payroll_date": self.transaction_date,
                            "ref_doctype": "Full and Final Statement",
                            "ref_docname": self.name,
                        }
                    )
                    additional_salary.insert()
                    additional_salary.submit()

                    original_receivable_component.append(
                        {"salary_component": component, "amount": amount}
                    )

        for payable in self.payables:
            if (
                payable.reference_document_type == "Salary Slip"
                and payable.reference_document
            ):
                salary_slip = frappe.get_doc("Salary Slip", payable.reference_document)

                salary_slip.custom_f_and_f_updated = 1
                salary_slip.save()


@frappe.whitelist()
def get_accrued_components(employee, company, relieving_date):
    from frappe.utils import getdate, flt
    from collections import defaultdict

    relieving_date = getdate(relieving_date)
    bonus_list = []
    reimbursement_list = []
    leave_encashment_list = []

    tax_list = []

    # Get latest Salary Structure Assignment
    get_latest_ssa = frappe.get_list(
        "Salary Structure Assignment",
        filters={
            "employee": employee,
            "company": company,
            "docstatus": 1,
            "from_date": ["<=", relieving_date],
        },
        fields=["name", "custom_payroll_period"],
        order_by="from_date desc",
        limit=1,
    )

    if get_latest_ssa:
        payroll_period = get_latest_ssa[0].custom_payroll_period

        get_salary_slip = frappe.get_all(
            "Salary Slip",
            filters={
                "employee": employee,
                "company": company,
                "docstatus": ["in", [0, 1]],
                "custom_payroll_period": payroll_period,
            },
            fields=["name"],
        )

        if get_salary_slip:
            for slip in get_salary_slip:
                get_each_sl = frappe.get_doc("Salary Slip", slip.name)
                for deduction in get_each_sl.deductions:
                    get_pt = frappe.get_doc(
                        "Salary Component", deduction.salary_component
                    )
                    if get_pt.component_type == "Professional Tax":
                        tax_list.append(
                            {
                                "salary_component": deduction.salary_component,
                                "amount": deduction.amount,
                                "id": get_each_sl.name,
                                "date": get_each_sl.posting_date,
                                "payment_days": get_each_sl.payment_days,
                            }
                        )
                    if (
                        get_pt.is_income_tax_component
                        and get_pt.variable_based_on_taxable_salary
                    ):
                        tax_list.append(
                            {
                                "salary_component": deduction.salary_component,
                                "amount": deduction.amount,
                                "id": get_each_sl.name,
                                "date": get_each_sl.posting_date,
                                "payment_days": get_each_sl.payment_days,
                            }
                        )

    leave_encashment = frappe.get_all(
        "Leave Encashment",
        filters={
            "employee": employee,
            "docstatus": 1,
        },
        fields=["*"],
    )
    for encashment in leave_encashment:
        leave_encashment_list.append(
            {
                "leave_type": encashment.leave_type,
                "encashment_days": encashment.encashment_days,
                "basic_amount": encashment.custom_basic_amount,
                "amount": encashment.encashment_amount,
            }
        )

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
        "leave_encashment": leave_encashment_list,
        "tax_list": tax_list,
    }
