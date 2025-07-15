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
        'Salary Structure Assignment',
        filters=conditions1,
        fields=['*']
    )

    earning_salary_components = set()
    deduction_salary_components = set()
    data = []

    ctc_components = frappe.get_all(
        "Salary Component",
        filters={"do_not_include_in_total": 0,"custom_sequence": [">", 0]},
        fields=["*"],
        order_by="custom_sequence asc"
    )
    frappe.msgprint(f"CTC Components: {ctc_components}")
    ctc_components_set = {component.name for component in ctc_components}

    for each_employee in get_all_ssa:
        # Initialize row data
        row = {
            'employee': each_employee.get("employee"),
            'employee_name': each_employee.get("employee_name"),
            'from_date': each_employee.get("from_date"),
            'doj': each_employee.get("custom_date_of_joining"),
            'regime': each_employee.get("income_tax_slab"),
            'salary_structure': each_employee.get("salary_structure"),
            'gross': 0,  # Initialize gross earnings
            'deduction': 0  # Initialize total deductions
        }

        salary_slip = make_salary_slip(
            source_name=each_employee.get("salary_structure"),
            employee=each_employee.get("employee"),
            print_format='Salary Slip Standard for CTC',
            posting_date=each_employee.get("from_date"),
            for_preview=1,
        )

        # Process earnings
        for earning in salary_slip.earnings:
            component_name = earning.salary_component
            if component_name in ctc_components_set:
                amount = earning.amount
                earning_salary_components.add(component_name)
                row[component_name] = round(row.get(component_name, 0) + amount)
                row['gross'] += amount  # Summing gross earnings

        # Process deductions
        for deduction in salary_slip.deductions:
            component_name = deduction.salary_component
            if component_name in ctc_components_set:
                amount = deduction.amount
                deduction_salary_components.add(component_name)
                row[component_name] = round(row.get(component_name, 0) + amount)
                row['deduction'] += amount  # Summing total deductions

        data.append(row)

    # Define columns with employee details
    columns = [
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Data", "width": 150},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 200},
        {"label": "Effective From", "fieldname": "from_date", "fieldtype": "Date", "width": 200},
        {"label": "Date of Joining", "fieldname": "doj", "fieldtype": "Date", "width": 200},
        {"label": "Income Tax Regime", "fieldname": "regime", "fieldtype": "Data", "width": 200},
        {"label": "Salary Structure", "fieldname": "salary_structure", "fieldtype": "Data", "width": 200}
    ]

    # Adding salary components to the columns
    for component in earning_salary_components:
        columns.append({
            "label": component,
            "fieldname": component,
            "fieldtype": "Currency",
            "width": 150
        })

    # Add gross earnings column
    columns.append({
        "label": "Gross Earnings",
        "fieldname": "gross",
        "fieldtype": "Currency",
        "width": 200
    })

    for component in deduction_salary_components:
        columns.append({
            "label": component,
            "fieldname": component,
            "fieldtype": "Currency",
            "width": 150
        })

    # Add total deduction column
    columns.append({
        "label": "Total Deduction",
        "fieldname": "deduction",
        "fieldtype": "Currency",
        "width": 200
    })

    return columns, data

def execute(filters=None):
    columns, data = get_all_employee(filters)
    return columns, data
