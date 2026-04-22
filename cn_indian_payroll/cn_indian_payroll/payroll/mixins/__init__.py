"""
Salary Slip mixins — imported by payroll/overrides/salary_slip.py.

Each mixin is a focused, independently-testable unit:
  LOPMixin      — LOP / attendance-cycle working-days
  TaxMixin      — variable tax, income-tax breakup, taxable-earnings
  BenefitsMixin — benefit claims, HRA / NPS / PF declaration sync
  ESICMixin     — ESIC and total-deduction helpers
"""

from cn_indian_payroll.cn_indian_payroll.payroll.mixins.benefits import BenefitsMixin
from cn_indian_payroll.cn_indian_payroll.payroll.mixins.esic import ESICMixin
from cn_indian_payroll.cn_indian_payroll.payroll.mixins.lop import LOPMixin
from cn_indian_payroll.cn_indian_payroll.payroll.mixins.tax import TaxMixin

__all__ = ["BenefitsMixin", "ESICMixin", "LOPMixin", "TaxMixin"]
