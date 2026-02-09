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

                console.log(options,"optionsoptionsoptions")

                // ✅ SAFE way to set child select options
                frm.fields_dict.table_peep.grid.update_docfield_property(
                    "item",
                    "options",
                    options.join("\n")
                );

                frm.refresh_field("table_peep");


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
                // let options = r.message.map(d => d.name);
                // options.unshift(""); // empty first option

                // // ✅ Set options to Select field
                // frm.set_df_property("company", "options", options.join("\n"));
                // frm.refresh_field("company");

                // console.log("Company options loaded:", options);

                let options = r.message.map(d => d.name);
                options.unshift("");

                // ✅ SAFE way to set child select options
                frm.fields_dict.map_the_company.grid.update_docfield_property(
                    "company_in_erp",
                    "options",
                    options.join("\n")
                );

                frm.refresh_field("map_the_company");
            }
        });


        frappe.call({
            method: "cn_indian_payroll.cn_indian_payroll.doctype.contract_employee_setting.contract_employee_setting.get_item_tax_template",
            callback: function (r) {

                if (!r.message || !r.message.length) {
                    frappe.msgprint("No Item Tax Template found");
                    return;
                }

                let options = r.message.map(d => d.name);
                options.unshift(""); // empty first option

                // ✅ Set options to Select field
                frm.set_df_property("item_tax_template", "options", options.join("\n"));
                frm.refresh_field("item_tax_template");


                // let options = r.message.map(d => d.name);
                // options.unshift("");

                // // ✅ SAFE way to set child select options
                // frm.fields_dict.map_the_department.grid.update_docfield_property(
                //     "department_in_erp",
                //     "options",
                //     options.join("\n")
                // );

                // frm.refresh_field("map_the_department");

            }
        });

        frappe.call({
            method: "cn_indian_payroll.cn_indian_payroll.doctype.contract_employee_setting.contract_employee_setting.get_payment_terms_template",
            callback: function (r) {

                if (!r.message || !r.message.length) {
                    frappe.msgprint("No Payment Terms Template found");
                    return;
                }

                let options = r.message.map(d => d.name);
                options.unshift(""); // empty first option

                // ✅ Set options to Select field
                frm.set_df_property("payment_terms_template", "options", options.join("\n"));
                frm.refresh_field("payment_terms_template");



                // let options = r.message.map(d => d.name);
                // options.unshift("");

                // // ✅ SAFE way to set child select options
                // frm.fields_dict.map_the_work_location.grid.update_docfield_property(
                //     "location_in_erp",
                //     "options",
                //     options.join("\n")
                // );

                // frm.refresh_field("map_the_work_location");

            }
        });




        frappe.call({
            method: "cn_indian_payroll.cn_indian_payroll.doctype.contract_employee_setting.contract_employee_setting.get_department_list",
            callback: function (r) {

                if (!r.message || !r.message.length) {
                    frappe.msgprint("No Department found");
                    return;
                }




                let options = r.message.map(d => d.name);
                options.unshift("");

                // ✅ SAFE way to set child select options
                frm.fields_dict.map_the_department.grid.update_docfield_property(
                    "department_in_erp",
                    "options",
                    options.join("\n")
                );

                frm.refresh_field("map_the_department");

            }
        });



        frappe.call({
            method: "cn_indian_payroll.cn_indian_payroll.doctype.contract_employee_setting.contract_employee_setting.get_worklocation_list",
            callback: function (r) {

                if (!r.message || !r.message.length) {
                    frappe.msgprint("No Work Location found");
                    return;
                }




                let options = r.message.map(d => d.name);
                options.unshift("");

                // ✅ SAFE way to set child select options
                frm.fields_dict.map_the_work_location.grid.update_docfield_property(
                    "location_in_erp",
                    "options",
                    options.join("\n")
                );

                frm.refresh_field("map_the_work_location");

            }
        });




    }
});
