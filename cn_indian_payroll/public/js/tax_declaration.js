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

            
    }
   
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