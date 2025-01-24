


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

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_consolidated_data()
    data = remove_employee_repetition(data)
    data = add_loan_perquisite(data)
    data = add_car_perquisite(data) 
    data = add_total_column(data) 
    return columns, data

def get_columns():
    return [
        {"fieldname": "employee", "label": "Employee", "fieldtype": "Data", "width": 150},
        {"fieldname": "month", "label": "Month", "fieldtype": "Data", "width": 100},
        {"fieldname": "basic", "label": "Basic", "fieldtype": "Float", "width": 150},
        {"fieldname": "hra", "label": "HRA", "fieldtype": "Float", "width": 150},
        {"fieldname": "twa", "label": "TWA", "fieldtype": "Float", "width": 120},
        {"fieldname": "total", "label": "Total", "fieldtype": "Float", "width": 150}, 
        {"fieldname": "loan_perquisite", "label": "Loan Perquisite", "fieldtype": "Float", "width": 150}, 
        {"fieldname": "car_perquisite", "label": "Car Perquisite", "fieldtype": "Float", "width": 150}, 
    ]

def get_consolidated_data():
    # Consolidated rows
    consolidated_rows = [
        {
            "employee": "SHINIL",
            "month": "",
            "basic": None,
            "hra": None,
            "twa": None,
            "total": None, 
            "loan_perquisite": None,
            "car_perquisite": None, 
        },
        {
            "employee": "SHARON",
            "month": "",
            "basic": None,
            "hra": None,
            "twa": None,
            "total": None, 
            "loan_perquisite": None,
            "car_perquisite": None, 
        },
    ]

    # Detailed rows for SHARON
    casual_leave_rows = [
        {
            "employee": "SHARON",
            "month": "April",
            "basic": 1,
            "hra": 2,
            "twa": 3,
            "total": None, 
            "loan_perquisite": None,
            "car_perquisite": None, 
        },
        {
            "employee": "SHARON",
            "month": "May",
            "basic": 11,
            "hra": 22,
            "twa": 33,
            "total": None, 
            "loan_perquisite": None,
            "car_perquisite": None, 
        },
        {
            "employee": "SHARON",
            "month": "SUM",
            "basic": 111,
            "hra": 222,
            "twa": 333,
            "total": None, 
            "loan_perquisite": None,
            "car_perquisite": None, 
        },

        {
            "employee": "SHARON",
            "month": "Projection",
            "basic": 111,
            "hra": 222,
            "twa": 333,
            "total": None, 
            "loan_perquisite": None,
            "car_perquisite": None, 
        },
        {
            "employee": "SHARON",
            "month": "Total(sum+projection)",
            "basic": 111,
            "hra": 222,
            "twa": 333,
            "total": None, 
            "loan_perquisite": None,
            "car_perquisite": None, 
        },
    ]

    # Detailed rows for SHINIL
    sick_leave_rows = [
        {
            "employee": "SHINIL",
            "month": "April",
            "basic": 1,
            "hra": 2,
            "twa": 3,
            "total": None, 
            "loan_perquisite": None,
            "car_perquisite": None, 
        },
        {
            "employee": "SHINIL",
            "month": "May",
            "basic": 11,
            "hra": 22,
            "twa": 33,
            "total": None, 
            "loan_perquisite": None,
            "car_perquisite": None, 
        },
        {
            "employee": "SHINIL",
            "month": "SUM",
            "basic": 111,
            "hra": 222,
            "twa": 333,
            "total": None, 
            "loan_perquisite": None,
            "car_perquisite": None, 
        },
        {
            "employee": "SHINIL",
            "month": "Projection",
            "basic": 111,
            "hra": 222,
            "twa": 333,
            "total": None, 
            "loan_perquisite": None,
            "car_perquisite": None, 
        },
        {
            "employee": "SHINIL",
            "month": "Total(sum+projection)",
            "basic": 111,
            "hra": 222,
            "twa": 333,
            "total": None, 
            "loan_perquisite": None,
            "car_perquisite": None, 
        },
    ]

    # Combine consolidated and detailed rows
    return (
        [consolidated_rows[0]]  # Consolidated row for SHINIL
        + sick_leave_rows       # Detailed rows for SHINIL
        + [consolidated_rows[1]]  # Consolidated row for SHARON
        + casual_leave_rows     # Detailed rows for SHARON
    )

def remove_employee_repetition(data):
    previous_employee = None
    for row in data:
        if row["employee"] == previous_employee:
            row["employee"] = ""
        else:
            previous_employee = row["employee"]
    return data

def add_loan_perquisite(data):
    # Add loan perquisite value (255) only to consolidated rows after total calculation
    for row in data:
        if row["month"] == "Total(sum+projection)":
            row["loan_perquisite"] = 255 
    return data

def add_car_perquisite(data):
    # Add car perquisite value (let's say 1000) only to consolidated rows after loan perquisite
    for row in data:
        if row["month"] == "Total(sum+projection)":
            row["car_perquisite"] = 1000 
    return data

def add_total_column(data):
    for row in data:
        if row["month"] == "Total(sum+projection)":
            if all(v is not None for v in (row["basic"], row["hra"], row["twa"])): 
                row["total"] = row["basic"] + row["hra"] + row["twa"] 
    return data