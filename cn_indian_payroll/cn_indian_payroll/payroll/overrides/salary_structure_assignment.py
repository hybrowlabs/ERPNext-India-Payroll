import json
from datetime import timedelta

import frappe
from frappe.utils import flt, getdate
from frappe.utils.pdf import get_pdf
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip
from hrms.payroll.doctype.salary_structure_assignment.salary_structure_assignment import (
    SalaryStructureAssignment,
)


class CustomSalaryStructureAssignment(SalaryStructureAssignment):
    def on_submit(self):
        self.insert_tax_declaration_list()

    def on_cancel(self):
        self.cancel_declaration()

    def cancel_declaration(self):
        declarations = frappe.get_list(
            "Employee Tax Exemption Declaration",
            filters={
                "payroll_period": self.custom_payroll_period,
                "employee": self.employee,
                "docstatus": ["in", [0, 1]],
            },
            fields=["name", "docstatus"],
        )

        for dec in declarations:
            doc = frappe.get_doc("Employee Tax Exemption Declaration", dec.name)

            if doc.docstatus == 1:
                doc.cancel()

            frappe.delete_doc(
                "Employee Tax Exemption Declaration", doc.name, force=1, ignore_permissions=True
            )

        remaining_assignments = frappe.get_all(
            "Salary Structure Assignment",
            filters={
                "employee": self.employee,
                "custom_payroll_period": self.custom_payroll_period,
                "docstatus": 1,
            },
            fields=["name"],
        )

        if remaining_assignments:
            latest_assignment = frappe.get_doc("Salary Structure Assignment", remaining_assignments[-1].name)

            latest_assignment.insert_tax_declaration_list()

        else:
            frappe.log_error(f"No active assignments for {self.employee}", "Cancel Declaration Info")

    def insert_tax_declaration_list(self):

        if not self.employee:
            return

        payroll_period = frappe.get_doc("Payroll Period", self.custom_payroll_period)
        payroll_start = getdate(payroll_period.start_date)
        payroll_end = getdate(payroll_period.end_date)

        settings = frappe.get_single("Payroll Settings")

        cycle_enabled = settings.custom_configure_attendance_cycle
        start_day = settings.custom_attendance_start_date or 1

        joining_date = getdate(self.from_date)

        if cycle_enabled:
            cutoff_date = payroll_start.replace(day=start_day)

            if joining_date > cutoff_date:
                effective_start = (joining_date.replace(day=1) + timedelta(days=32)).replace(day=1)
            else:
                effective_start = payroll_start
        else:
            effective_start = payroll_start

        total_months = (
            (payroll_end.year - effective_start.year) * 12 + (payroll_end.month - effective_start.month) + 1
        )

        salary_slips = frappe.get_all(
            "Salary Slip",
            filters={
                "employee": self.employee,
                "docstatus": 1,
                "start_date": [">=", payroll_start],
                "end_date": ["<=", payroll_end],
            },
            fields=["name"],
        )

        actual_months = len(salary_slips)

        actual_totals = {"PF": 0, "PT": 0, "NPS": 0}

        for ss in salary_slips:
            doc = frappe.get_doc("Salary Slip", ss.name)

            for d in doc.deductions:
                comp = frappe.get_doc("Salary Component", d.salary_component)

                if comp.component_type == "Provident Fund":
                    actual_totals["PF"] += flt(d.amount)

                elif comp.component_type == "Professional Tax":
                    actual_totals["PT"] += flt(d.amount)

            for e in doc.earnings:
                comp = frappe.get_doc("Salary Component", e.salary_component)

                if comp.component_type == "NPS":
                    actual_totals["NPS"] += flt(e.amount)

        remaining_months = max(total_months - actual_months, 0)

        latest_assignment = frappe.get_all(
            "Salary Structure Assignment",
            filters={"employee": self.employee, "docstatus": 1},
            fields=["salary_structure"],
            order_by="from_date desc",
            limit=1,
        )

        if not latest_assignment:
            return

        structure_doc = frappe.get_doc("Salary Structure", latest_assignment[0].salary_structure)

        has_pf = any(
            frappe.get_doc("Salary Component", d.salary_component).component_type == "Provident Fund"
            for d in structure_doc.deductions
        )

        has_pt = any(
            frappe.get_doc("Salary Component", d.salary_component).component_type == "Professional Tax"
            for d in structure_doc.deductions
        )

        has_nps = any(
            frappe.get_doc("Salary Component", e.salary_component).component_type == "NPS"
            for e in structure_doc.earnings
        )

        projected_totals = {"PF": 0, "PT": 0, "NPS": 0}

        if remaining_months > 0:
            preview_slip = make_salary_slip(
                source_name=latest_assignment[0].salary_structure,
                employee=self.employee,
                print_format="Salary Slip Standard",
                posting_date=effective_start,
                for_preview=1,
            )

            preview_slip.run_method("calculate_net_pay")

            for d in preview_slip.deductions:
                comp = frappe.get_doc("Salary Component", d.salary_component)

                if comp.component_type == "Provident Fund" and has_pf:
                    projected_totals["PF"] += flt(d.amount) * remaining_months

                elif comp.component_type == "Professional Tax" and has_pt:
                    projected_totals["PT"] += flt(d.amount) * remaining_months

            for e in preview_slip.earnings:
                comp = frappe.get_doc("Salary Component", e.salary_component)

                if comp.component_type == "NPS" and has_nps:
                    projected_totals["NPS"] += flt(e.amount) * remaining_months

        final_totals = {
            "PF": flt(actual_totals["PF"] + projected_totals["PF"], 2),
            "PT": flt(actual_totals["PT"] + projected_totals["PT"], 2),
            "NPS": flt(actual_totals["NPS"] + projected_totals["NPS"], 2),
        }

        sub_categories = frappe.get_all(
            "Employee Tax Exemption Sub Category",
            filters={"is_active": 1},
            fields=["name", "max_amount", "custom_component_type"],
        )

        final_rows = []

        for sub in sub_categories:
            comp_type = sub.custom_component_type

            if comp_type == "Provident Fund":
                amount = final_totals["PF"]

            elif comp_type == "Professional Tax":
                amount = final_totals["PT"]

            elif comp_type == "NPS":
                amount = final_totals["NPS"]

            else:
                continue

            allowed = min(amount, sub.max_amount or amount)

            final_rows.append(
                {"sub_category": sub.name, "max_amount": flt(sub.max_amount, 2), "amount": flt(allowed, 2)}
            )

        existing = frappe.get_list(
            "Employee Tax Exemption Declaration",
            filters={
                "employee": self.employee,
                "payroll_period": self.custom_payroll_period,
                "docstatus": ["in", [0, 1]],
            },
            fields=["name"],
        )

        if existing:
            doc = frappe.get_doc("Employee Tax Exemption Declaration", existing[0].name)
            doc.declarations = []
        else:
            doc = frappe.get_doc(
                {
                    "doctype": "Employee Tax Exemption Declaration",
                    "employee": self.employee,
                    "company": self.company,
                    "payroll_period": self.custom_payroll_period,
                    "currency": self.currency,
                    "custom_income_tax": self.income_tax_slab,
                    "custom_tax_regime": self.custom_tax_regime,
                    "custom_posting_date": self.from_date,
                }
            )

        for row in final_rows:
            doc.append(
                "declarations",
                {
                    "exemption_sub_category": row["sub_category"],
                    "max_amount": row["max_amount"],
                    "amount": row["amount"],
                },
            )

        doc.save(ignore_permissions=True)

        if doc.docstatus == 0:
            doc.submit()


@frappe.whitelist()
def generate_ctc_pdf(employee, salary_structure, posting_date=None, employee_benefits=None):
    frappe.only_for("HR Manager")

    if not frappe.has_permission("Employee", "read", employee):
        frappe.throw(frappe._("Not permitted to access this employee's CTC."), frappe.PermissionError)

    slip = make_salary_slip(
        source_name=salary_structure,
        employee=employee,
        print_format="Salary Slip Standard",
        posting_date=posting_date,
        for_preview=1,
    )

    if not slip:
        frappe.throw(frappe._("Unable to generate salary breakup. Check Salary Structure or Employee."))

    # Batch-fetch all salary components referenced in the slip
    all_comp_names = list(
        {e.salary_component for e in slip.get("earnings", [])}
        | {d.salary_component for d in slip.get("deductions", [])}
    )
    comp_map = {}
    if all_comp_names:
        for row in frappe.get_all(
            "Salary Component",
            filters={"name": ["in", all_comp_names]},
            fields=["name", "custom_is_part_of_ctc"],
        ):
            comp_map[row.name] = row

    earnings_list = []
    total_monthly_earnings = total_annual_earnings = 0
    for e in slip.get("earnings", []):
        comp_doc = frappe.get_doc("Salary Component", e.salary_component)
        if comp_doc.custom_is_part_of_ctc:
            amount = e.amount or 0
            earnings_list.append(
                {
                    "salary_component": e.salary_component,
                    "monthly_amount": round(amount),
                    "annual_amount": round(amount) * 12,
                }
            )
            total_monthly_earnings += round(amount)
            total_annual_earnings += round(amount) * 12

    deduction_list = []
    total_monthly_ded = total_annual_ded = 0
    for d in slip.get("deductions", []):
        comp_doc = frappe.get_doc("Salary Component", d.salary_component)
        if comp_doc.custom_is_part_of_ctc:
            amount = d.amount or 0
            deduction_list.append(
                {
                    "salary_component": d.salary_component,
                    "monthly_amount": round(amount),
                    "annual_amount": round(amount) * 12,
                }
            )
            total_monthly_ded += round(amount)
            total_annual_ded += round(amount) * 12

    if employee_benefits and isinstance(employee_benefits, str):
        try:
            employee_benefits = json.loads(employee_benefits)
        except Exception:
            employee_benefits = []

    reimbursement_list = []
    total_monthly_reim = total_annual_reim = 0
    for r in employee_benefits or []:
        comp_name = r.get("salary_component")
        amount = r.get("amount", 0) or 0
        if comp_name:
            reimbursement_list.append(
                {"salary_component": comp_name, "monthly_amount": amount / 12, "annual_amount": amount}
            )
            total_monthly_reim += amount / 12
            total_annual_reim += amount

    total_monthly_ctc = total_monthly_earnings + total_monthly_reim + total_monthly_ded
    total_annual_ctc = total_annual_earnings + total_annual_reim + total_annual_ded

    employee_doc = frappe.get_cached_doc("Employee", employee)

    context = {
        "employee": employee,
        "employee_name": employee_doc.employee_name,
        "department": employee_doc.department,
        "designation": employee_doc.designation,
        "company": slip.get("company") or "",
        "posting_date": slip.get("posting_date") or "",
        "salary_structure": slip.get("salary_structure") or "",
        "earnings": earnings_list,
        "reimbursements": reimbursement_list,
        "deductions": deduction_list,
        "total_monthly_earnings": total_monthly_earnings,
        "total_annual_earnings": total_annual_earnings,
        "total_monthly_reim": total_monthly_reim,
        "total_annual_reim": total_annual_reim,
        "total_monthly_ded": total_monthly_ded,
        "total_annual_ded": total_annual_ded,
        "total_monthly_ctc": total_monthly_ctc,
        "total_annual_ctc": total_annual_ctc,
    }

    html = frappe.render_template("cn_indian_payroll/templates/ctc_breakup_pdf.html", context)

    pdf_bytes = get_pdf(html)

    file_doc = frappe.get_doc(
        {
            "doctype": "File",
            "file_name": f"CTC_Breakup_{employee}.pdf",
            "attached_to_doctype": "Employee",
            "attached_to_name": employee,
            "content": pdf_bytes,
            "is_private": 0,
        }
    )
    file_doc.insert(ignore_permissions=True)

    return {"pdf_url": file_doc.file_url}
