// Copyright (c) 2025, Hybrowlabs technologies and contributors
// For license information, please see license.txt




frappe.query_reports["Monthly Salary Record (Consultants)"] = {
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
            "fieldname": "custom_payroll_period",
            "label": __("Payroll Period"),
            "fieldtype": "Link",
            "options": "Payroll Period",
            "reqd": 1
        },
        {
            "fieldname": "custom_employment_type",
            "label": __("Employment Type"),
            "fieldtype": "Link",
            "options": "Employment Type",
            "reqd": 0
        },
        {
            "fieldname": "custom_month",
            "label": __("Month"),
            "fieldtype": "Select",
            "options": [
                "All",
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December"
            ],
            "default": "All",
            "reqd": 1
        }
    ]
};
