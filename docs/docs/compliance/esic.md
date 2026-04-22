---
id: esic
title: ESIC
sidebar_position: 2
description: Employee State Insurance contribution calculation and ESIC register.
---

# ESIC

The Employee State Insurance Corporation (ESIC) provides medical, sickness, maternity, and disablement benefits. Contributions apply to employees earning up to ₹21,000/month gross.

---

## Contribution rates

| | Rate | On |
|---|---|---|
| **Employee** | 0.75% | Gross wages |
| **Employer** | 3.25% | Gross wages |

---

## Eligibility

An employee is ESIC-eligible if their **gross wages ≤ ₹21,000/month** (₹25,000 for persons with disabilities).

In Indian Payroll, eligibility is toggled per employee on the **Salary Structure Assignment** via the **Is ESIC** checkbox. The system does not automatically flip this flag if an employee's salary crosses the ceiling mid-year — HR must update the SSA.

:::tip
Create a monthly reminder to review ESIC eligibility for employees near the ₹21,000 gross threshold, especially after increments.
:::

---

## ESIC Number

Store the employee's ESIC IP number in the Employee master field `custom_esic_number`. This appears on the annual TDS statement and ESIC register.

---

## ESIC Register report

Go to **Reports → ESIC Register**.

Shows:
- Employee, ESIC IP number, gross wages, employee contribution (0.75%), employer contribution (3.25%).
- Filter by Company, Month, Payroll Period.

Use this report to verify amounts before filing the ESIC challan on the **ESIC portal** (https://esic.gov.in).

---

## State-wise applicability

Some states have full ESIC applicability; others are partially covered. The **India Payroll State** fixture marks each state as ESIC-applicable. Employees in non-applicable states are automatically excluded even if **Is ESIC** is checked on their assignment.
