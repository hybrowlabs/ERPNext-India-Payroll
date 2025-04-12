import frappe
from hrms.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry
from frappe import _
from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import get_accounting_dimensions

import json
from dateutil.relativedelta import relativedelta
from frappe.desk.reportview import get_match_cond
from frappe.model.document import Document
from frappe.query_builder.functions import Coalesce, Count
from frappe.utils import (
	DATE_FORMAT,
	add_days,
	add_to_date,
	cint,
	comma_and,
	date_diff,
	flt,
	get_link_to_form,
	getdate,
)

import erpnext

from erpnext.accounts.utils import get_fiscal_year

from hrms.payroll.doctype.salary_slip.salary_slip_loan_utils import if_lending_app_installed
from hrms.payroll.doctype.salary_withholding.salary_withholding import link_bank_entry_in_salary_withholdings

from hrms.payroll.doctype.payroll_entry.payroll_entry import submit_salary_slips_for_employees


def custom_get_salary_component_account(self, salary_component):
    """
    Custom function to override `get_salary_component_account` in PayrollEntry.
    """
    if not salary_component:
        return 

    get_doc = frappe.get_doc("Salary Component", salary_component)

    if get_doc.get("do_not_include_in_total") == 0:
        for j in get_doc.get("accounts", []):  
            if j.company == self.company:
                return j.account  

    return None

PayrollEntry.get_salary_component_account = custom_get_salary_component_account




def custom_make_accrual_jv_entry(self, submitted_salary_slips):
    """
    Custom function to override `make_accrual_jv_entry` in PayrollEntry.
    """
    self.check_permission("write")

    employee_wise_accounting_enabled = frappe.db.get_single_value(
        "Payroll Settings", "process_payroll_accounting_entry_based_on_employee"
    )

    self.employee_based_payroll_payable_entries = {}
    self._advance_deduction_entries = []

    earnings = self.get_salary_component_total(
        component_type="earnings",
        employee_wise_accounting_enabled=employee_wise_accounting_enabled,
    ) or {}

    deductions = self.get_salary_component_total(
        component_type="deductions",
        employee_wise_accounting_enabled=employee_wise_accounting_enabled,
    ) or {}

    earnings = {
        (component, cost_center): amount
        for (component, cost_center), amount in earnings.items()
        if component is not None
    }

    deductions = {
        (component, cost_center): amount
        for (component, cost_center), amount in deductions.items()
        if component is not None
    }

    precision = frappe.get_precision("Journal Entry Account", "debit_in_account_currency")

    if earnings or deductions:
        accounts = []
        currencies = []
        payable_amount = 0

        # ✅ Fix: Use get_accounting_dimensions() correctly
        accounting_dimensions = get_accounting_dimensions() or []

        company_currency = erpnext.get_company_currency(self.company)

        payable_amount = self.get_payable_amount_for_earnings_and_deductions(
            accounts,
            earnings,
            deductions,
            currencies,
            company_currency,
            accounting_dimensions,
            precision,
            payable_amount,
        )

        payable_amount = self.set_accounting_entries_for_advance_deductions(
            accounts,
            currencies,
            company_currency,
            accounting_dimensions,
            precision,
            payable_amount,
        )

        self.set_payable_amount_against_payroll_payable_account(
            accounts,
            currencies,
            company_currency,
            accounting_dimensions,
            precision,
            payable_amount,
            self.payroll_payable_account,
            employee_wise_accounting_enabled,
        )

        self.make_journal_entry(
            accounts,
            currencies,
            self.payroll_payable_account,
            voucher_type="Journal Entry",
            user_remark=_("Accrual Journal Entry for salaries from {0} to {1}").format(
                self.start_date, self.end_date
            ),
            submit_journal_entry=True,
            submitted_salary_slips=submitted_salary_slips,
        )

PayrollEntry.make_accrual_jv_entry = custom_make_accrual_jv_entry

@frappe.whitelist()
def custom_make_bank_entry(self, for_withheld_salaries=False):
    self.check_permission("write")
    self.employee_based_payroll_payable_entries = {}

    # Fetch payroll settings
    employee_wise_accounting_enabled = frappe.db.get_single_value(
        "Payroll Settings", "process_payroll_accounting_entry_based_on_employee"
    )

    # Initialize total salary slip amount
    salary_slip_total = 0
    salary_details = self.get_salary_slip_details(for_withheld_salaries)

    for salary_detail in salary_details:
        do_not_include_in_total = frappe.db.get_value(
            "Salary Component", salary_detail.salary_component, "do_not_include_in_total", cache=True
        )
        
        if do_not_include_in_total == 0:
            if salary_detail.parentfield == "earnings":
                (
                    is_flexible_benefit,
                    only_tax_impact,
                    create_separate_je,
                    statistical_component,
                ) = frappe.db.get_value(
                    "Salary Component",
                    salary_detail.salary_component,
                    (
                        "is_flexible_benefit",
                        "only_tax_impact",
                        "create_separate_payment_entry_against_benefit_claim",
                        "statistical_component",
                    ),
                    cache=True,
                )

                if only_tax_impact != 1 and statistical_component != 1:
                    if is_flexible_benefit == 1 and create_separate_je == 1:
                        self.set_accounting_entries_for_bank_entry(
                            salary_detail.amount, salary_detail.salary_component
                        )
                    else:
                        if employee_wise_accounting_enabled:
                            self.set_employee_based_payroll_payable_entries(
                                "earnings",
                                salary_detail.employee,
                                salary_detail.amount,
                                salary_detail.salary_structure,
                            )
                        salary_slip_total += salary_detail.amount

            elif salary_detail.parentfield == "deductions":
                statistical_component = frappe.db.get_value(
                    "Salary Component", salary_detail.salary_component, "statistical_component", cache=True
                )

                if not statistical_component:
                    if employee_wise_accounting_enabled:
                        self.set_employee_based_payroll_payable_entries(
                            "deductions",
                            salary_detail.employee,
                            salary_detail.amount,
                            salary_detail.salary_structure,
                        )
                    salary_slip_total -= salary_detail.amount

    # Process loan repayments
    total_loan_repayment = self.process_loan_repayments_for_bank_entry(salary_details) or 0
    salary_slip_total -= total_loan_repayment

    # Show salary slip total for debugging
    # frappe.msgprint(str(salary_slip_total))

    # Create bank entry if salary slip total is positive
    bank_entry = None
    if salary_slip_total > 0:
        remark = "withheld salaries" if for_withheld_salaries else "salaries"
        bank_entry = self.set_accounting_entries_for_bank_entry(salary_slip_total, remark)

        if for_withheld_salaries:
            link_bank_entry_in_salary_withholdings(salary_details, bank_entry.name)

    return bank_entry


PayrollEntry.make_bank_entry = custom_make_bank_entry

@frappe.whitelist()
def custom_submit_salary_slips(self):
    self.check_permission("write")
    salary_slips = self.get_sal_slip_list(ss_status=0)

    if len(salary_slips) > 30 or frappe.flags.enqueue_payroll_entry:
        self.db_set("status", "Queued")
        frappe.enqueue(
            submit_salary_slips_for_employees,
            timeout=3000,
            payroll_entry=self,
            salary_slips=salary_slips,
            publish_progress=False,
        )
        frappe.msgprint(
            _("Salary Slip submission is queued. It may take a few minutes"),
            alert=True,
            indicator="blue",
        )
    else:
        submit_salary_slips_for_employees(self, salary_slips, publish_progress=False)

    account_array = []

    # Properly filter for both reimbursement and accrual components
    get_reimbursement_component = frappe.get_list(
        "Salary Component",
        filters={"disabled": 0},
        fields=["name", "custom_is_reimbursement", "custom_is_accrual"]
    )

    # Check if data exists
    if get_reimbursement_component:
        for comp in get_reimbursement_component:
            if not (comp.custom_is_reimbursement or comp.custom_is_accrual):
                continue  # Skip components that are neither reimbursement nor accrual

            get_account = frappe.get_doc("Salary Component", comp.name)

            # Loop through related accounts
            for acc in get_account.accounts:
                if acc.company != self.company:
                    continue

                # Get company's reimbursement account mappings
                get_company = frappe.get_doc("Company", self.company)
                for reimb in get_company.custom_accrued_component_payable_account:
                    if reimb.salary_component != comp.name:
                        continue

                    for accrual_doctype in ["Employee Benefit Accrual", "Employee Bonus Accrual"]:
                        get_accrued_data = frappe.get_list(
                            accrual_doctype,
                            filters={
                                "payroll_entry": self.name,
                                "docstatus": ["in", [0, 1]],
                                "salary_component": reimb.salary_component
                            },
                            fields=["amount"]
                        )

                        if get_accrued_data:
                            accrued_sum = sum(item.amount for item in get_accrued_data)

                            account_array.append({
                                "payable_account": acc.account,
                                "payable_debit_amount": accrued_sum,
                                "payable_credit_amount": 0,
                                "expense_account": reimb.payable_account,
                                "expense_credit_amount": accrued_sum,
                                "expense_debit_amount": 0,
                            })

    # Create Journal Entry if needed
    if account_array:
        je = frappe.new_doc("Journal Entry")
        je.voucher_type = "Journal Entry"
        je.company = self.company
        je.posting_date = self.posting_date
        je.user_remark = "Reimbursement posting via Payroll Entry: " + self.name

        for entry in account_array:
            # Debit entry (Payable account)
            je.append("accounts", {
                "account": entry["payable_account"],
                "debit_in_account_currency": entry["payable_debit_amount"],
                "credit_in_account_currency": 0
            })

            # Credit entry (Expense account)
            je.append("accounts", {
                "account": entry["expense_account"],
                "debit_in_account_currency": 0,
                "credit_in_account_currency": entry["expense_credit_amount"]
            })

        je.insert()
        je.submit()





            


PayrollEntry.submit_salary_slips = custom_submit_salary_slips