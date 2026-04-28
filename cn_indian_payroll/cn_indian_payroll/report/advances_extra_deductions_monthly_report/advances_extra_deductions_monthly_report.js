// Copyright (c) 2026, Hybrowlabs technologies and contributors
// For license information, please see license.txt

frappe.query_reports["Advances Extra Deductions Monthly report"] = {
	"filters": [
        {
            fieldname: "employee",
            label: "Employee",
            fieldtype: "Link",
            options: "Employee"
        },
        {
            fieldname: "from_date",
            label: "From Date",
            fieldtype: "Date"
        },
        {
            fieldname: "to_date",
            label: "To Date",
            fieldtype: "Date"
        }
	]
};
