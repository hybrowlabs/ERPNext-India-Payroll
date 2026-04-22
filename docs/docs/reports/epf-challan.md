---
id: epf-challan
title: EPF Challan Report
sidebar_position: 2
description: Generate the ECR challan file for EPFO filing.
---

# EPF Challan Report

The **EPF Challan Report** produces the contribution summary and the **ECR (Electronic Challan-cum-Return)** text file for direct upload to the EPFO unified portal.

---

## Filters

| Filter | Required | Description |
|---|---|---|
| Company | Yes | Drives Basic and DA component lookup from Company master |
| Month | No | Filter by calendar month |
| Payroll Period | No | Filter by financial year |

---

## Columns

| Column | Description |
|---|---|
| UAN | Unique Account Number from Employee master |
| Employee | Employee ID |
| Employee Name | Full name |
| Month | Payroll month |
| Payroll Period | Financial year |
| Company | Entity |
| Gross Pay | Total gross earnings from slip |
| EPF Wages | Basic + DA (+ arrear components) |
| EPS Wages | min(EPF Wages, 15,000) |
| EDLI Wages | Same as EPF Wages |
| EPF Contribution (12%) | Employee EPF deducted |
| EPS Contribution (8.33%) | Employer EPS |
| EDLI Contribution (3.67%) | Employer EDLI |
| NCP Days | Non-Contributing Period days |
| Refund of Advances | Always 0 (manual entry if applicable) |

---

## Download ECR TXT

Click **Download ECR** at the top of the report. The downloaded file is pipe-delimited (`#~#`) in EPFO ECR v2 format:

```
UAN#~#Name#~#Gross#~#EPFWage#~#EPSWage#~#EDLIWage#~#EPF#~#EPS#~#EDLI#~#NCP#~#Refund
```

Upload this file at **EPFO Unified Portal → Establishment → ECR Upload**.

:::warning
The **Download ECR** button is restricted to **HR Manager** role. Accessing this endpoint without the role returns a permission error.
:::

---

## Employees excluded from the report

An employee is excluded if:
- `custom_is_epf` is unchecked on their active Salary Structure Assignment.
- No active submitted Salary Structure Assignment exists for the month.
