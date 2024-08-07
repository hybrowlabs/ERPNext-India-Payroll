import frappe

columns = [
    {"fieldname": "employee", "label": "Employee ID", "fieldtype": "Data", "width": 150},
    {"fieldname": "employee_name", "label": "Employee Name", "fieldtype": "Data", "width": 150},
    {"fieldname": "current_month", "label": "Current Month", "fieldtype": "Data", "width": 150},
    {"fieldname": "current_gross_pay", "label": "Gross Pay", "fieldtype": "Data", "width": 150},
    {"fieldname": "previous_month", "label": "Previous Month", "fieldtype": "Data", "width": 150},
    {"fieldname": "previous_gross_pay", "label": "Gross Pay", "fieldtype": "Data", "width": 150},
    {"fieldname": "difference", "label": "Difference", "fieldtype": "Data", "width": 150},
    {"fieldname": "remark", "label": "Remark", "fieldtype": "Data", "width": 150},
    {"fieldname": "status", "label": "Status", "fieldtype": "Data", "width": 150},
]

def get_salary_slips(filters=None):
    date_str = frappe.utils.nowdate()
    current_date = frappe.utils.getdate(date_str)
    
    month_number = current_date.month
    year_number = current_date.year
    
    if month_number == 1:
        previous_month_number = 12
        previous_year_number = year_number - 1
    else:
        previous_month_number = month_number - 1
        previous_year_number = year_number
    
    month_names = ["", "January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    
    current_month_name = month_names[month_number]
    previous_month_name = month_names[previous_month_number]
    
    if filters is None:
        filters = {}

    conditions1 = {"docstatus": ["in", [0, 1]], "custom_month": previous_month_name}
    conditions2 = {"docstatus": ["in", [0, 1]], "custom_month": current_month_name}

    if filters.get("employee"):
        conditions1["employee"] = filters["employee"]
        conditions2["employee"] = filters["employee"]
        
    if filters.get("previous_month"):
        conditions1["custom_month"] = filters["previous_month"]
        
    if filters.get("current_month"):
        conditions2["custom_month"] = filters["current_month"]
        
    data_previous = frappe.get_list(
        'Salary Slip',
        fields=["*"],
        filters=conditions1,
        order_by="name DESC",
        limit_page_length=0 
    )

    previous_month_data = []
    for j1 in data_previous:
        employee_data = frappe.get_doc('Employee', j1.employee)

        previous_array = {
            "employee": j1.employee,
            "employee_name": j1.employee_name,
            "month": j1.custom_month,
            "gross_pay": j1.custom_statutory_grosspay,
            "status": employee_data.status,
            "remark":j1.custom_new_joinee
        }
        previous_month_data.append(previous_array)

    data_current = frappe.get_list(
        'Salary Slip',
        fields=["*"],
        filters=conditions2,
        order_by="name DESC",
        limit_page_length=0  
    )

    current_month_data = []
    for j2 in data_current:
        employee_data = frappe.get_doc('Employee', j2.employee)  # Fetching employee data again
        current_array = {
            "employee": j2.employee,
            "employee_name": j2.employee_name,
            "month": j2.custom_month,
            "gross_pay": j2.custom_statutory_grosspay,
            "status": employee_data.status  # Use the same status field
        }
        current_month_data.append(current_array)
        
    # Process data
    final_data_map = {}
    
    for record in previous_month_data:
        employee_id = record['employee']
        final_data_map[employee_id] = {
            'employee': record['employee'], 
            'employee_name': record['employee_name'],
            'previous_month': record['month'],
            'previous_gross_pay': record['gross_pay'],
            'current_month': "-",
            'current_gross_pay': 0,
            'difference': 0,
            'status': record['status'],
            'remark':record['remark']
              
        }
    
    for record in current_month_data:
        employee_id = record['employee']
        if employee_id not in final_data_map:
            final_data_map[employee_id] = {
                'employee': record['employee'],
                'employee_name': record['employee_name'],
                'previous_month': "-",
                'previous_gross_pay': 0,
                'current_month': record['month'],
                'current_gross_pay': record['gross_pay'],
                'difference': record['gross_pay'],
                'status': record['status']  ,
                'remark':record['remark']

            }
        else:
            final_data_map[employee_id]['current_month'] = record['month']
            final_data_map[employee_id]['current_gross_pay'] = record['gross_pay']
            final_data_map[employee_id]['difference'] = (
                final_data_map[employee_id]['current_gross_pay'] - 
                final_data_map[employee_id]['previous_gross_pay']
            )
            # Ensure status is consistent
            final_data_map[employee_id]['status'] = record['status']
    
    final_array = list(final_data_map.values())
    return final_array

def execute(filters=None):
    data = get_salary_slips(filters)
    return columns, data
