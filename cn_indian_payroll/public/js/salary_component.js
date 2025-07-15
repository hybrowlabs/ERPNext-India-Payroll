frappe.ui.form.on('Salary Component', {

	onload: function(frm) {
		frm.set_query('custom_component', function() {
			return {
				filters: {
					custom_is_arrear: 0
				}
			};
		});
	},


	refresh(frm) {
		frm.trigger('toggle_appraisal_visibility');

	},

	custom_is_arrear: function(frm) {
		frm.trigger('toggle_appraisal_visibility');
		if (frm.doc.custom_is_arrear==1)
		{
			frm.set_value('depends_on_payment_days',0)
			frm.set_df_property('depends_on_payment_days', 'hidden', 1)
		}
		else{
			frm.set_value('depends_on_payment_days',1)
			frm.set_df_property('depends_on_payment_days', 'hidden', 0);
		}
	},

	custom_is_reimbursement: function(frm) {
		frm.trigger('toggle_appraisal_visibility');
	},

	custom_is_accrual: function(frm) {
		frm.trigger('toggle_appraisal_visibility');
	},

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

	toggle_appraisal_visibility: function(frm) {
		const is_arrear = frm.doc.custom_is_arrear;
		const is_reimbursement = frm.doc.custom_is_reimbursement;
		const is_accrual = frm.doc.custom_is_accrual;

		if (is_arrear || is_reimbursement || is_accrual) {
			frm.set_df_property('custom_is_part_of_appraisal', 'hidden', 1);
		} else {
			frm.set_df_property('custom_is_part_of_appraisal', 'hidden', 0);
		}
	}
});
