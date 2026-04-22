"""ESIC and total-deduction helpers for CustomSalarySlip."""

import frappe


class ESICMixin:

    def esic_amount_roundup(self) -> None:
        """Compute custom_total_deduction_amount = deductions + loan repayments."""
        self.custom_total_deduction_amount = (
            (self.total_deduction or 0) + (self.total_loan_repayment or 0)
        )
