// Copyright (c) 2025, Hybrowlabs technologies and contributors
// For license information, please see license.txt

frappe.query_reports["Increment Arrear Breakup"] = {
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
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": ["Draft","Submitted"],
            "reqd": 0
        },









	]
};
