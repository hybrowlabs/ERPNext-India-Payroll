frappe.ui.form.on('Payroll Entry', {
    refresh(frm) {
        if (frm.doc.docstatus == 1 && frm.doc.status == "Submitted") {
            frm.add_custom_button(__("View Salary Register"), function () {
                frappe.set_route("query-report", "Salary Book Register");
            });
        }

        if (frm.doc.custom_bonus_payment_mode == "Bonus Payout") {
            if (frm.doc.custom_additional_salary_submitted == 0) {
                frm.page.clear_primary_action();
            }

            if (
                frm.doc.custom_additional_salary_created == 0 &&
                frm.doc.custom_additional_salary_submitted == 0 &&
                frm.doc.employees.length > 0
            ) {
                frm.add_custom_button(__('Create Additional Salary'), function () {
                    frappe.call({
                        method: 'cn_indian_payroll.cn_indian_payroll.overrides.additional_salary.get_additional_salary',
                        args: {
                            payroll_id: frm.doc.name,
                            company: frm.doc.company
                        },
                        callback: function (response) {
                            if (response.message) {
                                frm.set_value("custom_additional_salary_created", 1);
                                frm.save();
                            }
                        }
                    });
                });
            }
            if (
                frm.doc.custom_additional_salary_created == 1 &&
                frm.doc.custom_additional_salary_submitted == 0 &&
                frm.doc.employees.length > 0
            ) {
                frm.add_custom_button(__("Submit Additional Salary"), function () {
                    frappe.call({
                        method: "cn_indian_payroll.cn_indian_payroll.overrides.additional_salary.additional_salary_submit",
                        args: {
                            additional: frm.doc.name
                        },
                        callback: function (res) {
                            frm.set_value("custom_additional_salary_submitted", 1);
                            frm.save();
                        }
                    });
                });
            }
        }
    }
});
