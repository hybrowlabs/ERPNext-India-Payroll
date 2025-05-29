import frappe
from hrms.payroll.doctype.employee_benefit_claim.employee_benefit_claim import (
    EmployeeBenefitClaim,
)
from frappe.utils import getdate


class CustomEmployeeBenefitClaim(EmployeeBenefitClaim):
    def on_submit(self):
        self.insert_future_benefit()
        self.insert_additional_salary()

    def insert_future_benefit(self):
        if self.custom_max_amount:
            if self.claimed_amount > self.custom_max_amount:
                doc1 = frappe.get_doc("Salary Component", self.earning_component)
                if doc1.component_type == "Vehicle Maintenance Reimbursement":
                    date_str = self.claim_date
                    year, month, day = map(int, date_str.split("-"))
                    new_month = month + 1
                    new_year = year
                    if new_month > 12:
                        new_month = 1
                        new_year += 1

                    next_month_date = f"{new_year}-{new_month:02d}-{day:02d}"

                    future_amount = self.claimed_amount - self.custom_max_amount
                    insert_doc = frappe.get_doc(
                        {
                            "doctype": "Employee Benefit Claim",
                            "employee": self.employee,
                            "claim_date": next_month_date,
                            "currency": self.currency,
                            "company": self.company,
                            "claimed_amount": future_amount,
                            "earning_component": self.earning_component,
                            "docstatus": 1,
                        }
                    )
                    insert_doc.insert()

    def insert_additional_salary(self):
        if self.employee and self.claimed_amount and self.earning_component:
            insert_doc = frappe.get_doc(
                {
                    "doctype": "Additional Salary",
                    "employee": self.employee,
                    "salary_component": self.earning_component,
                    "amount": self.claimed_amount,
                    "company": self.company,
                    "currency": self.currency,
                    "payroll_date": self.claim_date,
                    "overwrite_salary_structure_amount": 0,
                    "ref_doctype": self.doctype,
                    "ref_docname": self.name,
                }
            )

            insert_doc.insert()
            insert_doc.submit()


@frappe.whitelist()
def benefit_claim(doc):
    doc = frappe.get_doc(frappe.parse_json(doc))
    component_array = []

    # Get the LTA Reimbursement Salary Component
    lta_component_list = frappe.get_list(
        "Salary Component",
        filters={"component_type": "LTA Reimbursement"},
        fields=["name"],
        limit=1,
    )
    lta_component = lta_component_list[0].name if lta_component_list else None

    # Get the latest applicable Salary Structure Assignment
    get_ssa = frappe.get_list(
        "Salary Structure Assignment",
        filters={
            "employee": doc.employee,
            "docstatus": 1,
            "from_date": ["<=", getdate(doc.claim_date)],
        },
        fields=["name", "custom_payroll_period"],
        order_by="from_date desc",
        limit=1,
    )

    payroll_period = None

    if get_ssa:
        ssa_doc = frappe.get_doc("Salary Structure Assignment", get_ssa[0].name)
        payroll_period = get_ssa[0].custom_payroll_period

        for component in ssa_doc.custom_employee_reimbursements:
            if component.reimbursements != lta_component:
                component_array.append(component.reimbursements)

    return {"component_array": component_array, "payroll_period": payroll_period}


@frappe.whitelist()
def get_max_amount(doc):
    doc = frappe.get_doc(frappe.parse_json(doc))

    # Get the latest applicable Salary Structure Assignment
    get_ssa = frappe.get_list(
        "Salary Structure Assignment",
        filters={
            "employee": doc.employee,
            "docstatus": 1,
            "from_date": ["<=", getdate(doc.claim_date)],
        },
        fields=["name", "custom_payroll_period"],
        order_by="from_date desc",
        limit=1,
    )

    if not get_ssa:
        return 0

    ssa_doc = frappe.get_doc("Salary Structure Assignment", get_ssa[0].name)
    payroll_period = get_ssa[0].custom_payroll_period

    for component in ssa_doc.custom_employee_reimbursements:
        if component.reimbursements == doc.earning_component:
            eligible_amount = component.monthly_total_amount or 0
            salary_component = frappe.get_doc(
                "Salary Component", component.reimbursements
            )

            # Common claims retrieval
            claims = frappe.get_all(
                "Employee Benefit Claim",
                filters={
                    "employee": doc.employee,
                    "earning_component": doc.earning_component,
                    "docstatus": 1,
                    "custom_payroll_period": payroll_period,
                },
                fields=["*"],
            )
            claimed_total = sum([row.custom_paid_amount for row in claims])

            # For non-Vehicle Maintenance components
            if salary_component.component_type != "Vehicle Maintenance Reimbursement":
                accruals = frappe.get_all(
                    "Employee Benefit Accrual",
                    filters={
                        "employee": doc.employee,
                        "salary_component": doc.earning_component,
                        "docstatus": 1,
                        "payroll_period": payroll_period,
                    },
                    fields=["amount"],
                )
                accrued_total = sum([row.amount for row in accruals])

                max_amount = (accrued_total + eligible_amount) - claimed_total

                return max_amount

            else:
                accruals = frappe.get_all(
                    "Employee Benefit Accrual",
                    filters={
                        "employee": doc.employee,
                        "salary_component": doc.earning_component,
                        "docstatus": 1,
                        "payroll_period": payroll_period,
                    },
                    fields=["amount"],
                )
                accrued_total = sum([row.amount for row in accruals])
                accrued_months = len(accruals)

                payroll_doc = frappe.get_doc("Payroll Period", payroll_period)
                start_date = getdate(payroll_doc.start_date)
                end_date = getdate(payroll_doc.end_date)
                from_date = getdate(ssa_doc.from_date)

                effective_start_date = max(start_date, from_date)

                # Calculate total number of months including start and end month
                year_diff = end_date.year - effective_start_date.year
                month_diff = end_date.month - effective_start_date.month
                total_months = (year_diff * 12 + month_diff) + 1

                # Calculate future eligible (remaining) months
                future_eligible = (total_months - accrued_months) * eligible_amount

                # Final max amount = accrued + future - claimed
                max_amount = (accrued_total + future_eligible) - claimed_total

                return max_amount

    return 0
