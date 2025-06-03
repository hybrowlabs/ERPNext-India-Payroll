frappe.ui.form.on('Structure Setting', {
    refresh(frm) {
        frm.add_custom_button(__('Create Salary Structure Assignment'), function () {
            frappe.call({
                method: "cn_indian_payroll.cn_indian_payroll.overrides.structure_setting.create_salary_structure_assignment",
                args: {
                    company: frm.doc.company,
                    payroll_period: frm.doc.payroll_period,
                    income_tax_slab: frm.doc.income_tax_slab,
                    effective_date: frm.doc.effective_from
                },
                callback: function (r) {
                    if (r.message === "queued") {
                        frappe.show_alert({
                            message: __('Processing started. You will see progress updates.'),
                            indicator: 'blue'
                        });
                    }
                }
            });
        });

        frappe.realtime.on("ssa_progress", function (data) {
            if (data.progress) {
                frappe.show_progress(__('Creating Assignments'), data.progress, 100, __('Working...'));
            }
            if (data.progress === 100) {
                frappe.show_alert({
                    message: __('All assignments created successfully'),
                    indicator: 'green'
                });
            }
        });
    }
});
