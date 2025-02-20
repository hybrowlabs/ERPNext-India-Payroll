


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
import json

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
        {"fieldname": "salary_slip_id", "label": "Salary Slip ID", "fieldtype": "Link", "width": 150, "options": "Salary Slip"},
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

    columns.append({
        "fieldname": "loan_perquisite",
        "label": "Loan Perquisite",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "total_income",
        "label": "Total Income",
        "fieldtype": "Currency",
        "width": 120
    })


    #section 10 columns-----------

    columns.append({
        "fieldname": "hra_exemption",
        "label": "HRA Exemption",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "lta",
        "label": "LTA  U/s 10 (5)",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "education_allowance",
        "label": "Education Allowance",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "hostel_allowance",
        "label": "Hostel Allowances",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "uniform_allowance",
        "label": "Uniform Allowance",
        "fieldtype": "Currency",
        "width": 120
    })

    

    #Standard Deduction Columns-----------
    columns.append({
        "fieldname": "standard_deduction_old",
        "label": "Standard Deduction Old Regime",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "standard_deduction_new",
        "label": "Standard Deduction Old Regime",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "tax_on_employment",
        "label": "Tax on Employment",
        "fieldtype": "Currency",
        "width": 120
    })


    #80C Columns-----------
    columns.append({
        "label": "Investments In PF(Auto)",
        "fieldname": "pf_auto",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "label": "Pension Scheme Investments & ULIP",
        "fieldname": "pension_scheme",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "label": "Housing Loan Principal Repayment",
        "fieldname": "housing_loan",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "label": " PPF - Public Provident Fund",
        "fieldname": "ppf",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "label": " Home Loan Account Of National Housing Bank ",
        "fieldname": "home_loan",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "label": "LIC- Life Insurance Premium Directly Paid By Employee",
        "fieldname": "lic",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "label": "NSC - National Saving Certificate ",
        "fieldname": "nsc",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "label": "Mutual Funds - Notified Under Clause 23D Of Section 10",
        "fieldname": "mutual_fund",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "label": "ELSS - Equity Link Saving Scheme Of Mutual Funds ",
        "fieldname": "elss",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "tuition",
        "label": " Tuition Fees For Full Time Education ",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "fixed_deposit",
        "label": "Fixed Deposits In Banks (Period As Per Income Tax Guidelines) ",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "deposit",
        "label": "5 Years Term Deposit An Account Under Post Office Term Deposit Rules ",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "others",
        "label": "Others ",
        "fieldtype": "Currency",
        "width": 120
    })
    

    #80D Columns-----------

    columns.append({
        "fieldname": "mediclaim_self",
        "label": "Mediclaim Self, Spouse & Children (Below 60 years) ",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "mediclaim_self_senior",
        "label": "Mediclaim Self (Senior Citizen - 60 years & above) ",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "mediclaim_parents_below",
        "label": "Mediclaim Parents (Below 60 years) ",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "mediclaim_parents_senior",
        "label": "Mediclaim Parents (Senior Citizen - 60 years & above) ",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "preventive_health_checkup",
        "label": "Preventive Health Check-up for Parents ",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "preventive_health_checkup_self",
        "label": "Preventive Health Check-up ",
        "fieldtype": "Currency",
        "width": 120
    })

    #80DD and other columns-----------

    columns.append({
        "fieldname": "medical_treatment_insurance",
        "label": "Medical treatment / insurance of handicapped dependant ",
        "fieldtype": "Currency",
        "width": 120
    })

    columns.append({
        "fieldname": "medical_treatment_disease",
        "label": "Medical treatment (specified diseases only)",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "interest_repayment",
        "label": "Interest repayment of Loan for higher education",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "physical_disabled",
        "label": "Deduction for Physically Disabled",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "donation_80g",
        "label": "Donation U/S 80G",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "nps_deduction",
        "label": "NPS Deduction U/S 80CCD(2)",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "hsg",
        "label": "First HSG Loan Interest Ded.(80EE)",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "nps_contribution",
        "label": "Contribution in National Pension Scheme",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "tax_incentive",
        "label": "Tax Incentive for Affordable Housing for Ded U/S 80EEA ",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "tax_incentive_eeb",
        "label": "Tax Incentives for Electric Vehicles for Ded U/S 80EEB ",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "dona_political_party",
        "label": "Donations/contribution made to a political party or an electoral trust",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "interest_saving_account",
        "label": "Interest on deposits in saving account for Ded U/S 80TTA ",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "interest_fd",
        "label": "Interest on deposits in saving account for Ded U/S 80TTB ",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "deduction_80gg",
        "label": "Deduction U/S 80GG ",
        "fieldtype": "Currency",
        "width": 120
    })
    columns.append({
        "fieldname": "regime_80ccg",
        "label": "Rajiv Gandhi Equity Saving Scheme 80CCG",
        "fieldtype": "Currency",
        "width": 120
    })







    return columns

def get_salary_slip_data(filters=None):
    """Fetch salary slip data with earnings child table components as columns ordered by idx"""

    if not filters:
        filters = {}

    conditions = {"docstatus": ["in", [0, 1]]}
    declaration_condition = {"docstatus": ["in", [0, 1]]}

    if filters.get("company"):
        conditions["company"] = filters["company"]
        declaration_condition["company"] = filters["company"]
    if filters.get("employee"):
        conditions["employee"] = filters["employee"]
        declaration_condition["employee"] = filters["employee"]
    if filters.get("payroll_period"):
        conditions["custom_payroll_period"] = filters["payroll_period"]
        declaration_condition["payroll_period"] = filters["payroll_period"]

    salary_slips = frappe.get_list("Salary Slip", filters=conditions, fields=["*"])
    
    data = []
    previous_employee = None  
    previous_employee_name = None  
    previous_doj = None  
    previous_company_email = None
    previous_department = None
    previous_designation = None
    previous_pan = None
    employee_totals = {}  
    employee_counts = {}  

    amount_map = {}
    lta_map={}
    education_allowance_map={}
    hostel_allowance_map={}
    uniform_allowance_map={}

    pt_map = {}

    standard_deduction_new=0
    standard_deduction_old=0
    declarations = frappe.get_list(
        'Employee Tax Exemption Declaration',
        filters=declaration_condition,
        fields=['*']
    )
    
    for each_doc in declarations:
        if each_doc.custom_tax_regime=="Old Regime":
            get_tax_slab=frappe.get_doc("Income Tax Slab",each_doc.custom_income_tax)
            standard_deduction_old=get_tax_slab.standard_tax_exemption_amount
            amount_map[each_doc.employee] = each_doc.annual_hra_exemption
            get_doc=frappe.get_doc("Employee Tax Exemption Declaration",each_doc.name)

            form_data = json.loads(get_doc.custom_declaration_form_data or '{}')
            lta_map[each_doc.employee] = form_data.get("twentyeight", 0)
            education_allowance_map[each_doc.employee] = form_data.get("thirteen", 0)
            hostel_allowance_map[each_doc.employee] = form_data.get("twentysix", 0)
            uniform_allowance_map[each_doc.employee] = form_data.get("twentyFour", 0)
            pt_map[each_doc.employee] = form_data.get("nineteenNumber", 0)

        elif each_doc.custom_tax_regime=="New Regime":
            get_tax_slab=frappe.get_doc("Income Tax Slab",each_doc.custom_income_tax)
            standard_deduction_new=get_tax_slab.standard_tax_exemption_amount
        


    for slip in salary_slips:
        slip_doc = frappe.get_doc("Salary Slip", slip.name)
        get_employee = frappe.get_doc("Employee", slip_doc.employee)
        
        employee_counts[slip.employee] = employee_counts.get(slip.employee, 0) + 1
        
        row = {
            "employee": slip.employee if slip.employee != previous_employee else "",
            "employee_name": slip.employee_name if slip.employee_name != previous_employee_name else "",
            "doj": get_employee.date_of_joining if get_employee.date_of_joining != previous_doj else "",
            "email": get_employee.company_email if get_employee.company_email != previous_company_email else "",
            "department": get_employee.department if get_employee.department != previous_department else "",
            "designation": get_employee.designation if get_employee.designation != previous_designation else "",
            "pan": get_employee.pan_number if get_employee.pan_number != previous_pan else "",
            "salary_slip_id": slip.name,
            "month": slip.custom_month,
            "loan_perquisite": slip.custom_perquisite_amount 
        }

        earnings = sorted(slip_doc.earnings, key=lambda x: x.idx)
        
        for earning in earnings:
            get_tax_component = frappe.get_doc("Salary Component", earning.salary_component)
            
            if (
                get_tax_component.is_tax_applicable == 1 
                and get_tax_component.type == "Earning" 
                and get_tax_component.custom_tax_exemption_applicable_based_on_regime == 1 
                and (get_tax_component.custom_regime == "All" or get_tax_component.custom_regime == "New Regime")
            ):
                component_key = frappe.scrub(earning.salary_component)
                row[component_key] = earning.amount
                employee_totals.setdefault(slip.employee, {}).setdefault(component_key, 0)
                employee_totals[slip.employee][component_key] += earning.amount
        
        data.append(row)
        previous_employee, previous_doj, previous_employee_name, previous_company_email = (
            slip.employee, get_employee.date_of_joining, get_employee.employee_name, get_employee.company_email
        )
        previous_department, previous_designation, previous_pan = (
            get_employee.department, get_employee.designation, get_employee.pan_number
        )
        
        next_slip_index = salary_slips.index(slip) + 1
        if next_slip_index >= len(salary_slips) or salary_slips[next_slip_index].employee != slip.employee:
            actual_row = {"employee": "Actual", "salary_slip_id": "", "month": "", "loan_perquisite": 0}
            actual_row.update(employee_totals.get(slip.employee, {}))
            data.append(actual_row)
            
            projection_row = get_projection(slip.employee, employee_totals.get(slip.employee, {}), employee_counts[slip.employee], filters.get("payroll_period"))
            projection_row["loan_perquisite"] = 0  
            data.append(projection_row)
            
            combined_row = {
                "employee": "Total", 
                "salary_slip_id": "", 
                "month": "", 
                "loan_perquisite": slip.custom_perquisite_amount, 
                "total_income": 0, 
                "hra_exemption": amount_map.get(slip.employee, 0),
                "lta":lta_map.get(slip.employee, 0),
                "education_allowance":education_allowance_map.get(slip.employee, 0),
                "hostel_allowance":hostel_allowance_map.get(slip.employee, 0),
                "uniform_allowance":uniform_allowance_map.get(slip.employee, 0),
                "standard_deduction_old":standard_deduction_old,
                "standard_deduction_new":standard_deduction_new,
                "tax_on_employment":pt_map.get(slip.employee, 0)

            }
            
            for key in employee_totals.get(slip.employee, {}):
                combined_row[key] = employee_totals[slip.employee].get(key, 0) + projection_row.get(key, 0)
                combined_row["total_income"] += combined_row[key]  
            
            combined_row["total_income"] += combined_row["loan_perquisite"]
            data.append(combined_row)
            
            employee_totals.pop(slip.employee, None)

    return data

def get_projection(employee, employee_totals, slip_count, custom_payroll_period):
    projection = {"employee": "Projection", "salary_slip_id": "", "month": ""}

    ss_assignment = frappe.get_list(
    "Salary Structure Assignment",
    filters={"employee": employee, "docstatus": 1, "custom_payroll_period": custom_payroll_period},
    fields=["name", "from_date", "salary_structure", "custom_payroll_period"],
    order_by="from_date asc"  
    )

    if ss_assignment:
        first_assignment = ss_assignment[0]  # Get the first (earliest) assignment
        start_date = first_assignment["from_date"]
        first_assignment_structure = first_assignment["salary_structure"]

        last_assignment=ss_assignment[-1]
        last_start_date=last_assignment["from_date"]
        last_salary_structure=last_assignment["salary_structure"]
        

        payroll_period_doc = frappe.get_doc("Payroll Period", first_assignment["custom_payroll_period"])
        end_date = payroll_period_doc.end_date

        # Calculate month difference between start_date and end_date
        month_count = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + 1

        # frappe.msgprint(f"Months from {start_date} to {end_date}: {month_count}")

        salary_slip = make_salary_slip(
            source_name=last_salary_structure,
            employee=employee,
            print_format='Salary Slip Standard',
            posting_date=last_start_date,
            for_preview=1,  
        )

        for earning in salary_slip.earnings:
            get_tax_component = frappe.get_doc("Salary Component", earning.salary_component)
            if get_tax_component.is_tax_applicable == 1:
                component_key = frappe.scrub(earning.salary_component)
                if component_key in employee_totals:
                    projection[component_key] = (month_count - slip_count) * earning.amount
    
    return projection

    
