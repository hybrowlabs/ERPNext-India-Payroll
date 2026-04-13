import frappe

def get_salary_slips(filters=None):
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

        if filters.get("school") and each_employee.branch != filters["school"]:
            continue

        # Get salary structure assignment to check EPF eligibility
        pf_account = frappe.get_value(
            "Salary Structure Assignment",
            {"employee": each_salary_slip.employee},
            ["name", "custom_is_epf", "custom_is_eps"],
            as_dict=True
        )

        if not pf_account or not pf_account.custom_is_epf:
            continue  # Skip if not EPF eligible

        # Initialize basic and DA
        basic = 0
        da = 0

        for earning in each_salary_slip.earnings:
            if earning.salary_component == basic_component:
                basic = earning.amount
            if earning.salary_component == da_component:
                da = earning.amount

        is_eps = pf_account.get("custom_is_eps", 0)

        eligible_wage = min(round(float(basic or 0) + float(da or 0)), 15000)
        eps_wage = eligible_wage if is_eps else 0
        cr_ee = round(eligible_wage * 12 / 100)
        cr_eps = round(eligible_wage * 8.33 / 100) if is_eps else 0
        cr_er = cr_ee - cr_eps

        detailed_salary_slips.append({
            "uan": getattr(each_employee, "custom_uan", None),
            "employee_name": (each_salary_slip.employee_name or "").upper(),
            "gross_pay": basic,
            "epf_wages": eligible_wage,
            "eps_wages": eps_wage,
            "edli_wages": eligible_wage,
            "cr_ee": cr_ee,
            "cr_eps": cr_eps,
            "cr_er": cr_er,
            "ncp_days": each_salary_slip.custom_total_leave_without_pay or 0,
            "refund": 0,
        })

    return detailed_salary_slips

def execute(filters=None):
    columns = [
        {"fieldname": "uan", "label": "UAN", "fieldtype": "Data", "width": 150},
        {"fieldname": "employee_name", "label": "Employee Name", "fieldtype": "Data", "width": 200},
        {"fieldname": "gross_pay", "label": "Gross", "fieldtype": "Currency", "width": 150},
        {"fieldname": "epf_wages", "label": "Wage EPF", "fieldtype": "Currency", "width": 150},
        {"fieldname": "eps_wages", "label": "Wage EPS", "fieldtype": "Currency", "width": 150},
        {"fieldname": "edli_wages", "label": "Wage EDLI", "fieldtype": "Currency", "width": 150},
        {"fieldname": "cr_ee", "label": "CR EE", "fieldtype": "Currency", "width": 120},
        {"fieldname": "cr_eps", "label": "CR EPS", "fieldtype": "Currency", "width": 120},
        {"fieldname": "cr_er", "label": "CR ER", "fieldtype": "Currency", "width": 120},
        {"fieldname": "ncp_days", "label": "NCP Days", "fieldtype": "Float", "width": 120},
        {"fieldname": "refund", "label": "Refunds", "fieldtype": "Currency", "width": 150},
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
            str(row.get("uan", "")),
            row.get("employee_name", ""),
            r(row.get("gross_pay")),
            r(row.get("epf_wages")),
            r(row.get("eps_wages")),
            r(row.get("edli_wages")),
            r(row.get("cr_ee")),
            r(row.get("cr_eps")),
            r(row.get("cr_er")),
            r(row.get("ncp_days")),
            r(row.get("refund")),
        ])
        lines.append(line)

    return "\n".join(lines)
