---
id: salary-structure
title: Salary Structures & CTC
sidebar_position: 2
description: Build salary structures for Indian payroll with CTC, components, and tax regime awareness.
---

# Salary Structures & CTC

A **Salary Structure** in HRMS defines the formula-driven template applied to every employee's slip. Indian Payroll adds regime awareness, CTC-tracking, and a PDF breakup generator on top.

---

## Building a structure

Go to **HR → Payroll → Salary Structure → New**.

Typical Indian structure has:

### Earnings

| Component | Formula example | Notes |
|---|---|---|
| Basic | `base * 0.40` | 40% of CTC — EPF/HRA base |
| HRA | `basic * 0.50` | 50% for metro, 40% non-metro |
| Special Allowance | `base - basic - hra - ...` | Balancing component |
| LTA | Fixed or `basic * 0.083` | Tax-exempt under Old Regime |
| Food Coupon | Fixed ₹2,200/mo | Tax-exempt (Sodexo) |
| Medical Allowance | Fixed ₹1,250/mo | Old Regime exempt ≤ ₹15,000 p.a. |
| NPS (Employer) | `basic * 0.10` | 80CCD(2) exempt — both regimes |

### Deductions

| Component | Formula | Notes |
|---|---|---|
| EPF (Employee) | `min(basic, 15000) * 0.12` | Capped at ₹1,800/mo on ₹15K ceiling |
| ESIC (Employee) | `gross * 0.0075` | Only if gross ≤ ₹21,000 |
| Professional Tax | Slab from India Payroll State | Monthly slab |
| Income Tax | `(annual_tax - tax_paid_ytd) / months_remaining` | Computed by TaxMixin |

---

## Salary Structure Assignment

Each employee has one active **Salary Structure Assignment** per payroll period. Key India-specific fields:

### Statutory toggles

These are checked per employee — not everyone in the same structure necessarily has the same eligibility:

```
✓ Is EPF          — contributes at 12% of basic (capped at ₹15,000)
✓ Is ESIC         — gross wage ≤ ₹21,000
✓ Is NPS          — employer NPS contribution at configured %
✓ Is Food Coupon  — Sodexo / prepaid meal vouchers
✓ Is Uniform      — uniform allowance component active
✓ Is Medical      — fixed medical allowance active
```

### Car perquisite

If the company provides a vehicle, enable **Car Perquisite** and set:
- Cubic capacity (< 1600cc or ≥ 1600cc)
- Whether a driver is provided
- Per-rules valuation toggle

The perquisite value is added to taxable income for TDS.

---

## CTC Breakup PDF

On any **Salary Structure Assignment**, the **Generate CTC PDF** button produces a PDF letter showing the employee's full compensation package:

- Monthly and annual amounts for every CTC component.
- Reimbursements (LTA, Medical, Food Coupon).
- Employer contributions (EPF, NPS) shown separately.
- Total Monthly CTC and Total Annual CTC.

Access: **HR Manager** role required. The PDF is stored privately (not publicly accessible).

:::note
The CTC PDF is a preview — it uses the structure formula at the time of generation. If the employee's actual working days differ, the salary slip will show a different net pay.
:::

---

## Salary Component Library

Go to **Payroll → Salary Component Library Item** to see all pre-seeded components. Each item defines defaults for:
- Component type (`NPS`, `Provident Fund`, `ESIC`, `Professional Tax`, etc.)
- Sub-type (`Fixed` / `Variable`)
- Whether the component is part of CTC
- Tax exemption regime

When creating a new Salary Structure, you can import components from the library rather than defining each manually.

---

## Tax regime per employee

The **Tax Regime** field on Salary Structure Assignment (`New Regime` / `Old Regime`) drives:
1. Which earnings are marked tax-exempt on the slip.
2. Whether HRA exemption is calculated in the tax declaration.
3. Which tax slab is applied during TDS projection.

An employee can switch regime once per financial year. Changing the assignment mid-year creates a new SSA from the effective date — the TDS projection recomputes for remaining months automatically.
