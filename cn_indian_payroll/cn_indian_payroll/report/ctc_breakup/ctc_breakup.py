# import frappe
# from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip


# def get_all_employee(filters=None):
#     if filters is None:
#         filters = {}

#     conditions1 = {"docstatus": 1}

#     if filters.get("employee"):
#         conditions1["employee"] = filters["employee"]
#     if filters.get("payroll_period"):
#         conditions1["custom_payroll_period"] = filters["payroll_period"]
#     if filters.get("from_date"):
#         conditions1["from_date"] = (">=", filters["from_date"])

#     if filters.get("company"):
#         conditions1["company"] =  filters["company"]

#     get_all_ssa = frappe.get_list(
#         "Salary Structure Assignment", filters=conditions1, fields=["*"]
#     )

#     salary_components = set()
#     reimbursement_components = set()
#     data = []

#     ctc_components = frappe.get_all(
#         "Salary Component",
#         filters={"custom_is_part_of_ctc": 1},
#         fields=["*"],
#         order_by="custom_sequence asc",
#     )
#     ctc_components_set = set(component.name for component in ctc_components)

#     for each_employee in get_all_ssa:

#         row = {
#             "employee": each_employee.get("employee"),
#             "employee_name": each_employee.get("employee_name"),
#             "from_date": each_employee.get("from_date"),
#             "doj": each_employee.get("custom_date_of_joining"),

#             "fixed_gross_annual":each_employee.get("custom_fixed_gross_annual") if each_employee.get("custom_fixed_gross_annual") else 0,
#             "fixed_gross_monthly":round(each_employee.get("custom_fixed_gross_annual")/12) if each_employee.get("custom_fixed_gross_annual") else 0,

#             "base": each_employee.get("base"),
#             "monthly_ctc": round(each_employee.get("base") / 12),
#             "regime": each_employee.get("income_tax_slab"),
#         }


#         reimbursements = frappe.get_all(
#             "Employee Reimbursements",
#             filters={"parent": each_employee.get("name")},
#             fields=["reimbursements", "monthly_total_amount"],
#         )

#         for reimbursement in reimbursements:
#             component_name = reimbursement.get("reimbursements")
#             amount = reimbursement.get("monthly_total_amount")

#             if component_name:
#                 reimbursement_components.add(component_name)
#                 row[component_name] = round(row.get(component_name, 0) + amount)

#         # Generate the salary slip for each employee
#         salary_slip = make_salary_slip(
#             source_name=each_employee.get("salary_structure"),
#             employee=each_employee.get("employee"),
#             print_format="Salary Slip Standard",
#             posting_date=each_employee.get("from_date"),
#             for_preview=1,
#         )

#         for earning in salary_slip.earnings:
#             component_name = earning.salary_component
#             if component_name in ctc_components_set:
#                 amount = earning.amount
#                 salary_components.add(component_name)
#                 row[component_name] = round(row.get(component_name, 0) + amount)

#         # Process deductions
#         for deduction in salary_slip.deductions:
#             component_name = deduction.salary_component
#             if component_name in ctc_components_set:
#                 amount = deduction.amount
#                 salary_components.add(component_name)
#                 row[component_name] = round(row.get(component_name, 0) + amount)


#         data.append(row)

#     # Define columns with employee details, salary components, and allowances
#     columns = [
#         {
#             "label": "Employee",
#             "fieldname": "employee",
#             "fieldtype": "Data",
#             "width": 150,
#         },
#         {
#             "label": "Employee Name",
#             "fieldname": "employee_name",
#             "fieldtype": "Data",
#             "width": 200,
#         },
#         {
#             "label": "Date of Joining",
#             "fieldname": "doj",
#             "fieldtype": "Date",
#             "width": 200,
#         },
#         {
#             "label": "Effective From",
#             "fieldname": "from_date",
#             "fieldtype": "Date",
#             "width": 200,
#         },
#         {
#             "label": "Fixed Gross Annual",
#             "fieldname": "fixed_gross_annual",
#             "fieldtype": "Currency",
#             "width": 200,
#         },
#         {
#             "label": "Fixed Gross Monthly",
#             "fieldname": "fixed_gross_monthly",
#             "fieldtype": "Currency",
#             "width": 200,
#         },

#         {"label": "Annual CTC", "fieldname": "base", "fieldtype": "Data", "width": 200},
#         {
#             "label": "Monthly CTC",
#             "fieldname": "monthly_ctc",
#             "fieldtype": "Data",
#             "width": 200,
#         },
#         {
#             "label": "Income Tax Regime",
#             "fieldname": "regime",
#             "fieldtype": "Data",
#             "width": 200,
#         },
#     ]

#     # Adding salary components to the columns
#     for component in salary_components:
#         columns.append(
#             {
#                 "label": component,
#                 "fieldname": component,
#                 "fieldtype": "Currency",
#                 "width": 150,
#             }
#         )



#     # Adding reimbursement components to the columns
#     for component in reimbursement_components:
#         columns.append(
#             {
#                 "label": component,
#                 "fieldname": component,
#                 "fieldtype": "Currency",
#                 "width": 150,
#             }
#         )

#     return columns, data


# def execute(filters=None):
#     columns, data = get_all_employee(filters)
#     return columns, data


# import frappe
# from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip

# def get_all_employee(filters=None):
#     if filters is None:
#         filters = {}

#     conditions1 = {"docstatus": 1}

#     if filters.get("employee"):
#         conditions1["employee"] = filters["employee"]
#     if filters.get("payroll_period"):
#         conditions1["custom_payroll_period"] = filters["payroll_period"]
#     if filters.get("from_date"):
#         conditions1["from_date"] = (">=", filters["from_date"])
#     if filters.get("company"):
#         conditions1["company"] = filters["company"]

#     get_all_ssa = frappe.get_list(
#         "Salary Structure Assignment", filters=conditions1, fields=["*"]
#     )

#     reimbursement_components = set()
#     data = []

#     # Get CTC components in custom_sequence order
#     ctc_components = frappe.get_all(
#         "Salary Component",
#         filters={"custom_is_part_of_ctc": 1},
#         fields=["name", "custom_sequence"],
#         order_by="custom_sequence asc",
#     )
#     ctc_components_list = [component.name for component in ctc_components]  # ordered
#     ctc_components_lookup = set(ctc_components_list)  # for membership checking

#     for each_employee in get_all_ssa:

#         each_doc=frappe.get_doc("Salary Strucrte Assignment",each_employee.name)
#         for i in custom_variable_pay_components:
#             if i.part_of_ctc:
#                 array.append{"
#                 "component":i.variable_name,
#                 "amount":i.amount}
#             else:
#                 array.append{"
#                 "component":i.variable_name,
#                 "amount":i.amount}



#         row = {
#             "employee": each_employee.get("employee"),
#             "employee_name": each_employee.get("employee_name"),
#             "from_date": each_employee.get("from_date"),
#             "doj": each_employee.get("custom_date_of_joining"),
#             "pf_type":each_employee.get("custom_epf_type"),
#             "salary_structure":each_employee.get("salary_structure"),
#             "created_on": each_employee.get("creation"),
#             "created_by": each_employee.get("owner"),

#             "fixed_gross_annual": each_employee.get("custom_fixed_gross_annual") or 0,
#             "fixed_gross_monthly": round((each_employee.get("custom_fixed_gross_annual") or 0) / 12)
#                 if each_employee.get("custom_fixed_gross_annual") else 0,
#             "base": each_employee.get("base"),
#             "monthly_ctc": round((each_employee.get("base") or 0) / 12),
#             "regime": each_employee.get("income_tax_slab"),
#         }

#         # Reimbursements
#         reimbursements = frappe.get_all(
#             "Employee Reimbursements",
#             filters={"parent": each_employee.get("name")},
#             fields=["reimbursements", "monthly_total_amount"],
#         )
#         for reimbursement in reimbursements:
#             component_name = reimbursement.get("reimbursements")
#             amount = reimbursement.get("monthly_total_amount")
#             if component_name:
#                 reimbursement_components.add(component_name)
#                 row[component_name] = round(row.get(component_name, 0) + (amount or 0))

#         # Generate salary slip preview
#         salary_slip = make_salary_slip(
#             source_name=each_employee.get("salary_structure"),
#             employee=each_employee.get("employee"),
#             print_format="Salary Slip Standard",
#             posting_date=each_employee.get("from_date"),
#             for_preview=1,
#         )

#         # Earnings
#         for earning in salary_slip.earnings:
#             component_name = earning.salary_component
#             if component_name in ctc_components_lookup:
#                 amount = earning.amount
#                 row[component_name] = round(row.get(component_name, 0) + (amount or 0))

#         # Deductions
#         for deduction in salary_slip.deductions:
#             component_name = deduction.salary_component
#             if component_name in ctc_components_lookup:
#                 amount = deduction.amount
#                 row[component_name] = round(row.get(component_name, 0) + (amount or 0))

#         data.append(row)

#     # Columns
#     columns = [
#         {"label": "Employee", "fieldname": "employee", "fieldtype": "Data", "width": 150},
#         {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 200},
#         {"label": "Date of Joining", "fieldname": "doj", "fieldtype": "Date", "width": 200},
#         {"label": "PF Type", "fieldname": "pf_type", "fieldtype": "Data", "width": 200},
#         {"label": "Salary Structure", "fieldname": "salary_structure", "fieldtype": "Data", "width": 200},
#         {"label": "Created On", "fieldname": "created_on", "fieldtype": "Datetime", "width": 180},
#         {"label": "Created By", "fieldname": "created_by", "fieldtype": "Data", "width": 180},


#         {"label": "Effective From", "fieldname": "from_date", "fieldtype": "Date", "width": 200},
#         {"label": "Fixed Gross Annual", "fieldname": "fixed_gross_annual", "fieldtype": "Currency", "width": 200},
#         {"label": "Fixed Gross Monthly", "fieldname": "fixed_gross_monthly", "fieldtype": "Currency", "width": 200},
#         {"label": "Fixed CTC Annual", "fieldname": "fixed_gross_monthly", "fieldtype": "Currency", "width": 200},
#         {"label": "Fixed CTC Monthly", "fieldname": "fixed_gross_monthly", "fieldtype": "Currency", "width": 200},
#         {"label": "Total Annual CTC", "fieldname": "base", "fieldtype": "Data", "width": 200},
#         {"label": "Total Monthly CTC", "fieldname": "monthly_ctc", "fieldtype": "Data", "width": 200},
#         {"label": "Income Tax Regime", "fieldname": "regime", "fieldtype": "Data", "width": 200},
#     ]

#     # Add CTC components in custom_sequence order
#     for component in ctc_components_list:
#         columns.append({
#             "label": component,
#             "fieldname": component,
#             "fieldtype": "Currency",
#             "width": 150,
#         })

#     # Add reimbursement components (order here doesn’t matter, they’re dynamic)
#     for component in reimbursement_components:
#         columns.append({
#             "label": component,
#             "fieldname": component,
#             "fieldtype": "Currency",
#             "width": 150,
#         })

#     return columns, data

# def execute(filters=None):
#     columns, data = get_all_employee(filters)
#     return columns, data


# import frappe
# from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip


# def get_all_employee(filters=None):
#     if filters is None:
#         filters = {}

#     conditions = {"docstatus": 1}

#     if filters.get("employee"):
#         conditions["employee"] = filters["employee"]

#     if filters.get("payroll_period"):
#         conditions["custom_payroll_period"] = filters["payroll_period"]

#     if filters.get("from_date"):
#         conditions["from_date"] = (">=", filters["from_date"])

#     if filters.get("company"):
#         conditions["company"] = filters["company"]

#     salary_assignments = frappe.get_list(
#         "Salary Structure Assignment",
#         filters=conditions,
#         fields=["*"]
#     )

#     reimbursement_components = set()
#     variable_components_set = set()
#     data = []

#     # Get CTC components ordered
#     ctc_components = frappe.get_all(
#         "Salary Component",
#         filters={"custom_is_part_of_ctc": 1},
#         fields=["name", "custom_sequence"],
#         order_by="custom_sequence asc",
#     )

#     ctc_components_list = [d.name for d in ctc_components]
#     ctc_lookup = set(ctc_components_list)

#     for ssa in salary_assignments:

#         row = {
#             "employee": ssa.employee,
#             "employee_name": ssa.employee_name,
#             "from_date": ssa.from_date,
#             "doj": ssa.custom_date_of_joining,
#             "pf_type": ssa.custom_epf_type,
#             "salary_structure": ssa.salary_structure,
#             "created_on": ssa.creation,
#             "created_by": ssa.owner,

#             "fixed_gross_annual": ssa.custom_fixed_gross_annual or 0,
#             "fixed_gross_monthly": round((ssa.custom_fixed_gross_annual or 0) / 12)
#             if ssa.custom_fixed_gross_annual else 0,

#             "base": ssa.base,
#             "monthly_ctc": round((ssa.base or 0) / 12),
#             "regime": ssa.income_tax_slab,
#         }

#         # Load full SSA doc
#         ssa_doc = frappe.get_doc("Salary Structure Assignment", ssa.name)

#         # Variable Pay Components
#         if hasattr(ssa_doc, "custom_variable_pay_components"):
#             for comp in ssa_doc.custom_variable_pay_components:

#                 component = comp.variable_name
#                 amount = comp.amount or 0
#                 part_of_ctc = 1 if comp.part_of_ctc else 0

#                 variable_components_set.add(component)

#                 row[component] = round(row.get(component, 0) + amount)
#                 row[f"{component}_part_of_ctc"] = part_of_ctc

#         # Reimbursements
#         reimbursements = frappe.get_all(
#             "Employee Reimbursements",
#             filters={"parent": ssa.name},
#             fields=["reimbursements", "monthly_total_amount"]
#         )

#         for r in reimbursements:
#             comp = r.reimbursements
#             amount = r.monthly_total_amount or 0

#             reimbursement_components.add(comp)
#             row[comp] = round(row.get(comp, 0) + amount)

#         # Salary Slip Preview
#         salary_slip = make_salary_slip(
#             source_name=ssa.salary_structure,
#             employee=ssa.employee,
#             posting_date=ssa.from_date,
#             for_preview=1
#         )

#         # Earnings
#         for earning in salary_slip.earnings:
#             comp = earning.salary_component

#             if comp in ctc_lookup:
#                 row[comp] = round(row.get(comp, 0) + (earning.amount or 0))

#         # Deductions
#         for deduction in salary_slip.deductions:
#             comp = deduction.salary_component

#             if comp in ctc_lookup:
#                 row[comp] = round(row.get(comp, 0) + (deduction.amount or 0))

#         data.append(row)

#     # ---------------- Columns ----------------

#     columns = [
#         {"label": "Employee", "fieldname": "employee", "fieldtype": "Data", "width": 150},
#         {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 200},
#         {"label": "Date of Joining", "fieldname": "doj", "fieldtype": "Date", "width": 150},
#         {"label": "PF Type", "fieldname": "pf_type", "fieldtype": "Data", "width": 120},
#         {"label": "Salary Structure", "fieldname": "salary_structure", "fieldtype": "Data", "width": 200},
#         {"label": "Created On", "fieldname": "created_on", "fieldtype": "Datetime", "width": 160},
#         {"label": "Created By", "fieldname": "created_by", "fieldtype": "Data", "width": 150},

#         {"label": "Effective From", "fieldname": "from_date", "fieldtype": "Date", "width": 150},
#         {"label": "Fixed Gross Annual", "fieldname": "fixed_gross_annual", "fieldtype": "Currency", "width": 160},
#         {"label": "Fixed Gross Monthly", "fieldname": "fixed_gross_monthly", "fieldtype": "Currency", "width": 160},
#         {"label": "Total Annual CTC", "fieldname": "base", "fieldtype": "Currency", "width": 160},
#         {"label": "Total Monthly CTC", "fieldname": "monthly_ctc", "fieldtype": "Currency", "width": 160},
#         {"label": "Income Tax Regime", "fieldname": "regime", "fieldtype": "Data", "width": 150},
#     ]

#     # CTC Components
#     for comp in ctc_components_list:
#         columns.append({
#             "label": comp,
#             "fieldname": comp,
#             "fieldtype": "Currency",
#             "width": 140,
#         })

#     # Variable Pay Columns
#     for comp in variable_components_set:

#         columns.append({
#             "label": comp,
#             "fieldname": comp,
#             "fieldtype": "Currency",
#             "width": 140,
#         })

#         columns.append({
#             "label": f"{comp} Part of CTC",
#             "fieldname": f"{comp}_part_of_ctc",
#             "fieldtype": "Check",
#             "width": 120,
#         })

#     # Reimbursements
#     for comp in reimbursement_components:
#         columns.append({
#             "label": comp,
#             "fieldname": comp,
#             "fieldtype": "Currency",
#             "width": 140,
#         })

#     return columns, data


# def execute(filters=None):
#     columns, data = get_all_employee(filters)
#     return columns, data


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