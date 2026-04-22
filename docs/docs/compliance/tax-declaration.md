---
id: tax-declaration
title: Tax Exemption Declaration
sidebar_position: 5
description: How employees declare investments and how the system syncs them to TDS computation.
---

# Tax Exemption Declaration

An **Employee Tax Exemption Declaration** is submitted once per financial year per employee. It tells the payroll system what exemptions and deductions to apply when computing monthly TDS.

---

## Declaration lifecycle

<div class="flow-step"><div class="flow-step__num">1</div><div><strong>Employee submits</strong> declaration at the start of the FY (or within 30 days of joining).</div></div>
<div class="flow-step"><div class="flow-step__num">2</div><div><strong>HR approves</strong> — declaration is submitted (docstatus = 1).</div></div>
<div class="flow-step"><div class="flow-step__num">3</div><div><strong>Salary slip computation</strong> reads the declaration and uses declared amounts for TDS.</div></div>
<div class="flow-step"><div class="flow-step__num">4</div><div>At FY end, employees submit <strong>Proof of Investment (POI)</strong>. Unverified amounts are reduced to zero.</div></div>
<div class="flow-step"><div class="flow-step__num">5</div><div>Final month TDS is recomputed on verified amounts — any shortfall is recovered in the last payslip.</div></div>

---

## What can be declared

Each declaration row references an **Employee Tax Exemption Sub Category** (e.g. `80C - EPF`, `80C - ELSS`, `HRA`, `NPS 80CCD(1B)`).

Indian Payroll adds a `custom_component_type` field to each Sub Category to map it to a payroll component (`NPS`, `Provident Fund`, `Professional Tax`). This enables the system to automatically update statutory deduction amounts (EPF, NPS, PT) in the declaration whenever a salary slip is saved — so the employee doesn't have to manually maintain these.

---

## Auto-sync from salary slip

Each time a salary slip is saved, `update_declaration_component()` runs and:

1. Aggregates EPF (previous months + current month + projected future months).
2. Aggregates NPS contributions similarly.
3. Aggregates PT paid/projected.
4. Updates the matching declaration rows and the `custom_declaration_form_data` JSON field.
5. Recalculates HRA exemption if the regime is Old and rent > 0.

The `tax_exemption_declaration` total on the slip reflects these updated amounts.

---

## HRA Exemption (Old Regime)

HRA exemption is the **minimum** of three values:

```
Rule 1: Actual HRA received
Rule 2: Annual rent paid - 10% of Basic
Rule 3: 50% of Basic (metro) or 40% of Basic (non-metro)
```

Indian Payroll computes this automatically from:
- `monthly_house_rent` on the declaration.
- Basic salary from salary slips (previous + current + projected).
- `rented_in_metro_city` flag on the declaration.

A detailed month-wise HRA breakup table is stored on the declaration (`custom_hra_breakup`) and shown in the annual TDS statement.

---

## Declaration Form (Web View)

Employees can access a self-service tax declaration form at:

```
https://<your-site>/tax-exemptions
```

This is a Vue-based SPA (registered as a website route in hooks) where employees fill and save their investment details. On submit, a structured JSON is saved to `custom_declaration_form_data` on the declaration document.

---

## Tax Declaration History

Every time a declaration is updated, a **Tax Declaration History** record is created as an audit trail. The TDS statement (annual PDF) uses the most recent history entry for each payroll period.

---

## Proof of Investment

Go to **HR → Tax → Employee Tax Exemption Proof Submission**.

Employees upload proof documents (receipts, statements). HR verifies and updates the `verified_amount` on each sub-category. Unverified amounts are zeroed before the final payroll run.

:::warning
Always process proof verification before the **February payroll run** to ensure the year-end TDS shortfall or excess is adjusted in March (the last month of the Indian FY).
:::
