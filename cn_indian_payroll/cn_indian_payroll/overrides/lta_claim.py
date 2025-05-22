import frappe
from frappe.utils import getdate


def on_submit(self, method):
    insert_additional_salary(self)


def validate(self, method):

    validate_employee(self)


def before_submit(self, method):
    validate_taxable_amount(self)




def validate_taxable_amount(self):
    if self.income_tax_regime == "New Regime":
        if self.taxable_amount == 0:
            frappe.throw("Taxable Amount should Not be 0 in New Regime")

    elif self.income_tax_regime == "Old Regime":
        if self.taxable_amount == 0 and self.non_taxable_amount == 0:
            frappe.throw("Taxable Amount and Non taxable amount should be  0 in Old Regime")
def validate_employee(self):
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
                    'company': self.company,
                    'from_date': ['<=', self.claim_date],
                },
                fields=['*'],
                order_by='from_date desc',
                limit=1
            )

            if get_salary_assignment and get_salary_assignment[0].name:
                employee_doc = frappe.get_doc('Salary Structure Assignment', get_salary_assignment[0].name)

                if len(employee_doc.custom_employee_reimbursements) > 0:
                    for reimbursement in employee_doc.custom_employee_reimbursements:
                        component.append(reimbursement.reimbursements)


        if lta_data and lta_data[0].name not in component:

            frappe.throw("you are not eligible for claim LTA")
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


@frappe.whitelist()
def get_max_amount(doc):
    doc = frappe.get_doc(frappe.parse_json(doc))

    # Get latest Salary Structure Assignment
    get_ssa = frappe.get_list(
        "Salary Structure Assignment",
        filters={
            "employee": doc.employee,
            "docstatus": 1,
            "from_date": ["<=", doc.claim_date],
        },
        fields=["name", "custom_payroll_period"],
        order_by="from_date desc",
        limit=1,
    )

    if not get_ssa:
        return {"max_amount": 0, "payroll_period": None}

    ssa_doc = frappe.get_doc("Salary Structure Assignment", get_ssa[0].name)
    payroll_period = get_ssa[0].custom_payroll_period

    if not payroll_period:
        return {"max_amount": 0, "payroll_period": None}

    if ssa_doc.custom_employee_reimbursements:
        for component in ssa_doc.custom_employee_reimbursements:
            get_lta_component = frappe.get_doc(
                "Salary Component", component.reimbursements
            )

            if get_lta_component.component_type == "LTA Reimbursement":
                eligible_amount = component.monthly_total_amount or 0

                # Claimed total
                claims = frappe.get_all(
                    "LTA Claim",
                    filters={
                        "employee": doc.employee,
                        "docstatus": 1,
                        "payroll_period": payroll_period,
                    },
                    fields=["amount"],
                )
                claimed_total = sum([row.amount for row in claims])

                # Accrued total
                accruals = frappe.get_all(
                    "Employee Benefit Accrual",
                    filters={
                        "employee": doc.employee,
                        "salary_component": get_lta_component.name,
                        "docstatus": 1,
                        "payroll_period": payroll_period,
                    },
                    fields=["amount"],
                )
                accrued_total = sum([row.amount for row in accruals])
                accrued_months = len(accruals)

                # Get effective start date
                payroll_doc = frappe.get_doc("Payroll Period", payroll_period)
                start_date = getdate(payroll_doc.start_date)
                end_date = getdate(payroll_doc.end_date)
                from_date = getdate(ssa_doc.from_date)
                effective_start_date = max(start_date, from_date)

                # Total months in payroll period
                year_diff = end_date.year - effective_start_date.year
                month_diff = end_date.month - effective_start_date.month
                total_months = (year_diff * 12 + month_diff) + 1

                # Calculate future eligible amount
                future_eligible = (total_months - accrued_months) * eligible_amount

                # Final Max Amount = Accrued + Future Eligible - Already Claimed
                max_amount = (accrued_total + future_eligible) - claimed_total

                return {"max_amount": max_amount, "payroll_period": payroll_period}

    return {"max_amount": 0, "payroll_period": payroll_period}
