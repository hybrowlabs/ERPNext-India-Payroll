// Copyright (c) 2025, Hybrowlabs technologies and contributors
// For license information, please see license.txt

frappe.query_reports["Loan Repayment Schedule Report"] = {
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
			"fieldname": "loan_from",
			"label": __("Loan From Date"),
			"fieldtype": "Date",

		},
		{
			"fieldname": "loan_to",
			"label": __("Loan To Date"),
			"fieldtype": "Date",

		},

		{
			"fieldname": "loan_product",
			"label": __("Loan Type"),
			"fieldtype": "Link",
			"options": "Loan Product",
			"reqd": 0
		},

	]
};
