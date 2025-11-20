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

#     get_all_ssa = frappe.get_list(
#         'Salary Structure Assignment',
#         filters=conditions,
#         fields=['*']
#     )

#     earning_salary_components = set()
#     deduction_salary_components = set()
#     reimbursement_salary_components = set()
#     data = []

#     ctc_components = frappe.get_all(
#         "Salary Component",
#         filters={"do_not_include_in_total": 0,"custom_component_sequence": [">", 0]},
#         fields=["*"],
#         order_by="custom_component_sequence asc"
#     )
#     ctc_components_set = {component.name for component in ctc_components}

#     for each_employee in get_all_ssa:

#         row = {
#             'employee': each_employee.get("employee"),
#             'employee_name': each_employee.get("employee_name"),
#             'from_date': each_employee.get("from_date"),
#             'doj': each_employee.get("custom_date_of_joining"),
#             'regime': each_employee.get("income_tax_slab"),
#             'salary_structure': each_employee.get("salary_structure"),
#             'gross': 0,
#             'deduction': 0
#         }

#         salary_slip = make_salary_slip(
#             source_name=each_employee.get("salary_structure"),
#             employee=each_employee.get("employee"),
#             print_format='Salary Slip Standard for CTC',
#             posting_date=each_employee.get("from_date"),
#             for_preview=1,
#         )


#         for earning in salary_slip.earnings:
#             component_name = earning.salary_component
#             if component_name in ctc_components_set:
#                 amount = earning.amount
#                 earning_salary_components.add(component_name)
#                 row[component_name] = round(row.get(component_name, 0) + amount)
#                 row['gross'] += amount


#         for deduction in salary_slip.deductions:
#             component_name = deduction.salary_component
#             if component_name in ctc_components_set:
#                 amount = deduction.amount
#                 deduction_salary_components.add(component_name)
#                 row[component_name] = round(row.get(component_name, 0) + amount)
#                 row['deduction'] += amount

#         data.append(row)


#     columns = [
#         {"label": "Employee", "fieldname": "employee", "fieldtype": "Data", "width": 150},
#         {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 200},
#         {"label": "Effective From", "fieldname": "from_date", "fieldtype": "Date", "width": 200},
#         {"label": "Date of Joining", "fieldname": "doj", "fieldtype": "Date", "width": 200},
#         {"label": "Income Tax Regime", "fieldname": "regime", "fieldtype": "Data", "width": 200},
#         {"label": "Salary Structure", "fieldname": "salary_structure", "fieldtype": "Data", "width": 200}
#     ]


#     for component in earning_salary_components:
#         columns.append({
#             "label": component,
#             "fieldname": component,
#             "fieldtype": "Currency",
#             "width": 150
#         })


#     columns.append({
#         "label": "Gross Earnings",
#         "fieldname": "gross",
#         "fieldtype": "Currency",
#         "width": 200
#     })

#     for component in deduction_salary_components:
#         columns.append({
#             "label": component,
#             "fieldname": component,
#             "fieldtype": "Currency",
#             "width": 150
#         })

#     columns.append({
#         "label": "Total Deduction",
#         "fieldname": "deduction",
#         "fieldtype": "Currency",
#         "width": 200
#     })

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

    get_all_ssa = frappe.get_all(
        "Salary Structure Assignment", filters=conditions1, fields=["*"]
    )

    all_matched_components = set()
    component_sequence_map = {}
    reimbursement_components = set()
    data = []

    for each_employee in get_all_ssa:
        # Generate salary slip
        salary_slip = make_salary_slip(
            source_name=each_employee.get("salary_structure"),
            employee=each_employee.get("employee"),
            print_format="Salary Slip Standard",
            posting_date=each_employee.get("from_date"),
            for_preview=1,
        )

        row = {
            "employee": each_employee.get("employee"),
            "employee_name": each_employee.get("employee_name"),
            "from_date": each_employee.get("from_date"),
            "doj": each_employee.get("custom_date_of_joining"),
            "base": each_employee.get("base"),
            "monthly_ctc": round(each_employee.get("base") / 12),
            "regime": each_employee.get("income_tax_slab"),
        }

        # Collect earnings & deductions
        for section in [salary_slip.earnings, salary_slip.deductions]:
            for comp in section:
                component_name = comp.salary_component
                amount = comp.amount or 0

                # Fetch component doc to validate sequence and CTC flag
                component_doc = frappe.get_value(
                    "Salary Component",
                    component_name,
                    ["custom_component_sequence", "custom_is_part_of_ctc"],
                    as_dict=True,
                )
                if component_doc and component_doc.custom_is_part_of_ctc == 1:
                    # Safely convert sequence to int, fallback to 9999
                    sequence = (
                        int(component_doc.custom_component_sequence)
                        if component_doc.custom_component_sequence
                        and str(component_doc.custom_component_sequence).isdigit()
                        else 9999
                    )
                    all_matched_components.add(component_name)
                    component_sequence_map[component_name] = sequence
                    row[component_name] = round(row.get(component_name, 0) + amount)

        # Set missing to 0
        for comp in all_matched_components:
            row.setdefault(comp, 0)



        # Reimbursements
        reimbursements = frappe.get_all(
            "Employee Reimbursements",
            filters={"parent": each_employee.get("name")},
            fields=["reimbursements", "monthly_total_amount"],
        )

        for reimbursement in reimbursements:
            component_name = reimbursement.get("reimbursements")
            amount = reimbursement.get("monthly_total_amount") or 0

            if component_name:
                reimbursement_components.add(component_name)
                row[component_name] = round(row.get(component_name, 0) + amount)

        # Default 0 for reimbursements
        for comp in reimbursement_components:
            row.setdefault(comp, 0)

        data.append(row)

    # Sort matched components by sequence
    sorted_components = sorted(
        all_matched_components, key=lambda x: component_sequence_map.get(x, 9999)
    )

    # Columns
    columns = [
        {
            "label": "Employee",
            "fieldname": "employee",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "Employee Name",
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "label": "Effective From",
            "fieldname": "from_date",
            "fieldtype": "Date",
            "width": 150,
        },
        {
            "label": "Date of Joining",
            "fieldname": "doj",
            "fieldtype": "Date",
            "width": 150,
        },
        {
            "label": "Annual CTC",
            "fieldname": "base",
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "label": "Monthly CTC",
            "fieldname": "monthly_ctc",
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "label": "Income Tax Regime",
            "fieldname": "regime",
            "fieldtype": "Data",
            "width": 150,
        },
    ]

    for component in sorted_components:
        columns.append(
            {
                "label": component,
                "fieldname": component,
                "fieldtype": "Currency",
                "width": 150,
            }
        )



    for comp in sorted(reimbursement_components):
        columns.append(
            {
                "label": comp,
                "fieldname": comp,
                "fieldtype": "Currency",
                "width": 150,
            }
        )

    return columns, data


def execute(filters=None):
    columns, data = get_all_employee(filters)
    return columns, data
