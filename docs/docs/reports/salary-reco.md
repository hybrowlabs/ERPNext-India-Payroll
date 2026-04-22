---
id: salary-reco
title: Salary Reconciliation
sidebar_position: 7
description: Detect gross pay changes between two consecutive months.
---

# Salary Reconciliation

The **Salary Reconciliation** report compares each employee's gross pay between the **current month** and the **previous month**. It highlights new joiners, exits, and employees whose gross changed.

---

## Columns

| Column | Description |
|---|---|
| Employee | Employee ID |
| Employee Name | Full name |
| Current Month | Month name for the current period |
| Gross Pay (Current) | Statutory gross pay in the current month |
| Previous Month | Month name for the comparison period |
| Gross Pay (Previous) | Statutory gross pay in the previous month |
| Difference | Current − Previous gross |
| Status | Employee status (`Active`, `Left`, etc.) |
| Remark | Custom remark (e.g. increment, new joiner) |

---

## Filters

| Filter | Description |
|---|---|
| Company | Mandatory |
| Current Month | Defaults to current calendar month |
| Previous Month | Defaults to previous calendar month |
| Employee | Optional |

---

## Interpreting results

| Difference | Interpretation |
|---|---|
| Positive | Salary increment or new joining |
| Negative | Salary reduction, LOP, or exit |
| Current only (no previous) | New joiner this month |
| Previous only (no current) | Employee exited — no slip this month |
| Zero | No change |

---

## Use cases

- **Pre-payroll sanity check**: Run after creating slips, before submit. Any unexpected increase/decrease flags a data entry issue.
- **Audit trail**: Export to Excel and archive alongside the payroll register.
- **Increment rollout verification**: Confirm increment amounts match the approved hike letters.
