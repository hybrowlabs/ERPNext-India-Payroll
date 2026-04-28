// Copyright (c) 2026, Hybrowlabs technologies and contributors
// For license information, please see license.txt

frappe.query_reports["Loans_Monthly_Report"] = {
	"filters": [
        {
            fieldname: "employee",
            label: "Employee",
            fieldtype: "Link",
            options: "Employee"
        },

        {
            fieldname: "loan",
            label: "Loan",
            fieldtype: "Link",
            options: "Loan"
        }
	]
};
