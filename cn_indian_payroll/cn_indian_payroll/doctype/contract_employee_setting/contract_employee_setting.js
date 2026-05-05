

// frappe.ui.form.on("Contract Employee Setting", {
//     refresh(frm) {

//         // -----------------------------
//         // Helper function
//         // -----------------------------
//         function fetch_options(method, callback) {

//             frappe.call({
//                 method: method,

//                 callback: function (r) {

//                     if (!r.message || !r.message.length) {
//                         frappe.msgprint("No data found");
//                         return;
//                     }

//                     let options = r.message.map(d => d.name);
//                     options.unshift("");

//                     callback(options.join("\n"));
//                 },

//                 error: function () {
//                     frappe.msgprint("Server error while loading data");
//                 }
//             });
//         }


//         // -----------------------------
//         // Items (Child Table)
//         // -----------------------------
//         fetch_options(
//             "cn_indian_payroll.cn_indian_payroll.doctype.contract_employee_setting.contract_employee_setting.get_item_list",
//             function (opts) {

//                 frm.fields_dict.table_peep.grid.update_docfield_property(
//                     "item",
//                     "options",
//                     opts
//                 );

//                 frm.refresh_field("table_peep");
//             }
//         );


//         // -----------------------------
//         // Company Mapping
//         // -----------------------------
//         fetch_options(
//             "cn_indian_payroll.cn_indian_payroll.doctype.contract_employee_setting.contract_employee_setting.get_company_list",
//             function (opts) {

//                 frm.fields_dict.map_the_company.grid.update_docfield_property(
//                     "company_in_erp",
//                     "options",
//                     opts
//                 );

//                 frm.refresh_field("map_the_company");
//             }
//         );


//         // -----------------------------
//         // Item Tax Template
//         // -----------------------------
//         fetch_options(
//             "cn_indian_payroll.cn_indian_payroll.doctype.contract_employee_setting.contract_employee_setting.get_item_tax_template",
//             function (opts) {

                
//                 frm.fields_dict.map_the_company.grid.update_docfield_property(
//                     "item_tax_template",
//                     "options",
//                     opts
//                 );

//                 frm.refresh_field("map_the_company");
//             }
//         );


//         // -----------------------------
//         // Payment Terms Template
//         // -----------------------------
//         fetch_options(
//             "cn_indian_payroll.cn_indian_payroll.doctype.contract_employee_setting.contract_employee_setting.get_payment_terms_template",
//             function (opts) {


//                 frm.fields_dict.map_the_company.grid.update_docfield_property(
//                     "purchase_tax_template",
//                     "options",
//                     opts
//                 );

//                 frm.refresh_field("map_the_company");
//             }
//         );


//          fetch_options(
//             "cn_indian_payroll.cn_indian_payroll.doctype.contract_employee_setting.contract_employee_setting.get_tax_with_hold_category_list",
//             function (opts) {


//                 frm.fields_dict.map_the_company.grid.update_docfield_property(
//                     "tax_with_holding_category",
//                     "options",
//                     opts
//                 );

//                 frm.refresh_field("map_the_company");
//             }
//         );






        


//         // -----------------------------
//         // Department Mapping
//         // -----------------------------
//         fetch_options(
//             "cn_indian_payroll.cn_indian_payroll.doctype.contract_employee_setting.contract_employee_setting.get_department_list",
//             function (opts) {

//                 frm.fields_dict.map_the_department.grid.update_docfield_property(
//                     "department_in_erp",
//                     "options",
//                     opts
//                 );

//                 frm.refresh_field("map_the_department");
//             }
//         );


//         // -----------------------------
//         // Work Location Mapping
//         // -----------------------------
//         fetch_options(
//             "cn_indian_payroll.cn_indian_payroll.doctype.contract_employee_setting.contract_employee_setting.get_worklocation_list",
//             function (opts) {

//                 frm.fields_dict.map_the_work_location.grid.update_docfield_property(
//                     "location_in_erp",
//                     "options",
//                     opts
//                 );

//                 frm.refresh_field("map_the_work_location");
//             }
//         );
//     }
// });
