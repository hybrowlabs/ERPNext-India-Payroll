// Copyright (c) 2025, Hybrowlabs technologies and contributors
// For license information, please see license.txt

frappe.query_reports["New Joinee Arrear Report"] = {
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
            "fieldname": "joining_from",
            "label": __("Joining From"),
            "fieldtype": "Date",

        },
        {
            "fieldname": "joining_to",
            "label": __("Joining To"),
            "fieldtype": "Date",

        },

	]
};
