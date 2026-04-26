import frappe
from frappe import _
from frappe.utils import flt

EPF_WAGE_CEILING = 15000


def get_salary_slips(filters=None):
    if filters is None:
        filters = {}

    if not filters.get("company"):
        frappe.throw(_("Company is a mandatory filter."))

    if not filters.get("month"):
        frappe.throw(_("Month is a mandatory filter."))

    company_doc = frappe.get_cached_doc("Company", filters["company"])
    if not company_doc.basic_component:
        frappe.throw(_("Please configure the Basic Component in Company Master before running this report."))

    basic_component = company_doc.basic_component

    slip_filters = {"docstatus": 1, "company": filters["company"]}
    if filters.get("month"):
        slip_filters["custom_month"] = filters["month"]
    if filters.get("payroll_period"):
        slip_filters["custom_payroll_period"] = filters["payroll_period"]

    salary_slips = frappe.get_all(
        "Salary Slip",
        filters=slip_filters,
        fields=[
            "name",
            "employee",
            "employee_name",
            "custom_total_leave_without_pay",
            "custom_salary_structure_assignment",
        ],
    )
    if not salary_slips:
        return []

    slip_names = [s.name for s in salary_slips]
    emp_ids = list({s.employee for s in salary_slips})

    # Branch filter applied after fetching employees
    branch_filter = filters.get("branch")
    if branch_filter:
        emp_branches = {
            row.name: row.branch
            for row in frappe.get_all(
                "Employee",
                filters={"name": ["in", emp_ids]},
                fields=["name", "branch"],
            )
        }

    # Batch: employee UAN — one query
    emp_uan_map = {
        row.name: row.custom_uan
        for row in frappe.get_all(
            "Employee",
            filters={"name": ["in", emp_ids]},
            fields=["name", "custom_uan"],
        )
    }

    # Batch: SSA EPF/EPS flags via slip-level link, fallback to latest submitted SSA per employee
    # Fetch latest submitted SSA per employee; also serves as lookup for slip-level SSA links
    all_ssa = frappe.get_all(
        "Salary Structure Assignment",
        filters={"employee": ["in", emp_ids], "docstatus": 1},
        fields=["name", "employee", "from_date", "custom_is_epf", "custom_is_eps"],
        order_by="employee, from_date desc",
    )
    latest_ssa_map: dict[str, dict] = {}
    for ssa in all_ssa:
        if ssa.employee not in latest_ssa_map:
            latest_ssa_map[ssa.employee] = ssa

    # Map SSA name → SSA doc for slip-level links
    ssa_by_name = {ssa.name: ssa for ssa in all_ssa}

    # Batch: basic-component earnings for all slips — one query
    earnings_rows = frappe.get_all(
        "Salary Detail",
        filters={
            "parent": ["in", slip_names],
            "parentfield": "earnings",
            "salary_component": basic_component,
        },
        fields=["parent", "amount"],
    )
    basic_by_slip: dict[str, float] = {}
    for row in earnings_rows:
        basic_by_slip[row.parent] = basic_by_slip.get(row.parent, 0.0) + flt(row.amount or 0)

    result = []
    for slip in salary_slips:
        if branch_filter and emp_branches.get(slip.employee) != branch_filter:
            continue

        # Resolve SSA: prefer slip-level link, fall back to latest submitted SSA
        ssa = None
        if slip.custom_salary_structure_assignment:
            ssa = ssa_by_name.get(slip.custom_salary_structure_assignment)
        if not ssa:
            ssa = latest_ssa_map.get(slip.employee)

        if not ssa or not ssa.custom_is_epf:
            continue

        basic = basic_by_slip.get(slip.name, 0.0)
        is_eps = bool(ssa.custom_is_eps)

        wage_epf = min(basic, EPF_WAGE_CEILING)
        wage_eps = min(basic, EPF_WAGE_CEILING) if is_eps else 0
        wage_edli = min(basic, EPF_WAGE_CEILING)

        cr_ee = round(wage_epf * 12 / 100)
        cr_eps = round(wage_eps * 8.33 / 100) if is_eps else 0
        # CR ER is derived so that CR EPS + CR ER == CR EE always (EPFO audit invariant)
        cr_er = cr_ee - cr_eps

        result.append(
            {
                "uan": emp_uan_map.get(slip.employee) or "",
                "employee_name": (slip.employee_name or "").upper(),
                "gross": round(basic),
                "wage_epf": round(wage_epf),
                "wage_eps": round(wage_eps),
                "wage_edli": round(wage_edli),
                "cr_ee": cr_ee,
                "cr_eps": cr_eps,
                "cr_er": cr_er,
                "ncp_days": flt(slip.custom_total_leave_without_pay) or 0,
                "refunds": 0,
            }
        )

    return result


def execute(filters=None):
    columns = [
        {"fieldname": "uan", "label": _("UAN"), "fieldtype": "Data", "width": 150},
        {"fieldname": "employee_name", "label": _("Employee Name"), "fieldtype": "Data", "width": 220},
        {"fieldname": "gross", "label": _("Gross"), "fieldtype": "Int", "width": 120},
        {"fieldname": "wage_epf", "label": _("Wage EPF"), "fieldtype": "Int", "width": 120},
        {"fieldname": "wage_eps", "label": _("Wage EPS"), "fieldtype": "Int", "width": 120},
        {"fieldname": "wage_edli", "label": _("Wage EDLI"), "fieldtype": "Int", "width": 120},
        {"fieldname": "cr_ee", "label": _("CR EE"), "fieldtype": "Int", "width": 100},
        {"fieldname": "cr_eps", "label": _("CR EPS"), "fieldtype": "Int", "width": 100},
        {"fieldname": "cr_er", "label": _("CR ER"), "fieldtype": "Int", "width": 100},
        {"fieldname": "ncp_days", "label": _("NCP Days"), "fieldtype": "Float", "width": 110},
        {"fieldname": "refunds", "label": _("Refunds"), "fieldtype": "Int", "width": 100},
    ]
    return columns, get_salary_slips(filters)


@frappe.whitelist()
def download_ecr_txt(filters=None):
    import json

    frappe.only_for("HR Manager")

    if isinstance(filters, str):
        filters = json.loads(filters)

    salary_data = get_salary_slips(filters)
    if not salary_data:
        frappe.throw(_("No EPF-eligible salary slips found for the selected filters."))

    def r(value):
        return str(round(flt(value) or 0))

    lines = [
        "#~#".join(
            [
                str(row.get("uan") or "0"),
                row.get("employee_name") or "",
                r(row.get("gross")),
                r(row.get("wage_epf")),
                r(row.get("wage_eps")),
                r(row.get("wage_edli")),
                r(row.get("cr_ee")),
                r(row.get("cr_eps")),
                r(row.get("cr_er")),
                r(row.get("ncp_days")),
                r(row.get("refunds")),
            ]
        )
        for row in salary_data
    ]

    return "\n".join(lines)
