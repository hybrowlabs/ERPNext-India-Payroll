frappe.ui.form.on('Salary Component', {

	is_tax_applicable:function(frm)
	{
		if (frm.doc.is_tax_applicable) {
			frm.set_value('custom_tax_exemption_applicable_based_on_regime', 1);
		}
		else
		{
			frm.set_value('custom_tax_exemption_applicable_based_on_regime', 0);
		}

	},

	type:function(frm)
	{
		if (frm.doc.type=="Earning" && frm.doc.is_tax_applicable) {
			frm.set_value('custom_tax_exemption_applicable_based_on_regime', 1);
		}
		else
		{
			frm.set_value('custom_tax_exemption_applicable_based_on_regime', 0);
		}

	},


});
