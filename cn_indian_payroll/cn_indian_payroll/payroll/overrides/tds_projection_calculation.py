import json

import frappe
from frappe.utils import cstr, flt, getdate
from hrms.payroll.doctype.salary_slip.salary_slip import eval_tax_slab_condition
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip


@frappe.whitelist()
def calculate_tds_projection(doc):

    if isinstance(doc, str):
        doc = frappe._dict(json.loads(doc))

        if not doc.get("employee"):
            frappe.throw(frappe._("Employee is required to calculate TDS projection."))

        if not frappe.has_permission("Employee", "read", doc.get("employee")):
            frappe.throw(frappe._("Not permitted to access this employee's data."), frappe.PermissionError)

        current_taxable_earnings_old_regime = 0
        current_taxable_earnings_new_regime = 0
        future_taxable_earnings_old_regime = 0
        future_taxable_earnings_new_regime = 0

        tds_from_previous_employer = 0
        loan_perquisite_amount = 0

        pt_amount = 0
        pf_amount = 0
        nps_amount = 0

        old_regime_standard_value = 0
        new_regime_standard_value = 0

        hra_exemptions = 0

        old_regime_annual_taxable_income = 0
        new_regime_annual_taxable_income = 0

        num_months = 0
        slip_count = 0
        pf_max_amount = 0

        new_tax_slab = None
        old_tax_slab = None

        paid_tax = 0

        salary_assignment = frappe.get_list(
            "Salary Structure Assignment",
            filters={
                "employee": doc.employee,
                "docstatus": 1,
                "custom_payroll_period": doc.get("payroll_period"),
                "company": doc.get("company"),
            },
            fields=["name"],
            order_by="from_date asc",
            limit=1,
        )

        if not salary_assignment:
            frappe.throw(frappe._("No active Salary Structure Assignment found."))

        assignment = frappe.get_doc("Salary Structure Assignment", salary_assignment[0].name)

        employee = frappe.get_doc("Employee", assignment.employee)
        payroll_period = frappe.get_doc("Payroll Period", assignment.custom_payroll_period)

        effective_start_date = getdate(assignment.from_date)
        payroll_start_date = getdate(payroll_period.start_date)
        payroll_end_date = getdate(payroll_period.end_date)
        date_of_joining = getdate(employee.date_of_joining)

        tds_from_previous_employer = assignment.taxable_earnings_till_date or 0
        already_paid_previous_employer = assignment.tax_deducted_till_date or 0

        start_date = max(filter(None, [effective_start_date, payroll_start_date, date_of_joining]))

        num_months = (
            (payroll_end_date.year - start_date.year) * 12 + (payroll_end_date.month - start_date.month) + 1
        )

        loan_repayments = frappe.get_all(
            "Loan Repayment Schedule",
            filters={
                "custom_employee": doc.employee,
                "status": "Active",
                "docstatus": 1,
            },
            fields=["name"],
        )

        for repayment in loan_repayments:
            repayment_doc = frappe.get_doc("Loan Repayment Schedule", repayment.name)

            for perquisite in repayment_doc.custom_loan_perquisite or []:
                payment_date = getdate(perquisite.payment_date)

                if payroll_start_date <= payment_date <= payroll_end_date:
                    loan_perquisite_amount += perquisite.perquisite_amount or 0

        salary_slips = frappe.get_all(
            "Salary Slip",
            filters={
                "employee": doc.employee,
                "custom_payroll_period": doc.payroll_period,
                "docstatus": ["in", [0, 1]],
            },
            fields=["name", "custom_month_count", "current_month_income_tax"],
            order_by="end_date desc",
        )

        if not salary_slips:
            salary_slip_preview = make_salary_slip(
                source_name=assignment.salary_structure,
                employee=doc.employee,
                print_format="Salary Slip Standard",
                posting_date=assignment.from_date,
                for_preview=1,
            )

            if salary_slip_preview:
                for earning in salary_slip_preview.earnings:
                    component = frappe.get_cached_doc("Salary Component", earning.salary_component)

                    if not (
                        component.is_tax_applicable
                        and component.custom_tax_exemption_applicable_based_on_regime
                        and component.custom_component_sub_type == "Fixed"
                    ):
                        continue

                    if component.custom_regime in ["All", "Old Regime"]:
                        future_taxable_earnings_old_regime += earning.amount * num_months

                    if component.custom_regime in ["All", "New Regime"]:
                        future_taxable_earnings_new_regime += earning.amount * num_months

                    if component.custom_regime in ["All", "Old Regime"] and component.component_type == "NPS":
                        nps_amount += earning.amount * (num_months)

                for deduction in salary_slip_preview.deductions:
                    component = frappe.get_cached_doc("Salary Component", deduction.salary_component)

                    if component.custom_component_sub_type != "Fixed":
                        continue

                    if component.component_type == "Professional Tax":
                        pt_amount += deduction.amount * num_months

                    elif component.component_type == "Provident Fund":
                        pf_amount += deduction.amount * num_months

        else:
            slip_count = salary_slips[0].custom_month_count or 0

            for slip in salary_slips:
                salary_slip = frappe.get_doc("Salary Slip", slip.name)

                paid_tax += salary_slip.current_month_income_tax

                for earning in salary_slip.earnings:
                    component = frappe.get_cached_doc("Salary Component", earning.salary_component)

                    if not (
                        component.is_tax_applicable
                        and component.custom_tax_exemption_applicable_based_on_regime
                    ):
                        continue

                    if component.custom_regime in ["All", "Old Regime"]:
                        current_taxable_earnings_old_regime += earning.amount

                    if component.custom_regime in ["All", "New Regime"]:
                        current_taxable_earnings_new_regime += earning.amount

                    if component.custom_regime == "All" and component.component_type == "NPS":
                        nps_amount += earning.amount

                # Deductions
                for deduction in salary_slip.deductions:
                    component = frappe.get_cached_doc("Salary Component", deduction.salary_component)

                    if component.component_type == "Professional Tax":
                        pt_amount += deduction.amount

                    elif component.component_type == "Provident Fund":
                        pf_amount += deduction.amount

            salary_slip_preview = make_salary_slip(
                source_name=assignment.salary_structure,
                employee=doc.employee,
                print_format="Salary Slip Standard",
                posting_date=assignment.from_date,
                for_preview=1,
            )

            if salary_slip_preview:
                for earning in salary_slip_preview.earnings:
                    if earning.additional_salary:
                        continue

                    component = frappe.get_cached_doc("Salary Component", earning.salary_component)

                    if not (
                        component.is_tax_applicable
                        and component.custom_tax_exemption_applicable_based_on_regime
                        and component.custom_component_sub_type == "Fixed"
                    ):
                        continue

                    if component.custom_regime in ["All", "Old Regime"]:
                        future_taxable_earnings_old_regime += earning.amount * slip_count

                    if component.custom_regime in ["All", "New Regime"]:
                        future_taxable_earnings_new_regime += earning.amount * slip_count

                    if component.custom_regime == "All" and component.component_type == "NPS":
                        nps_amount += earning.amount * slip_count

                for deduction in salary_slip_preview.deductions:
                    if deduction.additional_salary:
                        continue

                    component = frappe.get_cached_doc("Salary Component", deduction.salary_component)

                    if component.custom_component_sub_type != "Fixed":
                        continue

                    if component.component_type == "Professional Tax":
                        pt_amount += deduction.amount * slip_count

                    elif component.component_type == "Provident Fund":
                        pf_amount += deduction.amount * slip_count

        total_annual_taxable_earning_old_regime = round(
            current_taxable_earnings_old_regime
            + future_taxable_earnings_old_regime
            + loan_perquisite_amount
            + tds_from_previous_employer
        )
        total_annual_taxable_earning_new_regime = round(
            current_taxable_earnings_new_regime
            + future_taxable_earnings_new_regime
            + loan_perquisite_amount
            + tds_from_previous_employer
        )

        latest_tax_slab_old_regime = frappe.get_list(
            "Income Tax Slab",
            filters={
                "company": doc.get("company"),
                "docstatus": 1,
                "disabled": 0,
                "custom_select_regime": "Old Regime",
            },
            fields=["name", "custom_select_regime", "standard_tax_exemption_amount"],
            order_by="effective_from DESC",
            limit=1,
        )

        if latest_tax_slab_old_regime:
            old_regime_standard_value = latest_tax_slab_old_regime[0].standard_tax_exemption_amount
            old_tax_slab = latest_tax_slab_old_regime[0].name

        latest_tax_slab_new_regime = frappe.get_list(
            "Income Tax Slab",
            filters={
                "company": doc.get("company"),
                "docstatus": 1,
                "disabled": 0,
                "custom_select_regime": "New Regime",
            },
            fields=["name", "custom_select_regime", "standard_tax_exemption_amount"],
            order_by="effective_from DESC",
            limit=1,
        )

        if latest_tax_slab_new_regime:
            new_regime_standard_value = latest_tax_slab_new_regime[0].standard_tax_exemption_amount
            new_tax_slab = latest_tax_slab_new_regime[0].name

        if doc.get("custom_tax_regime") == "Old Regime" and doc.get("monthly_house_rent"):
            hra_exemptions = doc.get("annual_hra_exemption")

        selected_regime = doc.get("custom_tax_regime")

        get_exemption_sub_category = frappe.get_list(
            "Employee Tax Exemption Sub Category",
            filters={
                "custom_component_type": "Provident Fund",
                "is_active": 1,
            },
            fields=["name", "max_amount"],
        )
        if get_exemption_sub_category:
            eighty_c_maximum_limit = get_exemption_sub_category[0].max_amount

        pf_max_amount = min(eighty_c_maximum_limit, pf_amount)

        if doc.get("custom_tax_regime") == "Old Regime":
            total_new_regime_deductions = nps_amount
            total_old_regime_deductions = (doc.get("total_exemption_amount") - (pt_amount)) + hra_exemptions
        if doc.get("custom_tax_regime") == "New Regime":
            total_new_regime_deductions = doc.get("total_exemption_amount")
            total_old_regime_deductions = pf_max_amount + pt_amount + nps_amount

        old_regime_annual_taxable_income = max(
            round(total_annual_taxable_earning_old_regime)
            - round(pt_amount)
            - old_regime_standard_value
            - hra_exemptions
            - round(total_old_regime_deductions),
            0,
        )

        new_regime_annual_taxable_income = max(
            round(total_annual_taxable_earning_new_regime)
            - new_regime_standard_value
            - round(total_new_regime_deductions),
            0,
        )

        eval_globals = frappe._dict()
        eval_locals = frappe._dict()

        old_tax_slab_doc = frappe.get_doc("Income Tax Slab", old_tax_slab)

        old_slab_result = calculate_tax_by_tax_slab(
            old_regime_annual_taxable_income,
            old_tax_slab_doc,
            eval_globals,
            eval_locals,
        )

        new_tax_slab_doc = frappe.get_doc("Income Tax Slab", new_tax_slab)

        new_slab_result = calculate_tax_by_tax_slab(
            new_regime_annual_taxable_income,
            new_tax_slab_doc,
            eval_globals,
            eval_locals,
        )

        return {
            "tds_from_previous_employer": round(tds_from_previous_employer),
            "future_taxable_earnings_old_regime": round(future_taxable_earnings_old_regime),
            "future_taxable_earnings_new_regime": round(future_taxable_earnings_new_regime),
            "current_taxable_earnings_old_regime": round(current_taxable_earnings_old_regime),
            "current_taxable_earnings_new_regime": round(current_taxable_earnings_new_regime),
            "loan_perquisite_amount": round(loan_perquisite_amount),
            "total_annual_taxable_earning_old_regime": (total_annual_taxable_earning_old_regime),
            "total_annual_taxable_earning_new_regime": (total_annual_taxable_earning_new_regime),
            "pt_amount": round(pt_amount),
            "old_regime_standard_value": old_regime_standard_value,
            "new_regime_standard_value": new_regime_standard_value,
            "nps_amount": round(nps_amount),
            "hra_exemptions": hra_exemptions,
            "total_old_regime_deductions": round(total_old_regime_deductions),
            "total_new_regime_deductions": round(total_new_regime_deductions),
            "old_regime_annual_taxable_income": round(old_regime_annual_taxable_income),
            "new_regime_annual_taxable_income": round(new_regime_annual_taxable_income),
            "new_regime_total_tax_on_income": round(new_slab_result.get("base_tax")),
            "new_regime_surcharge": round(new_slab_result.get("surcharge")),
            "new_regime_education_cess": round(new_slab_result.get("education_cess_amount")),
            "new_regime_total_tax_payable": round(new_slab_result.get("total_tax_payable")),
            "old_regime_total_tax_on_income": round(old_slab_result.get("base_tax")),
            "old_regime_surcharge": round(old_slab_result.get("surcharge")),
            "old_regime_education_cess": round(old_slab_result.get("education_cess_amount")),
            "old_regime_total_tax_payable": round(old_slab_result.get("total_tax_payable")),
            "already_paid_previous_employer": round(already_paid_previous_employer),
            "old_regime_balance_tds_payable": old_slab_result.get("total_tax_payable")
            - already_paid_previous_employer,
            "new_regime_balance_tds_payable": new_slab_result.get("total_tax_payable")
            - already_paid_previous_employer,
            "paid_tax": round(paid_tax),
            "old_regime_current_month_tax": round(
                (old_slab_result.get("total_tax_payable", 0) - already_paid_previous_employer - paid_tax)
                / (slip_count if slip_count else num_months)
            ),
            "new_regime_current_month_tax": round(
                (new_slab_result.get("total_tax_payable", 0) - already_paid_previous_employer - paid_tax)
                / (slip_count if slip_count else num_months)
            ),
            "selected_regime": selected_regime,
        }


def calculate_tax_by_tax_slab(
    annual_taxable_earning,
    tax_slab,
    eval_globals=None,
    eval_locals=None,
):
    eval_globals = eval_globals or {}
    eval_locals = eval_locals or {}

    if isinstance(tax_slab, str):
        tax_slab = frappe.get_doc("Income Tax Slab", tax_slab)

    eval_locals.update(
        {
            "annual_taxable_earning": annual_taxable_earning,
            "annual_taxable_amount": annual_taxable_earning,
        }
    )

    base_tax = 0
    rebate = 0
    surcharge = 0
    charge_percent = 0
    education_cess_amount = 0
    total_tax_payable = 0

    for slab in tax_slab.slabs:
        cond = cstr(slab.condition).strip()
        if cond and not eval_tax_slab_condition(cond, eval_globals, eval_locals):
            continue

        from_amt = slab.from_amount
        to_amt = slab.to_amount or annual_taxable_earning
        rate = slab.percent_deduction * 0.01

        if annual_taxable_earning > from_amt:
            taxable_range = min(annual_taxable_earning, to_amt) - from_amt
            base_tax += taxable_range * rate

    if (
        tax_slab.custom_marginal_relief_applicable
        and tax_slab.custom_minmum_value
        and tax_slab.custom_maximun_value
    ) and (tax_slab.custom_minmum_value < annual_taxable_earning < tax_slab.custom_maximun_value):
        excess_income = annual_taxable_earning - tax_slab.custom_minmum_value
        if base_tax > excess_income:
            base_tax = excess_income

    for d in tax_slab.other_taxes_and_charges:
        if d.custom_is_education_cess == 0:
            min_value = flt(d.min_taxable_income) or 0
            max_value = flt(d.max_taxable_income) or None

            if annual_taxable_earning >= min_value and (not max_value or annual_taxable_earning < max_value):
                charge_percent = flt(d.percent)
                surcharge = (base_tax * charge_percent) / 100.0

    for d in tax_slab.other_taxes_and_charges:
        if d.custom_is_education_cess == 1:
            total_tax_before_cess = base_tax + surcharge

            education_cess_amount = (total_tax_before_cess * flt(d.percent)) / 100.0

    total_tax_payable = round(education_cess_amount + surcharge + base_tax)

    return {
        "base_tax": round(base_tax, 2),
        "education_cess_amount": round(education_cess_amount, 2),
        "surcharge": round(surcharge, 2),
        "total_tax_payable": round(total_tax_payable, 2),
        "rebate": round(rebate, 2),
    }
