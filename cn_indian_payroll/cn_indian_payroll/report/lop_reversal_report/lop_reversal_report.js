// Copyright (c) 2025, Hybrowlabs technologies and contributors
// For license information, please see license.txt

frappe.query_reports["LOP Reversal Report"] = {
    "filters": [
        {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "reqd": 1
        },
        {
            "fieldname": "employee",
            "label": __("Employee"),
            "fieldtype": "Link",
            "options": "Employee",
            "reqd": 0
        },
        {
			"fieldname": "lop_reversal_month",
			"label": ("LOP Reversal Month"),
			"fieldtype": "Select",
			"options": ["", "January","February","March","April","May","June","July","August","September","October","November","December"]
		},

        {
            "fieldname": "payroll_period",
            "label": __("Payroll Period"),
            "fieldtype": "Link",
            "options": "Payroll Period",
			"reqd": 1
        }
    ]
};
