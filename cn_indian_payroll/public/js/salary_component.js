
frappe.ui.form.on('Salary Component', {
	refresh(frm) {

//----------------FILTER APPLIED IN Arrear component-------------------

        frm.fields_dict['custom_component'].get_query = function(doc) {
            return {
                filters: {
                    'custom_is_arrear': 0
                }
            };
        };

//----------------FILTER APPLIED IN Accrual Paid Out component-------------------

        frm.fields_dict['custom_paidout_component'].get_query = function(doc) {
            return {
                filters: {
                    'custom_is_arrear': 0
                }
            };
        };    
		
	},
    is_tax_applicable:function(frm)
    {
        if(frm.doc.is_tax_applicable == 1)
        {
            frm.set_value("custom_tax_exemption_applicable_based_on_regime",1);
            frm.set_value("custom_regime","All");           
        }
        else
        {
            frm.set_value("custom_tax_exemption_applicable_based_on_regime",0);
        }
        frm.refresh_field("tax_section");
    }
})



