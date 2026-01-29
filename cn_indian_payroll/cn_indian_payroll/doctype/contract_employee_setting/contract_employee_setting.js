frappe.ui.form.on("Contract Employee Setting", {
    refresh(frm) {

        frappe.call({
            method: "cn_indian_payroll.cn_indian_payroll.overrides.leegality.get_supplier_by_tax_id",
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
    }
});
