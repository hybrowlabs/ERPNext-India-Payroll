---
id: overview
title: Reports Overview
sidebar_position: 1
description: All statutory and management reports available in Indian Payroll.
---

# Reports Overview

Indian Payroll ships 13 reports — statutory compliance filings, management dashboards, and reconciliation tools.

| Report | Purpose | Roles |
|---|---|---|
| [EPF Challan Report](./epf-challan) | ECR file for EPFO portal + contribution summary | HR Manager |
| ESIC Register | ESIC IP-wise contribution register | HR Manager |
| [TDS Register](./tds-register) | Month-wise TDS deducted per employee | HR Manager |
| [Salary Book Register](./salary-book) | Full component-wise salary register | HR Manager |
| [Bank Mandate](./bank-mandate) | Net pay + bank account list for payment processing | HR Manager |
| [Monthly Salary MIS](./monthly-mis) | Aggregated payroll summary by month | HR Manager, System Manager |
| [Salary Reconciliation](./salary-reco) | Month-over-month gross pay change detection | HR Manager |
| Employee Reconciliation | Employees missing salary structures | HR Manager |
| CTC Breakup | Individual employee CTC structure | HR Manager |
| New Joinee Arrear Report | Arrear amounts for mid-month joiners | HR Manager |
| Accrued Bonus Summary | Accrued bonus per employee | HR Manager |
| Accrued Reimbursements Summary | Accrued reimbursements per employee | HR Manager |
| Loan Repayment Schedule Report | Outstanding loan schedule | HR Manager |

---

## Common filters

Most reports share these filters:

| Filter | Description |
|---|---|
| **Company** | Mandatory — scopes data to one company. |
| **Payroll Period** | Financial year — e.g. `FY 2024-25`. |
| **Month** | Calendar month name — e.g. `April`. |
| **Employee** | Optional — filter to a single employee. |

---

## Exporting data

All reports support:
- **Export to Excel / CSV** — via the standard Frappe report toolbar.
- **Print** — using the browser print dialog or Frappe print format.
- **ECR TXT** — EPF Challan only, via the dedicated download button.

---

## Report permissions

All payroll reports require **HR Manager** or **HR User** role. The **CTC Breakup** report additionally restricts access — employees cannot view other employees' CTC.
