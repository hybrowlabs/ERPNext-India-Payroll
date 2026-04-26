frappe.query_reports["EPF Challan Report"] = {
    filters: [
        {
            label: __("Company"),
            fieldname: "company",
            fieldtype: "Link",
            options: "Company",
            width: 200,
            reqd: 1,
            default: frappe.defaults.get_user_default("Company"),
        },
        {
            label: __("Month"),
            fieldname: "month",
            fieldtype: "Select",
            options: [
                "", "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December",
            ],
            width: 150,
            reqd: 1,
        },
        {
            label: __("Payroll Period"),
            fieldname: "payroll_period",
            fieldtype: "Link",
            options: "Payroll Period",
            width: 200,
        },
        {
            label: __("School / Branch"),
            fieldname: "branch",
            fieldtype: "Link",
            options: "Branch",
            width: 200,
        },
    ],

    onload: function (report) {
        report.page.add_inner_button(__("Download ECR Text File"), function () {
            const filters = report.get_values();
            if (!filters.company || !filters.month) {
                frappe.msgprint(__("Please select Company and Month before downloading."));
                return;
            }

            frappe.call({
                method: "cn_indian_payroll.cn_indian_payroll.report.epf_challan_report.epf_challan_report.download_ecr_txt",
                args: { filters: filters },
                callback: function (r) {
                    if (!r.message) {
                        frappe.msgprint(__("No data found for the selected filters."));
                        return;
                    }
                    const parts = [
                        "EPFO",
                        filters.month || "",
                        filters.company || "",
                        filters.payroll_period || "",
                        filters.branch || "",
                    ].filter(Boolean);
                    const filename = parts.join("_").replace(/\s+/g, "_") + ".txt";
                    const blob = new Blob([r.message], { type: "text/plain;charset=utf-8" });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement("a");
                    a.href = url;
                    a.download = filename;
                    a.click();
                    URL.revokeObjectURL(url);
                },
                error: function () {
                    frappe.msgprint(__("Failed to generate the ECR file. Please try again."));
                },
            });
        });
    },
};
