---
id: professional-tax
title: Professional Tax & LWF
sidebar_position: 3
description: State-wise Professional Tax slabs and Labour Welfare Fund deduction.
---

# Professional Tax & LWF

## Professional Tax

Professional Tax (PT) is a state-level tax on employment income. It is deducted from the employee's salary and remitted to the state government.

### Rates

PT is slab-based — the deduction amount depends on the employee's **monthly gross salary** and the **state** they work in. Rates differ widely:

| State | Example slab |
|---|---|
| Maharashtra | ₹200/mo if gross > ₹7,500 |
| Karnataka | ₹200/mo if gross > ₹15,000 |
| West Bengal | ₹150–₹200/mo based on slab |
| Tamil Nadu | Max ₹208/mo |
| Andhra Pradesh | Slab-based up to ₹2,500 p.a. |

Maximum PT under the Constitution is ₹2,500 per annum.

### How it's applied

1. The employee's **State** is set on their Salary Structure Assignment (`custom_state`).
2. The corresponding **India Payroll State** record defines the PT slab table.
3. When the salary slip is computed, the PT component amount is looked up from the slab based on the monthly gross.

### Employer liability

PT is a **deduction** from the employee's salary. The employer is responsible for collecting and remitting it to the state government, but it is not an employer cost (unlike EPF or ESIC).

---

## Labour Welfare Fund (LWF)

LWF is a statutory contribution to a state welfare fund. Unlike PT, it is often paid on a **half-yearly or annual basis** and may have both employee and employer components.

### Configuration

In **India Payroll State**, each state record has:
- **LWF Frequency** — `Monthly`, `Half-Yearly`, or `Annually`.
- **Employee LWF** — employee deduction amount.
- **Employer LWF** — employer contribution amount.

### Deduction timing

The salary slip deducts LWF only in the applicable months based on frequency:
- Monthly: every month.
- Half-yearly: June and December.
- Annually: March (or as per state rules).

### States with LWF

| State | Frequency |
|---|---|
| Maharashtra | Monthly |
| Karnataka | Half-yearly |
| Gujarat | Annually |
| Tamil Nadu | Annually |
| Andhra Pradesh | Half-yearly |

States not covered by LWF have a zero-amount record in the India Payroll State fixture.

---

## Tax treatment

- **PT**: Fully deductible from gross income for income tax purposes (Section 16(iii)).
- **LWF (Employee)**: Deductible from gross income where applicable.
