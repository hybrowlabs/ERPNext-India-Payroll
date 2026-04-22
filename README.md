# Chatnext India Payroll

A Frappe/HRMS app that extends ERPNext payroll for Indian statutory compliance — EPF, EPS, ESIC, Professional Tax, LWF, TDS, and Form 16.

---

## Requirements

| Dependency | Version |
|------------|---------|
| Frappe     | v16     |
| ERPNext    | v16     |
| HRMS       | v16     |

---

## Installation

```bash
bench get-app cn_indian_payroll https://github.com/hybrowlabs/ERPNext-India-Payroll
bench --site <your-site> install-app cn_indian_payroll
```

`install-app` automatically creates all custom fields via the `after_install` hook — no manual fixture import required.

---

## App Structure

```
cn_indian_payroll/
├── constants/
│   ├── __init__.py          # EPF, ESIC, tax, LWF, PT, payroll constants
│   └── custom_fields.py     # All custom field definitions as Python dicts
│
├── utils/
│   └── custom_fields.py     # create / delete / toggle helpers
│
├── exceptions.py            # App-level exceptions (IndianPayrollError, TaxCalculationError …)
├── install.py               # after_install  → creates custom fields
├── uninstall.py             # before_uninstall → removes custom fields
├── setup.py                 # Shared lifecycle logic called by install/uninstall
│
├── payroll/
│   ├── overrides/
│   │   ├── salary_slip.py               # CustomSalarySlip (composes mixins)
│   │   ├── payroll_entry.py
│   │   ├── salary_structure_assignment.py
│   │   ├── additional_salary.py
│   │   ├── salary_component.py
│   │   ├── structure_setting.py
│   │   ├── tds_printer.py
│   │   └── tds_projection_calculation.py
│   └── mixins/
│       ├── lop.py           # LOP reversal, attendance-cycle working days
│       ├── tax.py           # Variable tax, income-tax breakup, regime-aware earnings
│       ├── benefits.py      # Benefit claims, HRA/NPS/PF declaration sync
│       └── esic.py          # ESIC and total-deduction helpers
│
├── compliance/
│   └── overrides/
│       ├── tax_declaration.py
│       ├── declaration.py
│       ├── exemption_proof.py
│       ├── exemption_sub_category.py
│       └── payroll_configuration.py
│
├── loans/
│   └── overrides/
│       ├── loan_application.py
│       ├── loan_dashboard.py
│       └── loan_repayment.py
│
├── hr/
│   └── overrides/
│       ├── employee.py
│       └── full_and_final_settlement.py
│
└── patches/
    └── v16_0/               # Version-namespaced migration patches
        ├── income_tax_slab.py
        ├── salary_component.py
        ├── category.py
        └── sub_category.py
```

---

## Design Principles

- **No Customize Form** — all custom fields are defined as Python dicts in `constants/custom_fields.py` and installed programmatically on `bench install-app`. This avoids fixture JSON drift and keeps the field manifest version-controlled and reviewable as code.
- **Domain packages** — overrides are split into `payroll/`, `compliance/`, `loans/`, and `hr/` packages instead of a single flat `overrides/` directory.
- **Mixin decomposition** — `CustomSalarySlip` is composed from four focused mixins (`LOPMixin`, `TaxMixin`, `BenefitsMixin`, `ESICMixin`), each independently testable.
- **Frappe ORM** — queries use `frappe.qb` (Query Builder) for N+1-free bulk fetches; no raw SQL strings.
- **Versioned patches** — migration patches live under `patches/v16_0/` following the HRMS pattern.

---

## Uninstallation

```bash
bench --site <your-site> remove-app cn_indian_payroll
```

`remove-app` runs the `before_uninstall` hook which cleans up all custom fields owned by this app.

---

## Statutory Coverage

| Module | Coverage |
|--------|----------|
| EPF / EPS / EDLI | Contribution calculation, ECR challan report |
| ESIC | Applicability check, contribution deduction |
| Professional Tax | State-wise slab deduction |
| Labour Welfare Fund | State-wise applicability |
| Income Tax (TDS) | New Regime & Old Regime slabs, rebate u/s 87A, surcharge, cess, Form 16 |
| Loans | Perquisite valuation, repayment schedule |
| F&F Settlement | Final settlement computation |

---

## Branch Strategy

| Branch | Purpose |
|--------|---------|
| `version-16` | Stable production releases |
| `v2/dev/**`  | Active development |
| `refactor/**` | Structural / non-functional changes |
| `feat/**`    | New features |
| `fix/**`     | Bug fixes |

SonarQube scans run on every push to all of the above branches and on all pull requests targeting `main` or `version-16`.
