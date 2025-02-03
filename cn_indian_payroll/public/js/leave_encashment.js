frappe.ui.form.on('Leave Encashment', {
	refresh(frm) {
		// your code here
	},
    
    encashment_days:function(frm)
    {

        if(frm.doc.encashment_days)
        {
            if(frm.doc.custom_basic_amount)
            {
                frm.set_value("encashment_amount",(frm.doc.custom_basic_amount/30)*frm.doc.encashment_days)
            }
        }

    }
})



