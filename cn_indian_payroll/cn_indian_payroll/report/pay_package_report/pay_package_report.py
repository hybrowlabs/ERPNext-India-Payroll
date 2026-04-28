
import frappe
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip


def get_all_employee(filters=None):

    if filters is None:
        filters = {}

    conditions = {"docstatus": 1}

    if filters.get("employee"):
        conditions["employee"] = filters["employee"]

    if filters.get("payroll_period"):
        conditions["custom_payroll_period"] = filters["payroll_period"]

    if filters.get("from_date"):
        conditions["from_date"] = (">=", filters["from_date"])

    if filters.get("company"):
        conditions["company"] = filters["company"]

    salary_assignments = frappe.get_list(
        "Salary Structure Assignment",
        filters=conditions,
        fields=["*"]
    )

    data = []
    reimbursement_components = set()
    variable_components = set()

    # ---------------- Employee Mapping ----------------

    employee_map = {
        d.user_id: (d.name, d.employee_name)
        for d in frappe.get_all(
            "Employee",
            filters={"user_id": ["!=", ""]},
            fields=["name", "employee_name", "user_id"]
        )
    }

    # ---------------- CTC Components ----------------

    ctc_components = frappe.get_all(
        "Salary Component",
        filters={"custom_is_part_of_ctc": 1},
        fields=["name", "custom_sequence"],
        order_by="custom_sequence asc"
    )

    ctc_components_list = [d.name for d in ctc_components]
    ctc_lookup = set(ctc_components_list)

    # ---------------- Loop Employees ----------------

    for ssa in salary_assignments:

        # Created By Formatting
        emp = employee_map.get(ssa.owner)

        if emp:
            created_by_value = f"{emp[0]} ({emp[1]})"
        else:
            created_by_value = ssa.owner

        row = {
            "employee": ssa.employee,
            "employee_name": ssa.employee_name,
            "from_date": ssa.from_date,
            "doj": ssa.custom_date_of_joining,
            "pf_type": ssa.custom_epf_type,
            "salary_structure": ssa.salary_structure,
            "created_on": ssa.creation,
            "created_by": created_by_value,

            "fixed_gross_annual": ssa.custom_fixed_gross_annual or 0,
            "fixed_gross_monthly": round((ssa.custom_fixed_gross_annual or 0) / 12)
            if ssa.custom_fixed_gross_annual else 0,

            "base": ssa.base,
            "monthly_ctc": round((ssa.base or 0) / 12),
            "regime": ssa.income_tax_slab,
        }

        # Load full SSA document
        ssa_doc = frappe.get_doc("Salary Structure Assignment", ssa.name)

        # -------- Variable Pay Components --------

        if hasattr(ssa_doc, "custom_variable_pay_components"):

            for comp in ssa_doc.custom_variable_pay_components:

                component = comp.variable_name
                amount = comp.amount or 0
                part_of_ctc = 1 if comp.part_of_ctc else 0

                variable_components.add(component)

                row[component] = round(row.get(component, 0) + amount)
                row[f"{component}_part_of_ctc"] = part_of_ctc

        # -------- Reimbursements --------

        reimbursements = frappe.get_all(
            "Employee Reimbursements",
            filters={"parent": ssa.name},
            fields=["reimbursements", "monthly_total_amount"]
        )

        for r in reimbursements:

            component = r.reimbursements
            amount = r.monthly_total_amount or 0

            reimbursement_components.add(component)

            row[component] = round(row.get(component, 0) + amount)

        # -------- Salary Slip Preview --------

        salary_slip = make_salary_slip(
            source_name=ssa.salary_structure,
            employee=ssa.employee,
            posting_date=ssa.from_date,
            for_preview=1
        )

        # Earnings

        for earning in salary_slip.earnings:

            component = earning.salary_component

            if component in ctc_lookup:
                row[component] = round(row.get(component, 0) + (earning.amount or 0))

        # Deductions

        for deduction in salary_slip.deductions:

            component = deduction.salary_component

            if component in ctc_lookup:
                row[component] = round(row.get(component, 0) + (deduction.amount or 0))

        data.append(row)

    # ---------------- Columns ----------------

    columns = [

        {"label": "Employee", "fieldname": "employee", "fieldtype": "Data", "width": 140},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 200},
        {"label": "Date of Joining", "fieldname": "doj", "fieldtype": "Date", "width": 130},
        {"label": "PF Type", "fieldname": "pf_type", "fieldtype": "Data", "width": 120},
        {"label": "Salary Structure", "fieldname": "salary_structure", "fieldtype": "Data", "width": 180},
        {"label": "Created On", "fieldname": "created_on", "fieldtype": "Datetime", "width": 160},
        {"label": "Created By", "fieldname": "created_by", "fieldtype": "Data", "width": 200},

        {"label": "Effective From", "fieldname": "from_date", "fieldtype": "Date", "width": 130},
        {"label": "Fixed Gross Annual", "fieldname": "fixed_gross_annual", "fieldtype": "Currency", "width": 160},
        {"label": "Fixed Gross Monthly", "fieldname": "fixed_gross_monthly", "fieldtype": "Currency", "width": 160},
        {"label": "Total Annual CTC", "fieldname": "base", "fieldtype": "Currency", "width": 160},
        {"label": "Total Monthly CTC", "fieldname": "monthly_ctc", "fieldtype": "Currency", "width": 160},
        {"label": "Income Tax Regime", "fieldname": "regime", "fieldtype": "Data", "width": 150},
    ]

    # -------- CTC Components --------

    for comp in ctc_components_list:

        columns.append({
            "label": comp,
            "fieldname": comp,
            "fieldtype": "Currency",
            "width": 140,
        })

    # -------- Variable Components --------

    for comp in variable_components:

        columns.append({
            "label": comp,
            "fieldname": comp,
            "fieldtype": "Currency",
            "width": 140,
        })

        columns.append({
            "label": f"{comp} Part of CTC",
            "fieldname": f"{comp}_part_of_ctc",
            "fieldtype": "Check",
            "width": 140,
        })

    # -------- Reimbursements --------

    for comp in reimbursement_components:

        columns.append({
            "label": comp,
            "fieldname": comp,
            "fieldtype": "Currency",
            "width": 140,
        })

    return columns, data


def execute(filters=None):

    columns, data = get_all_employee(filters)

    return columns, data