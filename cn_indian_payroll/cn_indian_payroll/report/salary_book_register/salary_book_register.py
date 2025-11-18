# # Copyright (c) 2015, Frappe Technologies Pvt. Ltd.
# # License: GNU General Public License v3. See license.txt

# import frappe
# from frappe import _
# from frappe.utils import flt
# import erpnext

# salary_slip = frappe.qb.DocType("Salary Slip")
# salary_detail = frappe.qb.DocType("Salary Detail")
# salary_component = frappe.qb.DocType("Salary Component")


# def execute(filters=None):
# 	if not filters:
# 		filters = {}

# 	currency = filters.get("currency")
# 	company_currency = erpnext.get_company_currency(filters.get("company"))

# 	salary_slips = get_salary_slips(filters, company_currency)
# 	if not salary_slips:
# 		return [], []

# 	# included components
# 	earning_types, ded_types = get_earning_and_deduction_types(salary_slips)

# 	# --- Excluded earnings ---
# 	ex_earnings = get_excluded_earning_details(salary_slips, currency, company_currency)
# 	ex_earning_types = sorted({c for m in ex_earnings.values() for c in m}) if ex_earnings else []

# 	# --- Excluded deductions ---
# 	ex_deductions = get_excluded_deduction_details(salary_slips, currency, company_currency)
# 	ex_deduction_types = sorted({c for m in ex_deductions.values() for c in m}) if ex_deductions else []

# 	# build columns including excluded earnings/deductions
# 	columns = get_columns(earning_types, ded_types, ex_earning_types, ex_deduction_types)

# 	ss_earning_map = get_salary_slip_details(salary_slips, currency, company_currency, "earnings")
# 	ss_ded_map = get_salary_slip_details(salary_slips, currency, company_currency, "deductions")

# 	doj_map = get_employee_doj_map()

# 	data = []
# 	for ss in salary_slips:
# 		row = {
# 			"salary_slip_id": ss.name,
# 			"employee": ss.employee,
# 			"employee_name": ss.employee_name,
# 			"data_of_joining": doj_map.get(ss.employee),
# 			"branch": ss.branch,
# 			"department": ss.department,
# 			"designation": ss.designation,
# 			"company": ss.company,
# 			"start_date": ss.start_date,
# 			"end_date": ss.end_date,
# 			"total_working_days": ss.total_working_days,
# 			"leave_without_pay": ss.leave_without_pay,
# 			"absent_days": ss.absent_days,
# 			"payment_days": ss.payment_days,
# 			"arrear_days": ss.custom_lop_reversal_days,
# 			"currency": currency or company_currency,
# 			"total_loan_repayment": ss.total_loan_repayment,
# 			"employee_state": ss.custom_employee_state,
# 			"income_tax_slab": ss.custom_tax_regime,
# 			"annual_ctc": ss.custom_annual_ctc,
# 			"monthly_ctc": round(flt(ss.custom_annual_ctc) / 12, 2),
# 		}

# 		update_column_width(ss, columns)

# 		# include earnings
# 		for e in earning_types:
# 			row[frappe.scrub(e)] = ss_earning_map.get(ss.name, {}).get(e)

# 		# gross / total / net
# 		if currency == company_currency:
# 			row["gross_pay"] = flt(ss.gross_pay) * flt(ss.exchange_rate)
# 			row["total_deduction"] = flt(ss.total_deduction) * flt(ss.exchange_rate)
# 			row["net_pay"] = flt(ss.net_pay) * flt(ss.exchange_rate)
# 		else:
# 			row["gross_pay"] = ss.gross_pay
# 			row["total_deduction"] = ss.total_deduction
# 			row["net_pay"] = ss.net_pay

# 		# --- excluded earnings ---
# 		total_excluded_earn = 0
# 		for ex in ex_earning_types:
# 			fname = frappe.scrub(ex + "_excluded")
# 			amount = flt(ex_earnings.get(ss.name, {}).get(ex, 0))
# 			row[fname] = amount
# 			total_excluded_earn += amount

# 		# included deductions
# 		for d in ded_types:
# 			row[frappe.scrub(d)] = ss_ded_map.get(ss.name, {}).get(d)

# 		# --- excluded deductions ---
# 		total_excluded_ded = 0
# 		for exd in ex_deduction_types:
# 			fname = frappe.scrub(exd + "_excluded")
# 			amt = flt(ex_deductions.get(ss.name, {}).get(exd, 0))
# 			row[fname] = amt
# 			total_excluded_ded += amt

# 		# total income = gross + excluded earnings
# 		row["total_income"] = flt(row.get("gross_pay")) + total_excluded_earn

# 		data.append(row)

# 	return columns, data


# # =======================================================================


# def get_earning_and_deduction_types(salary_slips):
# 	salary_component_and_type = {"Earning": [], "Deduction": []}

# 	for comp in get_salary_components(salary_slips):
# 		component_type = get_salary_component_type(comp)
# 		salary_component_and_type[component_type].append(comp)

# 	return sorted(salary_component_and_type["Earning"]), sorted(salary_component_and_type["Deduction"])


# def update_column_width(ss, columns):
# 	if ss.branch: columns[3]["width"] = 120
# 	if ss.department: columns[4]["width"] = 120
# 	if ss.designation: columns[5]["width"] = 120
# 	if ss.leave_without_pay: columns[9]["width"] = 120


# def get_columns(earning_types, ded_types, ex_earning_types, ex_deduction_types):
# 	columns = [
# 		{"label": _("Salary Slip ID"), "fieldname": "salary_slip_id", "fieldtype": "Link", "options": "Salary Slip", "width": 150},
# 		{"label": _("Employee"), "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 120},
# 		{"label": _("Employee Name"), "fieldname": "employee_name", "fieldtype": "Data", "width": 140},
# 		{"label": _("Employee State"), "fieldname": "employee_state", "fieldtype": "Data", "width": 140},
# 		{"label": _("Income Tax Slab"), "fieldname": "income_tax_slab", "fieldtype": "Data", "width": 140},
# 		{"label": _("Date of Joining"), "fieldname": "data_of_joining", "fieldtype": "Date", "width": 80},
# 		{"label": _("Branch"), "fieldname": "branch", "fieldtype": "Link", "options": "Branch", "width": 80},
# 		{"label": _("Department"), "fieldname": "department", "fieldtype": "Link", "options": "Department", "width": 80},
# 		{"label": _("Designation"), "fieldname": "designation", "fieldtype": "Link", "options": "Designation", "width": 120},
# 		{"label": _("Company"), "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 120},
# 		{"label": _("Start Date"), "fieldname": "start_date", "fieldtype": "Data", "width": 120},
# 		{"label": _("End Date"), "fieldname": "end_date", "fieldtype": "Data", "width": 120},
# 		{"label": _("Total Working Days"), "fieldname": "total_working_days", "fieldtype": "Float", "width": 150},
# 		{"label": _("Leave Without Pay"), "fieldname": "leave_without_pay", "fieldtype": "Float", "width": 150},
# 		{"label": _("Absent Days"), "fieldname": "absent_days", "fieldtype": "Float", "width": 150},
# 		{"label": _("Payment Days"), "fieldname": "payment_days", "fieldtype": "Float", "width": 150},
# 		{"label": _("Arrear Days"), "fieldname": "arrear_days", "fieldtype": "Float", "width": 150},
# 		{"label": _("Annual CTC"), "fieldname": "annual_ctc", "fieldtype": "Float", "width": 150},
# 		{"label": _("Monthly CTC"), "fieldname": "monthly_ctc", "fieldtype": "Float", "width": 150},
# 	]

# 	# included earnings
# 	for e in earning_types:
# 		columns.append({
# 			"label": e,
# 			"fieldname": frappe.scrub(e),
# 			"fieldtype": "Currency",
# 			"options": "currency",
# 			"width": 120,
# 		})

# 	# Gross Earnings
# 	columns.append({
# 		"label": _("Gross Earnings"),
# 		"fieldname": "gross_pay",
# 		"fieldtype": "Currency",
# 		"options": "currency",
# 		"width": 120,
# 	})

# 	# excluded earnings
# 	for ex in ex_earning_types:
# 		columns.append({
# 			"label": f"{ex} (Excluded)",
# 			"fieldname": frappe.scrub(ex + "_excluded"),
# 			"fieldtype": "Currency",
# 			"options": "currency",
# 			"width": 120,
# 		})

# 	# total income
# 	columns.append({
# 		"label": _("Total Income"),
# 		"fieldname": "total_income",
# 		"fieldtype": "Currency",
# 		"options": "currency",
# 		"width": 150,
# 	})

# 	# included deductions
# 	for d in ded_types:
# 		columns.append({
# 			"label": d,
# 			"fieldname": frappe.scrub(d),
# 			"fieldtype": "Currency",
# 			"options": "currency",
# 			"width": 120,
# 		})

# 	# excluded deductions


# 	# Final totals
# 	columns.extend([
# 		{"label": _("Loan Repayment"), "fieldname": "total_loan_repayment", "fieldtype": "Currency", "options": "currency", "width": 120},
# 		{"label": _("Total Deduction"), "fieldname": "total_deduction", "fieldtype": "Currency", "options": "currency", "width": 120},
# 	])

# 	# Add excluded deduction columns AFTER Total Deduction
# 	for exd in ex_deduction_types:
# 		columns.append({
# 			"label": f"{exd} (Excluded)",
# 			"fieldname": frappe.scrub(exd + "_excluded"),
# 			"fieldtype": "Currency",
# 			"options": "currency",
# 			"width": 120,
# 		})

# 	# Finally add Net Pay
# 	columns.append({
# 		"label": _("Net Pay"),
# 		"fieldname": "net_pay",
# 		"fieldtype": "Currency",
# 		"options": "currency",
# 		"width": 120,
# 	})


# 	return columns


# # =======================================================================


# def get_salary_components(salary_slips):
# 	return (
# 		frappe.qb.from_(salary_detail)
# 		.where(
# 			(salary_detail.amount != 0)
# 			& (salary_detail.parent.isin([d.name for d in salary_slips]))
# 			& (salary_detail.do_not_include_in_total == 0)
# 		)
# 		.select(salary_detail.salary_component)
# 		.distinct()
# 	).run(pluck=True)


# def get_salary_component_type(salary_component):
# 	return frappe.db.get_value("Salary Component", salary_component, "type", cache=True)


# def get_salary_slips(filters, company_currency):
# 	doc_status = {"Draft": 0, "Submitted": 1, "Cancelled": 2}

# 	query = frappe.qb.from_(salary_slip).select(salary_slip.star)

# 	if filters.get("docstatus"):
# 		query = query.where(salary_slip.docstatus == doc_status[filters.get("docstatus")])
# 	if filters.get("from_date"):
# 		query = query.where(salary_slip.start_date >= filters.get("from_date"))
# 	if filters.get("to_date"):
# 		query = query.where(salary_slip.end_date <= filters.get("to_date"))
# 	if filters.get("company"):
# 		query = query.where(salary_slip.company == filters.get("company"))
# 	if filters.get("employee"):
# 		query = query.where(salary_slip.employee == filters.get("employee"))
# 	if filters.get("currency") and filters.get("currency") != company_currency:
# 		query = query.where(salary_slip.currency == filters.get("currency"))

# 	return query.run(as_dict=1) or []


# def get_employee_doj_map():
# 	employee = frappe.qb.DocType("Employee")
# 	rows = frappe.qb.from_(employee).select(employee.name, employee.date_of_joining).run()
# 	return frappe._dict(rows)


# # =======================================================================
# # Included components (do_not_include_in_total = 0)
# # =======================================================================

# def get_salary_slip_details(salary_slips, currency, company_currency, component_type):
# 	slip_names = [ss.name for ss in salary_slips]

# 	rows = (
# 		frappe.qb.from_(salary_slip)
# 		.join(salary_detail)
# 		.on(salary_slip.name == salary_detail.parent)
# 		.where(
# 			(salary_detail.parent.isin(slip_names))
# 			& (salary_detail.parentfield == component_type)
# 			& (salary_detail.do_not_include_in_total == 0)
# 		)
# 		.select(
# 			salary_detail.parent,
# 			salary_detail.salary_component,
# 			salary_detail.amount,
# 			salary_slip.exchange_rate,
# 		)
# 	).run(as_dict=1)

# 	m = {}

# 	for d in rows:
# 		m.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, 0.0)
# 		if currency == company_currency:
# 			m[d.parent][d.salary_component] += flt(d.amount) * flt(d.exchange_rate or 1)
# 		else:
# 			m[d.parent][d.salary_component] += flt(d.amount)

# 	return m


# # =======================================================================
# # Excluded earnings (do_not_include_in_total = 1)
# # =======================================================================

# def get_excluded_earning_details(salary_slips, currency, company_currency):
# 	slip_names = [ss.name for ss in salary_slips]

# 	rows = (
# 		frappe.qb.from_(salary_slip)
# 		.join(salary_detail)
# 		.on(salary_slip.name == salary_detail.parent)
# 		.where(
# 			(salary_detail.parent.isin(slip_names))
# 			& (salary_detail.parentfield == "earnings")
# 			& (salary_detail.do_not_include_in_total == 1)
# 		)
# 		.select(
# 			salary_detail.parent,
# 			salary_detail.salary_component,
# 			salary_detail.amount,
# 			salary_slip.exchange_rate,
# 		)
# 	).run(as_dict=1)

# 	m = {}

# 	for d in rows:
# 		m.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, 0.0)
# 		if currency == company_currency:
# 			m[d.parent][d.salary_component] += flt(d.amount) * flt(d.exchange_rate or 1)
# 		else:
# 			m[d.parent][d.salary_component] += flt(d.amount)

# 	return m


# # =======================================================================
# # Excluded deductions (NEW)
# # =======================================================================

# def get_excluded_deduction_details(salary_slips, currency, company_currency):
# 	slip_names = [ss.name for ss in salary_slips]

# 	rows = (
# 		frappe.qb.from_(salary_slip)
# 		.join(salary_detail)
# 		.on(salary_slip.name == salary_detail.parent)
# 		.where(
# 			(salary_detail.parent.isin(slip_names))
# 			& (salary_detail.parentfield == "deductions")
# 			& (salary_detail.do_not_include_in_total == 1)
# 		)
# 		.select(
# 			salary_detail.parent,
# 			salary_detail.salary_component,
# 			salary_detail.amount,
# 			salary_slip.exchange_rate,
# 		)
# 	).run(as_dict=1)

# 	m = {}

# 	for d in rows:
# 		m.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, 0.0)
# 		if currency == company_currency:
# 			m[d.parent][d.salary_component] += flt(d.amount) * flt(d.exchange_rate or 1)
# 		else:
# 			m[d.parent][d.salary_component] += flt(d.amount)

# 	return m


# Copyright (c) 2015, Frappe Technologies Pvt. Ltd.
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.utils import flt
import erpnext

salary_slip = frappe.qb.DocType("Salary Slip")
salary_detail = frappe.qb.DocType("Salary Detail")
salary_component = frappe.qb.DocType("Salary Component")


def execute(filters=None):
    if not filters:
        filters = {}

    currency = filters.get("currency")
    company_currency = erpnext.get_company_currency(filters.get("company"))

    salary_slips = get_salary_slips(filters, company_currency)
    if not salary_slips:
        return [], []

    # included components (ordered by custom_sequence_id)
    earning_types, ded_types = get_earning_and_deduction_types(salary_slips)

    # --- Excluded earnings (ordered by sequence) ---
    ex_earnings = get_excluded_earning_details(salary_slips, currency, company_currency)
    ex_earning_types = (
        sort_components_by_sequence({c for m in ex_earnings.values() for c in m})
        if ex_earnings
        else []
    )

    # --- Excluded deductions (ordered by sequence) ---
    ex_deductions = get_excluded_deduction_details(
        salary_slips, currency, company_currency
    )
    ex_deduction_types = (
        sort_components_by_sequence({c for m in ex_deductions.values() for c in m})
        if ex_deductions
        else []
    )

    # build columns including excluded earnings/deductions
    columns = get_columns(
        earning_types, ded_types, ex_earning_types, ex_deduction_types
    )

    ss_earning_map = get_salary_slip_details(
        salary_slips, currency, company_currency, "earnings"
    )
    ss_ded_map = get_salary_slip_details(
        salary_slips, currency, company_currency, "deductions"
    )

    doj_map = get_employee_doj_map()

    data = []
    for ss in salary_slips:
        row = {
            "salary_slip_id": ss.name,
            "employee": ss.employee,
            "employee_name": ss.employee_name,
            "data_of_joining": doj_map.get(ss.employee),
            "branch": ss.branch,
            "department": ss.department,
            "designation": ss.designation,
            "company": ss.company,
            "start_date": ss.start_date,
            "end_date": ss.end_date,
            "total_working_days": ss.total_working_days,
            "leave_without_pay": ss.leave_without_pay,
            "absent_days": ss.absent_days,
            "payment_days": ss.payment_days,
            "arrear_days": ss.custom_lop_reversal_days,
            "currency": currency or company_currency,
            "total_loan_repayment": ss.total_loan_repayment,
            "employee_state": ss.custom_employee_state,
            "income_tax_slab": ss.custom_tax_regime,
            "annual_ctc": ss.custom_annual_ctc,
            "monthly_ctc": round(flt(ss.custom_annual_ctc) / 12, 2),
        }

        update_column_width(ss, columns)

        # include earnings (ordered)
        for e in earning_types:
            row[frappe.scrub(e)] = ss_earning_map.get(ss.name, {}).get(e)

        # gross / total / net (preserve original currency behavior)
        if currency == company_currency:
            row["gross_pay"] = flt(ss.gross_pay) * flt(ss.exchange_rate)
            row["total_deduction"] = flt(ss.total_deduction) * flt(ss.exchange_rate)
            row["net_pay"] = flt(ss.net_pay) * flt(ss.exchange_rate)
        else:
            row["gross_pay"] = ss.gross_pay
            row["total_deduction"] = ss.total_deduction
            row["net_pay"] = ss.net_pay

        # --- excluded earnings (ordered) ---
        total_excluded_earn = 0
        for ex in ex_earning_types:
            fname = frappe.scrub(ex + "_excluded")
            amount = flt(ex_earnings.get(ss.name, {}).get(ex, 0))
            row[fname] = amount
            total_excluded_earn += amount

        # included deductions (ordered)
        for d in ded_types:
            row[frappe.scrub(d)] = ss_ded_map.get(ss.name, {}).get(d)

        # --- excluded deductions (ordered) ---
        total_excluded_ded = 0
        for exd in ex_deduction_types:
            fname = frappe.scrub(exd + "_excluded")
            amt = flt(ex_deductions.get(ss.name, {}).get(exd, 0))
            row[fname] = amt
            total_excluded_ded += amt

        # total income = gross + excluded earnings
        row["total_income"] = flt(row.get("gross_pay")) + total_excluded_earn

        # NOTE: You previously asked to show excluded deductions AFTER Total Deduction and BEFORE Net Pay.
        # We kept that order in get_columns(). The actual numeric "total_deduction" field here is unchanged.
        # If you want Total Deduction to include excluded deductions, uncomment the next line:
        # row["total_deduction"] = flt(row.get("total_deduction")) + total_excluded_ded

        data.append(row)

    return columns, data


# =======================================================================


def get_earning_and_deduction_types(salary_slips):
    """
    Return two ordered lists: (earning_types, deduction_types)
    Ordering is by Salary Component.custom_sequence_id asc, then name asc.
    """
    components = get_salary_components(salary_slips)
    if not components:
        return [], []

    # Fetch type and custom_sequence_id for these components and order by sequence then name
    rows = frappe.get_all(
        "Salary Component",
        filters={"name": ("in", components)},
        fields=["name", "type", "custom_sequence_id"],
        order_by="custom_sequence_id asc, name asc",
    )

    earning = []
    deduction = []
    for r in rows:
        # r["type"] expected to be "Earning" or "Deduction"
        if r.get("type") == "Earning" or r.get("type") == _("Earning"):
            earning.append(r.get("name"))
        elif r.get("type") == "Deduction" or r.get("type") == _("Deduction"):
            deduction.append(r.get("name"))

    return earning, deduction


def sort_components_by_sequence(comp_iterable):
    """
    Accepts an iterable/set of salary component names and returns a list sorted
    by custom_sequence_id asc, then name asc. If a component is missing from DB,
    it won't appear in the result.
    """
    if not comp_iterable:
        return []

    names = list(comp_iterable)
    rows = frappe.get_all(
        "Salary Component",
        filters={"name": ("in", names)},
        fields=["name", "custom_sequence_id"],
        order_by="custom_sequence_id asc, name asc",
    )

    # maintain only the names in order
    return [r.get("name") for r in rows]


def update_column_width(ss, columns):
    if ss.branch:
        columns[3]["width"] = 120
    if ss.department:
        columns[4]["width"] = 120
    if ss.designation:
        columns[5]["width"] = 120
    if ss.leave_without_pay:
        columns[9]["width"] = 120


def get_columns(earning_types, ded_types, ex_earning_types, ex_deduction_types):
    columns = [
        {
            "label": _("Salary Slip ID"),
            "fieldname": "salary_slip_id",
            "fieldtype": "Link",
            "options": "Salary Slip",
            "width": 150,
        },
        {
            "label": _("Employee"),
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 120,
        },
        {
            "label": _("Employee Name"),
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 140,
        },
        {
            "label": _("Employee State"),
            "fieldname": "employee_state",
            "fieldtype": "Data",
            "width": 140,
        },
        {
            "label": _("Income Tax Slab"),
            "fieldname": "income_tax_slab",
            "fieldtype": "Data",
            "width": 140,
        },
        {
            "label": _("Date of Joining"),
            "fieldname": "data_of_joining",
            "fieldtype": "Date",
            "width": 80,
        },
        {
            "label": _("Branch"),
            "fieldname": "branch",
            "fieldtype": "Link",
            "options": "Branch",
            "width": 80,
        },
        {
            "label": _("Department"),
            "fieldname": "department",
            "fieldtype": "Link",
            "options": "Department",
            "width": 80,
        },
        {
            "label": _("Designation"),
            "fieldname": "designation",
            "fieldtype": "Link",
            "options": "Designation",
            "width": 120,
        },
        {
            "label": _("Company"),
            "fieldname": "company",
            "fieldtype": "Link",
            "options": "Company",
            "width": 120,
        },
        {
            "label": _("Start Date"),
            "fieldname": "start_date",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": _("End Date"),
            "fieldname": "end_date",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": _("Total Working Days"),
            "fieldname": "total_working_days",
            "fieldtype": "Float",
            "width": 150,
        },
        {
            "label": _("Leave Without Pay"),
            "fieldname": "leave_without_pay",
            "fieldtype": "Float",
            "width": 150,
        },
        {
            "label": _("Absent Days"),
            "fieldname": "absent_days",
            "fieldtype": "Float",
            "width": 150,
        },
        {
            "label": _("Payment Days"),
            "fieldname": "payment_days",
            "fieldtype": "Float",
            "width": 150,
        },
        {
            "label": _("Arrear Days"),
            "fieldname": "arrear_days",
            "fieldtype": "Float",
            "width": 150,
        },
        {
            "label": _("Annual CTC"),
            "fieldname": "annual_ctc",
            "fieldtype": "Float",
            "width": 150,
        },
        {
            "label": _("Monthly CTC"),
            "fieldname": "monthly_ctc",
            "fieldtype": "Float",
            "width": 150,
        },
    ]

    # included earnings (in sequence)
    for e in earning_types:
        columns.append(
            {
                "label": e,
                "fieldname": frappe.scrub(e),
                "fieldtype": "Currency",
                "options": "currency",
                "width": 120,
            }
        )

    # Gross Earnings
    columns.append(
        {
            "label": _("Gross Earnings"),
            "fieldname": "gross_pay",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120,
        }
    )

    # excluded earnings (in sequence)
    for ex in ex_earning_types:
        columns.append(
            {
                "label": f"{ex} (Excluded)",
                "fieldname": frappe.scrub(ex + "_excluded"),
                "fieldtype": "Currency",
                "options": "currency",
                "width": 120,
            }
        )

    # total income
    columns.append(
        {
            "label": _("Total Income"),
            "fieldname": "total_income",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 150,
        }
    )

    # included deductions (in sequence)
    for d in ded_types:
        columns.append(
            {
                "label": d,
                "fieldname": frappe.scrub(d),
                "fieldtype": "Currency",
                "options": "currency",
                "width": 120,
            }
        )

    # Final totals (Loan Repayment, Total Deduction)
    columns.extend(
        [
            {
                "label": _("Loan Repayment"),
                "fieldname": "total_loan_repayment",
                "fieldtype": "Currency",
                "options": "currency",
                "width": 120,
            },
            {
                "label": _("Total Deduction"),
                "fieldname": "total_deduction",
                "fieldtype": "Currency",
                "options": "currency",
                "width": 120,
            },
        ]
    )

    # Add excluded deduction columns AFTER Total Deduction (in sequence)
    for exd in ex_deduction_types:
        columns.append(
            {
                "label": f"{exd} (Excluded)",
                "fieldname": frappe.scrub(exd + "_excluded"),
                "fieldtype": "Currency",
                "options": "currency",
                "width": 120,
            }
        )

    # Finally add Net Pay
    columns.append(
        {
            "label": _("Net Pay"),
            "fieldname": "net_pay",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120,
        }
    )

    return columns


# =======================================================================


def get_salary_components(salary_slips):
    """
    Return distinct salary component names used in the given salary_slips.
    (Only components with amount != 0 and do_not_include_in_total == 0)
    """
    return (
        frappe.qb.from_(salary_detail)
        .where(
            (salary_detail.amount != 0)
            & (salary_detail.parent.isin([d.name for d in salary_slips]))
            & (salary_detail.do_not_include_in_total == 0)
        )
        .select(salary_detail.salary_component)
        .distinct()
    ).run(pluck=True)


def get_salary_component_type(salary_component):
    return frappe.db.get_value("Salary Component", salary_component, "type", cache=True)


def get_salary_slips(filters, company_currency):
    doc_status = {"Draft": 0, "Submitted": 1, "Cancelled": 2}

    query = frappe.qb.from_(salary_slip).select(salary_slip.star)

    if filters.get("docstatus"):
        query = query.where(
            salary_slip.docstatus == doc_status[filters.get("docstatus")]
        )
    if filters.get("from_date"):
        query = query.where(salary_slip.start_date >= filters.get("from_date"))
    if filters.get("to_date"):
        query = query.where(salary_slip.end_date <= filters.get("to_date"))
    if filters.get("company"):
        query = query.where(salary_slip.company == filters.get("company"))
    if filters.get("employee"):
        query = query.where(salary_slip.employee == filters.get("employee"))
    if filters.get("currency") and filters.get("currency") != company_currency:
        query = query.where(salary_slip.currency == filters.get("currency"))

    return query.run(as_dict=1) or []


def get_employee_doj_map():
    employee = frappe.qb.DocType("Employee")
    rows = (
        frappe.qb.from_(employee).select(employee.name, employee.date_of_joining).run()
    )
    return frappe._dict(rows)


# =======================================================================
# Included components (do_not_include_in_total = 0)
# =======================================================================


def get_salary_slip_details(salary_slips, currency, company_currency, component_type):
    slip_names = [ss.name for ss in salary_slips]

    rows = (
        frappe.qb.from_(salary_slip)
        .join(salary_detail)
        .on(salary_slip.name == salary_detail.parent)
        .where(
            (salary_detail.parent.isin(slip_names))
            & (salary_detail.parentfield == component_type)
            & (salary_detail.do_not_include_in_total == 0)
        )
        .select(
            salary_detail.parent,
            salary_detail.salary_component,
            salary_detail.amount,
            salary_slip.exchange_rate,
        )
    ).run(as_dict=1)

    m = {}

    for d in rows:
        m.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, 0.0)
        if currency == company_currency:
            m[d.parent][d.salary_component] += flt(d.amount) * flt(d.exchange_rate or 1)
        else:
            m[d.parent][d.salary_component] += flt(d.amount)

    return m


# =======================================================================
# Excluded earnings (do_not_include_in_total = 1)
# =======================================================================


def get_excluded_earning_details(salary_slips, currency, company_currency):
    slip_names = [ss.name for ss in salary_slips]

    rows = (
        frappe.qb.from_(salary_slip)
        .join(salary_detail)
        .on(salary_slip.name == salary_detail.parent)
        .where(
            (salary_detail.parent.isin(slip_names))
            & (salary_detail.parentfield == "earnings")
            & (salary_detail.do_not_include_in_total == 1)
        )
        .select(
            salary_detail.parent,
            salary_detail.salary_component,
            salary_detail.amount,
            salary_slip.exchange_rate,
        )
    ).run(as_dict=1)

    m = {}

    for d in rows:
        m.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, 0.0)
        if currency == company_currency:
            m[d.parent][d.salary_component] += flt(d.amount) * flt(d.exchange_rate or 1)
        else:
            m[d.parent][d.salary_component] += flt(d.amount)

    return m


# =======================================================================
# Excluded deductions (do_not_include_in_total = 1)
# =======================================================================


def get_excluded_deduction_details(salary_slips, currency, company_currency):
    slip_names = [ss.name for ss in salary_slips]

    rows = (
        frappe.qb.from_(salary_slip)
        .join(salary_detail)
        .on(salary_slip.name == salary_detail.parent)
        .where(
            (salary_detail.parent.isin(slip_names))
            & (salary_detail.parentfield == "deductions")
            & (salary_detail.do_not_include_in_total == 1)
        )
        .select(
            salary_detail.parent,
            salary_detail.salary_component,
            salary_detail.amount,
            salary_slip.exchange_rate,
        )
    ).run(as_dict=1)

    m = {}

    for d in rows:
        m.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, 0.0)
        if currency == company_currency:
            m[d.parent][d.salary_component] += flt(d.amount) * flt(d.exchange_rate or 1)
        else:
            m[d.parent][d.salary_component] += flt(d.amount)

    return m
