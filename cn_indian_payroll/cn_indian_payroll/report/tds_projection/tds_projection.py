import frappe
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip

def get_salary_slips(filters=None):
    if filters is None:
        filters = {}

    conditions = {"docstatus": ["in", [1]]}

    if filters.get("company"):
        conditions["company"] = filters["company"]

    if filters.get("payroll_period"):
        conditions["custom_payroll_period"] = filters["payroll_period"]
        
    if filters.get("employee"):
        conditions["employee"] = filters["employee"]

    salary_structure_assignments = frappe.get_all(
        "Salary Structure Assignment", 
        filters=conditions, 
        fields=["*"],  
        order_by="from_date ASC"  # Ensure earliest dates are processed first
    )

    latest_salary_structure = {}
    first_salary_structure = {}

    for structure in salary_structure_assignments:
        employee_id = structure["employee"]
        
        # Keep only the latest assignment based on 'from_date'
        if employee_id not in latest_salary_structure or structure["from_date"] > latest_salary_structure[employee_id]["from_date"]:
            latest_salary_structure[employee_id] = structure  # Update to latest structure

        if employee_id not in first_salary_structure or structure["from_date"] < first_salary_structure[employee_id]["from_date"]:
            first_salary_structure[employee_id] = structure  # Update to earliest structure

    # Convert dictionary values to lists
    unique_salary_structures = list(latest_salary_structure.values())
    first_unique_salary_structures = list(first_salary_structure.values())

    first_employee_details = [
        {
            "employee": item["employee"],
            "from_date": item["from_date"],
            "salary_structure": item["salary_structure"]
        }
        for item in first_unique_salary_structures
    ]

    salary_components = {}
    final_data = []

    for structure in unique_salary_structures:
        employee = frappe.get_value(
            "Employee", 
            structure["employee"], 
            ["pan_number", "personal_email", "company_email"], 
            as_dict=True
        )

        structure["pan_number"] = employee.get("pan_number", "")
        structure["personal_email"] = employee.get("personal_email", "")
        structure["company_email"] = employee.get("company_email", "")

        salary_slips = frappe.get_all(
            "Salary Slip", 
            filters={"employee": structure["employee"], "docstatus": 1}, 
            fields=["name"]
        )

        salary_data = structure.copy()
        slip_count = len(salary_slips) if salary_slips else 0

        total_income = 0  # Initialize total income

        if salary_slips:
            for slip in salary_slips:
                salary_slip_doc = frappe.get_doc("Salary Slip", slip["name"])
                for earning in salary_slip_doc.earnings:
                    get_each_component = frappe.get_doc("Salary Component", earning.salary_component)
                    component_sequence = get_each_component.custom_sequence or 9999  # Default high value if no sequence
                    
                    if (
                        get_each_component.is_tax_applicable == 1 
                        and get_each_component.type == "Earning" 
                        and get_each_component.custom_tax_exemption_applicable_based_on_regime == 1 
                        and (get_each_component.custom_regime == "All" or get_each_component.custom_regime == "New Regime")
                    ):
                        salary_component = earning.salary_component
                        salary_components[salary_component] = component_sequence
                        salary_data[salary_component] = salary_data.get(salary_component, 0) + earning.amount
                        
                        # Add component to total income
                        total_income += earning.amount  

        # Handling missing salary slips
        last_employee_detail = next((d for d in first_employee_details if d["employee"] == structure["employee"]), None)
        
        if last_employee_detail:
            payroll_period_doc = frappe.get_doc("Payroll Period", structure["custom_payroll_period"])
            end_date = payroll_period_doc.end_date
            month_count = (end_date.year - last_employee_detail["from_date"].year) * 12 + \
                          (end_date.month - last_employee_detail["from_date"].month) + 1
            
            salary_slip = make_salary_slip(
                source_name=last_employee_detail["salary_structure"],
                employee=structure["employee"],
                print_format='Salary Slip Standard',
                posting_date=last_employee_detail["from_date"],
                for_preview=1,  
            )

            for projection_earning in salary_slip.earnings:
                get_tax_component = frappe.get_doc("Salary Component", projection_earning.salary_component)

                if (
                    get_tax_component.is_tax_applicable == 1 
                    and get_tax_component.type == "Earning" 
                    and get_tax_component.custom_tax_exemption_applicable_based_on_regime == 1 
                    and (get_tax_component.custom_regime == "All" or get_tax_component.custom_regime == "New Regime")
                ):
                    salary_component = projection_earning.salary_component
                    projected_income = projection_earning.amount * (month_count - slip_count)
                    salary_data[salary_component] = salary_data.get(salary_component, 0) + projected_income
                    
                    # Add projected amount to total income
                    total_income += projected_income  

        # Add total income to salary_data
        salary_data["total_income"] = total_income  

        final_data.append(salary_data)

    return final_data, salary_components

def execute(filters=None):
    columns = [
        {"label": "Employee ID", "fieldname": "employee", "fieldtype": "Data", "width": 120},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 120},
        {"label": "Company", "fieldname": "company", "fieldtype": "Data", "width": 150},
        {"label": "Payroll Period", "fieldname": "custom_payroll_period", "fieldtype": "Data", "width": 150},
        {"label": "Effective From Date", "fieldname": "from_date", "fieldtype": "Date", "width": 120},
        {"label": "Joining Date", "fieldname": "custom_date_of_joining", "fieldtype": "Date", "width": 120},
        {"label": "Opted Slab", "fieldname": "custom_tax_regime", "fieldtype": "Data", "width": 120},
        {"label": "Department", "fieldname": "department", "fieldtype": "Data", "width": 120},
        {"label": "Designation", "fieldname": "designation", "fieldtype": "Data", "width": 120},
        {"label": "PAN Number", "fieldname": "pan_number", "fieldtype": "Data", "width": 150},
        {"label": "Personal Email", "fieldname": "personal_email", "fieldtype": "Data", "width": 200},
        {"label": "Company Email", "fieldname": "company_email", "fieldtype": "Data", "width": 200},
    ]
    
    data, salary_components = get_salary_slips(filters)
    
    sorted_components = sorted(salary_components.items(), key=lambda x: x[1])
    for component, _ in sorted_components:
        columns.append({"label": component, "fieldname": component, "fieldtype": "Currency", "width": 120})

    columns.append(
        {"label": "Total Income", "fieldname": "total_income", "fieldtype": "Currency", "width": 150}
    )
    
    return columns, data
