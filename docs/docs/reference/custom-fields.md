---
id: custom-fields
title: Custom Fields Reference
sidebar_position: 2
description: All custom fields added to standard ERPNext/HRMS doctypes.
---

# Custom Fields Reference

All fields are prefixed `custom_` per Frappe's convention for programmatically-added fields. They are installed on `bench install-app` and removed on `bench remove-app`.

---

## Salary Slip

| Field | Type | Description |
|---|---|---|
| `custom_month` | Data | Calendar month name (April, May…) |
| `custom_payroll_period` | Link → Payroll Period | Financial year |
| `custom_annual_ctc` | Currency | Annual CTC at time of slip |
| `custom_statutory_grosspay` | Currency | Gross for statutory purposes (EPF wage base) |
| `custom_total_income` | Currency | Total taxable income |
| `custom_total_deduction_amount` | Currency | Sum of all deductions |
| `custom_net_pay_amount` | Currency | Net take-home |
| `custom_month_count` | Int | Remaining months in the payroll period |
| `custom_tax_regime` | Select | New Regime / Old Regime |
| `custom_lop_reversal_days` | Float | Days restored from Payroll Correction docs |
| `custom_total_leave_without_pay` | Float | absent_days + leave_without_pay |
| `custom_additional_tds_deducted_amount` | Currency | Manual TDS addition |
| `custom_rebate_under_section_87a` | Currency | Rebate computed |
| `custom_surcharge` | Currency | Surcharge amount |
| `custom_education_cess` | Currency | 4% cess |
| `custom_taxable_amount` | Currency | Net taxable income |
| `custom_tax_on_total_income` | Currency | Tax before cess/surcharge |
| `custom_total_tax_on_income` | Currency | Total tax after cess/surcharge |

---

## Employee

| Field | Type | Description |
|---|---|---|
| `custom_uan` | Data | Universal Account Number (EPF) |
| `custom_esic_number` | Data | ESIC IP number |

---

## Salary Structure Assignment

| Field | Type | Description |
|---|---|---|
| `custom_payroll_period` | Link → Payroll Period | |
| `custom_is_epf` | Check | EPF eligible |
| `custom_is_esic` | Check | ESIC eligible |
| `custom_is_nps` | Check | NPS participant |
| `custom_is_food_coupon` | Check | Food coupon applies |
| `custom_is_uniform_allowance` | Check | Uniform allowance applies |
| `custom_uniform_allowance_value` | Currency | Monthly uniform allowance |
| `custom_is_medical_allowance` | Check | Medical allowance applies |
| `custom_medical_allowance_value` | Currency | Monthly medical allowance |
| `custom_state` | Link → India Payroll State | Employee's work state |
| `custom_tax_regime` | Select | New Regime / Old Regime |
| `custom__car_perquisite` | Check | Company car perquisite |
| `custom_cubic_capacity_of_company` | Select | < 1600cc / ≥ 1600cc |
| `custom_car_perquisite_as_per_rules` | Check | Use per-rules valuation |
| `custom_driver_provided_by_company` | Check | Driver included |
| `custom_driver_perquisite_as_per_rules` | Check | Driver per-rules valuation |
| `custom_nps_percentage` | Percent | Employer NPS % of Basic |

---

## Employee Tax Exemption Declaration

| Field | Type | Description |
|---|---|---|
| `custom_tax_regime` | Select | New Regime / Old Regime |
| `custom_salary_structure_assignment` | Link → SSA | |
| `custom_posting_date` | Date | Last sync date from salary slip |
| `custom_status` | Select | Draft / Approved |
| `custom_declaration_form_data` | Long Text | JSON from the web form |
| `custom_check` | Check | HRA computed flag |
| `custom_basic` | Currency | Aggregated Basic for HRA |
| `custom_basic_as_per_salary_structure` | Currency | 10% of Basic |
| `custom_hra_breakup` | Table | Month-wise HRA breakdown |

---

## Salary Component

| Field | Type | Description |
|---|---|---|
| `custom_component_type` | Select | EPF / ESIC / NPS / PT / LTA Reimbursement / etc. |
| `custom_component_sub_type` | Select | Fixed / Variable |
| `custom_is_part_of_ctc` | Check | Show in CTC Breakup PDF |
| `custom_tax_exemption_applicable_based_on_regime` | Check | Regime-dependent exemption |
| `custom_regime` | Select | All / New Regime / Old Regime |

---

## Company

| Field | Type | Description |
|---|---|---|
| `basic_component` | Link → Salary Component | Basic wage component |
| `hra_component` | Link → Salary Component | HRA component |
| `custom_da_component` | Link → Salary Component | DA component (EPF wage) |
