// Copyright (c) 2026, Hybrowlabs technologies and contributors
// For license information, please see license.txt

frappe.query_reports["Benefits_Annual_Report"] = {
	"filters": [
        {
            fieldname: "employee",
            label: "Employee",
            fieldtype: "Link",
            options: "Employee"
        },

        {
            fieldname: "department",
            label: "Department",
            fieldtype: "Link",
            options: "Department"
        },

        {
            fieldname: "payout_month",
            label: "Payout Month",
            fieldtype: "Date"
        }

	]
};
