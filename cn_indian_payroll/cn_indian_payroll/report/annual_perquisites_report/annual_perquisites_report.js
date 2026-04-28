// Copyright (c) 2026, Hybrowlabs technologies and contributors
// For license information, please see license.txt

frappe.query_reports["Annual Perquisites Report"] = {
	"filters": [
        {
            fieldname: "company",
            label: "Business Unit",
            fieldtype: "Link",
            options: "Company"
        },
        {
            fieldname: "from_date",
            label: "From Date",
            fieldtype: "Date",
            reqd: 1
        },
        {
            fieldname: "to_date",
            label: "To Date",
            fieldtype: "Date",
            reqd: 1
        },
        {
            fieldname: "employee",
            label: "Employee",
            fieldtype: "Link",
            options: "Employee"
        },
        {
            fieldname: "branch",
            label: "Location",
            fieldtype: "Link",
            options: "Branch"
        },
        {
            fieldname: "department",
            label: "Department",
            fieldtype: "Link",
            options: "Department"
        },
        {
            fieldname: "designation",
            label: "Designation",
            fieldtype: "Link",
            options: "Designation"
        }
	]
};
