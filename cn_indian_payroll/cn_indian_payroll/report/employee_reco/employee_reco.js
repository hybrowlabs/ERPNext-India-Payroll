// Copyright (c) 2024, Hybrowlabs technologies and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Reco"] = {
	"filters": [

		{
            "label": "Select Month",
            "fieldname": "select_month",
            "fieldtype": "Select",
            "options": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            "width": 200
        },

		{
            "label": "Select Payroll Period",
            "fieldname": "payroll_period",
            "fieldtype": "Link",
            "options": "Payroll Period",
            "width": 200
        },


	]
};
