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

        if(frm.doc.employees) {
            let new_joinee_salary_arrear = false;
            $.each(frm.doc.employees, function(i, v) {
                if(v.custom_new_joinee_with_salary_arrear) {
                    new_joinee_salary_arrear = true;
                }
            });

            if(new_joinee_salary_arrear && frm.doc.custom_salary_arrear_created == 0) {
                frm.add_custom_button(
                    __("Generate New Joinee Arrear"),
                    function() {
                        frappe.call({
                            method: 'cn_indian_payroll.cn_indian_payroll.overrides.payroll_entry.create_new_joinee_arrear',
                            args: {
                                company: frm.doc.company,
                                doc_id: frm.doc.name,
                                start_date: frm.doc.start_date,
                                end_date: frm.doc.end_date,
                                employees: frm.doc.employees
                            },
                            freeze: true, // show "Processing..."
                            freeze_message: __("Creating New Joinee Arrears..."),
                            callback: function(response) {
                                if (response.message) {

                                    frappe.msgprint({
                                        title: __("Success"),
                                        message: __("New Joinee Arrear created successfully for all employees."),
                                        indicator: "green"
                                    });

                                    frm.reload_doc();
                                }
                            }
                        });

                    }
                );
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
});
