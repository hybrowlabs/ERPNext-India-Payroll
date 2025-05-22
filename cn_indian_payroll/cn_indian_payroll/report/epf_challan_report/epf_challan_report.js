frappe.query_reports["EPF Challan Report"] = {
    "filters": [
        {
            "label": "Employee ID",
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 200
        },
        {
            "label": "Month",
            "fieldname": "month",
            "fieldtype": "Select",
            "options": ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            "width": 200
        },
        {
            "label": "Company",
            "fieldname": "company",
            "fieldtype": "Link",
            "options": "Company",
            "width": 200,
            "reqd": 1
        },
        {
            "label": "Payroll Period",
            "fieldname": "payroll_period",
            "fieldtype": "Link",
            "options": "Payroll Period",
            "width": 200,
            "reqd": 1
        }
    ],

    onload: function(report) {
        report.page.add_inner_button("Download ECR Text File", function() {
            let filters = report.get_values();

            frappe.call({
                method: "cn_indian_payroll.cn_indian_payroll.report.epf_challan_report.epf_challan_report.download_ecr_txt",
                args: { filters: filters },
                callback: function(r) {
                    if (r.message) {
                        const blob = new Blob([r.message], { type: "text/plain;charset=utf-8" });
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement("a");
                        a.href = url;
                        a.download = "epf_ecr.txt";
                        a.click();
                        URL.revokeObjectURL(url);
                    } else {
                        frappe.msgprint("Failed to generate file.");
                    }
                }
            });
        });
    }
};
