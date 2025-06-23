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

    get_all_ssa = frappe.get_list(
        "Salary Structure Assignment", filters=conditions1, fields=["*"]
    )

    reimbursement_components = set()
    all_used_components = []
    data = []

    for each_employee in get_all_ssa:
        # Get components from assigned salary structure
        structure = frappe.get_doc(
            "Salary Structure", each_employee.get("salary_structure")
        )

        structure_component_names = set()
        for comp in structure.get("earnings", []) + structure.get("deductions", []):
            if comp.salary_component:
                structure_component_names.add(comp.salary_component)

        # Filter salary components based on structure & sequence
        matching_ctc_components = frappe.get_all(
            "Salary Component",
            filters={
                "name": ["in", list(structure_component_names)],
                "do_not_include_in_total": 0,
                "custom_sequence": [">", 0],
            },
            fields=["name"],
            order_by="custom_sequence asc",
        )

        ordered_ctc_components = [comp["name"] for comp in matching_ctc_components]
        ctc_components_set = set(ordered_ctc_components)
        all_used_components.extend(ordered_ctc_components)

        # Initialize row data
        row = {
            "employee": each_employee.get("employee"),
            "employee_name": each_employee.get("employee_name"),
            "from_date": each_employee.get("from_date"),
            "doj": each_employee.get("custom_date_of_joining"),
            "base": each_employee.get("base"),
            "monthly_ctc": round(each_employee.get("base") / 12),
            "regime": each_employee.get("income_tax_slab"),
        }

        # Allowance calculations
        hra_amount = special_amount = car_amount = incentive_amount = driver_amount = 0

        if each_employee.get("custom_is_special_hra") == 1:
            hra_amount = each_employee.get("custom_special_hra_amount_annual") / 12
        if each_employee.get("custom_is_special_conveyance") == 1:
            special_amount = (
                each_employee.get("custom_special_conveyance_amount_annual") / 12
            )
        if each_employee.get("custom_is_car_allowance") == 1:
            car_amount = each_employee.get("custom_car_allowance_amount_annual") / 12
        if each_employee.get("custom_is_incentive") == 1:
            incentive_amount = each_employee.get("custom_incentive_amount_annual") / 12
        if each_employee.get("custom_is_extra_driver_salary") == 1:
            driver_amount = each_employee.get("custom_extra_driver_salary_value") / 12

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

        # Generate salary slip
        salary_slip = make_salary_slip(
            source_name=each_employee.get("salary_structure"),
            employee=each_employee.get("employee"),
            print_format="Salary Slip Standard for CTC",
            posting_date=each_employee.get("from_date"),
            for_preview=1,
        )

        # Earnings
        for earning in salary_slip.earnings:
            component_name = earning.salary_component
            if component_name in ctc_components_set:
                amount = earning.amount or 0
                row[component_name] = round(row.get(component_name, 0) + amount)

        # Deductions
        for deduction in salary_slip.deductions:
            component_name = deduction.salary_component
            if component_name in ctc_components_set:
                amount = deduction.amount or 0
                row[component_name] = round(row.get(component_name, 0) + amount)

        # Set missing components to 0
        for component in ordered_ctc_components:
            row.setdefault(component, 0)

        # Add allowance values
        row["special_hra"] = round(hra_amount)
        row["special_conveyance"] = round(special_amount)
        row["car_allowance"] = round(car_amount)
        row["incentive"] = round(incentive_amount)
        row["extra_driver_salary"] = round(driver_amount)

        # Set missing reimbursements to 0
        for component in reimbursement_components:
            row.setdefault(component, 0)

        data.append(row)

    # Prepare column headers
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

    # Remove duplicates and preserve order of components
    seen = set()
    unique_ordered_components = []
    for comp in all_used_components:
        if comp not in seen:
            seen.add(comp)
            unique_ordered_components.append(comp)

    # Add matched salary components
    for component in unique_ordered_components:
        columns.append(
            {
                "label": component,
                "fieldname": component,
                "fieldtype": "Currency",
                "width": 150,
            }
        )

    # Add allowances
    columns.extend(
        [
            {
                "label": "Special HRA",
                "fieldname": "special_hra",
                "fieldtype": "Currency",
                "width": 150,
            },
            {
                "label": "Special Conveyance",
                "fieldname": "special_conveyance",
                "fieldtype": "Currency",
                "width": 150,
            },
            {
                "label": "Car Allowance",
                "fieldname": "car_allowance",
                "fieldtype": "Currency",
                "width": 150,
            },
            {
                "label": "Incentive",
                "fieldname": "incentive",
                "fieldtype": "Currency",
                "width": 150,
            },
            {
                "label": "Extra Driver Salary",
                "fieldname": "extra_driver_salary",
                "fieldtype": "Currency",
                "width": 150,
            },
        ]
    )

    # Add reimbursement components
    for component in sorted(reimbursement_components):
        columns.append(
            {
                "label": component,
                "fieldname": component,
                "fieldtype": "Currency",
                "width": 150,
            }
        )

    return columns, data


def execute(filters=None):
    columns, data = get_all_employee(filters)
    return columns, data
