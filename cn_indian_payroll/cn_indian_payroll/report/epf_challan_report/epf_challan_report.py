import frappe
from frappe import _
from frappe.utils import flt

EPF_WAGE_CEILING = 15000


def _validate_filters(filters):
	"""Validate mandatory filters and return basic_component from Company Master."""
	if not filters.get("company"):
		frappe.throw(_("Company is a mandatory filter."))

	company_doc = frappe.get_cached_doc("Company", filters["company"])

	if not company_doc.basic_component:
		frappe.throw(
			_("Please configure the Basic Component in Company Master before running this report.")
		)

	return company_doc.basic_component


def _build_sql_conditions(filters):
	"""Return (WHERE clause string, values dict) for the main Salary Slip query."""
	conditions = ["ss.docstatus = 1", "ss.company = %(company)s"]
	values = {"company": filters["company"]}

	if filters.get("month"):
		conditions.append("ss.custom_month = %(month)s")
		values["month"] = filters["month"]

	if filters.get("payroll_period"):
		conditions.append("ss.custom_payroll_period = %(payroll_period)s")
		values["payroll_period"] = filters["payroll_period"]

	if filters.get("branch"):
		conditions.append("e.branch = %(branch)s")
		values["branch"] = filters["branch"]

	return " AND ".join(conditions), values


def _get_salary_slip_rows(where_clause, values, basic_component):
	"""
	Single optimised query:
	  - Joins Salary Slip → Employee
	  - Joins to the SSA linked on the salary slip (custom_salary_structure_assignment)
	    as the primary source; falls back to the most-recent submitted SSA for the
	    employee/company if the slip-level link is absent.
	  - Uses a correlated sub-select to sum only the basic-component earnings rows.

	Only submitted slips (docstatus = 1) are returned so that the report is
	consistent with what was actually processed in payroll.
	"""
	values["basic_component"] = basic_component

	return frappe.db.sql(
		"""
		SELECT
			ss.name                                        AS slip_name,
			ss.employee,
			ss.employee_name,
			ss.custom_total_leave_without_pay              AS ncp_days,
			e.custom_uan                                   AS uan,

			/* EPF / EPS eligibility flags from the SSA used for this salary slip.
			   COALESCE falls back to the latest submitted SSA if the slip-level
			   link (custom_salary_structure_assignment) is not populated. */
			COALESCE(
				slip_ssa.custom_is_epf,
				fallback_ssa.custom_is_epf,
				0
			)                                              AS is_epf,
			COALESCE(
				slip_ssa.custom_is_eps,
				fallback_ssa.custom_is_eps,
				0
			)                                              AS is_eps,

			/* Sum of basic-component earnings rows for this slip */
			COALESCE((
				SELECT SUM(sd.amount)
				FROM   `tabSalary Detail` sd
				WHERE  sd.parent      = ss.name
				  AND  sd.parentfield = 'earnings'
				  AND  sd.salary_component = %(basic_component)s
			), 0)                                          AS basic_amount

		FROM `tabSalary Slip` ss

		INNER JOIN `tabEmployee` e
			ON  e.name = ss.employee

		/* SSA directly linked on the salary slip (most accurate) */
		LEFT JOIN `tabSalary Structure Assignment` slip_ssa
			ON  slip_ssa.name     = ss.custom_salary_structure_assignment
			AND slip_ssa.docstatus = 1

		/* Latest submitted SSA for the employee as a fallback */
		LEFT JOIN `tabSalary Structure Assignment` fallback_ssa
			ON  fallback_ssa.employee  = ss.employee
			AND fallback_ssa.company   = ss.company
			AND fallback_ssa.docstatus = 1
			AND fallback_ssa.from_date = (
				SELECT MAX(inner_ssa.from_date)
				FROM   `tabSalary Structure Assignment` inner_ssa
				WHERE  inner_ssa.employee  = ss.employee
				  AND  inner_ssa.company   = ss.company
				  AND  inner_ssa.docstatus = 1
			)

		WHERE {where_clause}

		ORDER BY ss.employee, ss.name
		""".format(where_clause=where_clause),
		values,
		as_dict=True,
	)


def _compute_row(slip):
	"""
	Apply EPF contribution rules to a single salary slip row and return a
	report-ready dict, or None if the employee is not EPF-eligible.

	Rules (per EPFO Regular Return format):
	  - Gross        : Basic component amount (no ceiling)
	  - Wage EPF     : min(Basic, 15000)
	  - Wage EPS     : min(Basic, 15000) if custom_is_eps = 1 else 0
	  - Wage EDLI    : min(Basic, 15000)
	  - CR EE        : round(Wage EPF × 12 / 100)
	  - CR EPS       : round(Wage EPS × 8.33 / 100) if custom_is_eps = 1 else 0
	  - CR ER        : CR EE − CR EPS  →  guarantees CR EPS + CR ER = CR EE always
	  - NCP Days     : custom_total_leave_without_pay from Salary Slip
	  - Refunds      : 0  (no advance refunds in scope)
	"""
	if not slip.get("is_epf"):
		return None

	basic = flt(slip.basic_amount)
	is_eps = bool(slip.get("is_eps"))

	wage_epf = min(basic, EPF_WAGE_CEILING)
	wage_eps = min(basic, EPF_WAGE_CEILING) if is_eps else 0
	wage_edli = min(basic, EPF_WAGE_CEILING)

	cr_ee = round(wage_epf * 12 / 100)
	cr_eps = round(wage_eps * 8.33 / 100) if is_eps else 0
	# CR ER is derived so that CR EPS + CR ER == CR EE always (audit invariant)
	cr_er = cr_ee - cr_eps

	return {
		"uan": slip.uan or "",
		"employee_name": (slip.employee_name or "").upper(),
		"gross": round(basic),
		"wage_epf": round(wage_epf),
		"wage_eps": round(wage_eps),
		"wage_edli": round(wage_edli),
		"cr_ee": cr_ee,
		"cr_eps": cr_eps,
		"cr_er": cr_er,
		"ncp_days": flt(slip.ncp_days) or 0,
		"refunds": 0,
	}


def get_salary_slips(filters=None):
	"""Entry point consumed by execute() and download_ecr_txt()."""
	if filters is None:
		filters = {}

	basic_component = _validate_filters(filters)
	where_clause, values = _build_sql_conditions(filters)

	rows = _get_salary_slip_rows(where_clause, values, basic_component)

	result = []
	for slip in rows:
		computed = _compute_row(slip)
		if computed:
			result.append(computed)

	return result


def execute(filters=None):
	columns = [
		{
			"fieldname": "uan",
			"label": _("UAN"),
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"fieldname": "employee_name",
			"label": _("Employee Name"),
			"fieldtype": "Data",
			"width": 220,
		},
		{
			"fieldname": "gross",
			"label": _("Gross"),
			"fieldtype": "Int",
			"width": 120,
		},
		{
			"fieldname": "wage_epf",
			"label": _("Wage EPF"),
			"fieldtype": "Int",
			"width": 120,
		},
		{
			"fieldname": "wage_eps",
			"label": _("Wage EPS"),
			"fieldtype": "Int",
			"width": 120,
		},
		{
			"fieldname": "wage_edli",
			"label": _("Wage EDLI"),
			"fieldtype": "Int",
			"width": 120,
		},
		{
			"fieldname": "cr_ee",
			"label": _("CR EE"),
			"fieldtype": "Int",
			"width": 100,
		},
		{
			"fieldname": "cr_eps",
			"label": _("CR EPS"),
			"fieldtype": "Int",
			"width": 100,
		},
		{
			"fieldname": "cr_er",
			"label": _("CR ER"),
			"fieldtype": "Int",
			"width": 100,
		},
		{
			"fieldname": "ncp_days",
			"label": _("NCP Days"),
			"fieldtype": "Float",
			"width": 110,
		},
		{
			"fieldname": "refunds",
			"label": _("Refunds"),
			"fieldtype": "Int",
			"width": 100,
		},
	]

	data = get_salary_slips(filters)
	return columns, data


@frappe.whitelist()
def download_ecr_txt(filters=None):
	"""
	Generate the EPFO ECR (Electronic Challan-cum-Return) text file.

	Format: fields separated by '#~#', one employee per line.
	Column order matches the EPFO upload portal:
	  UAN #~# Member Name #~# Gross Wages #~# EPF Wages #~# EPS Wages #~#
	  EDLI Wages #~# EPF Contri Remitted (CR EE) #~# EPS Contri Remitted (CR EPS) #~#
	  EPF Contri Due from ER (CR ER) #~# NCP Days #~# Refunds
	"""
	import json

	if isinstance(filters, str):
		filters = json.loads(filters)

	salary_data = get_salary_slips(filters)

	def r(value):
		return str(round(flt(value) or 0))

	lines = []
	for row in salary_data:
		line = "#~#".join([
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
		])
		lines.append(line)

	return "\n".join(lines)
