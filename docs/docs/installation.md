---
id: installation
title: Installation
sidebar_position: 2
description: Install Indian Payroll on a Frappe v16 bench.
---

# Installation

## Prerequisites

Before installing, ensure your bench has all required apps:

| Requirement | Minimum version |
|---|---|
| Python | 3.14 |
| Node.js | 24 |
| Frappe | v16 |
| ERPNext | v16 |
| HRMS | v16 |
| Lending | v16 |

:::info
Frappe v16.16.0+ requires Python ≥ 3.14. Use `python3 --version` to verify.
:::

---

## Step-by-step install

### 1. Get the app

```bash
bench get-app cn_indian_payroll https://github.com/hybrowlabs/ERPNext-India-Payroll
```

This clones the app into `apps/cn_indian_payroll` and installs its Python dependencies.

### 2. Install the Lending dependency

```bash
bench get-app lending https://github.com/frappe/lending
bench --site <your-site> install-app lending
```

Loan perquisite valuation relies on the Lending module's `Loan` and `Loan Repayment Schedule` doctypes.

### 3. Install Indian Payroll

```bash
bench --site <your-site> install-app cn_indian_payroll
```

The `after_install` hook runs automatically and:
- Creates the **Payroll Manager** role (idempotent — safe to re-run).
- Installs all **custom fields** across `Salary Slip`, `Employee`, `Company`, `Salary Structure Assignment`, and other standard doctypes.

No manual fixture import or database migration is needed.

---

## Verify the install

```bash
bench --site <your-site> list-apps
```

Expected output includes `cn_indian_payroll`.

Then open the site in your browser, navigate to **HR → Salary Slip**, and confirm the new fields (Month, Payroll Period, Annual CTC, etc.) are visible.

---

## Uninstall

```bash
bench --site <your-site> remove-app cn_indian_payroll
```

The `before_uninstall` hook automatically removes all custom fields added by this app. Standard doctypes are restored to their upstream state.

---

## Upgrade

```bash
cd apps/cn_indian_payroll
git pull
cd ../..
bench --site <your-site> migrate
```

Any schema changes in new releases are handled via version-namespaced migration patches in `cn_indian_payroll/patches/`.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: cn_indian_payroll` | Run `bench build` and restart workers. |
| Custom fields missing after install | Run `bench --site <site> migrate` to re-apply patches. |
| `Could not find DocType: Loan` | Install the `lending` app first. |
| Permission errors on install | Ensure bench user owns the `apps/` directory. |
