---
id: tds-register
title: TDS Register
sidebar_position: 5
description: Month-wise TDS deducted per employee — for quarterly TDS return filing.
---

# TDS Register

The **TDS Register** shows income tax deducted at source from each employee's salary. Use it to verify amounts before filing the quarterly **TDS Return (Form 24Q)**.

---

## Columns

| Column | Description |
|---|---|
| Employee | Employee ID |
| Employee Name | Full name |
| PAN | Employee PAN from Employee master |
| Month | Calendar month |
| Gross Salary | Total earnings in the month |
| Standard Deduction | ₹75,000 p.a. pro-rated |
| Taxable Income | Gross − exemptions − deductions |
| TDS Deducted | Income tax deducted in the month |
| Cumulative TDS | YTD tax deducted |

---

## Filing Form 24Q

1. Filter by Payroll Period and the quarter months (Q1: Apr–Jun, Q2: Jul–Sep, etc.).
2. Export to Excel.
3. Use the data to populate Form 24Q in your TDS return software (e.g. TRACES RPU).
4. Upload the FVU file on **TRACES** (https://tdscpc.gov.in).

:::tip
Generate this report after every payroll run to catch any employees where TDS was zero but should have been deducted (e.g. new joiners who crossed the basic exemption limit mid-year).
:::
