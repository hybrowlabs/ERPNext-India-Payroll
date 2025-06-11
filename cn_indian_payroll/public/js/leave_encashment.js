frappe.ui.form.on('Leave Encashment', {
	refresh(frm) {


        if(frm.doc.encashment_days)
            {
                if(frm.doc.custom_basic_amount)
                {
                    frm.set_value("encashment_amount",(frm.doc.custom_basic_amount/30)*frm.doc.encashment_days)
                }
            }

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

    },


})
