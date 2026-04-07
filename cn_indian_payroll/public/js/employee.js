

frappe.ui.form.on("Employee", {

    refresh(frm) {

            hide_consultant_fields(frm);

        // Run toggle logic
        // frm.trigger("toggle_fields");

        // if (frm.doc.custom_supplier_id) {
        //     fetch_bank_accounts(frm);
        // }
    },

    employment_type(frm) {
        hide_consultant_fields(frm);
    },

    // employment_type(frm) {
    //     // Re-check when employment type changes
    //     frm.trigger("toggle_fields");
    // },

    // custom_supplier_id(frm) {
    //     if (frm.doc.custom_supplier_id) {
    //         fetch_bank_accounts(frm);
    //     }
    // },

    // toggle_fields(frm) {

    //     if (frm._payroll_settings) {
    //         apply_settings(frm, frm._payroll_settings);
    //         return;
    //     }

    //     frappe.call({
    //         method: "frappe.client.get",
    //         args: {
    //             doctype: "Payroll Settings",
    //             name: "Payroll Settings"
    //         },
    //         callback(r) {

    //             if (!r.message) return;

    //             // Cache settings in form object
    //             frm._payroll_settings = r.message;

    //             apply_settings(frm, r.message);
    //         },
    //         error() {
    //             frappe.msgprint("Unable to load Payroll Settings");
    //         }
    //     });
    // }
});
function hide_consultant_fields(frm) {

    let fields_to_hide = [
        "custom_gst_number",
        "custom_trade_name",
        "custom_supplier_id",
        "custom_business_category",
        "custom_business_segment",
        "custom_work_flow_policy",
        "custom_bank_account_in_erp"
    ];

    frappe.call({
        method: "frappe.client.get",
        args: {
            doctype: "Payroll Settings",
            name: "Payroll Settings"
        },
        callback: function (r) {

            if (!r.message) return;

            let payroll_settings = r.message;

            let employment_types = [];

            if (payroll_settings.custom_hide_salary_structure_configuration) {
                employment_types = payroll_settings.custom_hide_salary_structure_configuration.map(row => row.employment_type);
            }

            
            let should_hide = employment_types.includes(frm.doc.employment_type);

            fields_to_hide.forEach(field => {
                frm.set_df_property(field, "hidden", should_hide ? 0 : 1);
            });
        }
    });
}


function apply_settings(frm, settings) {

    let config = settings.custom_hide_salary_structure_configuration || [];

    let is_match = config.some(row =>
        row.employment_type === frm.doc.employment_type
    );

    // Make fields required if match
    // frm.set_df_property("cell_number", "reqd", is_match ? 1 : 0);
    // frm.set_df_property("personal_email", "reqd", is_match ? 1 : 0);

    toggle_custom_fields(frm, is_match);

    // if (is_match) {
    //     load_select_options(frm);
    // }
}



function toggle_custom_fields(frm, show) {

    let fields = [
        "custom_gst_number",
        "custom_trade_name",
        "custom_supplier_id",
        "custom_business_category",
        "custom_business_segment",
        "custom_work_flow_policy",
        "custom_bank_account_in_erp"
    ];

    fields.forEach(field => {
        frm.set_df_property(field, "hidden", show ? 0 : 1);
    });

    frm.refresh_fields(fields);
}




function load_select_options(frm) {

    fetch_options(
        "cn_indian_payroll.cn_indian_payroll.doctype.contract_employee_setting.contract_employee_setting.get_business_segment_list",
        opts => set_options(frm, "custom_business_segment", opts)
    );

    fetch_options(
        "cn_indian_payroll.cn_indian_payroll.doctype.contract_employee_setting.contract_employee_setting.get_business_category_list",
        opts => set_options(frm, "custom_business_category", opts)
    );

    fetch_options(
        "cn_indian_payroll.cn_indian_payroll.doctype.contract_employee_setting.contract_employee_setting.get_workflow_policy_list",
        opts => set_options(frm, "custom_work_flow_policy", opts)
    );
}



function fetch_options(method, callback) {

    frappe.call({
        method: method,
        callback(r) {

            if (!r.message || !r.message.length) {
                return;
            }

            let options = r.message.map(d => d.name);
            options.unshift("");

            callback(options.join("\n"));
        },
        error() {
            frappe.msgprint("Server error while loading data");
        }
    });
}


function set_options(frm, fieldname, options) {

    frm.set_df_property(fieldname, "options", options);
    frm.refresh_field(fieldname);
}




function fetch_bank_accounts(frm) {

    frappe.call({
        method: "cn_indian_payroll.cn_indian_payroll.doctype.contract_employee_setting.contract_employee_setting.get_bank_accounts_by_supplier",
        args: {
            supplier_id: frm.doc.custom_supplier_id
        },
        callback(r) {

            if (r.message && r.message.length) {

                let options = ["", ...r.message].join("\n");

                frm.set_df_property(
                    "custom_bank_account_in_erp",
                    "options",
                    options
                );

                frm.refresh_field("custom_bank_account_in_erp");
            }
        }
    });
}