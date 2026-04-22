# Indian Payroll

> Full-stack Indian statutory payroll for ERPNext & HRMS — EPF, ESIC, Professional Tax, LWF, Income Tax (TDS), Form 16, Loans, and Full & Final Settlement.

**[Read the full documentation →](https://hybrowlabs.github.io/ERPNext-India-Payroll/)**

---

## What it does

Indian Payroll is a [Frappe](https://frappeframework.com) app that layers on top of [HRMS](https://github.com/frappe/hrms) and [ERPNext](https://erpnext.com) to provide complete Indian statutory compliance. It overrides five HRMS doctypes and adds Indian-specific computation, reports, and a tax declaration web portal — without modifying upstream code.

| Module | Coverage |
|--------|----------|
| **Salary Slip** | Attendance-aware LOP, LOP reversal, arrear, payslip PDF |
| **EPF / EPS / EDLI** | Contribution calculation, EPS Sep-2014 cut-off, ECR challan download |
| **ESIC** | Employee (0.75%) and employer (3.25%) contributions |
| **Professional Tax** | State-wise slab deduction |
| **LWF** | State-wise Labour Welfare Fund (monthly / half-yearly / annual) |
| **Income Tax (TDS)** | New Regime & Old Regime, 87A rebate, surcharge, cess, marginal relief |
| **Tax Declaration** | Self-service web form, HRA auto-calc, proof verification |
| **Form 16** | Month-wise annual statement, Part B PDF |
| **Loans** | Perquisite valuation, installment hold/extend/distribute |
| **Full & Final** | Gratuity, leave encashment, notice recovery |

---

## Requirements

| Dependency | Version |
|------------|---------|
| Python | ≥ 3.14 |
| Node.js | ≥ 24 |
| Frappe | v16 |
| ERPNext | v16 |
| HRMS | v16 |
| Lending | v16 |

---

## Quick Install

```bash
# 1. Get dependencies
bench get-app lending https://github.com/frappe/lending
bench get-app cn_indian_payroll https://github.com/hybrowlabs/ERPNext-India-Payroll

# 2. Install on your site
bench --site <your-site> install-app lending
bench --site <your-site> install-app cn_indian_payroll
```

`install-app` automatically creates all custom fields and the Payroll Manager role — no manual fixture import needed.

---

## Documentation

The full user manual is at:

**https://hybrowlabs.github.io/ERPNext-India-Payroll/**

Sections:
- [Installation](https://hybrowlabs.github.io/ERPNext-India-Payroll/installation)
- [Initial Configuration](https://hybrowlabs.github.io/ERPNext-India-Payroll/configuration)
- [Payroll Processing](https://hybrowlabs.github.io/ERPNext-India-Payroll/payroll/processing)
- [EPF / EPS / EDLI](https://hybrowlabs.github.io/ERPNext-India-Payroll/compliance/epf)
- [ESIC](https://hybrowlabs.github.io/ERPNext-India-Payroll/compliance/esic)
- [Income Tax (TDS)](https://hybrowlabs.github.io/ERPNext-India-Payroll/compliance/tds)
- [Tax Declaration](https://hybrowlabs.github.io/ERPNext-India-Payroll/compliance/tax-declaration)
- [Reports](https://hybrowlabs.github.io/ERPNext-India-Payroll/reports/overview)
- [API Reference](https://hybrowlabs.github.io/ERPNext-India-Payroll/reference/api)

---

## Architecture

```
cn_indian_payroll/
├── payroll/
│   ├── overrides/    # CustomSalarySlip, PayrollEntryOverride, SSA, etc.
│   └── mixins/       # LOPMixin, TaxMixin, BenefitsMixin, ESICMixin
├── compliance/
│   └── overrides/    # Tax declaration, exemption proof, payroll config
├── loans/
│   └── overrides/    # Loan installment management, perquisite valuation
├── hr/
│   └── overrides/    # Employee, Full & Final Settlement
├── report/           # 13 statutory and management reports
├── doctype/          # Custom doctypes (India Payroll State, Form 16, etc.)
└── patches/v16_0/    # Versioned migration patches
```

Design principles: no raw SQL, no N+1 queries, no `frappe.db.commit()` in lifecycle hooks, permission guards on all whitelisted endpoints. See the [Architecture reference](https://hybrowlabs.github.io/ERPNext-India-Payroll/reference/architecture) for details.

---

## Uninstall

```bash
bench --site <your-site> remove-app cn_indian_payroll
```

The `before_uninstall` hook removes all custom fields added by this app. Standard doctypes are restored to their upstream state.

---

## Branch strategy

| Branch | Purpose |
|--------|---------|
| `version-16` | Stable production releases |
| `refactor/**` | Structural / non-functional changes |
| `feat/**` | New features |
| `fix/**` | Bug fixes |

---

## License

MIT — see [LICENSE](./LICENSE).
