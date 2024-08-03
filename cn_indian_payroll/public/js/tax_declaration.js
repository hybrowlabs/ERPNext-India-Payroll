frappe.ui.form.on('Employee Tax Exemption Declaration', {

    refresh:function(frm)
    {







        
        















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
                frm.add_custom_button("Edit",function()
                {
                    edit(frm)
                    
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


function edit(frm) {
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
                        editable: true,
                       
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

            var total_amount=0
            values.details_table.forEach(row => {
                total_amount=total_amount+row.declared_amount
                let new_row = frm.add_child('declarations');
                new_row.exemption_sub_category = row.exemption_sub_category;
                new_row.exemption_category = row.employee_exemption_category;
                new_row.max_amount = row.maximum_amount;
                new_row.amount = row.declared_amount;
            });

            frm.refresh_field('declarations');

            frm.set_value("total_declared_amount",total_amount)
            frm.set_value("total_exemption_amount",total_amount)

            d.hide();
            frm.save('Update');

        }
    });

    d.show();
}





