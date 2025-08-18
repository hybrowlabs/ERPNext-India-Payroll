frappe.query_reports["Monthly Salary Record"] = {
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
            "fieldname": "start_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "reqd": 1
        },
        {
            "fieldname": "end_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "reqd": 1
        }
    ]
};
