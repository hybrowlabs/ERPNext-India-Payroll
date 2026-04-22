---
id: processing
title: Payroll Processing
sidebar_position: 1
description: End-to-end guide to running monthly payroll using Indian Payroll.
---

# Payroll Processing

This page covers the complete monthly payroll cycle — from creating the Payroll Entry to submitting and generating payment files.

---

## Overview

The payroll flow follows the standard HRMS model, with Indian-specific steps inserted at key points:

<div class="flow-step"><div class="flow-step__num">1</div><div><strong>Payroll Entry</strong> — select company, payroll period, month, cost centre, department filters.</div></div>
<div class="flow-step"><div class="flow-step__num">2</div><div><strong>Fill Employees</strong> — auto-populates eligible employees (must have an active Salary Structure Assignment).</div></div>
<div class="flow-step"><div class="flow-step__num">3</div><div><strong>Create Salary Slips</strong> — generates one Salary Slip per employee with all earnings, deductions, and statutory amounts computed.</div></div>
<div class="flow-step"><div class="flow-step__num">4</div><div><strong>Review &amp; Validate</strong> — check individual slips; any correction triggers a recompute.</div></div>
<div class="flow-step"><div class="flow-step__num">5</div><div><strong>Submit Payroll Entry</strong> — locks slips, posts journal entries to GL accounts.</div></div>
<div class="flow-step"><div class="flow-step__num">6</div><div><strong>Download Reports</strong> — Bank Mandate, EPF Challan, ESIC Register, TDS Register.</div></div>

---

## Payroll Entry

Go to **HR → Payroll → Payroll Entry → New**.

### Key fields

| Field | Description |
|---|---|
| **Company** | Drives EPF, PT, ESIC config from Company master. |
| **Payroll Period** | Financial year period — e.g. `FY 2024-25`. |
| **Custom Month** | Calendar month name — e.g. `April`. Used on every slip and report filter. |
| **Start / End Date** | Attendance cycle dates for this payroll run. |
| **Cost Centre** | Optional — filters employees by cost centre assignment. |
| **Department** | Optional — process payroll for a single department. |
| **Branch** | Optional — filter by branch. |

### Fill Employees

Click **Fill Employees** (requires HR Manager role). The system fetches all employees who:
1. Are `Active`.
2. Have a submitted Salary Structure Assignment with `from_date ≤ end_date`.

Employees without a valid structure assignment are silently skipped — check the **Employee Reconciliation** report to identify gaps.

---

## Salary Slip computation

When a Salary Slip is created or recalculated, the following sequence runs:

```
validate()
  ├── get_working_days_details()      # attendance / LOP / holidays
  ├── insert_lopreversal_days()       # payroll correction docs
  ├── calculate_net_pay()             # HRMS base — runs formulas
  ├── set_taxable_regime()            # stamps regime flags per earning row
  ├── calculate_variable_tax()        # TDS projection
  ├── update_benefit_claim_amount()   # marks benefit claims as paid
  └── update_declaration_component()  # syncs HRA/NPS/PF to declaration
```

### What appears on the slip

| Section | What it includes |
|---|---|
| **Earnings** | Basic, HRA, Special Allowance, NPS (employer), LTA, Food Coupon, any Variable earnings |
| **Deductions** | EPF (employee 12%), ESIC (employee 0.75%), PT, Income Tax (TDS), LWF |
| **Custom totals** | Annual CTC, Statutory Gross Pay, Total Income, Total Deduction, Net Pay |

---

## Custom fields on Salary Slip

| Field | Description |
|---|---|
| `custom_month` | Month name — used for filtering in all reports. |
| `custom_payroll_period` | Link to Payroll Period. |
| `custom_annual_ctc` | Employee's annual CTC at the time of slip. |
| `custom_statutory_grosspay` | Gross as defined under statutory rules (EPF wage base). |
| `custom_total_income` | Total taxable income for the month. |
| `custom_total_deduction_amount` | Sum of all deductions. |
| `custom_net_pay_amount` | Take-home after all deductions. |
| `custom_month_count` | Remaining months in the payroll period — used for TDS projection. |
| `custom_tax_regime` | `New Regime` or `Old Regime` — stamped from Salary Structure Assignment. |
| `custom_lop_reversal_days` | Days added back from approved Payroll Correction docs. |
| `custom_total_leave_without_pay` | Absent + LWP days — used in EPF challan NCP days. |
| `custom_additional_tds_deducted_amount` | Manual additional TDS for the month. |

---

## LOP and attendance cycle

### Standard LOP
Absent days and leaves without pay are picked from attendance records in the slip's start–end date range. The formula:

```
LWP = absent_days + leave_without_pay
payment_days = total_working_days - LWP
```

### LOP Reversal (Payroll Correction)
If attendance was incorrectly marked and corrected after payroll cut-off, create a **Payroll Correction** doc:
- Set `employee`, `payroll_date`, and `days_to_reverse`.
- Submit it.

The next salary slip automatically picks up `custom_lop_reversal_days` from all submitted Payroll Corrections in the slip period. These days are restored to payment days.

### Custom Attendance Cycle
If your company's attendance cycle doesn't match the calendar month (e.g. 21st–20th), enable **Configure Attendance Cycle** in Payroll Settings and set the cycle start day. The working days calculation uses this cycle instead of the calendar month boundary.

---

## Bulk Salary Structure Assignment

Go to **Payroll → Structure Setting → Create Salary Structure Assignment (Bulk)**.

This is a background-queued operation that:
1. Reads all Active employees.
2. Copies the latest submitted SSA per employee.
3. Creates a new SSA with the selected `effective_date`, `payroll_period`, and `income_tax_slab`.
4. Broadcasts progress via WebSocket so the UI progress bar updates live.

Useful at the start of a new financial year when tax slabs or regimes change.

---

## Submitting and posting

On **Submit**, the Payroll Entry:
1. Submits all individual Salary Slips (locks them from editing).
2. Posts journal entries — debit Salary Expense accounts, credit EPF/ESIC/PT/TDS payable accounts.
3. Each GL posting uses the cost centre from the slip.

:::warning
Do not manually commit in `on_submit` hooks. The framework handles the transaction. Adding `frappe.db.commit()` inside a lifecycle method breaks atomicity.
:::

---

## After submit — next steps

| Action | Where |
|---|---|
| Download bank payment file | **Bank Mandate** report |
| Download EPF challan | **EPF Challan Report** → Export ECR TXT |
| Download ESIC register | **ESIC Register** report |
| File TDS | **TDS Register** report |
| Distribute payslips | Salary Slip → Print → `Salary Slip Standard` format |
