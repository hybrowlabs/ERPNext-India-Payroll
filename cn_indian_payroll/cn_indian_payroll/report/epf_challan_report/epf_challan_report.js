// Copyright (c) 2024, Hybrowlabs technologies and contributors
// For license information, please see license.txt

frappe.query_reports["EPF Challan Report"] = {
	"filters": [

		{
            "label": "Employee ID",
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 200
        },
       
        {
            "label": "Month",
            "fieldname": "month",
            "fieldtype": "Select",
            "options": ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            "width": 200
        },

		{
            "label": "Company",
            "fieldname": "company",
            "fieldtype": "Link",
            "options": "Company",
            "width": 200,
			"reqd":1
        },

		{
            "label": "Payroll Period",
            "fieldname": "payroll_period",
            "fieldtype": "Link",
            "options": "Payroll Period",
            "width": 200,
			"reqd":1
        },
		









	]
};
