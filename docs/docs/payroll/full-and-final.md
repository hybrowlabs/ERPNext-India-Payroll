---
id: full-and-final
title: Full & Final Settlement
sidebar_position: 5
description: Computing F&F settlement on employee exit — gratuity, leave encashment, and notice recovery.
---

# Full & Final Settlement

When an employee exits, the **Full & Final Settlement** process computes all dues and recoveries payable on the last working day.

---

## What is computed

| Component | Basis |
|---|---|
| **Salary for worked days** | Pro-rated from last salary slip to exit date |
| **Leave Encashment** | Pending earned leaves × daily wage |
| **Gratuity** | 15/26 × last drawn Basic × years of service (≥ 5 years) |
| **Notice Period Recovery** | If employee did not serve notice, deduct remaining notice days at daily wage |
| **Pending Loan Deductions** | Outstanding loan installments become immediately payable |
| **EPF, ESIC, PT** | Computed on the final pro-rated salary |
| **TDS** | Recomputed on annual taxable income including all F&F components |

---

## Gratuity formula

```
Gratuity = (Last Basic + DA) × 15 / 26 × completed_years_of_service
```

- Applicable only if service ≥ 5 years.
- Capped at ₹20 lakh (currently).
- Tax-exempt up to the cap under Section 10(10).

---

## Leave encashment

```
Encashment = pending_earned_leave_days × (Basic + DA) / 26
```

Tax treatment:
- **During service**: Fully taxable.
- **On retirement / resignation**: Exempt up to ₹25 lakh (FY 2023-24 onwards) under Section 10(10AA).

---

## Process flow

<div class="flow-step"><div class="flow-step__num">1</div><div>HR marks employee as <strong>Resigned / Relieved</strong> with exit date.</div></div>
<div class="flow-step"><div class="flow-step__num">2</div><div>Create <strong>Full &amp; Final Settlement</strong> doc, select the employee.</div></div>
<div class="flow-step"><div class="flow-step__num">3</div><div>System auto-computes gratuity, leave encashment, notice recovery.</div></div>
<div class="flow-step"><div class="flow-step__num">4</div><div>HR reviews and adjusts manual components (ex-gratia, bonus, etc.).</div></div>
<div class="flow-step"><div class="flow-step__num">5</div><div>Submit — posts journal entries and generates the final payslip.</div></div>
<div class="flow-step"><div class="flow-step__num">6</div><div>Transfer net F&amp;F amount to employee bank account.</div></div>

---

## TDS on F&F

The F&F TDS is computed on the total annual income including:
- Regular salary earned during the year.
- Gratuity (taxable portion above exemption limit).
- Leave encashment (taxable portion).
- Ex-gratia / bonus paid on exit.

The system annualises and recomputes tax, then deducts the remaining TDS liability in the final payslip.
