// Copyright (c) 2026, Hybrowlabs technologies and contributors
// For license information, please see license.txt

frappe.query_reports["Loans_Annual_Report"] = {
	"filters": [
        {
            fieldname: "employee",
            label: "Employee",
            fieldtype: "Link",
            options: "Employee"
        },

        {
            fieldname: "loan_product",
            label: "Loan Type",
            fieldtype: "Link",
            options: "Loan Product"
        }
	]
};
