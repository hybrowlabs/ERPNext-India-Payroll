
frappe.query_reports["Historical CTC Proration"] = {
    "filters": [
        {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "reqd": 1,
            "default": frappe.defaults.get_user_default("company")
        },
        {
            "fieldname": "employee",
            "label": __("Employee"),
            "fieldtype": "Link",
            "options": "Employee"
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
            "options": "Employment Type"
        },
        {
            "fieldname": "custom_month",
            "label": __("Month"),
            "fieldtype": "Select",
            "options": [
                "All","January","February","March","April","May","June",
                "July","August","September","October","November","December"
            ],
            "default": "All",
            "reqd": 1
        }
    ],

    "onload": function(report) {

        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Payroll Settings"
            },
            callback: function(r) {
                if (r.message) {

                    let data = r.message.custom_hide_salary_structure_configuration || [];

                    if (data.length > 0) {

                        let employment_types = data.map(d => d.employment_type);

                        report.get_filter("custom_employment_type").get_query = function() {
                            return {
                                filters: {
                                    name: ["in", employment_types]
                                }
                            };
                        };

                        report.set_filter_value("custom_employment_type", employment_types[0]);
                    }
                }
            }
        });
    }
};