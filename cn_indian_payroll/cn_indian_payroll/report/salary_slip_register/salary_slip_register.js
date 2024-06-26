
frappe.query_reports["Salary Slip Register"] = {
    "filters": [
        {
            "label": "Employee ID",
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 200
        },
        {
            "label": "Income Tax Slab",
            "fieldname": "income_tax",
            "fieldtype": "Link",
            "options": "Income Tax Slab",
            "width": 200
        },
        
         {
            "label": "From date",
            "fieldname": "from_date",
            "fieldtype": "Date",
            
            "width": 200
        },
         {
            "label": "To Date",
            "fieldname": "to_date",
            "fieldtype": "Date",
            
            "width": 200
        },
        
        
        
    ]
}
