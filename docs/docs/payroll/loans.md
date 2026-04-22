---
id: loans
title: Loans & Perquisites
sidebar_position: 4
description: Employee loans, repayment schedule management, and perquisite valuation.
---

# Loans & Perquisites

Indian Payroll extends the **Lending** app's loan management with repayment schedule adjustments and perquisite tax valuation for concessional/interest-free loans.

---

## Loan perquisite

Under Income Tax rules, if a company provides a loan at zero interest or below the SBI benchmark rate, the interest difference is a **perquisite** — taxable in the employee's hands.

### Perquisite calculation

```
Perquisite value = Outstanding principal × (SBI rate − actual rate) × days/365
```

This perquisite is added to the employee's taxable income each month, increasing the TDS deduction accordingly.

### Configuration

On the employee's **Employee Perquisite Information** record:
- Set loan amount, actual interest rate, and SBI benchmark rate.
- The system auto-computes the monthly perquisite for inclusion in the salary slip.

---

## Repayment schedule management

The standard Lending app creates a fixed amortisation schedule. Indian Payroll adds three schedule-adjustment actions (HR Manager only):

### Extend Repayment Period

Shifts all installments from a given date forward by N months. Use this when an employee takes a leave of absence.

**Example**: Extending by 2 months from June moves June, July, August… to August, September, October…

### Recover Pending in Next Month

Skips N consecutive installments and adds their combined principal + interest to the next scheduled installment. The skipped rows are removed from the schedule.

**Example**: Skip June and July → July's installment absorbs both amounts.

### Distribute Across Future Months

Removes N installments and spreads their amounts equally across all remaining future installments.

---

## Deduction from salary slip

Loan repayments are deducted via an **Additional Salary** document (type: Deduction) linked to the **Loan Repayment Schedule** row. The Additional Salary auto-posts to the salary slip in the correct month.

---

## Loan Dashboard

Open any **Loan** document and click **View Dashboard** to see:
- Total disbursed amount.
- Total repaid to date.
- Outstanding balance.
- Schedule compliance (on-time vs. deferred installments).

---

## Access control

| Action | Required role |
|---|---|
| Extend / Recover / Distribute installments | HR Manager |
| View loan dashboard | HR User or HR Manager |
| Create loan | As per standard Lending permissions |
