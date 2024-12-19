// Copyright (c) 2024, Hybrowlabs technologies and contributors
// For license information, please see license.txt

frappe.query_reports["CTC BreakUp"] = {
	"filters": [

		{
            "label": "Employee ID",
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 200
        },

        {
            "label": "Payroll Period",
            "fieldname": "payroll_period",
            "fieldtype": "Link",
            "options": "Payroll Period",
            "width": 200
        },
        {
            "label": "Effective From",
            "fieldname": "from_date",
            "fieldtype": "Date",
            
            "width": 200
        },
       
       
		

	]
};



