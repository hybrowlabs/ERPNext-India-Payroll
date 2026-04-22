---
id: bank-mandate
title: Bank Mandate Report
sidebar_position: 4
description: Net pay with employee bank account details for bulk salary transfer.
---

# Bank Mandate Report

The **Bank Mandate** report lists each employee's net pay alongside their bank account number and IFSC code — the input file for bulk salary payment via NEFT/RTGS.

---

## Columns

| Column | Source |
|---|---|
| Salary Slip | Link to the slip |
| Account Number | `bank_ac_no` from Employee master |
| IFSC Code | `ifsc_code` from Employee master |
| Employee | Employee ID |
| Employee Name | Full name |
| Company | Entity |
| Payroll Period | Financial year |
| Month | Calendar month |
| Amount Paid | `net_pay` from Salary Slip |

---

## Filters

Company, Month, Payroll Period, Employee (optional).

---

## Uploading to bank

Most Indian banks accept a CSV or fixed-format text file for bulk salary credit. Export this report to CSV and reformat as per your bank's template (HDFC, SBI, ICICI, Axis, etc.).

:::info
Ensure employee bank details are kept current in the Employee master. Indian Payroll reads `bank_ac_no` and `ifsc_code` directly from the Employee record at report generation time.
:::

---

## Reconciliation

After payment, match the bank debit advice against the **Amount Paid** column to confirm all transfers were successful. Any rejections (invalid IFSC, closed account) should be rectified in the Employee master before the next run.
