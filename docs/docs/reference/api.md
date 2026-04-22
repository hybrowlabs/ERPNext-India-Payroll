---
id: api
title: API Reference
sidebar_position: 3
description: Whitelisted Python endpoints exposed by Indian Payroll.
---

# API Reference

All endpoints are Frappe whitelisted methods — callable via `frappe.call()` from the client or `POST /api/method/<dotted.path>` from external systems.

---

## Payroll

### `generate_ctc_pdf`

```
cn_indian_payroll.cn_indian_payroll.payroll.overrides.salary_structure_assignment.generate_ctc_pdf
```

**Role required**: HR Manager

Generates a CTC Breakup PDF for an employee and stores it as a private File attachment.

| Parameter | Type | Description |
|---|---|---|
| `employee` | String | Employee ID |
| `salary_structure` | String | Salary Structure name |
| `posting_date` | Date | Optional — defaults to today |
| `employee_benefits` | JSON | Optional — array of `{salary_component, amount}` |

**Returns**: `{ "pdf_url": "/private/files/CTC_Breakup_<emp>.pdf" }`

---

### `create_salary_structure_assignment`

```
cn_indian_payroll.cn_indian_payroll.payroll.overrides.structure_setting.create_salary_structure_assignment
```

**Role required**: HR Manager

Queues a background job that creates new Salary Structure Assignments for all active employees, copying forward the latest SSA fields.

| Parameter | Type | Description |
|---|---|---|
| `company` | String | Company name |
| `payroll_period` | String | Target payroll period |
| `income_tax_slab` | String | Income Tax Slab to assign |
| `effective_date` | Date | From date for new assignments |

**Returns**: `"queued"`. Progress is broadcast via WebSocket event `ssa_progress`.

---

### `get_annual_statement_pdf`

```
cn_indian_payroll.cn_indian_payroll.payroll.overrides.tds_printer.get_annual_statement_pdf
```

**Role required**: HR User (read access to Salary Slip)

Returns the HTML for the annual TDS statement for an employee.

| Parameter | Type | Description |
|---|---|---|
| `employee` | String | Employee ID |
| `payroll_period` | String | |
| `end_date` | Date | Project up to this date |
| `month` | String | Current month |
| `tax_regime` | String | New Regime / Old Regime |
| `id` | String | Salary Slip name (latest) |
| `income_tax_slab` | String | |

**Returns**: `{ "html": "..." }`

---

## Loans

### `hold_installments`

```
cn_indian_payroll.cn_indian_payroll.loans.overrides.loan_application.hold_installments
```

**Role required**: HR Manager

Adjusts a loan's repayment schedule by extending, recovering, or distributing installments.

| Parameter | Type | Description |
|---|---|---|
| `employee` | String | Employee ID |
| `payment_date` | Date | Target installment date |
| `company` | String | |
| `type` | String | `Extend Repayment Period` / `Recover Pending in Next Month` / `Distribute Across Future Months` |
| `number_of_months` | Int | Number of months to extend/skip |
| `doc_id` | String | Loan name |

**Returns**: `"success"`

---

### `edit_installment`

```
cn_indian_payroll.cn_indian_payroll.loans.overrides.loan_application.edit_installment
```

**Role required**: HR Manager

Partially pays an installment and redistributes the unpaid amount across future installments.

| Parameter | Type | Description |
|---|---|---|
| `employee` | String | |
| `payment_date` | Date | |
| `company` | String | |
| `hold_option` | String | Redistribution method |
| `number_of_months` | Int | |
| `repayment_amount` | Currency | Partial amount paid |
| `doc_id` | String | Loan name |

---

## Tax

### `calculate_tax`

```
cn_indian_payroll.cn_indian_payroll.tax_utils.calculate_tax
```

**Permission required**: Read access to the Employee Tax Exemption Declaration.

Displays a tax comparison popup (Old Regime vs. New Regime) for a given declaration.

| Parameter | Type | Description |
|---|---|---|
| `doc_name` | String | Employee Tax Exemption Declaration name |
| `totalincome` | Float | Optional override for total income |

---

### `download_ecr_txt`

```
cn_indian_payroll.cn_indian_payroll.report.epf_challan_report.epf_challan_report.download_ecr_txt
```

**Role required**: HR Manager

Returns the ECR text file content as a string.

| Parameter | Type | Description |
|---|---|---|
| `filters` | JSON | `{company, month, payroll_period}` |

**Returns**: Multi-line string in EPFO ECR v2 format.

---

## Error handling

All endpoints use standard Frappe error responses:
- `403 Forbidden` — permission check failed.
- `404 Not Found` — document not found.
- `417 Expectation Failed` — validation error (`frappe.throw()`).

Client-side: wrap calls in `frappe.call({ ... }).then(...).catch(frappe.msgprint)`.
