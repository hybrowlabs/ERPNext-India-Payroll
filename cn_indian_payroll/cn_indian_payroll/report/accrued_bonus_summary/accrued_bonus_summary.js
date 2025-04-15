

// Copyright (c) 2025, Hybrowlabs technologies and contributors
// For license information, please see license.txt

frappe.query_reports["Accrued Bonus Summary"] = {
	"filters": [


		{
            "label": "Employee",
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 200
        },

        {
            "label": "Salary Component",
			"fieldname": "salary_component",
            "fieldtype": "Link",
            "options": "Salary Component",
            "width": 200
        },
		{
            "label": "Company",
			"fieldname": "company",
            "fieldtype": "Link",
            "options": "Company",
            "width": 200,
			"reqd": 1,
        },
		{
            "label": "Payroll Period",
			"fieldname": "payroll_period",
            "fieldtype": "Link",
            "options": "Payroll Period",
            "width": 200,
			"reqd": 1,
        },


	]
};
