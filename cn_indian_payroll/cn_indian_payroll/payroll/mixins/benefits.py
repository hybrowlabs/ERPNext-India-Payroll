"""
Employee benefit claim and tax-exemption declaration mixin.

Handles syncing benefit-claim paid status back to the source doc,
and updating the declaration amounts (Basic, HRA, NPS, PF, PT)
whenever a salary slip is saved.
"""

import json
from datetime import timedelta

import frappe


class BenefitsMixin:
    def update_benefit_claim_amount(self) -> None:
        if not self.earnings:
            return

        for earning in self.earnings:
            additional_salary_name = earning.get("additional_salary")
            if not additional_salary_name:
                continue

            row = frappe.get_value(
                "Additional Salary",
                additional_salary_name,
                ["ref_doctype", "ref_docname"],
            )
            if not row:
                frappe.log_error(
                    f"Additional Salary '{additional_salary_name}' not found.",
                    "update_benefit_claim_amount",
                )
                continue

            ref_doctype, ref_docname = row
            if ref_doctype == "Employee Benefit Claim" and ref_docname:
                try:
                    benefit_claim = frappe.get_doc("Employee Benefit Claim", ref_docname)
                    benefit_claim.custom_is_paid = 1
                    benefit_claim.custom_paid_amount = earning.amount
                    benefit_claim.save(ignore_permissions=True)
                except frappe.DoesNotExistError:
                    frappe.log_error(
                        f"Employee Benefit Claim '{ref_docname}' not found.",
                        "update_benefit_claim_amount",
                    )

    def update_declaration_component(self) -> None:
        if not self.employee:
            return

        current_basic = current_hra = None
        (
            current_basic_value,
            current_hra_value,
            current_nps_value,
            current_epf_value,
            current_pt_value,
        ) = 0, 0, 0, 0, 0
        (
            previous_basic_value,
            previous_hra_value,
            previous_nps_value,
            previous_epf_value,
            previous_pt_value,
        ) = 0, 0, 0, 0, 0
        (
            future_basic_value,
            future_hra_value,
            future_nps_value,
            future_epf_value,
            future_pt_value,
        ) = 0, 0, 0, 0, 0

        company_doc = frappe.get_doc("Company", self.company)
        current_basic = company_doc.basic_component
        current_hra = company_doc.hra_component

        for earning in self.earnings or []:
            sc = frappe.get_cached_doc("Salary Component", earning.salary_component)
            if sc.component_type == "NPS":
                current_nps_value += earning.amount or 0
                if sc.custom_component_sub_type == "Fixed":
                    future_nps_value = (earning.default_amount or 0) * self.custom_month_count

            if earning.salary_component == current_basic:
                current_basic_value += earning.amount
                if sc.custom_component_sub_type == "Fixed":
                    future_basic_value = (earning.default_amount or 0) * self.custom_month_count

            if earning.salary_component == current_hra:
                current_hra_value += earning.amount
                if sc.custom_component_sub_type == "Fixed":
                    future_hra_value = (earning.default_amount or 0) * self.custom_month_count

        for deduction in self.deductions or []:
            sc = frappe.get_cached_doc("Salary Component", deduction.salary_component)
            if sc.component_type == "Provident Fund":
                current_epf_value += deduction.amount
                if sc.custom_component_sub_type == "Fixed":
                    future_epf_value = (deduction.default_amount or 0) * self.custom_month_count
            if sc.component_type == "Professional Tax":
                current_pt_value += deduction.amount
                if sc.custom_component_sub_type == "Fixed":
                    future_pt_value = (deduction.default_amount or 0) * self.custom_month_count

        prev_slips = frappe.get_list(
            "Salary Slip",
            filters={
                "employee": self.employee,
                "custom_payroll_period": self.custom_payroll_period,
                "docstatus": 1,
                "name": ["!=", self.name],
            },
            fields=["name"],
        )

        for slip_meta in prev_slips:
            prev_slip = frappe.get_doc("Salary Slip", slip_meta.name)
            for earning in prev_slip.earnings or []:
                sc = frappe.get_cached_doc("Salary Component", earning.salary_component)
                if sc.component_type == "NPS":
                    previous_nps_value += earning.amount
                if earning.salary_component == current_basic:
                    previous_basic_value += earning.amount
                if earning.salary_component == current_hra:
                    previous_hra_value += earning.amount

            for deduction in prev_slip.deductions or []:
                sc = frappe.get_cached_doc("Salary Component", deduction.salary_component)
                if sc.component_type == "Provident Fund":
                    previous_epf_value += deduction.amount
                if sc.component_type == "Professional Tax":
                    previous_pt_value += deduction.amount

        declaration_list = frappe.get_list(
            "Employee Tax Exemption Declaration",
            filters={
                "employee": self.employee,
                "payroll_period": self.custom_payroll_period,
                "docstatus": 1,
                "company": self.company,
            },
            fields=["*"],
        )
        if not declaration_list:
            return

        decl_doc = frappe.get_doc("Employee Tax Exemption Declaration", declaration_list[0].name)
        form_data = json.loads(declaration_list[0].custom_declaration_form_data or "[]")

        total_nps = round(previous_nps_value + future_nps_value + current_nps_value)
        total_pf = min(round(previous_epf_value + future_epf_value + current_epf_value), 150_000)
        total_pt = round(previous_pt_value + future_pt_value + current_pt_value)

        component_type_map = {"NPS": total_nps, "Provident Fund": total_pf, "Professional Tax": total_pt}

        for subcategory in decl_doc.declarations:
            sub_cat_doc = frappe.get_cached_doc(
                "Employee Tax Exemption Sub Category", subcategory.exemption_sub_category
            )
            if sub_cat_doc.custom_component_type in component_type_map:
                if self.custom_tax_regime == "New Regime" and sub_cat_doc.custom_component_type != "NPS":
                    continue
                subcategory.amount = component_type_map[sub_cat_doc.custom_component_type]

        for entry in form_data:
            subcat_name = entry.get("sub_category") or entry.get("id")
            component = frappe.get_all(
                "Employee Tax Exemption Sub Category",
                filters={"name": subcat_name},
                fields=["custom_component_type"],
                limit=1,
            )
            if not component:
                continue
            ctype = component[0].custom_component_type
            if ctype not in component_type_map:
                continue
            if self.custom_tax_regime == "New Regime" and ctype != "NPS":
                continue
            val = component_type_map[ctype]
            entry["amount"] = val
            entry["value"] = val

        decl_doc.custom_posting_date = self.posting_date
        decl_doc.custom_declaration_form_data = json.dumps(form_data)

        if self.custom_tax_regime == "Old Regime" and decl_doc.monthly_house_rent > 0:
            self._compute_hra_exemption(
                decl_doc,
                previous_basic_value,
                current_basic_value,
                future_basic_value,
                previous_hra_value,
                current_hra_value,
                future_hra_value,
            )

        decl_doc.custom_status = "Approved"
        decl_doc.save()
        frappe.db.commit()
        self.tax_exemption_declaration = decl_doc.total_exemption_amount

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _compute_hra_exemption(
        self,
        decl_doc,
        prev_basic,
        curr_basic,
        fut_basic,
        prev_hra,
        curr_hra,
        fut_hra,
    ) -> None:
        ss_assignments = frappe.get_list(
            "Salary Structure Assignment",
            filters={
                "employee": self.employee,
                "docstatus": 1,
                "company": self.company,
                "custom_payroll_period": self.custom_payroll_period,
                "from_date": ("<=", self.end_date),
            },
            fields=["name", "from_date", "custom_payroll_period", "salary_structure"],
            order_by="from_date desc",
        )
        if not ss_assignments:
            return

        last_assignment = ss_assignments[-1]
        start_date = last_assignment.from_date
        if not last_assignment.custom_payroll_period:
            return

        payroll_period = frappe.get_doc("Payroll Period", last_assignment.custom_payroll_period)
        end_date = payroll_period.end_date
        month_count = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1

        total_basic = round(prev_basic + fut_basic + curr_basic)
        total_hra = round(prev_hra + fut_hra + curr_hra)
        annual_hra = decl_doc.monthly_house_rent * month_count
        basic_10_pct = total_basic * 10 / 100

        rule2 = round(annual_hra - basic_10_pct)
        metro_pct = 50 if decl_doc.rented_in_metro_city else 40
        metro_hra = total_basic * metro_pct / 100

        final_hra_exemption = round(min(rule2, annual_hra, metro_hra))

        decl_doc.custom_check = 1
        decl_doc.custom_basic_as_per_salary_structure = round(basic_10_pct)
        decl_doc.salary_structure_hra = total_hra
        decl_doc.custom_basic = total_basic
        decl_doc.annual_hra_exemption = final_hra_exemption
        decl_doc.monthly_hra_exemption = round(final_hra_exemption / month_count)

        months = []
        current_date = start_date
        while current_date <= end_date:
            month_name = current_date.strftime("%B")
            if month_name not in months:
                months.append(month_name)
            current_date = (current_date.replace(day=28) + timedelta(days=4)).replace(day=1)

        earned_basic = (basic_10_pct * 10) * metro_pct / 100

        decl_doc.custom_hra_breakup = []
        for month in months:
            decl_doc.append(
                "custom_hra_breakup",
                {
                    "month": month,
                    "rent_paid": round(annual_hra),
                    "hra_received": round(total_hra),
                    "earned_basic": round(earned_basic),
                    "excess_of_rent_paid": round(rule2),
                    "exemption_amount": final_hra_exemption,
                },
            )
