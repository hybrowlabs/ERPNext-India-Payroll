


import frappe
from datetime import datetime

def get_salary_slips(filters=None):
    basic_component=None
    da_component=None
    if filters is None:
        filters = {}

    conditions = {"docstatus": ["in", [0, 1]]}

    if filters.get("month"):
        conditions["custom_month"] = filters["month"]

    if filters.get("payroll_period"):
        conditions["custom_payroll_period"] = filters["payroll_period"]

    if filters.get("company"):
        conditions["company"] = filters["company"]

        try:
            company_doc = frappe.get_doc("Company", filters["company"])
        except frappe.DoesNotExistError:
            frappe.throw("Invalid company specified.")

        if not company_doc.basic_component or not company_doc.custom_da_component:
            frappe.throw("Please set Basic Component and DA Component in Company Master.")

        basic_component = company_doc.basic_component
        da_component = company_doc.custom_da_component
    else:
        frappe.throw("Company is a mandatory filter.")

    salary_slips = frappe.get_list(
        'Salary Slip',
        fields=["name", "employee", "custom_month", "custom_payroll_period", "company", "gross_pay"],
        filters=conditions,
        order_by="name DESC",
    )

    detailed_salary_slips = []

    for slip in salary_slips:
        each_salary_slip = frappe.get_doc('Salary Slip', slip["name"])
        each_employee = frappe.get_doc("Employee", each_salary_slip.employee)

        pf_account = frappe.get_value(
            "Salary Structure Assignment",
            {"employee": each_salary_slip.employee},
            ["name", "custom_is_epf"],
            as_dict=True
        )

        if not pf_account or not pf_account.custom_is_epf:
            continue  # Skip if not EPF eligible

        basic = 0
        da = 0
        epf_amount_employee = 0
        epf_amount_employer = 0
        eps_amount = 0

        for earning in each_salary_slip.earnings:
            if earning.salary_component == basic_component:
                basic += earning.amount
            get_doc = frappe.get_doc("Salary Component", earning.salary_component)
            if get_doc.arrear_component == 1:
                basic += earning.amount
            if earning.salary_component == da_component:
                da += earning.amount
            if get_doc.arrear_component == 1:
                da += earning.amount

        for deduction in each_salary_slip.deductions:
            get_epf_component = frappe.get_doc("Salary Component", deduction.salary_component)
            if get_epf_component.component_type == "Provident Fund":
                epf_amount_employee += deduction.amount

        epf_edli_eligible_wage = round(float(basic or 0) + float(da or 0))

        # EPS eligibility check
        joining_date = getattr(each_employee, "date_of_joining", None)
        is_eps_applicable = True

        if joining_date and epf_edli_eligible_wage > 15000:
            if joining_date > datetime(2014, 9, 1).date():
                is_eps_applicable = False

        if is_eps_applicable:
            eps_eligible_wage = min(epf_edli_eligible_wage, 15000)
            epf_amount_employer = eps_eligible_wage * 8.33 / 100
            eps_amount = epf_edli_eligible_wage * 3.67 / 100
        else:
            eps_eligible_wage = 0
            epf_amount_employer = 0
            eps_amount = epf_edli_eligible_wage * 12 / 100  # Full to EPF

        detailed_salary_slips.append({
            "employee": each_salary_slip.employee,
            "employee_name": each_salary_slip.employee_name,
            "custom_month": each_salary_slip.custom_month,
            "custom_payroll_period": each_salary_slip.custom_payroll_period,
            "company": each_salary_slip.company,
            "uan": getattr(each_employee, "custom_uan", None),
            "gross_pay": round(each_salary_slip.gross_pay),
            "epf_wages": epf_edli_eligible_wage,
            "eps_wages": eps_eligible_wage,
            "edli_wages": epf_edli_eligible_wage,
            "ncp_days": each_salary_slip.custom_total_leave_without_pay or 0,
            "refund": 0,
            "epf_amount_employee": round(epf_amount_employee),
            "epf_amount_employer": round(epf_amount_employer),
            "eps_amount": round(eps_amount),
        })

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

    data = get_salary_slips(filters)

    return columns, data



@frappe.whitelist()
def download_ecr_txt(filters=None):
    import json
    if isinstance(filters, str):
        filters = json.loads(filters)

    salary_data = get_salary_slips(filters)
    lines = []

    def r(value):
        return str(round(value or 0))

    for row in salary_data:
        line = "#~#".join([
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
        lines.append(line)

    return "\n".join(lines)
