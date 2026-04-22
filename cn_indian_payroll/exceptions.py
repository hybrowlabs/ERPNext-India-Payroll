"""
Application-level exceptions for cn_indian_payroll.

Raise these instead of bare Exception / ValidationError so callers can
catch payroll-specific errors with a single except clause.
"""


class IndianPayrollError(Exception):
    """Root exception — catch this to handle any app-level error."""


class TaxCalculationError(IndianPayrollError):
    """Raised when income-tax slab evaluation or cess computation fails."""


class EPFError(IndianPayrollError):
    """Raised when EPF / EPS / EDLI contribution logic encounters bad data."""


class ESICError(IndianPayrollError):
    """Raised when ESIC applicability or contribution logic fails."""


class PayrollConfigurationError(IndianPayrollError):
    """Raised when a required payroll setting or structure is misconfigured."""


class SalaryComponentError(IndianPayrollError):
    """Raised when a salary component definition is invalid or missing."""


class LoanError(IndianPayrollError):
    """Raised when loan disbursement, repayment or recovery logic fails."""


class ExemptionError(IndianPayrollError):
    """Raised when tax exemption declaration or proof validation fails."""
