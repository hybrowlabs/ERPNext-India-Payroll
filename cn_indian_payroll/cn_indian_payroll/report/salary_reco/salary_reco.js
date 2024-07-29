frappe.query_reports["Salary Reco"] = {
    "filters": [
        {
            "label": "Employee ID",
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 200
        },
       
        {
            "label": "Current Month",
            "fieldname": "current_month",
            "fieldtype": "Select",
            "options": ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            "width": 200
        },
		{
            "label": "Previous Month",
            "fieldname": "previous_month",
            "fieldtype": "Select",
            "options": ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            "width": 200
        },
    ]
}
