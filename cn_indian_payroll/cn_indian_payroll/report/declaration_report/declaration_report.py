


# import frappe

# def execute(filters=None):
#     columns = get_columns()
#     data = get_consolidated_data()
#     data = remove_employee_repetition(data)
#     return columns, data

# def get_columns():
#     return [
#         {"fieldname": "employee", "label": "Employee", "fieldtype": "Data", "width": 150},
#         {"fieldname": "month", "label": "Month", "fieldtype": "Data", "width": 100},
#         {"fieldname": "basic", "label": "Basic", "fieldtype": "Float", "width": 150},
#         {"fieldname": "hra", "label": "HRA", "fieldtype": "Float", "width": 150},
#         {"fieldname": "twa", "label": "TWA", "fieldtype": "Float", "width": 120},
#     ]

# def get_consolidated_data():
#     # Consolidated rows
#     consolidated_rows = [
#         {
#             "employee": "SHINIL",
#             "month": "",
#             "basic": None,
#             "hra": None,
#             "twa": None,
#         },
#         {
#             "employee": "SHARON",
#             "month": "",
#             "basic": None,
#             "hra": None,
#             "twa": None,
#         },
#     ]

#     # Detailed rows for SHARON
#     casual_leave_rows = [
#         {
#             "employee": "SHARON",
#             "month": "April",
#             "basic": 1,
#             "hra": 2,
#             "twa": 3,
#         },
#         {
#             "employee": "SHARON",
#             "month": "May",
#             "basic": 11,
#             "hra": 22,
#             "twa": 33,
#         },
#         {
#             "employee": "SHARON",
#             "month": "SUM",
#             "basic": 111,
#             "hra": 222,
#             "twa": 333,
#         },

#         {
#             "employee": "SHARON",
#             "month": "Projection",
#             "basic": 111,
#             "hra": 222,
#             "twa": 333,
#         },
#         {
#             "employee": "SHARON",
#             "month": "Total(sum+projection)",
#             "basic": 111,
#             "hra": 222,
#             "twa": 333,
#         },
#     ]

#     # Detailed rows for SHINIL
#     sick_leave_rows = [
#         {
#             "employee": "SHINIL",
#             "month": "April",
#             "basic": 1,
#             "hra": 2,
#             "twa": 3,
#         },
#         {
#             "employee": "SHINIL",
#             "month": "May",
#             "basic": 11,
#             "hra": 22,
#             "twa": 33,
#         },
#         {
#             "employee": "SHINIL",
#             "month": "SUM",
#             "basic": 111,
#             "hra": 222,
#             "twa": 333,
#         },
#         {
#             "employee": "SHINIL",
#             "month": "Projection",
#             "basic": 111,
#             "hra": 222,
#             "twa": 333,
#         },
#         {
#             "employee": "SHINIL",
#             "month": "Total(sum+projection)",
#             "basic": 111,
#             "hra": 222,
#             "twa": 333,
#         },
#     ]

#     # Combine consolidated and detailed rows
#     return (
#         [consolidated_rows[0]]  # Consolidated row for SHINIL
#         + sick_leave_rows       # Detailed rows for SHINIL
#         + [consolidated_rows[1]]  # Consolidated row for SHARON
#         + casual_leave_rows     # Detailed rows for SHARON
#     )

# def remove_employee_repetition(data):
#     previous_employee = None
#     for row in data:
#         if row["employee"] == previous_employee:
#             row["employee"] = ""
#         else:
#             previous_employee = row["employee"]
#     return data



# import frappe

# def execute(filters=None):
#     columns = get_columns()
#     data = get_consolidated_data()
#     data = remove_employee_repetition(data)
#     data = add_total_column(data) 
#     return columns, data

# def get_columns():
#     return [
#         {"fieldname": "employee", "label": "Employee", "fieldtype": "Data", "width": 150},
#         {"fieldname": "month", "label": "Month", "fieldtype": "Data", "width": 100},
#         {"fieldname": "basic", "label": "Basic", "fieldtype": "Float", "width": 150},
#         {"fieldname": "hra", "label": "HRA", "fieldtype": "Float", "width": 150},
#         {"fieldname": "twa", "label": "TWA", "fieldtype": "Float", "width": 120},
#         {"fieldname": "total", "label": "Total", "fieldtype": "Float", "width": 150}, 
#     ]

# def get_consolidated_data():
#     # Consolidated rows
#     consolidated_rows = [
#         {
#             "employee": "SHINIL",
#             "month": "",
#             "basic": None,
#             "hra": None,
#             "twa": None,
#             "total": None, 
#         },
#         {
#             "employee": "SHARON",
#             "month": "",
#             "basic": None,
#             "hra": None,
#             "twa": None,
#             "total": None, 
#         },
#     ]

#     # Detailed rows for SHARON
#     casual_leave_rows = [
#         {
#             "employee": "SHARON",
#             "month": "April",
#             "basic": 1,
#             "hra": 2,
#             "twa": 3,
#             "total": None, 
#         },
#         {
#             "employee": "SHARON",
#             "month": "May",
#             "basic": 11,
#             "hra": 22,
#             "twa": 33,
#             "total": None, 
#         },
#         {
#             "employee": "SHARON",
#             "month": "SUM",
#             "basic": 111,
#             "hra": 222,
#             "twa": 333,
#             "total": None, 
#         },

#         {
#             "employee": "SHARON",
#             "month": "Projection",
#             "basic": 111,
#             "hra": 222,
#             "twa": 333,
#             "total": None, 
#         },
#         {
#             "employee": "SHARON",
#             "month": "Total(sum+projection)",
#             "basic": 111,
#             "hra": 222,
#             "twa": 333,
#             "total": None, 
#         },
#     ]

#     # Detailed rows for SHINIL
#     sick_leave_rows = [
#         {
#             "employee": "SHINIL",
#             "month": "April",
#             "basic": 1,
#             "hra": 2,
#             "twa": 3,
#             "total": None, 
#         },
#         {
#             "employee": "SHINIL",
#             "month": "May",
#             "basic": 11,
#             "hra": 22,
#             "twa": 33,
#             "total": None, 
#         },
#         {
#             "employee": "SHINIL",
#             "month": "SUM",
#             "basic": 111,
#             "hra": 222,
#             "twa": 333,
#             "total": None, 
#         },
#         {
#             "employee": "SHINIL",
#             "month": "Projection",
#             "basic": 111,
#             "hra": 222,
#             "twa": 333,
#             "total": None, 
#         },
#         {
#             "employee": "SHINIL",
#             "month": "Total(sum+projection)",
#             "basic": 111,
#             "hra": 222,
#             "twa": 333,
#             "total": None, 
#         },
#     ]

#     # Combine consolidated and detailed rows
#     return (
#         [consolidated_rows[0]]  # Consolidated row for SHINIL
#         + sick_leave_rows       # Detailed rows for SHINIL
#         + [consolidated_rows[1]]  # Consolidated row for SHARON
#         + casual_leave_rows     # Detailed rows for SHARON
#     )

# def remove_employee_repetition(data):
#     previous_employee = None
#     for row in data:
#         if row["employee"] == previous_employee:
#             row["employee"] = ""
#         else:
#             previous_employee = row["employee"]
#     return data

# def add_total_column(data):
#     for row in data:
#         if row["month"] == "Total(sum+projection)":
#             if all(v is not None for v in (row["basic"], row["hra"], row["twa"])): 
#                 row["total"] = row["basic"] + row["hra"] + row["twa"] 
#     return data


#___________________________________________________________________________________________________________________________





# import frappe

# def execute(filters=None):
#     columns = get_columns()
#     data = get_consolidated_data()
#     data = remove_employee_repetition(data)
#     data = add_loan_perquisite(data)
#     data = add_car_perquisite(data) 
#     data = add_total_column(data) 
#     return columns, data

# def get_columns():
#     return [
#         {"fieldname": "employee", "label": "Employee", "fieldtype": "Data", "width": 150},
#         {"fieldname": "month", "label": "Month", "fieldtype": "Data", "width": 100},
#         {"fieldname": "basic", "label": "Basic", "fieldtype": "Float", "width": 150},
#         {"fieldname": "hra", "label": "HRA", "fieldtype": "Float", "width": 150},
#         {"fieldname": "twa", "label": "TWA", "fieldtype": "Float", "width": 120},
#         {"fieldname": "total", "label": "Total", "fieldtype": "Float", "width": 150}, 
#         {"fieldname": "loan_perquisite", "label": "Loan Perquisite", "fieldtype": "Float", "width": 150}, 
#         {"fieldname": "car_perquisite", "label": "Car Perquisite", "fieldtype": "Float", "width": 150}, 
#     ]

# def get_consolidated_data():
#     # Consolidated rows
#     consolidated_rows = [
#         {
#             "employee": "SHINIL",
#             "month": "",
#             "basic": None,
#             "hra": None,
#             "twa": None,
#             "total": None, 
#             "loan_perquisite": None,
#             "car_perquisite": None, 
#         },
#         {
#             "employee": "SHARON",
#             "month": "",
#             "basic": None,
#             "hra": None,
#             "twa": None,
#             "total": None, 
#             "loan_perquisite": None,
#             "car_perquisite": None, 
#         },
#     ]

#     # Detailed rows for SHARON
#     casual_leave_rows = [
#         {
#             "employee": "SHARON",
#             "month": "April",
#             "basic": 1,
#             "hra": 2,
#             "twa": 3,
#             "total": None, 
#             "loan_perquisite": None,
#             "car_perquisite": None, 
#         },
#         {
#             "employee": "SHARON",
#             "month": "May",
#             "basic": 11,
#             "hra": 22,
#             "twa": 33,
#             "total": None, 
#             "loan_perquisite": None,
#             "car_perquisite": None, 
#         },
#         {
#             "employee": "SHARON",
#             "month": "SUM",
#             "basic": 111,
#             "hra": 222,
#             "twa": 333,
#             "total": None, 
#             "loan_perquisite": None,
#             "car_perquisite": None, 
#         },

#         {
#             "employee": "SHARON",
#             "month": "Projection",
#             "basic": 111,
#             "hra": 222,
#             "twa": 333,
#             "total": None, 
#             "loan_perquisite": None,
#             "car_perquisite": None, 
#         },
#         {
#             "employee": "SHARON",
#             "month": "Total(sum+projection)",
#             "basic": 111,
#             "hra": 222,
#             "twa": 333,
#             "total": None, 
#             "loan_perquisite": None,
#             "car_perquisite": None, 
#         },
#     ]

#     # Detailed rows for SHINIL
#     sick_leave_rows = [
#         {
#             "employee": "SHINIL",
#             "month": "April",
#             "basic": 1,
#             "hra": 2,
#             "twa": 3,
#             "total": None, 
#             "loan_perquisite": None,
#             "car_perquisite": None, 
#         },
#         {
#             "employee": "SHINIL",
#             "month": "May",
#             "basic": 11,
#             "hra": 22,
#             "twa": 33,
#             "total": None, 
#             "loan_perquisite": None,
#             "car_perquisite": None, 
#         },
#         {
#             "employee": "SHINIL",
#             "month": "SUM",
#             "basic": 111,
#             "hra": 222,
#             "twa": 333,
#             "total": None, 
#             "loan_perquisite": None,
#             "car_perquisite": None, 
#         },
#         {
#             "employee": "SHINIL",
#             "month": "Projection",
#             "basic": 111,
#             "hra": 222,
#             "twa": 333,
#             "total": None, 
#             "loan_perquisite": None,
#             "car_perquisite": None, 
#         },
#         {
#             "employee": "SHINIL",
#             "month": "Total(sum+projection)",
#             "basic": 111,
#             "hra": 222,
#             "twa": 333,
#             "total": None, 
#             "loan_perquisite": None,
#             "car_perquisite": None, 
#         },
#     ]


#     frappe.msgprint (str (
#         [consolidated_rows[0]]  # Consolidated row for SHINIL
#         + sick_leave_rows       # Detailed rows for SHINIL
#         + [consolidated_rows[1]]  # Consolidated row for SHARON
#         + casual_leave_rows     # Detailed rows for SHARON
#     ))

#     # Combine consolidated and detailed rows
#     return (
#         [consolidated_rows[0]]  # Consolidated row for SHINIL
#         + sick_leave_rows       # Detailed rows for SHINIL
#         + [consolidated_rows[1]]  # Consolidated row for SHARON
#         + casual_leave_rows     # Detailed rows for SHARON
#     )

# def remove_employee_repetition(data):
#     previous_employee = None
#     for row in data:
#         if row["employee"] == previous_employee:
#             row["employee"] = ""
#         else:
#             previous_employee = row["employee"]
#     return data

# def add_loan_perquisite(data):
#     for row in data:
#         if row["month"] == "Total(sum+projection)":
#             row["loan_perquisite"] = 255 
#     return data

# def add_car_perquisite(data):
#     # Add car perquisite value (let's say 1000) only to consolidated rows after loan perquisite
#     for row in data:
#         if row["month"] == "Total(sum+projection)":
#             row["car_perquisite"] = 1000 
#     return data

# def add_total_column(data):
#     for row in data:
#         if row["month"] == "Total(sum+projection)":
#             if all(v is not None for v in (row["basic"], row["hra"], row["twa"])): 
#                 row["total"] = row["basic"] + row["hra"] + row["twa"] 
#     return data


#/////////////////////////////////////////////////////////////////////////////////////////








# import frappe

# def execute(filters=None):
#     columns = get_columns()
#     data = get_employees(filters)  # Fetch employee data
#     data = get_consolidated_data()
#     # data = remove_employee_repetition()
#     return columns, data


# def get_employees(filters=None):
#     if filters is None:
#         filters = {}

#     conditions = {}
#     employee_condition = {"status": "Active"}  # Only fetch active employees

#     if filters.get("company"):
#         conditions["company"] = filters["company"]
#         employee_condition["company"] = filters["company"]

#     if filters.get("payroll_period"):
#         conditions["payroll_period"] = filters["payroll_period"]

#     if filters.get("employee"):
#         conditions["name"] = filters["employee"]
#         employee_condition["name"] = filters["employee"]  # Correct reference

#     # Fetch employee records
#     get_all_employee = frappe.get_list(
#         "Employee",
#         filters=employee_condition,
#         fields=["name", "employee_name", "date_of_joining", "company_email",
#                 "designation", "department", "pan_number", "status"],
#     )

#     data = []  # Initialize an empty list

#     if get_all_employee:
#         # frappe.msgprint(str(get_all_employee))

#         for emp in get_all_employee:
#             data.append({
#                 "employee": emp.name,
#                 "employee_name": emp.employee_name,
#                 "doj": emp.date_of_joining,
#                 "company_email": emp.company_email,  # Fixed missing comma
#                 "designation": emp.designation,
#                 "department": emp.department,
#                 "pan_number": emp.pan_number,
#                 "status": emp.status
#             })

#     return data  # Return the data list


# def get_columns():
#     columns= [
#         {"fieldname": "employee", "label": "Employee", "fieldtype": "Data", "width": 150},
#         {"fieldname": "employee_name", "label": "Employee Name", "fieldtype": "Data", "width": 100},
#         {"fieldname": "doj", "label": "Date of Joining", "fieldtype": "Date", "width": 150},  # Corrected column
#         {"fieldname": "company_email", "label": "Email", "fieldtype": "Data", "width": 150},
#         {"fieldname": "designation", "label": "Designation", "fieldtype": "Data", "width": 120},
#         {"fieldname": "department", "label": "Department", "fieldtype": "Data", "width": 150}, 
#         {"fieldname": "pan_number", "label": "PAN", "fieldtype": "Data", "width": 150}, 
#         {"fieldname": "status", "label": "Status", "fieldtype": "Data", "width": 150}, 
#     ]

#     return columns


# def get_salary_slip():

#     get_all_employee = frappe.get_list(
#         "Salary Slip",
#         filters=emp.name,"docstatus"[in[0,1]],
#         fields=["*"],
#     )
#     if len(get_all_employee)>0:
#         for j in get_all_employee:
#             get_doc=frappe.get_doc("Salary Slip",j.name)
#             columns.append({
#                     "label": get_doc.custom_month,
#                     "fieldname": get_doc.custom_month,
#                     "fieldtype": "Data",
#                     "width": 150
#                 })
#             for k in get_doc.earnings:

#                 columns.append({
#                     "label": k.salary_component,
#                     "fieldname": k.salary_component,
#                     "fieldtype": "Data",
#                     "width": 150
#                 })

                


    



   

#     return([consolidated_rows[0]]  # Consolidated row for SHINIL
#         + sick_leave_rows       # Detailed rows for SHINIL
#         + [consolidated_rows[1]]  # Consolidated row for SHARON
#         + casual_leave_rows)


    



# def remove_employee_repetition(data):
#     previous_employee = None
#     for row in data:
#         if row["employee"] == previous_employee:
#             row["employee"] = ""
#         else:
#             previous_employee = row["employee"]

#     frappe.msgprint(str(previous_employee))


#     # return data

# def add_loan_perquisite(data):
#     for row in data:
#         if row["month"] == "Total(sum+projection)":
#             row["loan_perquisite"] = 255 
#     return data

# def add_car_perquisite(data):
#     # Add car perquisite value (let's say 1000) only to consolidated rows after loan perquisite
#     for row in data:
#         if row["month"] == "Total(sum+projection)":
#             row["car_perquisite"] = 1000 
#     return data

# def add_total_column(data):
#     for row in data:
#         if row["month"] == "Total(sum+projection)":
#             if all(v is not None for v in (row["basic"], row["hra"], row["twa"])): 
#                 row["total"] = row["basic"] + row["hra"] + row["twa"] 
#     return data



import frappe
from datetime import datetime
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip

def execute(filters=None):
    columns = get_columns(filters)
    data = get_salary_slip_data(filters)
    return columns, data

def get_columns(filters):
    """Dynamically fetch salary components from Salary Slip earnings and create columns in order of idx"""

    columns = [
        {"fieldname": "employee", "label": "Employee", "fieldtype": "Data", "width": 150},
        {"fieldname": "employee_name", "label": "Employee Name", "fieldtype": "Data", "width": 150},
        {"fieldname": "email", "label": "Email", "fieldtype": "Data", "width": 150},
        {"fieldname": "doj", "label": "Date Of Joining", "fieldtype": "Date", "width": 150},
        {"fieldname": "department", "label": "Department", "fieldtype": "Data", "width": 150},
        {"fieldname": "designation", "label": "Designation", "fieldtype": "Data", "width": 150},
        {"fieldname": "pan", "label": "PAN", "fieldtype": "Data", "width": 150},
        {"fieldname": "salary_slip_id", "label": "Salary Slip ID", "fieldtype": "Link", "width": 150,"options":"Salary Slip"},
        {"fieldname": "month", "label": "Month", "fieldtype": "Data", "width": 100},

        
    ]

    salary_components = frappe.db.sql("""
        SELECT DISTINCT sd.salary_component, MIN(sd.idx) as min_idx
        FROM `tabSalary Detail` sd
        JOIN `tabSalary Slip` ss ON sd.parent = ss.name
        WHERE sd.parenttype = 'Salary Slip'
        GROUP BY sd.salary_component
        ORDER BY min_idx ASC
    """, as_dict=True)

    for component in salary_components:
        get_doc = frappe.get_doc("Salary Component", component.salary_component)

        if (
            get_doc.is_tax_applicable == 1
            and get_doc.type == "Earning"
            and get_doc.custom_tax_exemption_applicable_based_on_regime == 1
            and (get_doc.custom_regime == "All" or get_doc.custom_regime == "New Regime")
        ):
            columns.append({
                "fieldname": frappe.scrub(component.salary_component),
                "label": component.salary_component,
                "fieldtype": "Currency",
                "width": 120
            })

    return columns

def get_salary_slip_data(filters=None):
    """Fetch salary slip data with earnings child table components as columns ordered by idx"""

    if not filters:
        filters = {}

    conditions = {"docstatus": ["in", [0, 1]]}
    if filters.get("company"):
        conditions["company"] = filters["company"]
    if filters.get("employee"):
        conditions["employee"] = filters["employee"]

    salary_slips = frappe.get_list(
        "Salary Slip",
        filters=conditions,
        fields=["*"]
    )

    data = []
    previous_employee = None  
    previous_employee_name = None  
    previous_doj = None  
    previous_company_email=None
    previous_department=None
    previous_designation=None
    previous_pan=None
    employee_totals = {}  
    employee_counts = {}  

    for slip in salary_slips:
        slip_doc = frappe.get_doc("Salary Slip", slip.name)
        get_employee = frappe.get_doc("Employee", slip_doc.employee)

        if slip.employee not in employee_counts:
            employee_counts[slip.employee] = 0
        employee_counts[slip.employee] += 1

        row = {
            "employee": slip.employee if slip.employee != previous_employee else "",
            "employee_name": slip.employee_name if slip.employee_name != previous_employee_name else "",
            "doj": get_employee.date_of_joining if get_employee.date_of_joining != previous_doj else "",
            "email": get_employee.company_email if get_employee.company_email != previous_company_email else "",

            "department": get_employee.department if get_employee.department != previous_department else "",
            "designation": get_employee.designation if get_employee.designation != previous_designation else "",
            "pan": get_employee.pan_number if get_employee.pan_number != previous_pan else "",

            "salary_slip_id": slip.name,
            "month": slip.custom_month
        }

        earnings = sorted(slip_doc.earnings, key=lambda x: x.idx)
        
        for earning in earnings:
            component_key = frappe.scrub(earning.salary_component)
            row[component_key] = earning.amount
            
            if slip.employee not in employee_totals:
                employee_totals[slip.employee] = {}
            employee_totals[slip.employee][component_key] = employee_totals[slip.employee].get(component_key, 0) + earning.amount

        data.append(row)
        previous_employee = slip.employee
        previous_doj = get_employee.date_of_joining
        previous_employee_name = get_employee.employee_name
        previous_company_email=get_employee.company_email

        previous_department=get_employee.department
        previous_designation=get_employee.designation
        previous_pan=get_employee.pan_number

        next_slip_index = salary_slips.index(slip) + 1
        if next_slip_index >= len(salary_slips) or salary_slips[next_slip_index].employee != slip.employee:
            actual_row = {"employee": "Actual", "doj": "", "salary_slip_id": "", "month": ""}
            actual_row.update(employee_totals[slip.employee])
            data.append(actual_row)
            
            projection_row = get_projection(slip.employee, employee_totals[slip.employee], employee_counts[slip.employee])
            data.append(projection_row)
            
            combined_row = {"employee": "Total", "doj": "", "salary_slip_id": "", "month": ""}
            for key in employee_totals[slip.employee]:
                combined_row[key] = employee_totals[slip.employee].get(key, 0) + projection_row.get(key, 0)
            data.append(combined_row)
            
            employee_totals.pop(slip.employee)

    return data

def get_projection(employee, employee_totals, slip_count):
    projection = {"employee": "Projection", "doj": "", "salary_slip_id": "", "month": ""}

    ss_assignment = frappe.get_list(
        'Salary Structure Assignment',
        filters={'employee': employee, 'docstatus': 1},
        fields=['*'],
        order_by='from_date desc',
        limit=1
    )

    if ss_assignment:
        get_payroll = frappe.get_doc("Payroll Period", ss_assignment[0].custom_payroll_period)
        effective_start_date = ss_assignment[0].from_date
        payroll_end_date = get_payroll.end_date
        payroll_start_date = get_payroll.start_date
        doj = ss_assignment[0].custom_date_of_joining

        start_date = max(effective_start_date, payroll_start_date, doj)
        
        if isinstance(start_date, str):
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
        else:
            start = start_date  

        if isinstance(payroll_end_date, str):
            end = datetime.strptime(payroll_end_date, "%Y-%m-%d").date()
        else:
            end = payroll_end_date  

        num_months = (end.year - start.year) * 12 + (end.month - start.month) + 1
        
        salary_slip = make_salary_slip(
            source_name=ss_assignment[0].salary_structure,
            employee=ss_assignment[0].employee,
            print_format='Salary Slip Standard',
            posting_date=ss_assignment[0].from_date,
            for_preview=1,  
        )

        for earning in salary_slip.earnings:
            get_tax_component = frappe.get_doc("Salary Component", earning.salary_component)
            if get_tax_component.is_tax_applicable == 1:
                component_key = frappe.scrub(earning.salary_component)
                if component_key in employee_totals:
                    projection[component_key] = (num_months - slip_count) * earning.amount
    
    return projection