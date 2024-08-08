frappe.ui.form.on('Employee Tax Exemption Declaration', {

    refresh:function(frm)
    {
        // let set_array = ['Option 1', 'Option 2', 'Option 3','Option 3'];

        // let d = new frappe.ui.Dialog({
        //     title: 'Custom Dialog with Child Table',
        //     fields: [
        //         {
        //             fieldname: 'main_field',
        //             label: 'Main Field',
        //             fieldtype: 'Data',
        //             reqd: 1
        //         },
        //         {
        //             fieldname: 'child_table',
        //             label: 'Child Table',
        //             fieldtype: 'Table',
        //             cannot_add_rows: false,
        //             in_place_edit: true,
        //             data: [],
        //             fields: [
        //                 {
        //                     fieldtype: 'Select',
        //                     fieldname: 'child_field3',
        //                     label: 'Child Field 3',
        //                     options: set_array,
        //                     in_list_view: 1
        //                 },
        //                 {
        //                     fieldtype: 'Link',
        //                     fieldname: 'item',
        //                     label: 'Item',
        //                     options: "Item",
        //                     in_list_view: 1
        //                 },
        //                 {
        //                     fieldtype: 'Link',
        //                     fieldname: 'item_group',
        //                     label: 'Item Group',
        //                     in_list_view: 1,
        //                     options: 'Item Group',
        //                 },
        //             ]
        //         }
        //     ],
        //     primary_action_label: 'Submit',
        //     primary_action: function () {
        //         let values = d.get_values();
        //         if (!values) return;
        
        //         // Handle the values from the dialog
        //         console.log(values);
        
        //         // Optionally, you can process the child table data here
        //         let child_table_data = values.child_table;
        //         console.log('Child Table Data:', child_table_data);
        
        //         // Close the dialog
        //         d.hide();
        //     }
        // });
        
        // // Show the dialog
        // d.show();
        
        // // Attach event listeners after the dialog is shown
        // d.$wrapper.on('change', '[data-fieldname="child_field3"] select', function () {
        //     let selectedValue = $(this).val();
        //     console.log('Selected value in Child Field 3:', selectedValue);
        // });
        
        // d.$wrapper.on('change', '[data-fieldname="item"] input', function () {
        //     let selectedItem = $(this).val();
        //     console.log('Selected value in Item:', selectedItem);
        // });
        
        // d.$wrapper.on('change', '[data-fieldname="item_group"] input', function () {
        //     let selectedItem = $(this).val();
        //     console.log('Selected value in Item Group:', selectedItem);
        // });
        

















        if(frm.doc.custom_income_tax=="New Regime")
            {
                frm.set_df_property('declarations',  'read_only',  1);
            }


            // if(!frm.is_new()&& frm.doc.declarations.length>0)
            //     {
            //         $.each(frm.doc.declarations,function(i,v)
            //     {
            //         // console.log(v.exemption_category)
            //         if(v.exemption_category=="Section 80C")
            //             {
            //                 console.log(v.exemption_sub_category)
            //                 // frm.fields_dict['declarations'].grid.toggle_enable('amount', false, row.idx - 1);
            //                 cur_frm.fields_dict.declarations.grid.fields_map.amount.read_only = true;


            //             }
            //     })

                    

            //     }

            if(frm.doc.docstatus==1)
            {
                frm.add_custom_button("Edit Declaration",function()
                {
                    // edit(frm)
                    edit_declaration(frm)
                    
                })
            }



            
    },

    
   
});


frappe.ui.form.on('Employee Tax Exemption Declaration Category', {
    refresh(frm) {
        // your code here
    },
    
    amount:function(frm,cdt,cdn)
    {
        var d=locals[cdt][cdn]
        // console.log(d,"000")
        
        
        if(d.amount>d.max_amount)
        {
            frappe.model.set_value(cdt, cdn, "amount", 0);
            msgprint("You Cant Enter Amount Greater than "+d.max_amount)
        }
    },

    

    exemption_sub_category: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];

        console.log(d.exemption_sub_category);

        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Employee Tax Exemption Sub Category",
                filters: { name: d.exemption_sub_category },
                fields: ["*"] 
            },
            callback: function(res) {
                if (res.message) {

                    
                    if(res.message.custom_is_nps==1)
                    {

                        frappe.call({
                            "method": "frappe.client.get_list",
                            args: {
                                doctype: "Salary Structure Assignment",
                                filters: { employee: frm.doc.employee ,docstatus:1},
                                fields: ["*"],
                                order_by: "from_date desc",
                                limit: 1
                            },
                            callback: function(kes) {
                                if (kes.message && kes.message.length > 0) {


                                    if(kes.message[0].custom_is_nps==1)
                                    {
                                        
                                        let nps_amount = Math.round((kes.message[0].base/12 * 0.35));
                                        let nps_percentage=Math.round(nps_amount*kes.message[0].custom_nps_percentage/100);
                                        let nps_amount_year = Math.round(nps_percentage * 12);
                                        frappe.model.set_value(cdt, cdn, "max_amount", nps_amount_year);
                                        frappe.model.set_value(cdt, cdn, "amount", nps_amount_year);



                                    }
                                    else{
                                        frappe.model.set_value(cdt, cdn, "max_amount", 0);
                                    }



                                }
                            }
                        })



                    }


                    if(res.message.custom_is_epf==1)
                        {
    
                            frappe.call({
                                "method": "frappe.client.get_list",
                                args: {
                                    doctype: "Salary Structure Assignment",
                                    filters: { employee: frm.doc.employee ,docstatus:1},
                                    fields: ["*"],
                                    order_by: "from_date desc",
                                    limit: 1
                                },
                                callback: function(kes) {
                                    if (kes.message && kes.message.length > 0) {
    
                                        
    
                                        if(kes.message[0].custom_is_epf==1)
                                        {
                                            
                                            let epf_amount = Math.round((kes.message?.at(0).base/12)*0.35);
                                            
                                            let epf_percentage=Math.round(epf_amount*12/100);
                                            
                                           
                                            let epf_amount_year = Math.round(epf_percentage * 12);

                                            if(epf_amount_year>res.message.max_amount)
                                            {
                                                frappe.model.set_value(cdt, cdn, "max_amount", res.message.max_amount);
                                                frappe.model.set_value(cdt, cdn, "amount", res.message.max_amount);

                                                
                                            }

                                            else
                                            {
                                                frappe.model.set_value(cdt, cdn, "max_amount", epf_amount_year);
                                                frappe.model.set_value(cdt, cdn, "amount", epf_amount_year);
                                            }


                                            
    
    
    
                                        }
                                        else{
                                            frappe.model.set_value(cdt, cdn, "max_amount", 0);
                                        }
    
    
    
                                    }
                                }
                            })
    
    
    
                        }


                        frappe.model.set_value(cdt, cdn, "max_amount", res.message.max_amount);



                    
                } 
                
            },
           
        });
    }
})


// function edit(frm) {
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
//                         editable: true,
                       
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

//             var total_amount=0
//             values.details_table.forEach(row => {
//                 total_amount=total_amount+row.declared_amount
//                 let new_row = frm.add_child('declarations');
//                 new_row.exemption_sub_category = row.exemption_sub_category;
//                 new_row.exemption_category = row.employee_exemption_category;
//                 new_row.max_amount = row.maximum_amount;
//                 new_row.amount = row.declared_amount;
//             });

//             frm.refresh_field('declarations');

//             frm.set_value("total_declared_amount",total_amount)
//             frm.set_value("total_exemption_amount",total_amount)

//             // d.hide();
//             frm.save('Update');

//             console.log(values,"=========")

//             values.details_table.forEach(row => {
                
//                 let new_row = frm.add_child('decladeclaration_detailsrations');
//                 exemption_sub_category = row.exemption_sub_category;
//                 exemption_category = row.employee_exemption_category;
//                 max_amount = row.maximum_amount;
//                 amount = row.declared_amount;
//             });


//             frappe.db.insert({
//                 "doctype": "Tax Declaration History",
//                 "employee": frm.doc.first_name,
//                 "employee_name": frm.doc,last_name,
//                 "income_tax":
//                 "company":
//                 "posting_date":
//                 "payroll_period":
//                 "tax_exemption":
//                 "declaration_details":
//                 [
//                     "exemption_sub_category":exemption_sub_category,
//                     "exemption_category":exemption_category,
//                     "maximum_exempted_amount":max_amount,
//                     "declared_amount":amount,
//                 ]


//              });

//         }
//     });

//     d.show();
// }




function edit(frm) 
{
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
                        fieldtype: 'Link',
                        options: 'Employee Tax Exemption Sub Category',
                        in_list_view: 1,
                        editable: true,
                        onchange: function() {
                            console.log(d.get_field('details_table').get_value());
                        }
                    },
                    {
                        label: 'Employee Tax Exemption Category',
                        fieldname: 'employee_exemption_category',
                        fieldtype: 'Link',
                        options: 'Employee Tax Exemption Category',
                        in_list_view: 1,
                        editable: true
                    },
                    {
                        label: 'Maximum Exempted Amount',
                        fieldname: 'maximum_amount',
                        fieldtype: 'Currency',
                        in_list_view: 1
                    },
                    {
                        label: 'Declared Amount',
                        fieldname: 'declared_amount',
                        fieldtype: 'Currency',
                        in_list_view: 1,
                        editable: true
                    }
                ]
            }
        ],
        size: 'large',
        primary_action_label: 'Submit',
        primary_action(values) {
            frm.clear_table('declarations');

            var total_amount = 0;
            values.details_table.forEach(row => {
                total_amount += row.declared_amount;
                let new_row = frm.add_child('declarations');
                new_row.exemption_sub_category = row.exemption_sub_category;
                new_row.exemption_category = row.employee_exemption_category;
                new_row.max_amount = row.maximum_amount;
                new_row.amount = row.declared_amount;
            });

            frm.refresh_field('declarations');

            frm.set_value("total_declared_amount", total_amount);
            frm.set_value("total_exemption_amount", total_amount);

            frm.save('Update');

           

            frappe.db.insert({
                "doctype": "Tax Declaration History",
                "employee": frm.doc.employee,
                "employee_name": frm.doc.employee_name,
                "company": frm.doc.company,
                "tax_exemption":frm.doc.name,
                "income_tax":frm.doc.custom_income_tax,
                "posting_date": frappe.datetime.nowdate(),
                "payroll_period": frm.doc.payroll_period,
                "monthly_house_rent": frm.doc.monthly_house_rent,
                "rented_in_metro_city": frm.doc.rented_in_metro_city,
                "hra_as_per_salary_structure": frm.doc.hra_as_per_salary_structure,
                "total_declared_amount": frm.doc.total_declared_amount,
                "annual_hra_exemption": frm.doc.annual_hra_exemption,
                "monthly_hra_exemption": frm.doc.monthly_hra_exemption,
                "total_exemption_amount": frm.doc.total_exemption_amount,
                "declaration_details": values.details_table.map(row => ({
                    "exemption_sub_category": row.exemption_sub_category,
                    "exemption_category": row.employee_exemption_category,
                    "maximum_exempted_amount": row.maximum_amount,
                    "declared_amount": row.declared_amount
                }))
            })
            
            
            
            

            d.hide();
        }
    });

    d.show();
}


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





function edit_declaration(frm) {
    if (frm.doc.employee) {
        var sub_category = [];

        // Fetch all active Employee Tax Exemption Sub Categories
        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Employee Tax Exemption Sub Category",
                filters: { "is_active": 1 },
                fields: ["*"],
                limit_page_length: 999999999999
            },
            callback: function(subcategory_response) {
                if (subcategory_response.message && subcategory_response.message.length > 0) {
                    subcategory_response.message.forEach(function(v) {
                        sub_category.push(v.name);
                    });
                }
            }
        });

        // Fetch the latest Salary Structure Assignment
        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Salary Structure Assignment",
                filters: { "employee": frm.doc.employee, "docstatus": 1 },
                fields: ["*"],
                limit: 1,
                order_by: "from_date desc"
            },
            callback: function(res) {
                if (res.message && res.message.length > 0) {
                    let component_array = [];
                    let salary_structure = res.message[0];

                    if (salary_structure.income_tax_slab === "Old Regime") {
                        if (salary_structure.custom_is_uniform_allowance == 1) {
                            let value = salary_structure.custom_uniform_allowance_value;
                            if (value) {
                                frappe.call({
                                    method: "frappe.client.get_list",
                                    args: {
                                        doctype: "Employee Tax Exemption Sub Category",
                                        filters: { "custom_is_uniform": 1 },
                                        fields: ["*"]
                                    },
                                    callback: function(response) {
                                        if (response.message && response.message.length > 0) {
                                            component_array.push({
                                                "sub_category": response.message[0].name,
                                                "category": response.message[0].exemption_category,
                                                "max_amount": value,
                                                "amount": value
                                            });
                                        }
                                    }
                                });
                            }
                        }

                        if (salary_structure.custom_is_epf == 1) {
                            let epf_amount = Math.round((salary_structure.base * 0.35) / 12 * 0.12);
                            if (epf_amount) {
                                frappe.call({
                                    method: "frappe.client.get_list",
                                    args: {
                                        doctype: "Employee Tax Exemption Sub Category",
                                        filters: { "custom_is_epf": 1 },
                                        fields: ["*"]
                                    },
                                    callback: function(kes) {
                                        if (kes.message && kes.message.length > 0) {
                                            component_array.push({
                                                "sub_category": kes.message[0].name,
                                                "category": kes.message[0].exemption_category,
                                                "max_amount": epf_amount,
                                                "amount": epf_amount
                                            });
                                        }
                                    }
                                });
                            }
                        }

                        if (salary_structure.custom_is_nps == 1) {
                            let nps_amount = Math.round(((salary_structure.base * 0.35) / 12 * salary_structure.custom_nps_percentage) / 100);
                            if (nps_amount) {
                                frappe.call({
                                    method: "frappe.client.get_list",
                                    args: {
                                        doctype: "Employee Tax Exemption Sub Category",
                                        filters: { "custom_is_nps": 1 },
                                        fields: ["*"]
                                    },
                                    callback: function(mes) {
                                        if (mes.message && mes.message.length > 0) {
                                            component_array.push({
                                                "sub_category": mes.message[0].name,
                                                "category": mes.message[0].exemption_category,
                                                "max_amount": nps_amount,
                                                "amount": nps_amount
                                            });
                                        }
                                    }
                                });
                            }
                        }

                        if (salary_structure.custom_state) {
                            frappe.call({
                                method: "frappe.client.get_list",
                                args: {
                                    doctype: "Employee Tax Exemption Sub Category",
                                    filters: { "custom_is_pt": 1 },
                                    fields: ["*"]
                                },
                                callback: function(jes) {
                                    if (jes.message && jes.message.length > 0) {
                                        component_array.push({
                                            "sub_category": jes.message[0].name,
                                            "category": jes.message[0].exemption_category,
                                            "max_amount": jes.message[0].max_amount,
                                            "amount": jes.message[0].max_amount
                                        });
                                    }
                                }
                            });
                        }

                        // Delay to ensure all async calls are completed
                        setTimeout(function() {
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
                                                editable: true,
                                                read_only: 1
                                            },
                                            {
                                                label: 'Maximum Exempted Amount',
                                                fieldname: 'maximum_amount',
                                                fieldtype: 'Currency',
                                                in_list_view: 1,
                                                read_only: 1
                                            },
                                            {
                                                label: 'Declared Amount',
                                                fieldname: 'declared_amount',
                                                fieldtype: 'Currency',
                                                in_list_view: 1,
                                                editable: true
                                            }
                                        ]
                                    }
                                ],
                                size: 'large',
                                primary_action_label: 'Submit',
                                primary_action(values) {
                                    frm.clear_table('declarations');

                                    var total_amount = 0;
                                    values.details_table.forEach(row => {
                                        total_amount += row.declared_amount;
                                        let new_row = frm.add_child('declarations');
                                        new_row.exemption_sub_category = row.exemption_sub_category;
                                        new_row.exemption_category = row.employee_exemption_category;
                                        new_row.max_amount = row.maximum_amount;
                                        new_row.amount = row.declared_amount;
                                    });

                                    frm.refresh_field('declarations');

                                    frm.set_value("total_declared_amount", total_amount);
                                    frm.set_value("total_exemption_amount", total_amount);

                                    frm.save('Update');


                                frappe.db.insert({
                                        doctype: "Tax Declaration History",
                                        employee: frm.doc.employee,
                                        employee_name: frm.doc.employee_name,
                                        company: frm.doc.company,
                                        tax_exemption: frm.doc.name,
                                        income_tax: frm.doc.custom_income_tax,
                                        posting_date: frappe.datetime.nowdate(),
                                        payroll_period: frm.doc.payroll_period,
                                        monthly_house_rent: frm.doc.monthly_house_rent,
                                        rented_in_metro_city: frm.doc.rented_in_metro_city,
                                        hra_as_per_salary_structure: frm.doc.salary_structure_hra,
                                        total_declared_amount: frm.doc.total_declared_amount,
                                        annual_hra_exemption: frm.doc.annual_hra_exemption,
                                        monthly_hra_exemption: frm.doc.monthly_hra_exemption,
                                        total_exemption_amount: frm.doc.total_exemption_amount,
                                        declaration_details: values.details_table.map(row => ({
                                            exemption_sub_category: row.exemption_sub_category,
                                            exemption_category: row.employee_exemption_category,
                                            maximum_exempted_amount: row.maximum_amount,
                                            declared_amount: row.declared_amount
                                        })),
                                        hra_breakup: frm.doc.custom_hra_breakup.map(row => ({
                                            month: row.month,
                                            rent_paid: row.rent_paid,
                                            earned_basic: row.earned_basic,
                                            hra_received: row.hra_received,
                                            excess_of_rent_paid: row.excess_of_rent_paid,
                                            exemption_amount: row.exemption_amount
                                        }))
                                    });
                                    
                                    


                                    d.hide();
                                }
                            });

                            d.fields_dict.details_table.df.data = [];
                            component_array.forEach(item => {
                                d.fields_dict.details_table.df.data.push({
                                    exemption_sub_category: item.sub_category,
                                    employee_exemption_category: item.category,
                                    maximum_amount: item.max_amount,
                                    declared_amount: item.amount
                                });
                            });
                            d.fields_dict.details_table.grid.refresh();

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
                                                let category_max_amount=r.message.max_amount;
                                                d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.employee_exemption_category = category;
                                                d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.maximum_amount = category_max_amount;
                                                d.fields_dict.details_table.grid.refresh();
                                            }
                                        }
                                    });
                                }
                            });

                            d.$wrapper.on('change', '[data-fieldname="declared_amount"] input', function () {
                                let selectedAmount = $(this).val();
                                console.log('Selected value in Amount:', selectedAmount);
                                
                            });

                        }, 1000);
                    }
                }
            }
        });
    }
}

