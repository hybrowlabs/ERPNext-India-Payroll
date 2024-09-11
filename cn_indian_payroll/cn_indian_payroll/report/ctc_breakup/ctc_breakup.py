import frappe
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip

def get_all_employee(filters=None):
    if filters is None:
        filters = {}

    conditions1 = {"docstatus": 1}

    if filters.get("employee"):
        conditions1["employee"] = filters["employee"]

    get_all_ssa = frappe.get_list('Salary Structure Assignment',
                filters=conditions1,
                fields=['*']
            )

    salary_components = set()  
    reimbursement_components = set()  
    data = []
    
    ctc_components = frappe.get_all("Salary Component", filters={"custom_is_part_of_ctc": 1}, fields=["name"],order_by="custom_sequence asc")
    ctc_components_set = set(component.name for component in ctc_components)

    for each_employee in get_all_ssa:
        # Initialize row data
        row = {
            'employee': each_employee.get("employee"),
            'employee_name': each_employee.get("employee_name"),
            'from_date': each_employee.get("from_date"),
        }

        # Calculate allowances
        hra_amount = special_amount = car_amount = incentive_amount = driver_amount = 0

        if each_employee.get("custom_is_special_hra") == 1:
            hra_amount = each_employee.get("custom_special_hra_amount_annual") / 12
        if each_employee.get("custom_is_special_conveyance") == 1:
            special_amount = each_employee.get("custom_special_conveyance_amount_annual") / 12
        if each_employee.get("custom_is_car_allowance") == 1:
            car_amount = each_employee.get("custom_car_allowance_amount_annual") / 12
        if each_employee.get("custom_is_incentive") == 1:
            incentive_amount = each_employee.get("custom_incentive_amount_annual") / 12
        if each_employee.get("custom_is_extra_driver_salary") == 1:
            driver_amount = each_employee.get("custom_extra_driver_salary_value") / 12

        # Fetch reimbursements for the current employee
        reimbursements = frappe.get_all(
            'Employee Reimbursements',
            filters={"parent": each_employee.get("name")},
            fields=["reimbursements", "monthly_total_amount"]
        )

        # Process reimbursements
        for reimbursement in reimbursements:
            component_name = reimbursement.get("reimbursements")
            amount = reimbursement.get("monthly_total_amount")

            if component_name:
                reimbursement_components.add(component_name)
                row[component_name] = round(row.get(component_name, 0) + amount)

        # Generate the salary slip for each employee
        salary_slip = make_salary_slip(
            source_name=each_employee.get("salary_structure"),
            employee=each_employee.get("employee"),
            print_format='Salary Slip Standard for CTC',  # Ensure this exists
        )

        # Process earnings
        for earning in salary_slip.earnings:
            component_name = earning.salary_component
            if component_name in ctc_components_set:
                amount = earning.amount
                salary_components.add(component_name)
                row[component_name] = round(row.get(component_name, 0) + amount)

        # Process deductions
        for deduction in salary_slip.deductions:
            component_name = deduction.salary_component
            if component_name in ctc_components_set:
                amount = deduction.amount
                salary_components.add(component_name)
                row[component_name] = round(row.get(component_name, 0) + amount)

        # Add allowances to row
        row['special_hra'] = round(hra_amount)
        row['special_conveyance'] = round(special_amount)
        row['car_allowance'] = round(car_amount)
        row['incentive'] = round(incentive_amount)
        row['extra_driver_salary'] = round(driver_amount)

        data.append(row)

    # Define columns with employee details, salary components, and allowances
    columns = [
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Data", "width": 150},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 200},
        {"label": "Effective From", "fieldname": "from_date", "fieldtype": "Date", "width": 200}
    ]
    
    # Adding salary components to the columns
    for component in salary_components:
        columns.append({
            "label": component,
            "fieldname": component,
            "fieldtype": "Currency",
            "width": 150
        })

    # Adding allowances and extra fields to the columns
    columns.extend([
        {"label": "Special HRA", "fieldname": "special_hra", "fieldtype": "Currency", "width": 200},
        {"label": "Special Conveyance", "fieldname": "special_conveyance", "fieldtype": "Currency", "width": 200},
        {"label": "Car Allowance", "fieldname": "car_allowance", "fieldtype": "Currency", "width": 200},
        {"label": "Incentive", "fieldname": "incentive", "fieldtype": "Currency", "width": 200},
        {"label": "Extra Driver Salary", "fieldname": "extra_driver_salary", "fieldtype": "Currency", "width": 200},
    ])

    # Adding reimbursement components to the columns
    for component in reimbursement_components:
        columns.append({
            "label": component,
            "fieldname": component,
            "fieldtype": "Currency",
            "width": 150
        })

    return columns, data

def execute(filters=None):
    columns, data = get_all_employee(filters)
    return columns, data
