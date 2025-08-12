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


import frappe
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip

def get_all_employee(filters=None):
    if filters is None:
        filters = {}

    conditions1 = {"docstatus": 1}

    if filters.get("employee"):
        conditions1["employee"] = filters["employee"]
    if filters.get("payroll_period"):
        conditions1["custom_payroll_period"] = filters["payroll_period"]
    if filters.get("from_date"):
        conditions1["from_date"] = (">=", filters["from_date"])
    if filters.get("company"):
        conditions1["company"] = filters["company"]

    get_all_ssa = frappe.get_list(
        "Salary Structure Assignment", filters=conditions1, fields=["*"]
    )

    reimbursement_components = set()
    data = []

    # Get CTC components in custom_sequence order
    ctc_components = frappe.get_all(
        "Salary Component",
        filters={"custom_is_part_of_ctc": 1},
        fields=["name", "custom_sequence"],
        order_by="custom_sequence asc",
    )
    ctc_components_list = [component.name for component in ctc_components]  # ordered
    ctc_components_lookup = set(ctc_components_list)  # for membership checking

    for each_employee in get_all_ssa:
        row = {
            "employee": each_employee.get("employee"),
            "employee_name": each_employee.get("employee_name"),
            "from_date": each_employee.get("from_date"),
            "doj": each_employee.get("custom_date_of_joining"),
            "fixed_gross_annual": each_employee.get("custom_fixed_gross_annual") or 0,
            "fixed_gross_monthly": round((each_employee.get("custom_fixed_gross_annual") or 0) / 12)
                if each_employee.get("custom_fixed_gross_annual") else 0,
            "base": each_employee.get("base"),
            "monthly_ctc": round((each_employee.get("base") or 0) / 12),
            "regime": each_employee.get("income_tax_slab"),
        }

        # Reimbursements
        reimbursements = frappe.get_all(
            "Employee Reimbursements",
            filters={"parent": each_employee.get("name")},
            fields=["reimbursements", "monthly_total_amount"],
        )
        for reimbursement in reimbursements:
            component_name = reimbursement.get("reimbursements")
            amount = reimbursement.get("monthly_total_amount")
            if component_name:
                reimbursement_components.add(component_name)
                row[component_name] = round(row.get(component_name, 0) + (amount or 0))

        # Generate salary slip preview
        salary_slip = make_salary_slip(
            source_name=each_employee.get("salary_structure"),
            employee=each_employee.get("employee"),
            print_format="Salary Slip Standard",
            posting_date=each_employee.get("from_date"),
            for_preview=1,
        )

        # Earnings
        for earning in salary_slip.earnings:
            component_name = earning.salary_component
            if component_name in ctc_components_lookup:
                amount = earning.amount
                row[component_name] = round(row.get(component_name, 0) + (amount or 0))

        # Deductions
        for deduction in salary_slip.deductions:
            component_name = deduction.salary_component
            if component_name in ctc_components_lookup:
                amount = deduction.amount
                row[component_name] = round(row.get(component_name, 0) + (amount or 0))

        data.append(row)

    # Columns
    columns = [
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Data", "width": 150},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 200},
        {"label": "Date of Joining", "fieldname": "doj", "fieldtype": "Date", "width": 200},
        {"label": "Effective From", "fieldname": "from_date", "fieldtype": "Date", "width": 200},
        {"label": "Fixed Gross Annual", "fieldname": "fixed_gross_annual", "fieldtype": "Currency", "width": 200},
        {"label": "Fixed Gross Monthly", "fieldname": "fixed_gross_monthly", "fieldtype": "Currency", "width": 200},
        {"label": "Annual CTC", "fieldname": "base", "fieldtype": "Data", "width": 200},
        {"label": "Monthly CTC", "fieldname": "monthly_ctc", "fieldtype": "Data", "width": 200},
        {"label": "Income Tax Regime", "fieldname": "regime", "fieldtype": "Data", "width": 200},
    ]

    # Add CTC components in custom_sequence order
    for component in ctc_components_list:
        columns.append({
            "label": component,
            "fieldname": component,
            "fieldtype": "Currency",
            "width": 150,
        })

    # Add reimbursement components (order here doesn’t matter, they’re dynamic)
    for component in reimbursement_components:
        columns.append({
            "label": component,
            "fieldname": component,
            "fieldtype": "Currency",
            "width": 150,
        })

    return columns, data

def execute(filters=None):
    columns, data = get_all_employee(filters)
    return columns, data
