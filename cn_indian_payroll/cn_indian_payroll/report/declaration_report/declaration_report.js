// Copyright (c) 2025, Hybrowlabs technologies and contributors
// For license information, please see license.txt

frappe.query_reports["Declaration Report"] = {
	"filters": [

		

		{
            "label": "Select Payroll Period",
            "fieldname": "payroll_period",
            "fieldtype": "Link",
            "options": "Payroll Period",
            "width": 200,
			"reqd":1
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
            "label": "Employee",
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Company",
            "width": 200
        },


	]
};
