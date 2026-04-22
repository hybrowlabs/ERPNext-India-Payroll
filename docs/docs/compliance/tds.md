---
id: tds
title: Income Tax (TDS)
sidebar_position: 4
description: TDS computation under New and Old Regime — slabs, rebate, surcharge, cess, and monthly deduction.
---

# Income Tax (TDS)

Income Tax is deducted at source (TDS) from salary under **Section 192 of the Income Tax Act**. Indian Payroll computes TDS monthly by projecting annual income and spreading the liability across remaining months.

---

## Tax regimes

Employees choose between:

| Regime | Exemptions | Deductions |
|---|---|---|
| **New Regime (115BAC)** | None (no HRA, LTA, 80C, etc.) | Only NPS u/s 80CCD(2) and standard deduction |
| **Old Regime** | HRA, LTA, 80C, 80D, NPS, PT, etc. | Full chapter VIA deductions |

The regime is stamped on the Salary Structure Assignment and cannot change mid-year without creating a new assignment.

---

## TDS computation sequence

Each month, the salary slip recomputes TDS:

```
1. annual_taxable_income
   = projected_annual_earnings             # remaining months × current month earnings
   + previous_months_earnings              # actuals already paid
   - standard_deduction (₹75,000)         # both regimes from FY 2024-25
   - HRA exemption                         # Old Regime only
   - Chapter VIA deductions                # Old Regime only (80C, 80D, NPS, PT)

2. annual_tax = tax_slab(annual_taxable_income)
   + surcharge (if applicable)
   + 4% health & education cess

3. rebate_87A = min(annual_tax, 25,000)   # if annual_taxable_income ≤ ₹7L (New)
                                          # or ≤ ₹5L (Old)
   net_annual_tax = annual_tax - rebate_87A

4. monthly_tds = (net_annual_tax - tax_paid_ytd) / months_remaining
```

---

## Tax slabs

### New Regime (FY 2024-25)

| Income range | Rate |
|---|---|
| Up to ₹3,00,000 | Nil |
| ₹3,00,001 – ₹7,00,000 | 5% |
| ₹7,00,001 – ₹10,00,000 | 10% |
| ₹10,00,001 – ₹12,00,000 | 15% |
| ₹12,00,001 – ₹15,00,000 | 20% |
| Above ₹15,00,000 | 30% |

### Old Regime

| Income range | Rate |
|---|---|
| Up to ₹2,50,000 | Nil |
| ₹2,50,001 – ₹5,00,000 | 5% |
| ₹5,00,001 – ₹10,00,000 | 20% |
| Above ₹10,00,000 | 30% |

---

## Surcharge

| Annual income | Surcharge rate |
|---|---|
| ₹50L – ₹1Cr | 10% |
| ₹1Cr – ₹2Cr | 15% |
| ₹2Cr – ₹5Cr | 25% |
| Above ₹5Cr | 37% (Old) / 25% (New) |

---

## Marginal relief

When income slightly exceeds a surcharge threshold, the additional tax can exceed the extra income. Indian Payroll applies **marginal relief**:

```
if base_tax > excess_income_over_threshold:
    rebate = base_tax - excess_income_over_threshold
    base_tax -= rebate
```

Configure this on the Income Tax Slab with `custom_marginal_relief_applicable`, `custom_minimum_value`, and `custom_maximum_value`.

---

## Standard deduction

₹75,000 per annum (FY 2024-25 onwards, both regimes). Applied automatically.

---

## Section 80C and Chapter VIA (Old Regime)

Employees declare investments via **Tax Exemption Declaration**. Common deductions:

| Section | Deduction | Limit |
|---|---|---|
| 80C | EPF, ELSS, PPF, LIC, Home loan principal | ₹1,50,000 |
| 80CCD(1B) | Additional NPS | ₹50,000 |
| 80CCD(2) | Employer NPS | No limit |
| 80D | Medical insurance premium | ₹25,000–₹50,000 |
| 24(b) | Home loan interest | ₹2,00,000 |

---

## Custom additional TDS

If an employee has outside income (rental, capital gains), HR can set **Additional TDS Amount** (`custom_additional_tds_deducted_amount`) on any salary slip. This is added on top of the computed TDS for that month.

---

## TDS Projection

Go to **Payroll → TDS Projection** to see a month-by-month forecast of TDS liability for any employee for the rest of the financial year. Useful for planning declarations or flagging employees at risk of short deduction.
