// // Copyright (c) 2025, Auriga IT and contributors
// // For license information, please see license.txt

// frappe.query_reports["Salary Book Register"] = {


// 	onload: function(report) {
//         let company = frappe.defaults.get_user_default("Company");

//         if (company) {
//             report.set_filter_value("company", company);
// 			console.log("Default company set to:", company);
//         }
//     },


// 	filters: [
// 		// {
// 		// 	fieldname: "from_date",
// 		// 	label: __("From"),
// 		// 	fieldtype: "Date",
// 		// 	default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
// 		// 	reqd: 1,
// 		// 	width: "100px",
// 		// },
// 		// {
// 		// 	fieldname: "to_date",
// 		// 	label: __("To"),
// 		// 	fieldtype: "Date",
// 		// 	default: frappe.datetime.get_today(),
// 		// 	reqd: 1,
// 		// 	width: "100px",
// 		// },

// 		        {
//             "label": "Calendar",
//             "fieldname": "calendar",
//             "fieldtype": "Select",
//             "options": ["","Hijri", "Gregorian"].join("\n"),
//             "width": 200,
//             // "reqd": 1,
//             "default": "Hijri",
//             "on_change": function(report) {

//                 let calendar = report.get_filter_value("calendar");

//                 let hijri_months = [
//                     "", "Moharram al-Haraam", "Safar al-Muzaffar",
//                     "Rabi al-Awwal", "Rabi al-Aakhar",
//                     "Jumada al-Ula", "Jumada al-Ukhra",
//                     "Rajab al-Asab", "Shabaan al-Karim",
//                     "Ramadaan al-Moazzam", "Shawwal al-Mukarram",
//                     "Zilqadah al-Haraam", "Zilhaj al-Haraam"
//                 ];

//                 let gregorian_months = [
//                     "", "January", "February", "March", "April",
//                     "May", "June", "July", "August",
//                     "September", "October", "November", "December"
//                 ];

//                 let month_filter = report.get_filter("month");

//                 if (!calendar) {
//                     month_filter.df.options = "";
//                     month_filter.refresh();
//                     report.set_filter_value("month", "");
//                     return;
//                 }

//                 let months = calendar === "Hijri" ? hijri_months : gregorian_months;

//                 month_filter.df.options = months.join("\n");
//                 month_filter.refresh();

//                 report.set_filter_value("month", "");
//             }
//         },

//         {
//             "label": "Month",
//             "fieldname": "month",
//             "fieldtype": "Select",
//             "options": "",
//             "width": 200
//         },
// 		{
// 			fieldname: "currency",
// 			fieldtype: "Link",
// 			options: "Currency",
// 			label: __("Currency"),
// 			default: erpnext.get_currency(frappe.defaults.get_default("Company")),
// 			width: "50px",
// 		},
// 		{
// 			fieldname: "employee",
// 			label: __("Employee"),
// 			fieldtype: "Link",
// 			options: "Employee",
// 			width: "100px",
// 		},
// 		{
// 			fieldname: "branch",
// 			label: __("Branch"),
// 			fieldtype: "Link",
// 			options: "Branch",
// 			width: "100px",
// 		},

// 		{
// 			fieldname: "company",
// 			label: __("Company"),
// 			fieldtype: "Link",
// 			options: "Company",
// 			default: frappe.defaults.get_user_default("Company"),
// 			width: "100px",
// 			reqd: 1,
// 		},
// 		{
// 			fieldname: "docstatus",
// 			label: __("Document Status"),
// 			fieldtype: "Select",
// 			options: ["Draft", "Submitted", "Cancelled"],
// 			default: "Submitted",
// 			width: "100px",
// 		},


// 	],
// };


// Copyright (c) 2025, Auriga IT and contributors
// For license information, please see license.txt
// Copyright (c) 2025, Auriga IT and contributors
// For license information, please see license.txt

frappe.query_reports["Salary Book Register"] = {

    onload: function(report) {
        let company = frappe.defaults.get_user_default("Company");

        if (company) {
            report.set_filter_value("company", company);
        }

        // Apply column toggle after initial render
        setTimeout(() => {
            toggle_columns(report);
        }, 800);
    },

    filters: [

        {
            "label": "Calendar",
            "fieldname": "calendar",
            "fieldtype": "Select",
            "options": ["", "Hijri", "Gregorian"].join("\n"),
            "width": 200,
            "default": "Hijri",

            "on_change": function(report) {

                let calendar = report.get_filter_value("calendar");

                let hijri_months = [
                    "", "Moharram al-Haraam", "Safar al-Muzaffar",
                    "Rabi al-Awwal", "Rabi al-Aakhar",
                    "Jumada al-Ula", "Jumada al-Ukhra",
                    "Rajab al-Asab", "Shabaan al-Karim",
                    "Ramadaan al-Moazzam", "Shawwal al-Mukarram",
                    "Zilqadah al-Haraam", "Zilhaj al-Haraam"
                ];

                let gregorian_months = [
                    "", "January", "February", "March", "April",
                    "May", "June", "July", "August",
                    "September", "October", "November", "December"
                ];

                let month_filter = report.get_filter("month");

                if (!calendar) {
                    month_filter.df.options = "";
                    month_filter.refresh();
                    report.set_filter_value("month", "");
                    return;
                }

                let months = calendar === "Hijri" ? hijri_months : gregorian_months;

                month_filter.df.options = months.join("\n");
                month_filter.refresh();

                report.set_filter_value("month", "");

                report.refresh();

                setTimeout(() => {
                    toggle_columns(report);
                }, 500);
            }
        },

        {
            "label": "Month",
            "fieldname": "month",
            "fieldtype": "Select",
            "options": "",
            "width": 200
        },

        {
            fieldname: "currency",
            fieldtype: "Link",
            options: "Currency",
            label: __("Currency"),
            default: erpnext.get_currency(frappe.defaults.get_default("Company")),
            width: "80px",
        },

        {
            fieldname: "employee",
            label: __("Employee"),
            fieldtype: "Link",
            options: "Employee",
            width: "120px",
        },

        {
            fieldname: "branch",
            label: __("Branch"),
            fieldtype: "Link",
            options: "Branch",
            width: "120px",
        },

        {
            fieldname: "company",
            label: __("Company"),
            fieldtype: "Link",
            options: "Company",
            default: frappe.defaults.get_user_default("Company"),
            width: "120px",
            reqd: 1,
        },

        {
            fieldname: "docstatus",
            label: __("Document Status"),
            fieldtype: "Select",
            options: ["Draft", "Submitted", "Cancelled"],
            default: "Submitted",
            width: "120px",
        }
    ]
};



function toggle_columns(report) {

    let calendar = report.get_filter_value("calendar");

    let hijri_fields = ["hijri_start_date", "hijri_end_date", "hijri_months"];
    let gregorian_fields = ["start_date", "end_date"];

    if (!report.datatable) return;

    report.datatable.datamanager.columns.forEach(col => {

        if (calendar === "Gregorian" && hijri_fields.includes(col.id)) {
            report.datatable.hideColumn(col.id);
        }

        else if (calendar === "Hijri" && gregorian_fields.includes(col.id)) {
            report.datatable.hideColumn(col.id);
        }

        else {
            report.datatable.showColumn(col.id);
        }
    });
}
