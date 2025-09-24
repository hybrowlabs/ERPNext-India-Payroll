// Copyright (c) 2025, Hybrowlabs technologies and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Advance Report"] = {

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
				"fieldname": "advance_from",
				"label": __("Advance From Date"),
				"fieldtype": "Date",

			},
			{
				"fieldname": "advance_to",
				"label": __("Advance To Date"),
				"fieldtype": "Date",

			},
			{
				"fieldname": "advance_type",
				"label": __("Advance Type"),
				"fieldtype": "Select",
				"options": ["Salary Advance","Reimbursement / Expense Advance"],
				"reqd": 0
			},

		]
};
