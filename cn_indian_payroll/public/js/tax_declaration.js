frappe.ui.form.on('Employee Tax Exemption Declaration', {

    refresh:function(frm)
    {
        if(frm.doc.custom_income_tax=="New Regime")
            {
                frm.set_df_property('declarations',  'read_only',  1);
            }
    }
   
});


frappe.ui.form.on('Employee Tax Exemption Declaration Category', {
    refresh(frm) {
        // your code here
    },
    
    amount:function(frm,cdt,cdn)
    {
        var d=locals[cdt][cdn]
        console.log(d,"000")
        
        
        if(d.amount>d.max_amount)
        {
            frappe.model.set_value(cdt, cdn, "amount", 0);
            msgprint("You Cant Enter Amount Greater than "+d.max_amount)
        }
    }
})