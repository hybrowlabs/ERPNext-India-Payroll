---
id: architecture
title: Architecture
sidebar_position: 1
description: App structure, doctype overrides, mixins, and design principles.
---

# Architecture

## Directory layout

```
cn_indian_payroll/
├── cn_indian_payroll/          # App Python package
│   ├── hooks.py                # Frappe hook registrations
│   ├── install.py              # after_install entry point
│   ├── uninstall.py            # before_uninstall entry point
│   ├── setup.py                # Shared lifecycle logic
│   │
│   ├── constants/
│   │   ├── __init__.py         # EPF/ESIC/PT/TDS numeric constants
│   │   └── custom_fields.py    # All custom field definitions (Python dicts)
│   │
│   ├── utils/
│   │   └── custom_fields.py    # create / delete helpers
│   │
│   └── cn_indian_payroll/      # App module
│       ├── payroll/
│       │   ├── overrides/
│       │   │   ├── salary_slip.py              # CustomSalarySlip
│       │   │   ├── payroll_entry.py            # PayrollEntryOverride
│       │   │   ├── salary_structure_assignment.py
│       │   │   ├── additional_salary.py
│       │   │   ├── structure_setting.py        # Bulk SSA creation
│       │   │   └── tds_printer.py              # Annual statement PDF
│       │   └── mixins/
│       │       ├── lop.py                      # LOPMixin
│       │       ├── tax.py                      # TaxMixin
│       │       ├── benefits.py                 # BenefitsMixin
│       │       └── esic.py                     # ESICMixin
│       │
│       ├── compliance/
│       │   └── overrides/
│       │       ├── tax_declaration.py          # CustomEmployeeTaxExemptionDeclaration
│       │       ├── declaration.py
│       │       ├── exemption_proof.py
│       │       └── payroll_configuration.py
│       │
│       ├── loans/
│       │   └── overrides/
│       │       ├── loan_application.py         # hold_installments, edit_installment
│       │       ├── loan_dashboard.py
│       │       └── loan_repayment.py           # doc_events hook
│       │
│       ├── hr/
│       │   └── overrides/
│       │       ├── employee.py
│       │       └── full_and_final_settlement.py
│       │
│       ├── report/             # All 13 Frappe reports
│       ├── doctype/            # Custom doctypes
│       └── patches/            # Migration patches (v16_0/)
```

---

## Doctype overrides

| Standard Doctype | Override class | Key additions |
|---|---|---|
| `Salary Slip` | `CustomSalarySlip` | Mixin composition, LOP reversal, regime stamping |
| `Payroll Entry` | `PayrollEntryOverride` | `fill_employee_details` with SSA validation |
| `Salary Structure Assignment` | `CustomSalaryStructureAssignment` | Declaration creation on submit, CTC PDF |
| `Employee Tax Exemption Declaration` | `CustomEmployeeTaxExemptionDeclaration` | HRA auto-compute, declaration syncing |
| `Additional Salary` | `CustomAdditionalSalary` | Benefit claim linkage |

---

## Mixin composition

`CustomSalarySlip` inherits from four mixins and the base HRMS `SalarySlip`:

```python
class CustomSalarySlip(LOPMixin, TaxMixin, BenefitsMixin, ESICMixin, SalarySlip):
    ...
```

| Mixin | Responsibility |
|---|---|
| `LOPMixin` | LOP reversal days, attendance cycle working days |
| `TaxMixin` | Variable TDS, taxable earnings projection, regime-aware component flagging |
| `BenefitsMixin` | Benefit claim paid-status sync, HRA/NPS/PF declaration update |
| `ESICMixin` | ESIC contribution computation, total deduction aggregation |

---

## Custom fields approach

All custom fields are defined as Python dicts in `constants/custom_fields.py` and installed programmatically via `create_custom_fields()`. This avoids:
- Fixture JSON drift (no `custom_fields.json` that goes out of sync).
- Manual `bench migrate` after import.
- Conflicts between apps that export the same doctype's fixtures.

On `bench install-app`, the `after_install` hook installs all fields atomically.

---

## Design principles

1. **No raw SQL** — all queries use `frappe.get_all` / `frappe.qb`.
2. **No N+1 queries** — child table rows are fetched in one batch query per table, then grouped in Python.
3. **No `frappe.db.commit()` in lifecycle hooks** — the framework's transaction wraps the entire document save; manual commits break atomicity.
4. **`get_cached_doc` for lookup-only reads** — Company, Salary Component, Payroll Period.
5. **Minimal `fields=["*"]`** — only the specific fields needed are fetched.
6. **Permission guards on all `@frappe.whitelist()` endpoints** — `frappe.only_for()` or `frappe.has_permission()` on every public method.

---

## Hook registrations

```python
# hooks.py
after_install     = "cn_indian_payroll.install.after_install"
before_uninstall  = "cn_indian_payroll.uninstall.before_uninstall"

override_doctype_class = { ... }   # 5 doctype overrides

doc_events = {
    "Loan Repayment Schedule": {
        "before_save": "...",
        "before_update_after_submit": "..."
    }
}

doctype_js = { ... }               # JS extensions for 7 doctypes

fixtures = [
    "Print Format", "Income Tax Regime", "Salary Component Library Item",
    "India Payroll State", "Frequency", "Zone", "Skill Level"
]

website_route_rules = [
    {"from_route": "/tax-exemptions/<path:app_path>", "to_route": "tax-exemptions"}
]
```
