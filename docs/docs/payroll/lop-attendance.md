---
id: lop-attendance
title: LOP & Attendance
sidebar_position: 3
description: How Leave Without Pay, absent days, LOP reversal, and attendance cycles work.
---

# LOP & Attendance

Indian Payroll extends HRMS's attendance handling with LOP reversal and configurable attendance cycles.

---

## How payment days are calculated

```
total_working_days  = calendar days in slip period
                      − non-working days (weekends per policy)
                      − holidays in Holiday List

LWP                 = leave_without_pay + absent_days
payment_days        = total_working_days − LWP

pro_rated_amount    = component_amount × (payment_days / total_working_days)
```

Any component marked **Do Not Include in Total** is excluded from this pro-ration.

---

## LOP Reversal (Payroll Correction)

A **Payroll Correction** document allows HR to add back days that were incorrectly marked absent after payroll was processed.

### Creating a correction

1. Go to **HR → Payroll → Payroll Correction → New**.
2. Set **Employee**, **Payroll Date** (within the target slip's date range), and **Days to Reverse**.
3. Submit the document.

### Effect on the next slip

When the next salary slip for that employee is generated:
- The system sums all submitted Payroll Correction records whose `payroll_date` falls within `start_date` to `end_date`.
- This sum is stored as `custom_lop_reversal_days` on the slip.
- Payment days are increased by this amount.

:::info
LOP reversal applies to the **current** slip — it does not retroactively amend the slip where the absence occurred. Accounting correction (if needed) is done manually.
:::

---

## Custom Attendance Cycle

Some companies run attendance from mid-month to mid-month (e.g. 21st to 20th). In that case:

1. Go to **HR → Settings → Payroll Settings**.
2. Enable **Configure Attendance Cycle**.
3. Set **Attendance Cycle Start Day** (e.g. `21`).

The working days calculation will use this cycle boundary instead of the calendar month. The salary slip's `start_date` and `end_date` must be set to match the cycle (e.g. 21 Mar – 20 Apr for the April payroll).

---

## Half-day handling

Set **Daily Wages Fraction for Half Day** in Payroll Settings (default `0.5`).

Half-day attendance records deduct `1 − fraction` from payment days. Example: if fraction = 0.5, a half-day deducts 0.5 days from payment days.

---

## Attendance fields on Salary Slip

| Field | Source | Meaning |
|---|---|---|
| `total_working_days` | Computed | Calendar working days in the slip period |
| `payment_days` | Computed | `working_days − LWP − absent` |
| `absent_days` | Attendance | Days with Absent status |
| `leave_without_pay` | Leave | Approved LWP leaves |
| `custom_lop_reversal_days` | Payroll Correction | Days added back via corrections |
| `custom_total_leave_without_pay` | Computed | `absent_days + leave_without_pay` — used in EPF NCP days |
