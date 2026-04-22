---
id: epf
title: EPF / EPS / EDLI
sidebar_position: 1
description: Provident Fund, Employee Pension Scheme, and EDLI contributions — calculation and challan.
---

# EPF / EPS / EDLI

The Employees' Provident Fund (EPF) is governed by the **EPF & MP Act, 1952**. Indian Payroll handles contribution calculation, eligibility checks, and ECR challan generation.

---

## Contribution rates

| | Rate | On |
|---|---|---|
| **Employee EPF** | 12% | Basic + DA (capped at ₹15,000/month ceiling) |
| **Employer EPS** | 8.33% | EPS wage (min of EPF wage, ₹15,000) |
| **Employer EPF** | 3.67% | EPF wage (employer EPF = 12% − EPS) |
| **EDLI** | 0.5% | EPF wage |
| **Admin charges** | 0.5% | EPF wage (employer) |

---

## EPF wage ceiling

The statutory ceiling for EPF contribution is ₹15,000/month on **Basic + DA**:

```
EPF Wage         = min(Basic + DA, 15,000)    # if capped; or full Basic+DA if not
Employee EPF     = EPF Wage × 12%
EPS Wage         = min(EPF Wage, 15,000)
Employer EPS     = EPS Wage × 8.33%
Employer EPF     = EPF Wage × 3.67%           # goes to EPF account
```

Employees can contribute on actual Basic + DA beyond ₹15,000 (VPF — Voluntary Provident Fund). This is configured on the Salary Structure formula.

---

## EPS eligibility — Sep 2014 cut-off

Employees who **joined after 1 September 2014** and whose EPF wage exceeds ₹15,000 are **not eligible for EPS**. For such employees:

```
EPS Wage         = 0
Employer EPS     = 0
Employer EPF     = EPF Wage × 12%    # full employer share goes to EPF
```

Indian Payroll automatically applies this rule using the employee's `date_of_joining` and their current EPF wage.

---

## Enabling EPF per employee

On the **Salary Structure Assignment**, check **Is EPF**. Employees without this flag are excluded from EPF deduction and from the EPF Challan report.

---

## UAN

Store the employee's **Universal Account Number** in the Employee master field `custom_uan`. This appears on the EPF Challan report and ECR file.

---

## ECR Challan report

Go to **Reports → EPF Challan Report**.

Filters:
- **Company** (mandatory)
- **Month**
- **Payroll Period**

Columns: UAN, Employee, Gross Pay, EPF Wage, EPS Wage, EDLI Wage, EPF Contribution (12%), EPS Contribution (8.33%), EDLI Contribution, NCP Days, Refund.

### Download ECR TXT

Click **Download ECR** to get the file in the EPFO ECR v2 format:

```
UAN#~#EmployeeName#~#GrossPay#~#EPFWage#~#EPSWage#~#EDLIWage#~#EPF#~#EPS#~#EDLI#~#NCPDays#~#Refund
```

Upload this file directly on the **EPFO Unified Portal** (https://unifiedportal-emp.epfindia.gov.in).

---

## NCP Days

**NCP (Non-Contributing Period)** days = `custom_total_leave_without_pay` from the salary slip. These are reported per employee in the ECR file so EPFO can correctly compute benefit eligibility.
