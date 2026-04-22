---
id: configuration
title: Initial Configuration
sidebar_position: 3
description: Configure the Company master, payroll settings, and salary components before running payroll.
---

# Initial Configuration

After install, complete these one-time configurations before processing your first payroll.

---

## 1. Company master

Go to **Accounting → Company → [Your Company]** and set the Indian Payroll fields:

| Field | Description |
|---|---|
| **Basic Component** | The Salary Component used as the Basic wage (e.g. `Basic`). Used by HRA and EPF calculations. |
| **HRA Component** | The Salary Component for House Rent Allowance. Required for HRA exemption calculation. |
| **DA Component** | Dearness Allowance component. Used in EPF wage calculation. |
| **PF Account** | GL Account for Provident Fund liability. |
| **ESIC Account** | GL Account for ESIC liability. |

---

## 2. Payroll Settings

Go to **HR → Settings → Payroll Settings**:

- Set **Payroll Based On** — `Attendance` (recommended) or `Leave`.
- Enable **Configure Attendance Cycle** if your month runs from a non-calendar start date (e.g. 21st to 20th).
- Set **Daily Wages Fraction for Half Day** (default `0.5`).

---

## 3. Income Tax Regime

Go to **Payroll → Income Tax Regime** (a custom doctype added by this app):

- Create records for **New Regime** and **Old Regime**.
- Each regime points to the corresponding **Income Tax Slab** from HRMS.

These are pre-seeded via fixtures on install. You only need to update the slabs when the Finance Bill changes tax rates.

---

## 4. India Payroll State

Go to **Payroll → India Payroll State**. Each state record defines:

- **Professional Tax slab** — monthly gross to PT amount mapping.
- **LWF (Labour Welfare Fund)** — frequency (monthly/half-yearly/annually) and amount.
- **ESIC applicability** — toggle per state.

Default state records are seeded from fixtures on install.

---

## 5. Salary Components

For each Salary Component used in Indian payroll, open the component and set:

| Field | Where to set | Meaning |
|---|---|---|
| **Component Type** | Salary Component → Indian Payroll tab | `NPS`, `Provident Fund`, `Professional Tax`, `ESIC`, etc. |
| **Component Sub Type** | Same tab | `Fixed` (constant amount) or `Variable` (formula-driven). |
| **Is Part of CTC** | Same tab | Include this component in the CTC Breakup PDF. |
| **Arrear Component** | Same tab | If checked, amount is added to EPF/DA wage base. |
| **Tax Exemption Applicable** | Same tab | Whether this earning is exempt under Old Regime. |
| **Regime** | Same tab | `All`, `New Regime`, or `Old Regime`. |

---

## 6. Salary Structure Assignment

When assigning a structure to an employee, the custom fields on the **Salary Structure Assignment** form let you toggle eligibility per employee:

| Field | Description |
|---|---|
| **Is EPF** | Employee is EPF-eligible (contributes at 12%). |
| **Is ESIC** | Employee is ESIC-eligible (gross ≤ ₹21,000/month). |
| **Is NPS** | Employee participates in NPS (employer contribution). |
| **Is Food Coupon** | Sodexo/food coupon benefit applies. |
| **Is Medical Allowance** | Fixed medical allowance (Old Regime exempt up to ₹15,000 p.a.). |
| **Is Uniform Allowance** | Uniform allowance applies. |
| **State** | Employee's work state — drives PT and LWF slabs. |
| **Tax Regime** | `New Regime` or `Old Regime`. |
| **Car Perquisite** | Enable if company car is provided. |
| **NPS %** | Employer NPS contribution as % of Basic. |

---

## 7. Payroll Period

Create a **Payroll Period** (standard HRMS doctype) for each financial year:

- **Start Date**: 1 April
- **End Date**: 31 March
- **Company**: Your company

Indian Payroll uses the payroll period to aggregate YTD tax, track declarations, and project future months for TDS calculation.

---

## Checklist

| Step | Done? |
|---|---|
| Company master — Basic, HRA, DA components set | ☐ |
| Income Tax slabs linked to regimes | ☐ |
| State PT/LWF slabs reviewed | ☐ |
| Salary Components typed (EPF, PT, ESIC, NPS) | ☐ |
| Salary Structure created with correct formulas | ☐ |
| Payroll Period created for current FY | ☐ |
| Employees have Salary Structure Assignments | ☐ |
