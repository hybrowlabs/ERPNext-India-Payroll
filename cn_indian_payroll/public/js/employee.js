frappe.ui.form.on("Employee", {

    refresh(frm) {
        frm.trigger("toggle_fields");
    },

    custom_supplier_id(frm) {

        if (frm.doc.custom_supplier_id) {
            fetch_bank_accounts(frm);
        }
    },

    toggle_fields(frm) {

        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Payroll Settings",
                name: "Payroll Settings"
            },
            callback(r) {

                if (!r.message) return;

                let settings = r.message;
                let config = settings.custom_hide_salary_structure_configuration || [];

                let is_match = false;

               
                config.forEach(row => {
                    if (row.employment_type === frm.doc.employment_type) {
                        is_match = true;
                        frm.set_df_property("cell_number","reqd", 1);
                        frm.set_df_property("personal_email","reqd", 1);
                    }
                    else{
                        frm.set_df_property("cell_number","reqd", 0);
                        frm.set_df_property("personal_email","reqd", 0);
                    }
                });


               
                toggle_custom_fields(frm, is_match);


               
                if (is_match) {

                    load_select_options(frm);

                    if (frm.doc.custom_supplier_id) {
                        fetch_bank_accounts(frm);
                    }
                }
            }
        });
    }

});


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
        frm.set_df_property(field, "hidden", !show);
        frm.set_df_property(field, "reqd", show);

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
                frappe.msgprint("No data found");
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
