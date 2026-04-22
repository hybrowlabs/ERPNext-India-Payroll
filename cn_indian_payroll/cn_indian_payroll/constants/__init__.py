"""
India Payroll — application-wide constants.

All magic numbers, ceiling values, regime identifiers and lookup tables
live here so that business logic never has raw literals scattered across it.
"""

# ---------------------------------------------------------------------------
# EPF / EPS / EDLI
# ---------------------------------------------------------------------------

EPF_WAGE_CEILING: int = 15_000
"""Statutory wage ceiling (₹) above which EPF contributions are capped."""

EPF_EMPLOYEE_RATE: float = 12.0
"""Employee contribution rate (%) — Section 6, EPF & MP Act 1952."""

EPS_RATE: float = 8.33
"""Employer pension contribution rate (%) — Section 6A, EPS 1995."""

# CR ER is always derived: CR EE − CR EPS  (audit invariant)

ESIC_EMPLOYEE_RATE: float = 0.75
"""Employee ESIC contribution rate (%)."""

ESIC_EMPLOYER_RATE: float = 3.25
"""Employer ESIC contribution rate (%)."""

ESIC_WAGE_CEILING: int = 21_000
"""Monthly wage ceiling (₹) above which ESIC is not applicable."""

# ---------------------------------------------------------------------------
# Tax
# ---------------------------------------------------------------------------

EDUCATION_CESS_RATE: float = 4.0
"""Education & health cess rate (%) applied on income tax + surcharge."""

REBATE_87A_LIMIT_NEW_REGIME: int = 700_000
"""Taxable income limit (₹) below which full rebate u/s 87A is available (New Regime)."""

REBATE_87A_LIMIT_OLD_REGIME: int = 500_000
"""Taxable income limit (₹) below which full rebate u/s 87A is available (Old Regime)."""

TAX_REGIME_NEW: str = "New Regime"
TAX_REGIME_OLD: str = "Old Regime"

# ---------------------------------------------------------------------------
# LWF
# ---------------------------------------------------------------------------

LWF_STATES: tuple[str, ...] = (
    "Andhra Pradesh",
    "Gujarat",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Odisha",
    "Punjab",
    "Tamil Nadu",
    "Telangana",
)

# ---------------------------------------------------------------------------
# Professional Tax
# ---------------------------------------------------------------------------

PT_EXEMPT_STATES: frozenset[str] = frozenset(
    {
        "Arunachal Pradesh",
        "Delhi",
        "Goa",
        "Haryana",
        "Himachal Pradesh",
        "Jammu and Kashmir",
        "Ladakh",
        "Rajasthan",
        "Uttarakhand",
    }
)

# ---------------------------------------------------------------------------
# Months
# ---------------------------------------------------------------------------

MONTH_NAMES: tuple[str, ...] = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)

MONTH_NUMBER: dict[str, int] = {name: i + 1 for i, name in enumerate(MONTH_NAMES)}

# ---------------------------------------------------------------------------
# Payroll
# ---------------------------------------------------------------------------

SUBMITTED: int = 1
DRAFT: int = 0
CANCELLED: int = 2

PAYROLL_FREQUENCY_MONTHLY: str = "Monthly"

# ---------------------------------------------------------------------------
# Perquisite
# ---------------------------------------------------------------------------

CAR_PERQUISITE_OPTIONS: tuple[str, ...] = (
    "Car > 1600 CC",
    "Car < 1600 CC",
)
