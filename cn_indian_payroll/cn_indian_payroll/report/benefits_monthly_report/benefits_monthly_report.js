// Copyright (c) 2026, Hybrowlabs technologies and contributors
// For license information, please see license.txt

frappe.query_reports["Benefits Monthly Report"] = {
	"filters": [
        {
            fieldname: "employee",
            label: "Employee",
            fieldtype: "Link",
            options: "Employee"
        },

        {
            fieldname: "salary_component",
            label: "Component Name",
            fieldtype: "Link",
            options: "Salary Component"
        },

        {
            fieldname: "payout_month",
            label: "Payout Month",
            fieldtype: "Date"
        }
	]
};
