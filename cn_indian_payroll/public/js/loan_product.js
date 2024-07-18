frappe.ui.form.on('Loan Product', {
	onload(frm) {
        if(frm.is_new())
            {
                frm.set_value("custom_loan_perquisite_threshold_amount",20000)
            }

    },

        })