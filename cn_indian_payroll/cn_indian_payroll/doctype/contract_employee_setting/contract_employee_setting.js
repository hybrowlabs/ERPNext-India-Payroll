frappe.ui.form.on("Contract Employee Setting", {
    refresh(frm) {

        frappe.call({
            method: "cn_indian_payroll.cn_indian_payroll.doctype.contract_employee_setting.contract_employee_setting.get_supplier_by_tax_id",
            callback: function (r) {

                if (!r.message || !r.message.length) {
                    frappe.msgprint("No Supplier found");
                    return;
                }

                // build select options
                let options = r.message.map(d => d.name);
                options.unshift("");

                // ✅ SAFE way to set child select options
                frm.fields_dict.table_peep.grid.update_docfield_property(
                    "item",
                    "options",
                    options.join("\n")
                );

                frm.refresh_field("table_peep");

                console.log("Supplier options loaded:", options);
            }
        });


        frappe.call({
            method: "cn_indian_payroll.cn_indian_payroll.doctype.contract_employee_setting.contract_employee_setting.get_company_list",
            callback: function (r) {

                if (!r.message || !r.message.length) {
                    frappe.msgprint("No Company found");
                    return;
                }

                // Build options list
                let options = r.message.map(d => d.name);
                options.unshift(""); // empty first option

                // ✅ Set options to Select field
                frm.set_df_property("company", "options", options.join("\n"));
                frm.refresh_field("company");

                console.log("Company options loaded:", options);
            }
        });

    }
});
