frappe.ui.form.on('Payroll Entry', {
    refresh(frm) {


        // frm.fields_dict.custom_download_new_joinee_arrear.wrapper.innerHTML =
        //     new_joinee_buttons_html();

            window.download_new_joinee_data = function () {

            if (!frm.doc.custom_new_joinee_arrear_child ||
                !frm.doc.custom_new_joinee_arrear_child.length) {
                frappe.msgprint("No New Joinee data to download");
                return;
            }

            frappe.call({
                method: "cn_indian_payroll.cn_indian_payroll.overrides.payroll_config.download_new_joinee_excel",
                args: {
                    docname: frm.doc.name
                },
                freeze: true,
                callback: function (r) {
                    if (r.message) {
                        window.open(r.message);
                    }
                }
            });
        };






        // frm.fields_dict.custom_download_attendance_data.wrapper.innerHTML =
        //     get_attendance_action_buttons_html();

        // expose function globally (important)
        window.download_attendance_data = function () {

            if (!frm.doc.custom_employee_attendance_details_list ||
                !frm.doc.custom_employee_attendance_details_list.length) {
                frappe.msgprint("No attendance data to download");
                return;
            }

            frappe.call({
                method: "cn_indian_payroll.cn_indian_payroll.overrides.payroll_config.download_attendance_excel",
                args: {
                    docname: frm.doc.name
                },
                freeze: true,
                callback: function (r) {
                    if (r.message) {
                        window.open(r.message);
                    }
                }
            });
        };




        frm.fields_dict.custom_process_regularize_data.wrapper.innerHTML =
        get_action_buttons_html_attendance_regularise();


        $(document).on("click", "#download-attendance", function () {
            const frm = cur_frm;
            if (!frm || frm.is_new()) return;

            frappe.call({
                method: "cn_indian_payroll.cn_indian_payroll.overrides.payroll_config.download_attendance_regularise_excel",
                args: {
                    docname: frm.doc.name
                },
                freeze: true,
                callback(r) {
                    if (r.message) {
                        window.open(r.message);
                    }
                }
            });
        });


        $(document).on("click", "#process-attendance", function () {
    const frm = cur_frm;
    if (!frm || frm.is_new()) return;

    frappe.confirm(
        "Are you sure you want to process attendance data?",
        () => {
            frappe.call({
                method: "cn_indian_payroll.cn_indian_payroll.overrides.payroll_config.process_attendance_regularization",
                args: {
                    payroll_entry: frm.doc.name
                },
                freeze: true,
                callback(r) {
                    if (r.message) {
                        frappe.msgprint(`
                            ✅ Processed: ${r.message.processed || 0}<br>
                            ⚠ Errors: ${r.message.errors?.length ? r.message.errors.join("<br>") : "None"}
                        `);
                        frm.reload_doc();
                    }
                }
            });
        }
    );
});




//------------------------------------------------------------------------------------------------------


if(frm.doc.custom_upload_file)
{



        frm.fields_dict.custom_create_extra_payment.wrapper.innerHTML =
            custom_create_extra_payment();


            window.create_extrapayment = function () {

            if (!frm.doc.custom_additional_extra_payments_details ||
                !frm.doc.custom_additional_extra_payments_details.length) {
                frappe.msgprint("No Extrapayment data to Create");
                return;
            }

            frappe.call({
                method: "cn_indian_payroll.cn_indian_payroll.overrides.payroll_config.create_extra_payment",
                args: {
                    docname: frm.doc.name
                },
                freeze: true,
                callback(r) {
                    if (r.message) {
                        frappe.msgprint({
                            title: "Additional Salary Creation",
                            message: `
                                ✅ Created: ${r.message.created}<br>
                                ⏭ Skipped (already exists): ${r.message.skipped}
                            `,
                            indicator: "green"
                        });
                    }
                }
            });

        };

}

else{
    frm.fields_dict.custom_create_extra_payment.wrapper.innerHTML =""
}

//------------------------------------------------------------------------------------




        frm.fields_dict.custom_create_offcycle_payment.wrapper.innerHTML =
            custom_create_offcycle_payment();


            window.create_offcyclepayment = function () {

            if (!frm.doc.custom_offcycle_data ||
                !frm.doc.custom_offcycle_data.length) {
                frappe.msgprint("No Offcycle data to Create");
                return;
            }

            frappe.call({
                method: "cn_indian_payroll.cn_indian_payroll.overrides.payroll_config.create_offcycle_payment",
                args: {
                    docname: frm.doc.name
                },
                freeze: true,
                callback(r) {
                    if (r.message) {
                        frappe.msgprint({
                            title: "Additional Salary Creation",
                            message: `
                                ✅ Created: ${r.message.created}<br>
                                ⏭ Skipped (already exists): ${r.message.skipped}
                            `,
                            indicator: "green"
                        });
                    }
                }
            });

        };




//----------------------------------------------------------------------------------------



            // frm.fields_dict.custom_off_cycle_download.wrapper.innerHTML =
            // custom_offcycle_payment();
            // bind_offcycle_buttons(frm);

            // render_attach_button_offcycle(frm);







        // if (frm.is_new()) {
        //     frm.fields_dict.custom_attach_options.wrapper.innerHTML = "";
        //     return;
        // }



        // frm.fields_dict.custom_attach_options.wrapper.innerHTML =
        //     get_action_buttons_html();

        //     bind_action_buttons(frm);


        //     render_attach_button(frm);










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


    // custom_download_template(frm) {
    //     console.log("Downloading Template");
    //     frappe.call({
    //         method: "cn_indian_payroll.cn_indian_payroll.overrides.payroll_config.download_additional_salary_template",
    //         callback(r) {
    //             if (r.message) {
    //                 window.open(r.message);
    //             }
    //         }
    //     });
    // },

//     custom_process(frm) {
//     frappe.call({
//         method: "cn_indian_payroll.cn_indian_payroll.overrides.payroll_config.process_uploaded_excel",
//         args: {
//             payroll_entry: frm.doc.name
//         },
//         callback(r) {
//             if (r.message) {
//                 frappe.msgprint(
//                     `Created: ${r.message.success}<br>Errors: ${r.message.errors.length}`
//                 );
//             }
//         }
//     });
// },




// custom_process_regularize(frm){
//     console.log("Processing Attendance Regularization");
//     frappe.call({
//         method: "cn_indian_payroll.cn_indian_payroll.overrides.payroll_config.process_attendance_regularization",
//         args: {
//             payroll_entry: frm.doc.name
//         },
//         callback(r) {
//             if (r.message) {
//                 frappe.msgprint(
//                     `Processed Attendance Regularization `
//                 );
//             }
//         }
//     });
// }


});
function get_action_buttons_html() {
    return `
        <div style="
            display: flex;
            gap: 14px;
            margin-top: 10px;
            margin-bottom: 10px;
        ">

            ${make_action_btn("📥", "Download Template", "download-template", "#2563eb")}

            ${make_action_btn("📎", "Attach Template", "attach-template", "#7c3aed")}

            ${make_action_btn("⬆️", "Upload Data", "upload-data", "#16a34a")}

        </div>
    `;
}


function custom_offcycle_payment() {
    return `
        <div style="
            display: flex;
            gap: 14px;
            margin-top: 10px;
            margin-bottom: 10px;
        ">

            ${make_action_btn("📥", "Download Template", "download-offcycle-template", "#2563eb")}

            ${make_action_btn("📎", "Attach Template", "attach-offcycle-template", "#7c3aed")}

            ${make_action_btn("⬆️", "Upload Data", "upload-offcycle-data", "#16a34a")}

        </div>
    `;
}





function get_action_buttons_html_attendance_regularise() {
    return `
        <div style="
            display: flex;
            gap: 14px;
            margin-top: 10px;
            margin-bottom: 10px;
        ">
            
            ${make_action_btn("⬆️", "Process Data", "process-attendance", "#16a34a")}
        </div>
    `;
}






function make_action_btn(icon, label, id, color) {
    return `
        <button id="${id}"
            style="
                flex: 1;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
                padding: 10px 0;
                font-size: 14px;
                border-radius: 10px;
                border: 1px solid ${color};
                background: ${color};
                color: #fff;
                cursor: pointer;
                box-shadow: 0 2px 6px rgba(0,0,0,0.15);
            ">
            <span style="font-size:18px;">${icon}</span>
            <span class="btn-label">${label}</span>
        </button>
    `;
}


function bind_action_buttons(frm) {

    // DOWNLOAD TEMPLATE
    $("#download-template").off("click").on("click", function () {
        download_excel_template();
    });

    // ATTACH TEMPLATE
    $("#attach-template").off("click").on("click", function () {
        open_file_uploader(frm);
    });

    // UPLOAD DATA
    $("#upload-data").off("click").on("click", function () {
        upload_excel_data(frm);
    });
}



function bind_offcycle_buttons(frm) {

    // DOWNLOAD TEMPLATE
    $("#download-offcycle-template").off("click").on("click", function () {
        download_excel_template_offcycle();
    });

    // ATTACH TEMPLATE
    $("#attach-offcycle-template").off("click").on("click", function () {
        open_file_uploader_offcycle(frm);
    });

    // UPLOAD DATA
    $("#upload-offcycle-data").off("click").on("click", function () {
        upload_excel_data_offcycle(frm);
    });
}


function open_file_uploader(frm) {

    new frappe.ui.FileUploader({
        doctype: frm.doctype,
        docname: frm.docname,
        allow_multiple: false,

        on_success(file) {
            frm.set_value("custom_upload_file", file.file_url)
                .then(() => {
                    frm.save();
                    render_attach_button(frm);

                    frappe.msgprint({
                        title: "File Attached",
                        message: `File <b>${file.file_name}</b> attached successfully.`,
                        indicator: "green"
                    });
                });
        }
    });
}

function open_file_uploader_offcycle(frm) {

    new frappe.ui.FileUploader({
        doctype: frm.doctype,
        docname: frm.docname,
        allow_multiple: false,

        on_success(file) {
            frm.set_value("custom_offcycle_attach", file.file_url)
                .then(() => {
                    frm.save();
                    render_attach_button_offcycle(frm);

                    frappe.msgprint({
                        title: "File Attached",
                        message: `File <b>${file.file_name}</b> attached successfully.`,
                        indicator: "green"
                    });
                });
        }
    });
}





function render_attach_button(frm) {
    const btn = $("#attach-template");

    if (frm.doc.custom_upload_file) {
        const file_name = frm.doc.custom_upload_file.split("/").pop();

        btn.html(`
            <span style="font-size:18px;">📎</span>
            <span class="btn-label"
                  style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:70%;">
                ${file_name}
            </span>
            <span class="clear-attach-main"
                  style="margin-left:8px; cursor:pointer; font-weight:bold;">❌</span>
        `);

    } else {
        btn.html(make_action_btn(
            "📎",
            "Attach Template",
            "attach-template",
            "#7c3aed"
        ));
    }
}



function render_attach_button_offcycle(frm) {
    const btn = $("#attach-offcycle-template");

    if (frm.doc.custom_offcycle_attach) {
        const file_name = frm.doc.custom_offcycle_attach.split("/").pop();

        btn.html(`
            <span style="font-size:18px;">📎</span>
            <span class="btn-label"
                  style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:70%;">
                ${file_name}
            </span>
            <span class="clear-attach-main"
                  style="margin-left:8px; cursor:pointer; font-weight:bold;">❌</span>
        `);

    } else {
        btn.html(make_action_btn(
            "📎",
            "Attach Template",
            "attach-template",
            "#7c3aed"
        ));
    }
}




function download_excel_template() {
    window.open(
        "/api/method/cn_indian_payroll.cn_indian_payroll.overrides.payroll_config.download_extrapayment_template"
    );
}

function download_excel_template_offcycle() {
    window.open(
        "/api/method/cn_indian_payroll.cn_indian_payroll.overrides.payroll_config.download_offcycle_template"
    );
}


function new_joinee_buttons_html() {
    return `
        <div style="display:flex; gap:12px; margin-top:10px;">
            <button
                onclick="download_new_joinee_data()"
                style="
                    background-color:#16a34a;
                    color:white;
                    border:none;
                    padding:6px 12px;
                    border-radius:6px;
                    cursor:pointer;
                ">
                ⬇️ Download New Joinee Data
            </button>
        </div>
    `;
}



function get_attendance_action_buttons_html() {
    return `
        <div style="display:flex; gap:12px; margin-top:10px;">
            <button
                onclick="download_attendance_data()"
                style="
                    background-color:#16a34a;
                    color:white;
                    border:none;
                    padding:6px 12px;
                    border-radius:6px;
                    cursor:pointer;
                ">
                ⬇️ Download Attendance Data
            </button>
        </div>
    `;
}

function custom_create_extra_payment() {
    return `
        <div style="display:flex; gap:12px; margin-top:10px;">
            <button
                onclick="create_extrapayment()"
                style="
                    background-color:#16a34a;
                    color:white;
                    border:none;
                    padding:6px 12px;
                    border-radius:6px;
                    cursor:pointer;
                ">
                ⬇️ Create ExtraPayment/Extra Deduction Data
            </button>
        </div>
    `;
}

function custom_create_offcycle_payment() {
    return `
        <div style="display:flex; gap:12px; margin-top:10px;">
            <button
                onclick="create_offcyclepayment()"
                style="
                    background-color:#16a34a;
                    color:white;
                    border:none;
                    padding:6px 12px;
                    border-radius:6px;
                    cursor:pointer;
                ">
                ⬇️ Create Off Cycle Payment
            </button>
        </div>
    `;
}



function upload_excel_data(frm) {
    if (!frm.doc.custom_upload_file) {
        frappe.msgprint("Please attach a file first");
        return;
    }

    frappe.call({
        method: "cn_indian_payroll.cn_indian_payroll.overrides.payroll_config.process_uploaded_excel",
        args: {
            payroll_entry: frm.doc.name
        },
        callback(r) {
            if (r.message) {
                frappe.msgprint(`
                    ✅ Rows added: ${r.message.success}<br>
                    ⚠ Errors: ${r.message.errors.length ? r.message.errors.join("<br>") : "None"}
                `);
                frm.reload_doc();
            }
        }
    });
}


function upload_excel_data_offcycle(frm) {
    if (!frm.doc.custom_offcycle_attach) {
        frappe.msgprint("Please attach a file first");
        return;
    }

    frappe.call({
        method: "cn_indian_payroll.cn_indian_payroll.overrides.payroll_config.process_uploaded_excel_offcycle",
        args: {
            payroll_entry: frm.doc.name
        },
        callback(r) {
            if (r.message) {
                frappe.msgprint(`
                    ✅ Rows added: ${r.message.success}<br>
                    ⚠ Errors: ${r.message.errors.length ? r.message.errors.join("<br>") : "None"}
                `);
                frm.reload_doc();
            }
        }
    });
}
