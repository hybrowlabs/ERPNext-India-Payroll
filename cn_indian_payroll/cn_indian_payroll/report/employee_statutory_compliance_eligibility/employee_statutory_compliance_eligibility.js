// Copyright (c) 2025, Hybrowlabs technologies and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Statutory Compliance Eligibility"] = {
	"filters": [


		{
            "label": "Employee ID",
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 200
        },

        {
            "label": "Company",
            "fieldname": "company",
            "fieldtype": "Link",
            "options": "Company",
            "width": 200,
            "reqd": 1
        },


	]
};
