from datetime import datetime

import frappe


def get_salary_slips(filters=None):
    if filters is None:
        filters = {}

    if not filters.get("company"):
        frappe.throw("Company is a mandatory filter.")

    try:
        company_doc = frappe.get_cached_doc("Company", filters["company"])
    except frappe.DoesNotExistError:
        frappe.throw("Invalid company specified.")

    if not company_doc.basic_component or not company_doc.custom_da_component:
        frappe.throw("Please set Basic Component and DA Component in Company Master.")

    basic_component = company_doc.basic_component
    da_component = company_doc.custom_da_component

    conditions = {"docstatus": ["in", [0, 1]], "company": filters["company"]}
    if filters.get("month"):
        conditions["custom_month"] = filters["month"]
    if filters.get("payroll_period"):
        conditions["custom_payroll_period"] = filters["payroll_period"]

    salary_slips = frappe.get_all(
        "Salary Slip",
        filters=conditions,
        fields=["name", "employee", "employee_name", "custom_month", "custom_payroll_period",
                "company", "gross_pay", "custom_total_leave_without_pay"],
        order_by="name DESC",
    )
    if not salary_slips:
        return []

    slip_names = [s.name for s in salary_slips]
    emp_ids = list({s.employee for s in salary_slips})

    # Batch: EPF eligibility — one query
    epf_eligible_set = set(
        frappe.get_all(
            "Salary Structure Assignment",
            filters={"employee": ["in", emp_ids], "docstatus": 1, "custom_is_epf": 1},
            pluck="employee",
        )
    )

    # Batch: employee UAN and joining date — one query
    emp_map = {
        row.name: row
        for row in frappe.get_all(
            "Employee",
            filters={"name": ["in", emp_ids]},
            fields=["name", "custom_uan", "date_of_joining"],
        )
    }

    # Batch: all salary component types — one query
    all_components = frappe.get_all(
        "Salary Component",
        fields=["name", "component_type", "arrear_component"],
    )
    comp_map = {c.name: c for c in all_components}

    # Batch: all salary details for these slips — two queries (earnings + deductions)
    earnings_rows = frappe.get_all(
        "Salary Detail",
        filters={"parent": ["in", slip_names], "parentfield": "earnings"},
        fields=["parent", "salary_component", "amount"],
    )
    deductions_rows = frappe.get_all(
        "Salary Detail",
        filters={"parent": ["in", slip_names], "parentfield": "deductions"},
        fields=["parent", "salary_component", "amount"],
    )

    # Group details by slip name
    earnings_by_slip: dict[str, list] = {}
    for row in earnings_rows:
        earnings_by_slip.setdefault(row.parent, []).append(row)

    deductions_by_slip: dict[str, list] = {}
    for row in deductions_rows:
        deductions_by_slip.setdefault(row.parent, []).append(row)

    detailed_salary_slips = []

    for slip in salary_slips:
        if slip.employee not in epf_eligible_set:
            continue

        emp = emp_map.get(slip.employee)
        joining_date = emp.date_of_joining if emp else None

        basic = da = epf_amount_employee = 0

        for earning in earnings_by_slip.get(slip.name, []):
            comp = comp_map.get(earning.salary_component)
            if earning.salary_component == basic_component:
                basic += earning.amount or 0
            if earning.salary_component == da_component:
                da += earning.amount or 0
            if comp and comp.arrear_component:
                basic += earning.amount or 0
                da += earning.amount or 0

        for deduction in deductions_by_slip.get(slip.name, []):
            comp = comp_map.get(deduction.salary_component)
            if comp and comp.component_type == "Provident Fund":
                epf_amount_employee += deduction.amount or 0

        epf_edli_eligible_wage = round(float(basic) + float(da))

        is_eps_applicable = not (
            joining_date
            and epf_edli_eligible_wage > 15000
            and joining_date > datetime(2014, 9, 1).date()
        )

        if is_eps_applicable:
            eps_eligible_wage = min(epf_edli_eligible_wage, 15000)
            epf_amount_employer = eps_eligible_wage * 8.33 / 100
            eps_amount = epf_edli_eligible_wage * 3.67 / 100
        else:
            eps_eligible_wage = 0
            epf_amount_employer = 0
            eps_amount = epf_edli_eligible_wage * 12 / 100

        detailed_salary_slips.append(
            {
                "employee": slip.employee,
                "employee_name": slip.employee_name,
                "custom_month": slip.custom_month,
                "custom_payroll_period": slip.custom_payroll_period,
                "company": slip.company,
                "uan": emp.custom_uan if emp else None,
                "gross_pay": round(slip.gross_pay or 0),
                "epf_wages": epf_edli_eligible_wage,
                "eps_wages": eps_eligible_wage,
                "edli_wages": epf_edli_eligible_wage,
                "ncp_days": slip.custom_total_leave_without_pay or 0,
                "refund": 0,
                "epf_amount_employee": round(epf_amount_employee),
                "epf_amount_employer": round(epf_amount_employer),
                "eps_amount": round(eps_amount),
            }
        )

    return detailed_salary_slips


def execute(filters=None):
    columns = [
        {"fieldname": "uan", "label": "UAN", "fieldtype": "Data", "width": 150},
        {"fieldname": "employee", "label": "Employee", "fieldtype": "Link", "options": "Employee", "width": 150},
        {"fieldname": "employee_name", "label": "Employee Name", "fieldtype": "Data", "width": 200},
        {"fieldname": "custom_month", "label": "Month", "fieldtype": "Data", "width": 100},
        {"fieldname": "custom_payroll_period", "label": "Payroll Period", "fieldtype": "Data", "width": 150},
        {"fieldname": "company", "label": "Company", "fieldtype": "Link", "options": "Company", "width": 150},
        {"fieldname": "gross_pay", "label": "Gross Pay", "fieldtype": "Currency", "width": 150},
        {"fieldname": "epf_wages", "label": "EPF Wages", "fieldtype": "Currency", "width": 150},
        {"fieldname": "eps_wages", "label": "EPS Wages", "fieldtype": "Currency", "width": 150},
        {"fieldname": "edli_wages", "label": "EDLI Wages", "fieldtype": "Currency", "width": 150},
        {"fieldname": "epf_amount_employee", "label": "EPF Contribution (12%)", "fieldtype": "Currency", "width": 150},
        {"fieldname": "epf_amount_employer", "label": "EPS Contribution(8.33%)", "fieldtype": "Currency", "width": 150},
        {"fieldname": "eps_amount", "label": "EDLI Contribution", "fieldtype": "Currency", "width": 150},
        {"fieldname": "ncp_days", "label": "NCP Days", "fieldtype": "Float", "width": 120},
        {"fieldname": "refund", "label": "Refund Of Advances", "fieldtype": "Currency", "width": 150},
    ]

    return columns, get_salary_slips(filters)


@frappe.whitelist()
def download_ecr_txt(filters=None):
    import json

    frappe.only_for("HR Manager")

    if isinstance(filters, str):
        filters = json.loads(filters)

    salary_data = get_salary_slips(filters)

    def r(value):
        return str(round(value or 0))

    lines = [
        "#~#".join([
            str(row.get("uan") or "0"),
            row.get("employee_name") or "",
            r(row.get("gross_pay")),
            r(row.get("epf_wages")),
            r(row.get("eps_wages")),
            r(row.get("edli_wages")),
            r(row.get("epf_amount_employee")),
            r(row.get("epf_amount_employer")),
            r(row.get("eps_amount")),
            r(row.get("ncp_days")),
            r(row.get("refund")),
        ])
        for row in salary_data
    ]

    return "\n".join(lines)
