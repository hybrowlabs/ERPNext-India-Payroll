frappe.ui.form.on('Salary Component', {
	refresh(frm) {
		// Apply visibility rules on form load
		frm.trigger('toggle_appraisal_visibility');
	},

	custom_is_arrear: function(frm) {
		frm.trigger('toggle_appraisal_visibility');
	},

	custom_is_reimbursement: function(frm) {
		frm.trigger('toggle_appraisal_visibility');
	},

	custom_is_accrual: function(frm) {
		frm.trigger('toggle_appraisal_visibility');
	},

	toggle_appraisal_visibility: function(frm) {
		const is_arrear = frm.doc.custom_is_arrear;
		const is_reimbursement = frm.doc.custom_is_reimbursement;
		const is_accrual = frm.doc.custom_is_accrual;

		// Hide the field if any of the flags are true
		if (is_arrear || is_reimbursement || is_accrual) {
			frm.set_df_property('custom_is_part_of_appraisal', 'hidden', 1);
		} else {
			frm.set_df_property('custom_is_part_of_appraisal', 'hidden', 0);
		}
	}
});
