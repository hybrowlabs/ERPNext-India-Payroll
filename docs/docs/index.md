---
id: index
slug: /
title: Introduction
sidebar_position: 1
description: Indian Payroll — full-stack statutory payroll extension for ERPNext and HRMS.
---

# Indian Payroll

**Indian Payroll** is a [Frappe](https://frappeframework.com) app that extends [ERPNext](https://erpnext.com) and [HRMS](https://github.com/frappe/hrms) with complete Indian statutory payroll compliance — EPF, ESIC, Professional Tax, LWF, TDS under both regimes, Form 16, and more.

It does **not** replace HRMS. It layers on top of it — overriding specific doctypes, adding Indian-specific fields, computations, and statutory reports without touching the upstream schema.

---

## What it covers

<div class="feature-grid">
  <div class="feature-card">
    <div class="feature-card__icon">🧾</div>
    <div class="feature-card__title">Salary Slip</div>
    <div class="feature-card__desc">Attendance-aware LOP, LOP reversal, arrear calculation, payslip PDF with full breakup.</div>
  </div>
  <div class="feature-card">
    <div class="feature-card__icon">🏛️</div>
    <div class="feature-card__title">EPF / EPS / EDLI</div>
    <div class="feature-card__desc">Contribution calculation, EPS eligibility cut-off (Sep 2014), ECR challan download.</div>
  </div>
  <div class="feature-card">
    <div class="feature-card__icon">🏥</div>
    <div class="feature-card__title">ESIC</div>
    <div class="feature-card__desc">Gross-wage eligibility check, employee (0.75%) and employer (3.25%) contributions.</div>
  </div>
  <div class="feature-card">
    <div class="feature-card__icon">📋</div>
    <div class="feature-card__title">Professional Tax</div>
    <div class="feature-card__desc">State-wise slab deduction with LWF (Labour Welfare Fund) frequency support.</div>
  </div>
  <div class="feature-card">
    <div class="feature-card__icon">💰</div>
    <div class="feature-card__title">Income Tax (TDS)</div>
    <div class="feature-card__desc">New and Old Regime slabs, rebate u/s 87A, surcharge, 4% cess, marginal relief.</div>
  </div>
  <div class="feature-card">
    <div class="feature-card__icon">📄</div>
    <div class="feature-card__title">Form 16 & Annual Statement</div>
    <div class="feature-card__desc">Month-wise tax breakup, HRA exemption, declaration history, annual statement PDF.</div>
  </div>
  <div class="feature-card">
    <div class="feature-card__icon">🏦</div>
    <div class="feature-card__title">Loans</div>
    <div class="feature-card__desc">Perquisite valuation on interest-free / concessional loans, installment management.</div>
  </div>
  <div class="feature-card">
    <div class="feature-card__icon">🤝</div>
    <div class="feature-card__title">Full & Final Settlement</div>
    <div class="feature-card__desc">Gratuity, leave encashment, and notice-period recovery computation on exit.</div>
  </div>
</div>

---

## How it fits into the stack

```
┌──────────────────────────────────────────────────────┐
│                  Your ERPNext Site                   │
├──────────────────────────────────────────────────────┤
│  cn_indian_payroll  ← this app                       │
│  ┌──────────────┐  ┌───────────┐  ┌───────────────┐  │
│  │  Payroll     │  │Compliance │  │  Loans / HR   │  │
│  │  overrides   │  │overrides  │  │  overrides    │  │
│  └──────┬───────┘  └─────┬─────┘  └──────┬────────┘  │
├─────────┼────────────────┼───────────────┼────────────┤
│  HRMS   │  Salary Slip   │  Tax Decl.    │  Loan      │
│         │  Payroll Entry │  Exemption    │  Employee  │
├─────────┼────────────────┼───────────────┼────────────┤
│ ERPNext │  Company       │  Accounts     │  Assets    │
├─────────┼────────────────┼───────────────┼────────────┤
│ Frappe  │  Framework / ORM / Auth / Queue / Scheduler │
└──────────────────────────────────────────────────────┘
```

The app overrides five HRMS/ERPNext doctypes and adds one `doc_events` hook for loan repayment — everything else is additive (new doctypes, reports, custom fields).

---

## Required apps

| App | Version |
|-----|---------|
| Frappe | v16 |
| ERPNext | v16 |
| HRMS | v16 |
| Lending | v16 |

---

## Next steps

- [Install the app →](/installation)
- [Configure your first site →](/configuration)
- [Run your first payroll →](/payroll/processing)
