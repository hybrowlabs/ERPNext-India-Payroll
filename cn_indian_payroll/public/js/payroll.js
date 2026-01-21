frappe.ui.form.on('Payroll Entry', {
    refresh(frm) {



        if (
            frm.doc.custom_bank_sheet_generated == 0 &&
            frm.doc.docstatus === 1 &&
            frm.doc.status === "Submitted"
        ) {
            frm.add_custom_button(
                __("Generate Bank Mandate Sheet"),
                function() {
                    let d = new frappe.ui.Dialog({
                        title: __("Bank Mandate Details"),
                        fields: [
                            {
                                label: "Debit Account No",
                                fieldname: "debit_account_no",
                                fieldtype: "Data",
                                reqd: 1
                            },
                            {
                                label: "Pay Mode",
                                fieldname: "pay_mode",
                                fieldtype: "Select",
                                // options: ["NEFT", "RTGS", "IMPS"],
                                options: ["N", "R", "I"],

                                reqd: 1
                            },
                            {
                                label: "Payment Instruction Date",
                                fieldname: "payment_instruction_date",
                                fieldtype: "Date",
                                reqd: 1,
                                default: frappe.datetime.get_today()
                            },
                            {
                                label: "Credit Narration",
                                fieldname: "credit_narration",
                                fieldtype: "Small Text",
                                reqd: 1

                            }
                        ],
                        primary_action_label: __("Submit"),
                        primary_action(values) {
                            // Call backend with user inputs
                            frappe.call({
                                method: "cn_indian_payroll.cn_indian_payroll.overrides.additional_salary.update_payment_details",
                                args: {
                                    docname: frm.doc.name,
                                    debit_account_no: values.debit_account_no,
                                    pay_mode: values.pay_mode,
                                    payment_instruction_date: values.payment_instruction_date,
                                    credit_narration: values.credit_narration
                                },
                                callback: function(r) {
                                    if (!r.exc) {
                                        frappe.msgprint(__("Bank Mandate Sheet Generated Successfully"));
                                        frm.reload_doc();
                                    }
                                }
                            });
                            d.hide();
                        }
                    });

                    d.show();
                },
                __("Create")
            );
        }





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


    },

    custom_employment_type: function (frm) {
		frm.events.clear_employee_table(frm);
	},

    clear_employee_table: function (frm) {
		frm.clear_table("employees");
		frm.refresh();
	},
    custom_month(frm) {
        if (frm.doc.custom_month) {
            frappe.call({
                method: "cn_indian_payroll.cn_indian_payroll.overrides.tds_projection_calculation.get_payroll_period_dates_on_month",
                args: {

                    month: frm.doc.custom_month,
                    posting_date: frm.doc.posting_date
                },
                callback: function (r) {
                    if (r.message) {

                    frm.set_value("payroll_frequency","Monthly")

                    frm.set_value("start_date", r.message.start_date);
                    frm.set_value("end_date", r.message.end_date);


                    }
                }
            });
        }

    },


    custom_download_template(frm) {
        console.log("Downloading Template");
        frappe.call({
            method: "cn_indian_payroll.cn_indian_payroll.overrides.payroll_config.download_additional_salary_template",
            callback(r) {
                if (r.message) {
                    window.open(r.message);
                }
            }
        });
    },

    custom_process(frm) {
    frappe.call({
        method: "cn_indian_payroll.cn_indian_payroll.overrides.payroll_config.process_uploaded_excel",
        args: {
            payroll_entry: frm.doc.name
        },
        callback(r) {
            if (r.message) {
                frappe.msgprint(
                    `Created: ${r.message.success}<br>Errors: ${r.message.errors.length}`
                );
            }
        }
    });
},

custom_process_regularize(frm){
    console.log("Processing Attendance Regularization");
    frappe.call({
        method: "cn_indian_payroll.cn_indian_payroll.overrides.payroll_config.process_attendance_regularization",
        args: {
            payroll_entry: frm.doc.name
        },
        callback(r) {
            if (r.message) {
                frappe.msgprint(
                    `Processed Attendance Regularization `
                );
            }
        }
    });
}


});
