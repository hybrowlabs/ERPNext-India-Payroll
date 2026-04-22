"""
CustomSalarySlip — thin override that composes the domain mixins.

Business logic lives in payroll/mixins/:
  LOPMixin      — working-days / LOP reversal
  TaxMixin      — variable tax, breakup, taxable-earnings queries
  BenefitsMixin — benefit claims, HRA/NPS/PF declaration sync
  ESICMixin     — ESIC and total-deduction helpers
"""

import frappe
from frappe import _
from frappe.query_builder import Order
from frappe.utils import get_link_to_form

from hrms.payroll.doctype.payroll_period.payroll_period import get_period_factor
from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip

from cn_indian_payroll.cn_indian_payroll.constants import MONTH_NAMES
from cn_indian_payroll.cn_indian_payroll.payroll.mixins import (
    BenefitsMixin,
    ESICMixin,
    LOPMixin,
    TaxMixin,
)


class CustomSalarySlip(LOPMixin, TaxMixin, BenefitsMixin, ESICMixin, SalarySlip):
    """
    MRO: LOPMixin → TaxMixin → BenefitsMixin → ESICMixin → SalarySlip → Document
    """

    # ------------------------------------------------------------------
    # Lifecycle hooks
    # ------------------------------------------------------------------

    def validate(self):
        super().validate()
        self.set_month()
        self.set_sub_period()
        self.update_total_lop()
        self.set_taxable_regime()
        self.insert_lopreversal_days()

    def before_save(self):
        self.esic_amount_roundup()
        self.update_declaration_component()
        self.tax_calculation()

    # ------------------------------------------------------------------
    # Utility methods that don't fit a single domain mixin
    # ------------------------------------------------------------------

    def set_month(self) -> None:
        month_number = int(str(self.start_date)[5:7])
        self.custom_month = MONTH_NAMES[month_number - 1]

    def set_sub_period(self) -> None:
        sub_period = get_period_factor(
            self.employee,
            self.start_date,
            self.end_date,
            self.payroll_frequency,
            self.payroll_period,
            joining_date=self.joining_date,
            relieving_date=self.relieving_date,
        )[1]
        self.custom_month_count = sub_period - 1

    def check_sal_struct(self):
        ss = frappe.qb.DocType("Salary Structure")
        ssa = frappe.qb.DocType("Salary Structure Assignment")

        query = (
            frappe.qb.from_(ssa)
            .join(ss)
            .on(ssa.salary_structure == ss.name)
            .select(
                ssa.salary_structure,
                ssa.custom_payroll_period,
                ssa.name,
                ssa.income_tax_slab,
                ssa.custom_tax_regime,
            )
            .where(
                (ssa.docstatus == 1)
                & (ss.docstatus == 1)
                & (ss.is_active == "Yes")
                & (ssa.employee == self.employee)
                & (
                    (ssa.from_date <= self.start_date)
                    | (ssa.from_date <= self.end_date)
                    | (ssa.from_date <= self.joining_date)
                )
            )
            .orderby(ssa.from_date, order=Order.desc)
            .limit(1)
        )

        if not self.salary_slip_based_on_timesheet and self.payroll_frequency:
            query = query.where(ss.payroll_frequency == self.payroll_frequency)

        st_name = query.run()

        if st_name:
            self.salary_structure = st_name[0][0]
            self.custom_payroll_period = st_name[0][1]
            self.custom_salary_structure_assignment = st_name[0][2]
            self.custom_income_tax_slab = st_name[0][3]
            self.custom_tax_regime = st_name[0][4]
            return self.salary_structure

        self.salary_structure = None
        frappe.msgprint(
            _(
                "No active or default Salary Structure found for employee {0} for the given dates"
            ).format(self.employee),
            title=_("Salary Structure Missing"),
        )

    def eval_condition_and_formula(self, struct_row, data):
        try:
            condition = struct_row.condition
            formula = struct_row.formula
            amount = struct_row.amount

            if condition and not _safe_eval(condition, self.whitelisted_globals, data):
                return None

            if struct_row.amount_based_on_formula and formula:
                amount = float(
                    _safe_eval(formula, self.whitelisted_globals, data)
                )
                amount = round(amount, struct_row.precision("amount"))

            if amount:
                data[struct_row.abbr] = amount

            return amount

        except NameError as ne:
            _throw_error_message(struct_row, ne, _("Name error"), _("This error can be due to missing or deleted field."))
        except SyntaxError as se:
            _throw_error_message(struct_row, se, _("Syntax error"), _("This error can be due to invalid syntax."))
        except Exception as exc:
            _throw_error_message(struct_row, exc, _("Error in formula or condition"), _("This error can be due to invalid formula or condition."))
            raise


# ---------------------------------------------------------------------------
# Module-level helpers
# ---------------------------------------------------------------------------

def _safe_eval(
    code: str,
    eval_globals: dict | None = None,
    eval_locals: dict | None = None,
):
    import unicodedata

    code = unicodedata.normalize("NFKC", code)
    _check_attributes(code)

    whitelisted_globals = {
        "int": int, "float": float, "long": int, "round": round,
        "sum": sum, "min": min, "max": max, "next": next, "len": len,
    }

    if not eval_globals:
        eval_globals = {}
    eval_globals["__builtins__"] = {}
    eval_globals.update(whitelisted_globals)

    return eval(code, eval_globals, eval_locals)  # nosemgrep


def _check_attributes(code: str) -> None:
    import ast
    from frappe.utils.safe_exec import UNSAFE_ATTRIBUTES

    unsafe_attrs = set(UNSAFE_ATTRIBUTES).union(["__"]) - {"format"}
    for attribute in unsafe_attrs:
        if attribute in code:
            raise SyntaxError(
                f'Illegal rule {frappe.bold(code)}. Cannot use "{attribute}"'
            )

    tree = ast.parse(code, mode="eval")
    for node in ast.walk(tree):
        if isinstance(node, ast.NamedExpr):
            raise SyntaxError(
                f"Operation not allowed: line {node.lineno} column {node.col_offset}"
            )
        if (
            isinstance(node, ast.Attribute)
            and isinstance(node.attr, str)
            and node.attr in UNSAFE_ATTRIBUTES
        ):
            raise SyntaxError(
                f'Illegal rule {frappe.bold(code)}. Cannot use "{node.attr}"'
            )


def _throw_error_message(row, error, title, description=None):
    data = frappe._dict(
        {
            "doctype": row.parenttype,
            "name": row.parent,
            "doclink": get_link_to_form(row.parenttype, row.parent),
            "row_id": row.idx,
            "error": error,
            "title": title,
            "description": description or "",
        }
    )
    message = _(
        "Error while evaluating the {doctype} {doclink} at row {row_id}. <br><br>"
        " <b>Error:</b> {error} <br><br> <b>Hint:</b> {description}"
    ).format(**data)
    frappe.throw(message, title=title)
