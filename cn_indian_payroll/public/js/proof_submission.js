frappe.ui.form.on('Employee Tax Exemption Proof Submission', {
    onload(frm) {

        if(frm.doc.custom_declaration_id) {
            console.log("Fetching declaration data for ID:", frm.doc.custom_declaration_id);
            frappe.db.get_value(
                'Employee Tax Exemption Declaration',
                frm.doc.custom_declaration_id,
                '*',
                (r) => {
                    if(r ) {


                        console.log("Declaration Data:", r);
                        const data = r;
                        frm.set_value("house_rent_payment_amount", data.monthly_house_rent);
                        frm.set_value("custom_annual_hra_exemption", data.annual_hra_exemption);
                        frm.set_value("rented_in_metro_city", data.rented_in_metro_city);
                        frm.set_value("total_eligible_hra_exemption", data.total_eligible_hra_exemption);
                        frm.set_value("monthly_hra_exemption", data.monthly_hra_exemption);
                    }
                }
            );
        }
    },

});
