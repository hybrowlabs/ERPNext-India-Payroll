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
                fields: ["*"] // Specify fields explicitly
            },
            callback: function(res) {
                if (res.message) {
                    frappe.model.set_value(cdt, cdn, "max_amount", res.message.max_amount);
                } else {
                    console.error('No data returned for the selected exemption sub-category.');
                }
            },
           
        });
    }
})