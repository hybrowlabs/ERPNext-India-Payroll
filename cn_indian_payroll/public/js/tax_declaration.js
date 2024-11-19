frappe.ui.form.on('Employee Tax Exemption Declaration', {

    refresh:function(frm)
    {
       



        if(frm.doc.custom_tax_regime=="New Regime")
            {
                frm.set_df_property('declarations',  'read_only',  1);
            }



            if(frm.doc.docstatus==1)
            {
                frm.add_custom_button("Edit Declaration",function()
                {
                    
                    // edit_declaration(frm)

                    edit(frm)
                    
                })
                frm.change_custom_button_type('Edit Declaration', null, 'primary');
            }

        



            
    },

    
   
});









function edit_declaration(frm) {
    if (frm.doc.employee) {
        var sub_category = [];

        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Employee Tax Exemption Sub Category",
                filters: {
                    "is_active": 1,
                    "name": ["not in", ["Employee Provident Fund (Auto)", "NPS Contribution by Employer", "Tax on employment (Professional Tax)"]]
                },
                fields: ["*"],
                limit_page_length: 999999999999
            },
            callback: function(subcategory_response) {
                if (subcategory_response.message && subcategory_response.message.length > 0) {
                    subcategory_response.message.forEach(function(v) {
                        sub_category.push(v.name);
                    });
                }

                if (frm.doc.custom_tax_regime === "Old Regime") {
                    let component_array = [];

                    let d = new frappe.ui.Dialog({
                        title: 'Enter details',
                        fields: [
                            {
                                label: 'Details Table',
                                fieldname: 'details_table',
                                fieldtype: 'Table',
                                fields: [
                                    {
                                        label: 'Exemption Sub Category',
                                        fieldname: 'exemption_sub_category',
                                        fieldtype: 'Select',
                                        options: sub_category,
                                        in_list_view: 1,
                                        editable: true
                                    },
                                    {
                                        label: 'Employee Tax Exemption Category',
                                        fieldname: 'employee_exemption_category',
                                        fieldtype: 'Data',
                                        in_list_view: 1,
                                        read_only: 1
                                    },
                                    {
                                        label: 'Maximum Exempted Amount',
                                        fieldname: 'maximum_amount',
                                        fieldtype: 'Data',
                                        in_list_view: 1,
                                        read_only: 1
                                    },
                                    {
                                        label: 'Declared Amount',
                                        fieldname: 'declared_amount',
                                        fieldtype: 'Data',
                                        in_list_view: 1,
                                        editable: true,
                                    },
                                ]
                            },
                            {
                                fieldtype: 'Section Break'
                            },
                            {
                                label: 'Monthly HRA Amount',
                                fieldname: 'hra_amount',
                                fieldtype: 'Currency',
                            },
                            {
                                fieldtype: 'Column Break'
                            },
                            {
                                label: 'Rented in Metro City',
                                fieldname: 'rented_in_metro_city',
                                fieldtype: 'Check',
                            }
                        ],
                        size: 'large',
                        primary_action_label: 'Submit',
                        primary_action(values) {
                            // let total_exe_amount = 0;
                            // $.each(frm.doc.declarations, function(i, k) {
                            //     if (k.exemption_category == "Section 80C") {
                            //         total_exe_amount = k.max_amount - k.amount;
                            //     }
                            // });

                            // let total_80C = 0;
                            // $.each(values.details_table, function(i, m) {
                            //     if (m.employee_exemption_category == "Section 80C") {
                            //         total_80C += parseFloat(m.declared_amount);
                            //     }
                            // });

                            // if (total_80C > total_exe_amount) {
                            //     frappe.msgprint(`You can't enter an amount greater than ${total_exe_amount} for Section 80C.`);
                            // } else {
                                // Add declarations with specific sub-categories to component_array
                                $.each(frm.doc.declarations, function(i, m) {
                                    if (["NPS Contribution by Employer", "Tax on employment (Professional Tax)", "Employee Provident Fund (Auto)","Uniform Allowance"].includes(m.exemption_sub_category)) {
                                        component_array.push({
                                            "sub_category": m.exemption_sub_category,
                                            "category": m.exemption_category,
                                            "max_amount": m.max_amount,
                                            "amount": m.amount
                                        });
                                    }
                                });

                                // Add dialog box values to component_array
                                $.each(values.details_table, function(i, w) {
                                    component_array.push({
                                        "sub_category": w.exemption_sub_category,
                                        "category": w.employee_exemption_category,
                                        "max_amount": w.maximum_amount,
                                        "amount": w.declared_amount
                                    });
                                });

                                console.log(component_array);

                                // Update child table
                                frm.clear_table('declarations');
                                component_array.forEach(row => {
                                    let new_row = frm.add_child('declarations');
                                    new_row.exemption_sub_category = row.sub_category;
                                    new_row.exemption_category = row.category;
                                    new_row.max_amount = row.max_amount;
                                    new_row.amount = row.amount;
                                });


                                frm.set_value("monthly_house_rent", values.hra_amount);
                                frm.set_value("rented_in_metro_city", values.rented_in_metro_city);
                                frm.set_value("custom_posting_date",frappe.datetime.nowdate())
                                frm.refresh_field('declarations');
                                frm.save('Update');
                                d.hide();



                            // }
                        }
                    });

                    d.show();

                    // Update employee_exemption_category when exemption_sub_category changes
                    d.$wrapper.on('change', '[data-fieldname="exemption_sub_category"] select', function() {
                        let selectedValue = $(this).val();
                        let rowIndex = $(this).closest('.grid-row').index();

                        if (selectedValue) {
                            frappe.call({
                                method: 'frappe.client.get',
                                args: {
                                    doctype: "Employee Tax Exemption Sub Category",
                                    name: selectedValue
                                },
                                callback: function(r) {
                                    if (r.message) {
                                        let category = r.message.exemption_category;
                                        let category_max_amount = r.message.max_amount;
                                        d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.employee_exemption_category = category;
                                        d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.maximum_amount = category_max_amount;
                                        d.fields_dict.details_table.grid.refresh();
                                    }
                                }
                            });
                        }
                    });

                    // Validate declared_amount input
                    // d.$wrapper.on('change', '[data-fieldname="declared_amount"] input', function() {
                    //     let rowIndex = $(this).closest('.grid-row').index();
                    //     let selectedAmount = $(this).val();
                    //     let maxAmount = d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.maximum_amount;
                    //     let component = d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.employee_exemption_category;

                    //     if (component == "Section 80C") {
                    //         $.each(frm.doc.declarations, function(i, v) {
                    //             if (v.exemption_category == component) {
                    //                 if (v.amount == 150000) {
                    //                     frappe.msgprint("You can't enter the amount here because your Section 80C is at the maximum.");
                    //                     d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.declared_amount = undefined;
                    //                     d.fields_dict.details_table.grid.refresh();
                    //                 } else {
                    //                     let remainingAmount = maxAmount - parseFloat(v.amount);

                    //                     if (selectedAmount > remainingAmount) {
                    //                         frappe.msgprint(`You can't enter an amount greater than ${remainingAmount}.`);
                    //                         d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.declared_amount = undefined;
                    //                         d.fields_dict.details_table.grid.refresh();
                    //                     }
                    //                 }
                    //             }
                    //         });
                    //     } 
                    //     else 
                    //     {

                    //         console.log(selectedAmount,"selectedAmount")
                    //         console.log(maxAmount,"maxAmount")
                    //         if (selectedAmount > maxAmount) {
                    //             frappe.msgprint(`You can't enter an amount greater than ${maxAmount}.`);
                    //             d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.declared_amount = undefined;
                    //             d.fields_dict.details_table.grid.refresh();
                    //         }
                    //     }
                    // });
                } else {
                    frappe.msgprint("You can't Edit the declaration because you are in the New regime.");
                }
            }
        });
    }
}



function edit(frm) {
    var component_array = [];
    var component_array_not_include = [];
    var sub_category = [];

    var component_from_dialogue=[]

    // Collect data from frm.doc.declarations
    $.each(frm.doc.declarations, function(i, m) {
        if (["NPS Contribution by Employer", "Tax on employment (Professional Tax)", "Employee Provident Fund (Auto)"].includes(m.exemption_sub_category)) {
            component_array.push({
                "exemption_sub_category": m.exemption_sub_category,
                "employee_exemption_category": m.exemption_category,
                "maximum_amount": m.max_amount,
                "declared_amount": m.amount
            });
        } else {
            component_array_not_include.push({
                "exemption_sub_category": m.exemption_sub_category,
                "employee_exemption_category": m.exemption_category,
                "maximum_amount": m.max_amount,
                "declared_amount": m.amount
            });
        }
    });

    // Fetch active subcategories
    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Employee Tax Exemption Sub Category",
            filters: {
                "is_active": 1,
                "name": ["not in", ["Employee Provident Fund (Auto)", "NPS Contribution by Employer", "Tax on employment (Professional Tax)"]]
            },
            fields: ["name"],
            limit_page_length: 999999999999
        },
        callback: function(subcategory_response) {
            if (subcategory_response.message && subcategory_response.message.length > 0) {
                sub_category = subcategory_response.message.map(v => v.name);

                if (frm.doc.custom_tax_regime === "Old Regime") {
                    let d = new frappe.ui.Dialog({
                        title: 'Declare Your Exemptions',
                        fields: [
                            {
                                label: 'Exemptions Auto Calculated',
                                fieldname: 'details_table',
                                fieldtype: 'Table',
                                cannot_add_rows: 1,
                                cannot_delete_rows: 1,
                                fields: [
                                    {
                                        label: 'Exemption Sub Category',
                                        fieldname: 'exemption_sub_category',
                                        fieldtype: 'Data',
                                        in_list_view: 1,
                                        read_only: 1
                                    },
                                    {
                                        label: 'Employee Tax Exemption Category',
                                        fieldname: 'employee_exemption_category',
                                        fieldtype: 'Data',
                                        in_list_view: 1,
                                        read_only: 1
                                    },
                                    {
                                        label: 'Maximum Exempted Amount',
                                        fieldname: 'maximum_amount',
                                        fieldtype: 'Data',
                                        in_list_view: 1,
                                        read_only: 1
                                    },
                                    {
                                        label: 'Declared Amount',
                                        fieldname: 'declared_amount',
                                        fieldtype: 'Data',
                                        in_list_view: 1,
                                        read_only: 1
                                    },
                                ]
                            },
                            {
                                fieldtype: 'Section Break'
                            },
                            {
                                label: 'Declare Tax Exemptions',
                                fieldname: 'custom_details_table',
                                fieldtype: 'Table',
                                fields: [
                                    {
                                        label: 'Exemption Sub Category',
                                        fieldname: 'custom_exemption_sub_category',
                                        fieldtype: 'Select',
                                        in_list_view: 1,
                                        options: sub_category.join('\n'),
                                        editable: true
                                    },
                                    {
                                        label: 'Employee Tax Exemption Category',
                                        fieldname: 'custom_employee_exemption_category',
                                        fieldtype: 'Data',
                                        in_list_view: 1,
                                        read_only: 1
                                    },
                                    {
                                        label: 'Maximum Exempted Amount',
                                        fieldname: 'custom_maximum_amount',
                                        fieldtype: 'Data',
                                        in_list_view: 1,
                                        read_only: 1
                                    },
                                    {
                                        label: 'Declared Amount',
                                        fieldname: 'custom_declared_amount',
                                        fieldtype: 'Data',
                                        in_list_view: 1,
                                        editable: true,
                                        reqd:1
                                    },
                                ]
                            },

                            {
                                fieldtype: 'Section Break'
                            },
                            {
                                label: 'Monthly HRA Amount',
                                fieldname: 'hra_amount',
                                fieldtype: 'Float',
                                default:frm.doc.monthly_house_rent,
                            },
                            {
                                fieldtype: 'Column Break'
                            },
                            {
                                label: 'Rented in Metro City',
                                fieldname: 'rented_in_metro_city',
                                fieldtype: 'Check',
                                default:frm.doc.rented_in_metro_city
                            },
                    
                        ],
                        size: 'large',
                        primary_action_label: 'Submit',
                        primary_action(values) {
                            d.hide();

                            // console.log(values)


                            $.each(values.details_table, function(i, w) {
                                component_from_dialogue.push({
                                    "sub_category": w.exemption_sub_category,
                                    "category": w.employee_exemption_category,
                                    "max_amount": w.maximum_amount,
                                    "amount": w.declared_amount
                                });
                            });

                            $.each(values.custom_details_table, function(i, m) {
                                component_from_dialogue.push({
                                    "sub_category": m.custom_exemption_sub_category,
                                    "category": m.custom_employee_exemption_category,
                                    "max_amount": m.custom_maximum_amount,
                                    "amount": m.custom_declared_amount
                                });
                            });

                            frm.clear_table('declarations');
                            component_from_dialogue.forEach(row => {
                                    let new_row = frm.add_child('declarations');
                                    new_row.exemption_sub_category = row.sub_category;
                                    new_row.exemption_category = row.category;
                                    new_row.max_amount = row.max_amount;
                                    new_row.amount = row.amount;
                                });

                                

                                frm.set_value("custom_check",0)
                                frm.set_value("monthly_house_rent", values.hra_amount);
                                frm.set_value("rented_in_metro_city", values.rented_in_metro_city);
                                frm.set_value("custom_posting_date",frappe.datetime.nowdate())
                                frm.refresh_field('declarations');
                                frm.save('Update');
                                d.hide();




                        }
                    });

                    // Populate the dialog's first table
                    let table_field = d.get_field('details_table');
                    if (!table_field.df.data) {
                        table_field.df.data = [];
                    }
                    component_array.forEach(item => {
                        table_field.df.data.push({
                            "exemption_sub_category": item.exemption_sub_category,
                            "employee_exemption_category": item.employee_exemption_category,
                            "maximum_amount": item.maximum_amount,
                            "declared_amount": item.declared_amount
                        });
                    });
                    table_field.grid.refresh();

                    let custom_table_field = d.get_field('custom_details_table');
                    if (!custom_table_field.df.data) {
                        custom_table_field.df.data = [];
                    }
                    component_array_not_include.forEach(item => {
                        custom_table_field.df.data.push({
                            "custom_exemption_sub_category": item.exemption_sub_category,
                            "custom_employee_exemption_category": item.employee_exemption_category,
                            "custom_maximum_amount": item.maximum_amount,
                            "custom_declared_amount": item.declared_amount
                        });
                    });
                    custom_table_field.grid.refresh();

                    d.show();  



                    d.$wrapper.on('change', '[data-fieldname="custom_exemption_sub_category"] select', function() {
                        let selectedValue = $(this).val();
                        let rowIndex = $(this).closest('.grid-row').index();

                        console.log(selectedValue,"7777")

                        if (selectedValue) {
                            frappe.call({
                                method: 'frappe.client.get',
                                args: {
                                    doctype: "Employee Tax Exemption Sub Category",
                                    name: selectedValue
                                },
                                callback: function(r) {
                                    if (r.message) {
                                        let category = r.message.exemption_category;
                                        let category_max_amount = r.message.max_amount;
                                        d.fields_dict.custom_details_table.grid.grid_rows[rowIndex].doc.custom_employee_exemption_category = category;
                                        d.fields_dict.custom_details_table.grid.grid_rows[rowIndex].doc.custom_maximum_amount = category_max_amount;
                                        d.fields_dict.custom_details_table.grid.refresh();
                                    }
                                }
                            });

                            


                        }
                    });

                    d.$wrapper.on('change', '[data-fieldname="custom_declared_amount"] input', function() {
                        let rowIndex = $(this).closest('.grid-row').index();
                        let selectedAmount = $(this).val();
                        
                        let component = d.fields_dict.custom_details_table.grid.grid_rows[rowIndex].doc.custom_exemption_sub_category;

                        if(component=="Uniform Allowance") {
                               

                                frappe.call({
                                    method: "frappe.client.get_list",
                                    args: {
                                        doctype: "Salary Structure Assignment",
                                        filters: { employee: frm.doc.employee, 'docstatus': 1 },
                                        fields: ["*"],
                                        limit: 1,
                                        order_by: "from_date desc"
                                    },
                                    callback: function(res) {
                                        if (res.message && res.message.length > 0) {

                                            if(res.message[0].custom_is_uniform_allowance==0)
                                            {
                                                msgprint("You Are Not Eligible for Uniform Allowance")
                                                d.fields_dict.custom_details_table.grid.grid_rows[rowIndex].doc.custom_declared_amount = 0;
                                                d.fields_dict.custom_details_table.grid.refresh();

                                            }

                                        }
                                    }
                                })



                            }
                        
                    })
                }

                else{
                    msgprint("You Cant Edit Declaration,Because You are in The New Regime")
                }
            }
        }
    });
}

































// frappe.ui.form.on('Employee Tax Exemption Declaration Category', {
//     refresh(frm) {
//         // your code here
//     },
    
//     amount:function(frm,cdt,cdn)
//     {
//         var d=locals[cdt][cdn]
//         // console.log(d,"000")
        
        
//         if(d.amount>d.max_amount)
//         {
//             frappe.model.set_value(cdt, cdn, "amount", 0);
//             msgprint("You Cant Enter Amount Greater than "+d.max_amount)
//         }
//     },

    

//     exemption_sub_category: function(frm, cdt, cdn) {
//         var d = locals[cdt][cdn];

//         console.log(d.exemption_sub_category);

//         frappe.call({
//             method: "frappe.client.get",
//             args: {
//                 doctype: "Employee Tax Exemption Sub Category",
//                 filters: { name: d.exemption_sub_category },
//                 fields: ["*"] 
//             },
//             callback: function(res) {
//                 if (res.message) {

                    
//                     if(res.message.custom_is_nps==1)
//                     {

//                         frappe.call({
//                             "method": "frappe.client.get_list",
//                             args: {
//                                 doctype: "Salary Structure Assignment",
//                                 filters: { employee: frm.doc.employee ,docstatus:1},
//                                 fields: ["*"],
//                                 order_by: "from_date desc",
//                                 limit: 1
//                             },
//                             callback: function(kes) {
//                                 if (kes.message && kes.message.length > 0) {


//                                     if(kes.message[0].custom_is_nps==1)
//                                     {
                                        
//                                         let nps_amount = Math.round((kes.message[0].base/12 * 0.35));
//                                         let nps_percentage=Math.round(nps_amount*kes.message[0].custom_nps_percentage/100);
//                                         let nps_amount_year = Math.round(nps_percentage * 12);
//                                         frappe.model.set_value(cdt, cdn, "max_amount", nps_amount_year);
//                                         frappe.model.set_value(cdt, cdn, "amount", nps_amount_year);



//                                     }
//                                     else{
//                                         frappe.model.set_value(cdt, cdn, "max_amount", 0);
//                                     }



//                                 }
//                             }
//                         })



//                     }


//                     if(res.message.custom_is_epf==1)
//                         {
    
//                             frappe.call({
//                                 "method": "frappe.client.get_list",
//                                 args: {
//                                     doctype: "Salary Structure Assignment",
//                                     filters: { employee: frm.doc.employee ,docstatus:1},
//                                     fields: ["*"],
//                                     order_by: "from_date desc",
//                                     limit: 1
//                                 },
//                                 callback: function(kes) {
//                                     if (kes.message && kes.message.length > 0) {
    
                                        
    
//                                         if(kes.message[0].custom_is_epf==1)
//                                         {
                                            
//                                             let epf_amount = Math.round((kes.message?.at(0).base/12)*0.35);
                                            
//                                             let epf_percentage=Math.round(epf_amount*12/100);
                                            
                                           
//                                             let epf_amount_year = Math.round(epf_percentage * 12);

//                                             if(epf_amount_year>res.message.max_amount)
//                                             {
//                                                 frappe.model.set_value(cdt, cdn, "max_amount", res.message.max_amount);
//                                                 frappe.model.set_value(cdt, cdn, "amount", res.message.max_amount);

                                                
//                                             }

//                                             else
//                                             {
//                                                 frappe.model.set_value(cdt, cdn, "max_amount", epf_amount_year);
//                                                 frappe.model.set_value(cdt, cdn, "amount", epf_amount_year);
//                                             }


                                            
    
    
    
//                                         }
//                                         else{
//                                             frappe.model.set_value(cdt, cdn, "max_amount", 0);
//                                         }
    
    
    
//                                     }
//                                 }
//                             })
    
    
    
//                         }


//                         frappe.model.set_value(cdt, cdn, "max_amount", res.message.max_amount);



                    
//                 } 
                
//             },
           
//         });
//     }
// })






// function edit(frm) 
// {
//     let d = new frappe.ui.Dialog({
//         title: 'Enter details',
//         fields: [
//             {
//                 label: 'Details Table',
//                 fieldname: 'details_table',
//                 fieldtype: 'Table',
//                 fields: [
//                     {
//                         label: 'Exemption Sub Category',
//                         fieldname: 'exemption_sub_category',
//                         fieldtype: 'Link',
//                         options: 'Employee Tax Exemption Sub Category',
//                         in_list_view: 1,
//                         editable: true,
//                         onchange: function() {
//                             console.log(d.get_field('details_table').get_value());
//                         }
//                     },
//                     {
//                         label: 'Employee Tax Exemption Category',
//                         fieldname: 'employee_exemption_category',
//                         fieldtype: 'Link',
//                         options: 'Employee Tax Exemption Category',
//                         in_list_view: 1,
//                         editable: true
//                     },
//                     {
//                         label: 'Maximum Exempted Amount',
//                         fieldname: 'maximum_amount',
//                         fieldtype: 'Currency',
//                         in_list_view: 1
//                     },
//                     {
//                         label: 'Declared Amount',
//                         fieldname: 'declared_amount',
//                         fieldtype: 'Currency',
//                         in_list_view: 1,
//                         editable: true
//                     }
//                 ]
//             }
//         ],
//         size: 'large',
//         primary_action_label: 'Submit',
//         primary_action(values) {
//             frm.clear_table('declarations');

//             var total_amount = 0;
//             values.details_table.forEach(row => {
//                 total_amount += row.declared_amount;
//                 let new_row = frm.add_child('declarations');
//                 new_row.exemption_sub_category = row.exemption_sub_category;
//                 new_row.exemption_category = row.employee_exemption_category;
//                 new_row.max_amount = row.maximum_amount;
//                 new_row.amount = row.declared_amount;
//             });

//             frm.refresh_field('declarations');

//             frm.set_value("total_declared_amount", total_amount);
//             frm.set_value("total_exemption_amount", total_amount);

//             frm.save('Update');

           

//             frappe.db.insert({
//                 "doctype": "Tax Declaration History",
//                 "employee": frm.doc.employee,
//                 "employee_name": frm.doc.employee_name,
//                 "company": frm.doc.company,
//                 "tax_exemption":frm.doc.name,
//                 "income_tax":frm.doc.custom_income_tax,
//                 "posting_date": frappe.datetime.nowdate(),
//                 "payroll_period": frm.doc.payroll_period,
//                 "monthly_house_rent": frm.doc.monthly_house_rent,
//                 "rented_in_metro_city": frm.doc.rented_in_metro_city,
//                 "hra_as_per_salary_structure": frm.doc.hra_as_per_salary_structure,
//                 "total_declared_amount": frm.doc.total_declared_amount,
//                 "annual_hra_exemption": frm.doc.annual_hra_exemption,
//                 "monthly_hra_exemption": frm.doc.monthly_hra_exemption,
//                 "total_exemption_amount": frm.doc.total_exemption_amount,
//                 "declaration_details": values.details_table.map(row => ({
//                     "exemption_sub_category": row.exemption_sub_category,
//                     "exemption_category": row.employee_exemption_category,
//                     "maximum_exempted_amount": row.maximum_amount,
//                     "declared_amount": row.declared_amount
//                 }))
//             })
            
            
            
            

//             d.hide();
//         }
//     });

//     d.show();
// }


// function edit_declaration(frm) {
//     if (frm.doc.employee) {
//         frappe.call({
//             method: "frappe.client.get_list",
//             args: {
//                 doctype: "Salary Structure Assignment",
//                 filters: { "employee": frm.doc.employee, "docstatus": 1 },
//                 fields: ["*"],
//                 limit: 1,
//                 order_by: "from_date desc",
//             },
//             callback: function(res) {
//                 if (res.message && res.message.length > 0) {
//                     let component_array = [];

//                     if (res.message[0].income_tax_slab === "Old Regime") {
//                         if (res.message[0].custom_is_uniform_allowance == 1) {
//                             let value = res.message[0].custom_uniform_allowance_value;
//                             if (value) {
//                                 frappe.call({
//                                     method: "frappe.client.get_list",
//                                     args: {
//                                         doctype: "Employee Tax Exemption Sub Category",
//                                         filters: { "custom_is_uniform": 1 },
//                                         fields: ["*"],
//                                     },
//                                     callback: function(response) {
//                                         if (response.message && response.message.length > 0) {
//                                             component_array.push({
//                                                 "sub_category": response.message[0].name,
//                                                 "category": response.message[0].exemption_category,
//                                                 "max_amount": value,
//                                                 "amount": value
//                                             });
//                                         }
//                                     }
//                                 });
//                             }
//                         }

//                         if (res.message[0].custom_is_epf == 1) {
//                             let epf_amount = Math.round((res.message[0].base * 0.35) / 12 * 0.12);
//                             if (epf_amount) {
//                                 frappe.call({
//                                     method: "frappe.client.get_list",
//                                     args: {
//                                         doctype: "Employee Tax Exemption Sub Category",
//                                         filters: { "custom_is_epf": 1 },
//                                         fields: ["*"],
//                                     },
//                                     callback: function(kes) {
//                                         if (kes.message && kes.message.length > 0) {
//                                             component_array.push({
//                                                 "sub_category": kes.message[0].name,
//                                                 "category": kes.message[0].exemption_category,
//                                                 "max_amount": epf_amount,
//                                                 "amount": epf_amount
//                                             });
//                                         }
//                                     }
//                                 });
//                             }
//                         }

//                         if (res.message[0].custom_is_nps == 1) {
//                             let nps_amount = Math.round(((res.message[0].base * 0.35) / 12 * res.message[0].custom_nps_percentage) / 100);
//                             if (nps_amount) {
//                                 frappe.call({
//                                     method: "frappe.client.get_list",
//                                     args: {
//                                         doctype: "Employee Tax Exemption Sub Category",
//                                         filters: { "custom_is_nps": 1 },
//                                         fields: ["*"],
//                                     },
//                                     callback: function(mes) {
//                                         if (mes.message && mes.message.length > 0) {
//                                             component_array.push({
//                                                 "sub_category": mes.message[0].name,
//                                                 "category": mes.message[0].exemption_category,
//                                                 "max_amount": nps_amount,
//                                                 "amount": nps_amount
//                                             });
//                                         }
//                                     }
//                                 });
//                             }
//                         }

//                         if (res.message[0].custom_state) {
//                             frappe.call({
//                                 method: "frappe.client.get_list",
//                                 args: {
//                                     doctype: "Employee Tax Exemption Sub Category",
//                                     filters: { "custom_is_pt": 1 },
//                                     fields: ["*"],
//                                 },
//                                 callback: function(jes) {
//                                     if (jes.message && jes.message.length > 0) {
//                                         component_array.push({
//                                             "sub_category": jes.message[0].name,
//                                             "category": jes.message[0].exemption_category,
//                                             "max_amount": jes.message[0].max_amount,
//                                             "amount": jes.message[0].max_amount
//                                         });
//                                     }
//                                 }
//                             });
//                         }

//                         setTimeout(function() {
                            

//                             let d = new frappe.ui.Dialog({
//                                 title: 'Enter details',
//                                 fields: [
//                                     {
//                                         label: 'Details Table',
//                                         fieldname: 'details_table',
//                                         fieldtype: 'Table',
//                                         fields: [
//                                             {
//                                                 label: 'Exemption Sub Category',
//                                                 fieldname: 'exemption_sub_category',
//                                                 fieldtype: 'Link',
//                                                 options: 'Employee Tax Exemption Sub Category',
//                                                 in_list_view: 1,
//                                                 editable: true,
//                                                 // onchange: function() {
//                                                 //     let table_field = d.fields_dict.details_table;
//                                                 //     let data = table_field.df.data;
                            
//                                                 //     // Access the table data directly
//                                                 //     if (data.length > 0) {
//                                                 //         data.forEach(row => {
//                                                 //             console.log(row.exemption_sub_category);
//                                                 //         });
//                                                 //     } else {
//                                                 //         console.log("No data in table");
//                                                 //     }
//                                                 // }

                                               
//                                             },
//                                             {
//                                                 label: 'Employee Tax Exemption Category',
//                                                 fieldname: 'employee_exemption_category',
//                                                 fieldtype: 'Link',
//                                                 options: 'Employee Tax Exemption Category',
//                                                 in_list_view: 1,
//                                                 editable: true
//                                             },
//                                             {
//                                                 label: 'Maximum Exempted Amount',
//                                                 fieldname: 'maximum_amount',
//                                                 fieldtype: 'Currency',
//                                                 in_list_view: 1,
//                                                 read_only:1
//                                             },
//                                             {
//                                                 label: 'Declared Amount',
//                                                 fieldname: 'declared_amount',
//                                                 fieldtype: 'Currency',
//                                                 in_list_view: 1,
//                                                 editable: true
//                                             }
//                                         ]
//                                     }
//                                 ],
//                                 size: 'large',
//                                 primary_action_label: 'Submit',
//                                 primary_action(values) {
//                                     frm.clear_table('declarations');
                        
//                                     var total_amount = 0;
//                                     values.details_table.forEach(row => {
//                                         total_amount += row.declared_amount;
//                                         let new_row = frm.add_child('declarations');
//                                         new_row.exemption_sub_category = row.exemption_sub_category;
//                                         new_row.exemption_category = row.employee_exemption_category;
//                                         new_row.max_amount = row.maximum_amount;
//                                         new_row.amount = row.declared_amount;
//                                     });
                        
//                                     frm.refresh_field('declarations');
                        
//                                     frm.set_value("total_declared_amount", total_amount);
//                                     frm.set_value("total_exemption_amount", total_amount);
                        
//                                     frm.save('Update');
                        
                                   
                        
//                                     frappe.db.insert({
//                                         doctype: "Tax Declaration History",
//                                         employee: frm.doc.employee,
//                                         employee_name: frm.doc.employee_name,
//                                         company: frm.doc.company,
//                                         tax_exemption: frm.doc.name,
//                                         income_tax: frm.doc.custom_income_tax,
//                                         posting_date: frappe.datetime.nowdate(),
//                                         payroll_period: frm.doc.payroll_period,
//                                         monthly_house_rent: frm.doc.monthly_house_rent,
//                                         rented_in_metro_city: frm.doc.rented_in_metro_city,
//                                         hra_as_per_salary_structure: frm.doc.salary_structure_hra,
//                                         total_declared_amount: frm.doc.total_declared_amount,
//                                         annual_hra_exemption: frm.doc.annual_hra_exemption,
//                                         monthly_hra_exemption: frm.doc.monthly_hra_exemption,
//                                         total_exemption_amount: frm.doc.total_exemption_amount,
//                                         declaration_details: values.details_table.map(row => ({
//                                             exemption_sub_category: row.exemption_sub_category,
//                                             exemption_category: row.employee_exemption_category,
//                                             maximum_exempted_amount: row.maximum_amount,
//                                             declared_amount: row.declared_amount
//                                         })),
//                                         hra_breakup: frm.doc.custom_hra_breakup.map(row => ({
//                                             month: row.month,
//                                             rent_paid: row.rent_paid,
//                                             earned_basic: row.earned_basic,
//                                             hra_received: row.hra_received,
//                                             excess_of_rent_paid: row.excess_of_rent_paid,
//                                             exemption_amount: row.exemption_amount
//                                         }))
//                                     });
                                    
                                    
                                    
                        
//                                     d.hide();
//                                 }
//                             });

                            
//                             d.fields_dict.details_table.df.data = [];
//                             component_array.forEach(item => {
//                                 d.fields_dict.details_table.df.data.push({
//                                     exemption_sub_category: item.sub_category,
//                                     employee_exemption_category: item.category,
//                                     maximum_amount: item.max_amount,
//                                     declared_amount: item.amount
//                                 });
//                             });
//                             d.fields_dict.details_table.grid.refresh();

//                             d.show();
//                         }, 1000);  
//                     }


//                     if (res.message[0].income_tax_slab === "New Regime") {
                       

//                         if (res.message[0].custom_is_nps == 1) {
//                             let nps_amount = Math.round(((res.message[0].base * 0.35) / 12 * res.message[0].custom_nps_percentage) / 100);
//                             if (nps_amount) {
//                                 frappe.call({
//                                     method: "frappe.client.get_list",
//                                     args: {
//                                         doctype: "Employee Tax Exemption Sub Category",
//                                         filters: { "custom_is_nps": 1 },
//                                         fields: ["*"],
//                                     },
//                                     callback: function(mes) {
//                                         if (mes.message && mes.message.length > 0) {
//                                             component_array.push({
//                                                 "sub_category": mes.message[0].name,
//                                                 "category": mes.message[0].exemption_category,
//                                                 "max_amount": nps_amount,
//                                                 "amount": nps_amount
//                                             });
//                                         }
//                                     }
//                                 });
//                             }
//                         }

                       
//                         setTimeout(function() {
                            

//                             let d = new frappe.ui.Dialog({
//                                 title: 'Enter details',
//                                 fields: [
//                                     {
//                                         label: 'Details Table',
//                                         fieldname: 'details_table',
//                                         fieldtype: 'Table',
//                                         fields: [
//                                             {
//                                                 label: 'Exemption Sub Category',
//                                                 fieldname: 'exemption_sub_category',
//                                                 fieldtype: 'Link',
//                                                 options: 'Employee Tax Exemption Sub Category',
//                                                 in_list_view: 1,
//                                                 editable: true,
//                                             },
//                                             {
//                                                 label: 'Employee Tax Exemption Category',
//                                                 fieldname: 'employee_exemption_category',
//                                                 fieldtype: 'Link',
//                                                 options: 'Employee Tax Exemption Category',
//                                                 in_list_view: 1,
//                                                 editable: true
//                                             },
//                                             {
//                                                 label: 'Maximum Exempted Amount',
//                                                 fieldname: 'maximum_amount',
//                                                 fieldtype: 'Currency',
//                                                 in_list_view: 1,
//                                                 read_only:1
//                                             },
//                                             {
//                                                 label: 'Declared Amount',
//                                                 fieldname: 'declared_amount',
//                                                 fieldtype: 'Currency',
//                                                 in_list_view: 1,
//                                                 editable: true
//                                             }
//                                         ]
//                                     }
//                                 ],
//                                 size: 'large',
//                                 primary_action_label: 'Submit',
//                                 primary_action(values) {
//                                     frm.clear_table('declarations');
                        
//                                     var total_amount = 0;
//                                     values.details_table.forEach(row => {
//                                         total_amount += row.declared_amount;
//                                         let new_row = frm.add_child('declarations');
//                                         new_row.exemption_sub_category = row.exemption_sub_category;
//                                         new_row.exemption_category = row.employee_exemption_category;
//                                         new_row.max_amount = row.maximum_amount;
//                                         new_row.amount = row.declared_amount;
//                                     });
                        
//                                     frm.refresh_field('declarations');
                        
//                                     frm.set_value("total_declared_amount", total_amount);
//                                     frm.set_value("total_exemption_amount", total_amount);
                        
//                                     frm.save('Update');
                        
                                   
                        
//                                     frappe.db.insert({
//                                         doctype: "Tax Declaration History",
//                                         employee: frm.doc.employee,
//                                         employee_name: frm.doc.employee_name,
//                                         company: frm.doc.company,
//                                         tax_exemption: frm.doc.name,
//                                         income_tax: frm.doc.custom_income_tax,
//                                         posting_date: frappe.datetime.nowdate(),
//                                         payroll_period: frm.doc.payroll_period,
//                                         monthly_house_rent: frm.doc.monthly_house_rent,
//                                         rented_in_metro_city: frm.doc.rented_in_metro_city,
//                                         hra_as_per_salary_structure: frm.doc.salary_structure_hra,
//                                         total_declared_amount: frm.doc.total_declared_amount,
//                                         annual_hra_exemption: frm.doc.annual_hra_exemption,
//                                         monthly_hra_exemption: frm.doc.monthly_hra_exemption,
//                                         total_exemption_amount: frm.doc.total_exemption_amount,
//                                         declaration_details: values.details_table.map(row => ({
//                                             exemption_sub_category: row.exemption_sub_category,
//                                             exemption_category: row.employee_exemption_category,
//                                             maximum_exempted_amount: row.maximum_amount,
//                                             declared_amount: row.declared_amount
//                                         })),
                                        
//                                     });
                                    
                                    
                                    
                        
//                                     d.hide();
//                                 }
//                             });

                            
//                             d.fields_dict.details_table.df.data = [];
//                             component_array.forEach(item => {
//                                 d.fields_dict.details_table.df.data.push({
//                                     exemption_sub_category: item.sub_category,
//                                     employee_exemption_category: item.category,
//                                     maximum_amount: item.max_amount,
//                                     declared_amount: item.amount
//                                 });
//                             });
//                             d.fields_dict.details_table.grid.refresh();

//                             d.show();
//                         }, 1000);  
//                     }


//                 }
//             }
//         });
//     }
// }





// function edit_declaration(frm) {
//     if (frm.doc.employee) {
//         var sub_category = [];

//         // Fetch all active Employee Tax Exemption Sub Categories
//         frappe.call({
//             method: "frappe.client.get_list",
//             args: {
//                 doctype: "Employee Tax Exemption Sub Category",
//                 filters: { "is_active": 1 },
//                 fields: ["*"],
//                 limit_page_length: 999999999999
//             },
//             callback: function(subcategory_response) {
//                 if (subcategory_response.message && subcategory_response.message.length > 0) {
//                     subcategory_response.message.forEach(function(v) {
//                         sub_category.push(v.name);
//                     });
//                 }
//             }
//         });

//         // Fetch the latest Salary Structure Assignment
//         frappe.call({
//             method: "frappe.client.get_list",
//             args: {
//                 doctype: "Salary Structure Assignment",
//                 filters: { "employee": frm.doc.employee, "docstatus": 1 },
//                 fields: ["*"],
//                 limit: 1,
//                 order_by: "from_date desc"
//             },
//             callback: function(res) {
//                 if (res.message && res.message.length > 0) {
//                     let component_array = [];
//                     let salary_structure = res.message[0];

//                     if (salary_structure.income_tax_slab === "Old Regime") {
//                         if (salary_structure.custom_is_uniform_allowance == 1) {
//                             let value = salary_structure.custom_uniform_allowance_value;
//                             if (value) {
//                                 frappe.call({
//                                     method: "frappe.client.get_list",
//                                     args: {
//                                         doctype: "Employee Tax Exemption Sub Category",
//                                         filters: { "custom_is_uniform": 1 },
//                                         fields: ["*"]
//                                     },
//                                     callback: function(response) {
//                                         if (response.message && response.message.length > 0) {
//                                             component_array.push({
//                                                 "sub_category": response.message[0].name,
//                                                 "category": response.message[0].exemption_category,
//                                                 "max_amount": value,
//                                                 "amount": value
//                                             });
//                                         }
//                                     }
//                                 });
//                             }
//                         }

//                         if (salary_structure.custom_is_epf == 1) {
//                             let epf_amount = Math.round((salary_structure.base * 0.35) / 12 * 0.12);
//                             if (epf_amount) {
//                                 frappe.call({
//                                     method: "frappe.client.get_list",
//                                     args: {
//                                         doctype: "Employee Tax Exemption Sub Category",
//                                         filters: { "custom_is_epf": 1 },
//                                         fields: ["*"]
//                                     },
//                                     callback: function(kes) {
//                                         if (kes.message && kes.message.length > 0) {
//                                             component_array.push({
//                                                 "sub_category": kes.message[0].name,
//                                                 "category": kes.message[0].exemption_category,
//                                                 "max_amount": epf_amount,
//                                                 "amount": epf_amount
//                                             });
//                                         }
//                                     }
//                                 });
//                             }
//                         }

//                         if (salary_structure.custom_is_nps == 1) {
//                             let nps_amount = Math.round(((salary_structure.base * 0.35) / 12 * salary_structure.custom_nps_percentage) / 100);
//                             if (nps_amount) {
//                                 frappe.call({
//                                     method: "frappe.client.get_list",
//                                     args: {
//                                         doctype: "Employee Tax Exemption Sub Category",
//                                         filters: { "custom_is_nps": 1 },
//                                         fields: ["*"]
//                                     },
//                                     callback: function(mes) {
//                                         if (mes.message && mes.message.length > 0) {
//                                             component_array.push({
//                                                 "sub_category": mes.message[0].name,
//                                                 "category": mes.message[0].exemption_category,
//                                                 "max_amount": nps_amount,
//                                                 "amount": nps_amount
//                                             });
//                                         }
//                                     }
//                                 });
//                             }
//                         }

//                         if (salary_structure.custom_state) {
//                             frappe.call({
//                                 method: "frappe.client.get_list",
//                                 args: {
//                                     doctype: "Employee Tax Exemption Sub Category",
//                                     filters: { "custom_is_pt": 1 },
//                                     fields: ["*"]
//                                 },
//                                 callback: function(jes) {
//                                     if (jes.message && jes.message.length > 0) {
//                                         component_array.push({
//                                             "sub_category": jes.message[0].name,
//                                             "category": jes.message[0].exemption_category,
//                                             "max_amount": jes.message[0].max_amount,
//                                             "amount": jes.message[0].max_amount
//                                         });
//                                     }
//                                 }
//                             });
//                         }

//                         // Delay to ensure all async calls are completed
//                         setTimeout(function() {
//                             let d = new frappe.ui.Dialog({
//                                 title: 'Enter details',
//                                 fields: [
//                                     {
//                                         label: 'Details Table',
//                                         fieldname: 'details_table',
//                                         fieldtype: 'Table',
//                                         fields: [
//                                             {
//                                                 label: 'Exemption Sub Category',
//                                                 fieldname: 'exemption_sub_category',
//                                                 fieldtype: 'Select',
//                                                 options: sub_category,
//                                                 in_list_view: 1,
//                                                 editable: true
//                                             },
//                                             {
//                                                 label: 'Employee Tax Exemption Category',
//                                                 fieldname: 'employee_exemption_category',
//                                                 fieldtype: 'Data',
//                                                 in_list_view: 1,
//                                                 editable: true,
//                                                 read_only: 1
//                                             },
//                                             {
//                                                 label: 'Maximum Exempted Amount',
//                                                 fieldname: 'maximum_amount',
//                                                 fieldtype: 'Currency',
//                                                 in_list_view: 1,
//                                                 read_only: 1
//                                             },
//                                             {
//                                                 label: 'Declared Amount',
//                                                 fieldname: 'declared_amount',
//                                                 fieldtype: 'Currency',
//                                                 in_list_view: 1,
//                                                 editable: true
//                                             }
//                                         ]
//                                     }
//                                 ],
//                                 size: 'large',
//                                 primary_action_label: 'Submit',
//                                 primary_action(values) {
//                                     frm.clear_table('declarations');

//                                     var total_amount = 0;
//                                     values.details_table.forEach(row => {
//                                         total_amount += row.declared_amount;
//                                         let new_row = frm.add_child('declarations');
//                                         new_row.exemption_sub_category = row.exemption_sub_category;
//                                         new_row.exemption_category = row.employee_exemption_category;
//                                         new_row.max_amount = row.maximum_amount;
//                                         new_row.amount = row.declared_amount;
//                                     });

//                                     frm.refresh_field('declarations');

//                                     frm.set_value("total_declared_amount", total_amount);
//                                     frm.set_value("total_exemption_amount", total_amount);

//                                     frm.save('Update');


//                                 frappe.db.insert({
//                                         doctype: "Tax Declaration History",
//                                         employee: frm.doc.employee,
//                                         employee_name: frm.doc.employee_name,
//                                         company: frm.doc.company,
//                                         tax_exemption: frm.doc.name,
//                                         income_tax: frm.doc.custom_income_tax,
//                                         posting_date: frappe.datetime.nowdate(),
//                                         payroll_period: frm.doc.payroll_period,
//                                         monthly_house_rent: frm.doc.monthly_house_rent,
//                                         rented_in_metro_city: frm.doc.rented_in_metro_city,
//                                         hra_as_per_salary_structure: frm.doc.salary_structure_hra,
//                                         total_declared_amount: frm.doc.total_declared_amount,
//                                         annual_hra_exemption: frm.doc.annual_hra_exemption,
//                                         monthly_hra_exemption: frm.doc.monthly_hra_exemption,
//                                         total_exemption_amount: frm.doc.total_exemption_amount,
//                                         declaration_details: values.details_table.map(row => ({
//                                             exemption_sub_category: row.exemption_sub_category,
//                                             exemption_category: row.employee_exemption_category,
//                                             maximum_exempted_amount: row.maximum_amount,
//                                             declared_amount: row.declared_amount
//                                         })),
//                                         hra_breakup: frm.doc.custom_hra_breakup.map(row => ({
//                                             month: row.month,
//                                             rent_paid: row.rent_paid,
//                                             earned_basic: row.earned_basic,
//                                             hra_received: row.hra_received,
//                                             excess_of_rent_paid: row.excess_of_rent_paid,
//                                             exemption_amount: row.exemption_amount
//                                         }))
//                                     });
                                    
                                    


//                                     d.hide();
//                                 }
//                             });

//                             d.fields_dict.details_table.df.data = [];
//                             component_array.forEach(item => {
//                                 d.fields_dict.details_table.df.data.push({
//                                     exemption_sub_category: item.sub_category,
//                                     employee_exemption_category: item.category,
//                                     maximum_amount: item.max_amount,
//                                     declared_amount: item.amount
//                                 });
//                             });
//                             d.fields_dict.details_table.grid.refresh();

//                             d.show();

//                             // Update employee_exemption_category when exemption_sub_category changes
//                             d.$wrapper.on('change', '[data-fieldname="exemption_sub_category"] select', function() {
//                                 let selectedValue = $(this).val();
//                                 let rowIndex = $(this).closest('.grid-row').index();

//                                 if (selectedValue) {
//                                     frappe.call({
//                                         method: 'frappe.client.get',
//                                         args: {
//                                             doctype: "Employee Tax Exemption Sub Category",
//                                             name: selectedValue
//                                         },
//                                         callback: function(r) {
//                                             if (r.message) {
//                                                 let category = r.message.exemption_category;
//                                                 let category_max_amount=r.message.max_amount;
//                                                 d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.employee_exemption_category = category;
//                                                 d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.maximum_amount = category_max_amount;
//                                                 d.fields_dict.details_table.grid.refresh();
//                                             }
//                                         }
//                                     });
//                                 }
//                             });

//                             d.$wrapper.on('change', '[data-fieldname="declared_amount"] input', function () {
//                                 let selectedAmount = $(this).val();
//                                 console.log('Selected value in Amount:', selectedAmount);
                                
//                             });

//                         }, 1000);
//                     }
//                 }
//             }
//         });
//     }
// }




// function edit_declaration(frm) {
//     if (frm.doc.employee) {
//         var sub_category = [];

//         // Fetch all active Employee Tax Exemption Sub Categories
//         frappe.call({
//             method: "frappe.client.get_list",
//             args: {
//                 doctype: "Employee Tax Exemption Sub Category",
//                 filters: { "is_active": 1 },
//                 fields: ["*"],
//                 limit_page_length: 999999999999
//             },
//             callback: function(subcategory_response) {
//                 if (subcategory_response.message && subcategory_response.message.length > 0) {
//                     subcategory_response.message.forEach(function(v) {
//                         sub_category.push(v.name);
//                     });
//                 }
//             }
//         });

//         // Fetch the latest Salary Structure Assignment
//         frappe.call({
//             method: "frappe.client.get_list",
//             args: {
//                 doctype: "Salary Structure Assignment",
//                 filters: { "employee": frm.doc.employee, "docstatus": 1 },
//                 fields: ["*"],
//                 limit: 1,
//                 order_by: "from_date desc"
//             },
//             callback: function(res) {
//                 if (res.message && res.message.length > 0) {
//                     let component_array = [];
//                     let salary_structure = res.message[0];

//                     if (salary_structure.income_tax_slab === "Old Regime") {
//                         if (salary_structure.custom_is_uniform_allowance == 1) {
//                             let value = salary_structure.custom_uniform_allowance_value;
//                             if (value) {
//                                 frappe.call({
//                                     method: "frappe.client.get_list",
//                                     args: {
//                                         doctype: "Employee Tax Exemption Sub Category",
//                                         filters: { "custom_is_uniform": 1 },
//                                         fields: ["*"]
//                                     },
//                                     callback: function(response) {
//                                         if (response.message && response.message.length > 0) {
//                                             component_array.push({
//                                                 "sub_category": response.message[0].name,
//                                                 "category": response.message[0].exemption_category,
//                                                 "max_amount": value,
//                                                 "amount": value
//                                             });
//                                         }
//                                     }
//                                 });
//                             }
//                         }

//                         if (salary_structure.custom_is_epf == 1) {
//                             let epf_amount = Math.round((salary_structure.base * 0.35) / 12 * 0.12);
//                             if (epf_amount) {
//                                 frappe.call({
//                                     method: "frappe.client.get_list",
//                                     args: {
//                                         doctype: "Employee Tax Exemption Sub Category",
//                                         filters: { "custom_is_epf": 1 },
//                                         fields: ["*"]
//                                     },
//                                     callback: function(kes) {
//                                         if (kes.message && kes.message.length > 0) {
//                                             component_array.push({
//                                                 "sub_category": kes.message[0].name,
//                                                 "category": kes.message[0].exemption_category,
//                                                 "max_amount": epf_amount,
//                                                 "amount": epf_amount
//                                             });
//                                         }
//                                     }
//                                 });
//                             }
//                         }

//                         if (salary_structure.custom_is_nps == 1) {
//                             let nps_amount = Math.round(((salary_structure.base * 0.35) / 12 * salary_structure.custom_nps_percentage) / 100);
//                             if (nps_amount) {
//                                 frappe.call({
//                                     method: "frappe.client.get_list",
//                                     args: {
//                                         doctype: "Employee Tax Exemption Sub Category",
//                                         filters: { "custom_is_nps": 1 },
//                                         fields: ["*"]
//                                     },
//                                     callback: function(mes) {
//                                         if (mes.message && mes.message.length > 0) {
//                                             component_array.push({
//                                                 "sub_category": mes.message[0].name,
//                                                 "category": mes.message[0].exemption_category,
//                                                 "max_amount": nps_amount,
//                                                 "amount": nps_amount
//                                             });
//                                         }
//                                     }
//                                 });
//                             }
//                         }

//                         if (salary_structure.custom_state) {
//                             frappe.call({
//                                 method: "frappe.client.get_list",
//                                 args: {
//                                     doctype: "Employee Tax Exemption Sub Category",
//                                     filters: { "custom_is_pt": 1 },
//                                     fields: ["*"]
//                                 },
//                                 callback: function(jes) {
//                                     if (jes.message && jes.message.length > 0) {
//                                         component_array.push({
//                                             "sub_category": jes.message[0].name,
//                                             "category": jes.message[0].exemption_category,
//                                             "max_amount": jes.message[0].max_amount,
//                                             "amount": jes.message[0].max_amount
//                                         });
//                                     }
//                                 }
//                             });
//                         }

//                         // Delay to ensure all async calls are completed
//                         setTimeout(function() {
//                             let d = new frappe.ui.Dialog({
//                                 title: 'Enter details',
//                                 fields: [
//                                     {
//                                         label: 'Details Table',
//                                         fieldname: 'details_table',
//                                         fieldtype: 'Table',
//                                         fields: [
//                                             {
//                                                 label: 'Exemption Sub Category',
//                                                 fieldname: 'exemption_sub_category',
//                                                 fieldtype: 'Select',
//                                                 options: sub_category,
//                                                 in_list_view: 1,
//                                                 editable: true
//                                             },
//                                             {
//                                                 label: 'Employee Tax Exemption Category',
//                                                 fieldname: 'employee_exemption_category',
//                                                 fieldtype: 'Data',
//                                                 in_list_view: 1,
//                                                 editable: true,
//                                                 read_only: 1
//                                             },
//                                             {
//                                                 label: 'Maximum Exempted Amount',
//                                                 fieldname: 'maximum_amount',
//                                                 fieldtype: 'Currency',
//                                                 in_list_view: 1,
//                                                 read_only: 1
//                                             },
//                                             {
//                                                 label: 'Declared Amount',
//                                                 fieldname: 'declared_amount',
//                                                 fieldtype: 'Currency',
//                                                 in_list_view: 1,
//                                                 editable: true
//                                             }
//                                         ]
//                                     }
//                                 ],
//                                 size: 'large',
//                                 primary_action_label: 'Submit',
//                                 primary_action(values) {
//                                     frm.clear_table('declarations');

//                                     var total_amount = 0;
//                                     values.details_table.forEach(row => {
//                                         total_amount += row.declared_amount;
//                                         let new_row = frm.add_child('declarations');
//                                         new_row.exemption_sub_category = row.exemption_sub_category;
//                                         new_row.exemption_category = row.employee_exemption_category;
//                                         new_row.max_amount = row.maximum_amount;
//                                         new_row.amount = row.declared_amount;
//                                     });

//                                     frm.refresh_field('declarations');

//                                     frm.set_value("total_declared_amount", total_amount);
//                                     frm.set_value("total_exemption_amount", total_amount);

//                                     frm.save('Update');


//                                 frappe.db.insert({
//                                         doctype: "Tax Declaration History",
//                                         employee: frm.doc.employee,
//                                         employee_name: frm.doc.employee_name,
//                                         company: frm.doc.company,
//                                         tax_exemption: frm.doc.name,
//                                         income_tax: frm.doc.custom_income_tax,
//                                         posting_date: frappe.datetime.nowdate(),
//                                         payroll_period: frm.doc.payroll_period,
//                                         monthly_house_rent: frm.doc.monthly_house_rent,
//                                         rented_in_metro_city: frm.doc.rented_in_metro_city,
//                                         hra_as_per_salary_structure: frm.doc.salary_structure_hra,
//                                         total_declared_amount: frm.doc.total_declared_amount,
//                                         annual_hra_exemption: frm.doc.annual_hra_exemption,
//                                         monthly_hra_exemption: frm.doc.monthly_hra_exemption,
//                                         total_exemption_amount: frm.doc.total_exemption_amount,
//                                         declaration_details: values.details_table.map(row => ({
//                                             exemption_sub_category: row.exemption_sub_category,
//                                             exemption_category: row.employee_exemption_category,
//                                             maximum_exempted_amount: row.maximum_amount,
//                                             declared_amount: row.declared_amount
//                                         })),
//                                         hra_breakup: frm.doc.custom_hra_breakup.map(row => ({
//                                             month: row.month,
//                                             rent_paid: row.rent_paid,
//                                             earned_basic: row.earned_basic,
//                                             hra_received: row.hra_received,
//                                             excess_of_rent_paid: row.excess_of_rent_paid,
//                                             exemption_amount: row.exemption_amount
//                                         }))
//                                     });
                                    
                                    


//                                     d.hide();
//                                 }
//                             });

//                             d.fields_dict.details_table.df.data = [];
//                             component_array.forEach(item => {
//                                 d.fields_dict.details_table.df.data.push({
//                                     exemption_sub_category: item.sub_category,
//                                     employee_exemption_category: item.category,
//                                     maximum_amount: item.max_amount,
//                                     declared_amount: item.amount
//                                 });
//                             });
//                             d.fields_dict.details_table.grid.refresh();

//                             d.show();

//                             // Update employee_exemption_category when exemption_sub_category changes
//                             d.$wrapper.on('change', '[data-fieldname="exemption_sub_category"] select', function() {
//                                 let selectedValue = $(this).val();
//                                 let rowIndex = $(this).closest('.grid-row').index();

//                                 if (selectedValue) {
//                                     frappe.call({
//                                         method: 'frappe.client.get',
//                                         args: {
//                                             doctype: "Employee Tax Exemption Sub Category",
//                                             name: selectedValue
//                                         },
//                                         callback: function(r) {
//                                             if (r.message) {
//                                                 let category = r.message.exemption_category;
//                                                 let category_max_amount=r.message.max_amount;
//                                                 d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.employee_exemption_category = category;
//                                                 d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.maximum_amount = category_max_amount;
//                                                 d.fields_dict.details_table.grid.refresh();
//                                             }
//                                         }
//                                     });
//                                 }
//                             });

//                             d.$wrapper.on('change', '[data-fieldname="declared_amount"] input', function () {
//                                 let selectedAmount = $(this).val();
//                                 console.log('Selected value in Amount:', selectedAmount);
                                
//                             });

//                         }, 1000);
//                     }
//                 }
//             }
//         });
//     }
// }




// function edit_declaration(frm) {
//     if (frm.doc.employee) {
//         var sub_category = [];

//         frappe.call({
//             method: "frappe.client.get_list",
//             args: {
//                 doctype: "Employee Tax Exemption Sub Category",
//                 filters: {
//                     "is_active": 1,
//                     "name": ["not in", ["Employee Provident Fund (Auto)", "NPS Contribution by Employer", "Tax on employment (Professional Tax)"]]
//                 },
//                 fields: ["*"],
//                 limit_page_length: 999999999999
//             },
//             callback: function(subcategory_response) {
//                 if (subcategory_response.message && subcategory_response.message.length > 0) {
//                     subcategory_response.message.forEach(function(v) {
//                         sub_category.push(v.name);
//                     });
//                 }

//                 if (frm.doc.custom_income_tax === "Old Regime") {
//                     let d = new frappe.ui.Dialog({
//                         title: 'Enter details',
//                         fields: [
//                             {
//                                 label: 'Details Table',
//                                 fieldname: 'details_table',
//                                 fieldtype: 'Table',
//                                 fields: [
//                                     {
//                                         label: 'Exemption Sub Category',
//                                         fieldname: 'exemption_sub_category',
//                                         fieldtype: 'Select',
//                                         options: sub_category,
//                                         in_list_view: 1,
//                                         editable: true
//                                     },
//                                     {
//                                         label: 'Employee Tax Exemption Category',
//                                         fieldname: 'employee_exemption_category',
//                                         fieldtype: 'Data',
//                                         in_list_view: 1,
//                                         read_only: 1
//                                     },
//                                     {
//                                         label: 'Maximum Exempted Amount',
//                                         fieldname: 'maximum_amount',
//                                         fieldtype: 'Currency',
//                                         in_list_view: 1,
//                                         read_only: 1
//                                     },
//                                     {
//                                         label: 'Declared Amount',
//                                         fieldname: 'declared_amount',
//                                         fieldtype: 'Currency',
//                                         in_list_view: 1,
//                                         editable: true,
//                                     },
                                    

//                                 ]
//                             },

//                             {
//                                 fieldtype: 'Section Break'
//                             },
//                             {
//                                 label: 'Monthly HRA Amount',
//                                 fieldname: 'hra_amount',
//                                 fieldtype: 'Currency',
                                
//                             },
//                             {
//                                 fieldtype: 'Column Break'
//                             },
//                             {
//                                 label: 'Rented in Metro City',
//                                 fieldname: 'rented_in_metro_city',
//                                 fieldtype: 'Check',
                                
//                             }
//                         ],
//                         size: 'large',
//                         primary_action_label: 'Submit',
//                         primary_action(values) {
//                             let total_exe_amount = 0;
//                             $.each(frm.doc.declarations, function(i, k) {
//                                 if (k.exemption_category == "Section 80C") {
//                                     total_exe_amount = k.max_amount - k.amount;
//                                 }
//                             });

//                             let total_80C = 0;
//                             $.each(values.details_table, function(i, m) {
//                                 if (m.employee_exemption_category == "Section 80C") {
//                                     total_80C += parseFloat(m.declared_amount);
//                                 }
//                             });

//                             if (total_80C > total_exe_amount) {
//                                 frappe.msgprint(`You can't enter an amount greater than ${total_exe_amount} for Section 80C.`);
//                             } else {
//                                 let component_array = [];

//                                 // Fetch Salary Structure and other values
//                                 frappe.call({
//                                     method: "frappe.client.get_list",
//                                     args: {
//                                         doctype: "Salary Structure Assignment",
//                                         filters: { "employee": frm.doc.employee, "docstatus": 1 },
//                                         fields: ["*"],
//                                         limit: 1,
//                                         order_by: "from_date desc"
//                                     },
//                                     callback: function(res) {
//                                         if (res.message && res.message.length > 0) {
//                                             let salary_structure = res.message[0];

//                                             let promises = [];

//                                             if (salary_structure.custom_is_uniform_allowance == 1) {
//                                                 let value = salary_structure.custom_uniform_allowance_value;
//                                                 if (value) {
//                                                     promises.push(frappe.call({
//                                                         method: "frappe.client.get_list",
//                                                         args: {
//                                                             doctype: "Employee Tax Exemption Sub Category",
//                                                             filters: { "custom_salary_component": "Uniform" },
//                                                             fields: ["*"]
//                                                         },
//                                                         callback: function(response) {
//                                                             if (response.message && response.message.length > 0) {
//                                                                 component_array.push({
//                                                                     "sub_category": response.message[0].name,
//                                                                     "category": response.message[0].exemption_category,
//                                                                     "max_amount": value,
//                                                                     "amount": value
//                                                                 });
//                                                             }
//                                                         }
//                                                     }));
//                                                 }
//                                             }

//                                             if (salary_structure.custom_is_epf == 1) {
//                                                 let epf_amount = Math.round((salary_structure.base * 0.35) / 12 * 0.12);
//                                                 let epf_amount_annual=epf_amount*12
//                                                 if (epf_amount) {
//                                                     promises.push(frappe.call({
//                                                         method: "frappe.client.get_list",
//                                                         args: {
//                                                             doctype: "Employee Tax Exemption Sub Category",
//                                                             filters: { "custom_salary_component": "Employee Provident Fund" },
//                                                             fields: ["*"]
//                                                         },
//                                                         callback: function(kes) {
//                                                             if (kes.message && kes.message.length > 0) {
//                                                                 if (epf_amount_annual>150000)
//                                                                 {
//                                                                     component_array.push({
//                                                                         "sub_category": kes.message[0].name,
//                                                                         "category": kes.message[0].exemption_category,
//                                                                         "max_amount": kes.message[0].max_amount,
//                                                                         "amount": 150000
//                                                                     });
//                                                                 }
//                                                                 else{

//                                                                     component_array.push({
//                                                                         "sub_category": kes.message[0].name,
//                                                                         "category": kes.message[0].exemption_category,
//                                                                         "max_amount": kes.message[0].max_amount,
//                                                                         "amount": epf_amount_annual
//                                                                     });

//                                                                 }
//                                                             }
//                                                         }
//                                                     }));
//                                                 }
//                                             }

//                                             if (salary_structure.custom_is_nps == 1) {
//                                                 let nps_amount = Math.round((((salary_structure.base * 0.35) / 12 * salary_structure.custom_nps_percentage) / 100));
//                                                 let nps_amount_annual=nps_amount*12
//                                                 if (nps_amount) {
//                                                     promises.push(frappe.call({
//                                                         method: "frappe.client.get_list",
//                                                         args: {
//                                                             doctype: "Employee Tax Exemption Sub Category",
//                                                             filters: { "custom_salary_component": "NPS" },
//                                                             fields: ["*"]
//                                                         },
//                                                         callback: function(mes) {
//                                                             if (mes.message && mes.message.length > 0) {
//                                                                 component_array.push({
//                                                                     "sub_category": mes.message[0].name,
//                                                                     "category": mes.message[0].exemption_category,
//                                                                     "max_amount": nps_amount_annual,
//                                                                     "amount": nps_amount_annual
//                                                                 });
//                                                             }
//                                                         }
//                                                     }));
//                                                 }
//                                             }

//                                             if (salary_structure.custom_state) {
//                                                 promises.push(frappe.call({
//                                                     method: "frappe.client.get_list",
//                                                     args: {
//                                                         doctype: "Employee Tax Exemption Sub Category",
//                                                         filters: { "custom_salary_component": "Professional Tax (Gujarat)" },
//                                                         fields: ["*"]
//                                                     },
//                                                     callback: function(jes) {
//                                                         if (jes.message && jes.message.length > 0) {
//                                                             component_array.push({
//                                                                 "sub_category": jes.message[0].name,
//                                                                 "category": jes.message[0].exemption_category,
//                                                                 "max_amount": jes.message[0].max_amount,
//                                                                 "amount": jes.message[0].max_amount
//                                                             });
//                                                         }
//                                                     }
//                                                 }));
//                                             }

//                                             // Add dialog box values to component_array
//                                             $.each(values.details_table, function(i, w) {
//                                                 component_array.push({
//                                                     "sub_category": w.exemption_sub_category,
//                                                     "category": w.employee_exemption_category,
//                                                     "max_amount": w.maximum_amount,
//                                                     "amount": w.declared_amount
//                                                 });
//                                             });

//                                             // Wait for all async calls to finish
//                                             Promise.all(promises).then(() => {
//                                                 // Now update the child table
//                                                 frm.clear_table('declarations');
//                                                 frm.refresh_field('declarations');

//                                                 component_array.forEach(row => {
//                                                     let new_row = frm.add_child('declarations');
//                                                     new_row.exemption_sub_category = row.sub_category;
//                                                     new_row.exemption_category = row.category;
//                                                     new_row.max_amount = row.max_amount;
//                                                     new_row.amount = row.amount;
//                                                 });

//                                                 frm.refresh_field('declarations');
//                                                 frm.set_value("monthly_house_rent",values.hra_amount)
//                                                 frm.set_value("rented_in_metro_city",values.rented_in_metro_city)
//                                                 frm.save('Update');
//                                                 d.hide();
//                                             });
//                                         }
//                                     }
//                                 });
//                             }
//                         }
//                     });

//                     d.show();

//                     // Update employee_exemption_category when exemption_sub_category changes
//                     d.$wrapper.on('change', '[data-fieldname="exemption_sub_category"] select', function() {
//                         let selectedValue = $(this).val();
//                         let rowIndex = $(this).closest('.grid-row').index();

//                         if (selectedValue) {
//                             frappe.call({
//                                 method: 'frappe.client.get',
//                                 args: {
//                                     doctype: "Employee Tax Exemption Sub Category",
//                                     name: selectedValue
//                                 },
//                                 callback: function(r) {
//                                     if (r.message) {
//                                         let category = r.message.exemption_category;
//                                         let category_max_amount = r.message.max_amount;
//                                         d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.employee_exemption_category = category;
//                                         d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.maximum_amount = category_max_amount;
//                                         d.fields_dict.details_table.grid.refresh();
//                                     }
//                                 }
//                             });
//                         }
//                     });

//                     d.$wrapper.on('change', '[data-fieldname="declared_amount"] input', function() {
//                         let rowIndex = $(this).closest('.grid-row').index();
//                         let selectedAmount = parseFloat($(this).val());
//                         let maxAmount = parseFloat(d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.maximum_amount);
//                         let component = d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.employee_exemption_category;

//                         if (component == "Section 80C") {
//                             $.each(frm.doc.declarations, function(i, v) {
//                                 if (v.exemption_category == component) {
//                                     if (v.amount == 150000) {
//                                         frappe.msgprint("You can't enter the amount here because your Section 80C is at the maximum.");
//                                         d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.declared_amount = undefined;
//                                         d.fields_dict.details_table.grid.refresh();
//                                     } else {
//                                         let remainingAmount = maxAmount - parseFloat(v.amount);

//                                         if (selectedAmount > remainingAmount) {
//                                             frappe.msgprint(`You can't enter an amount greater than ${remainingAmount}.`);
//                                             d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.declared_amount = undefined;
//                                             d.fields_dict.details_table.grid.refresh();
//                                         }
//                                     }
//                                 }
//                             });
//                         } else {
//                             if (selectedAmount > maxAmount) {
//                                 frappe.msgprint(`You can't enter an amount greater than ${maxAmount}.`);
//                                 d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.declared_amount = undefined;
//                                 d.fields_dict.details_table.grid.refresh();
//                             }
//                         }
//                     });
//                 } else {
//                     frappe.msgprint("You can't Edit the declaration because you are in the New regime.");
//                 }
//             }
//         });
//     }
// }

