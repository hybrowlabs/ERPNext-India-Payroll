frappe.ui.form.on('Employee Tax Exemption Proof Submission', {
    refresh(frm) {
        console.log("Hello");

        if (frm.doc.custom_exemption_declaration && frm.is_new()) {
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Employee Tax Exemption Declaration",
                    name: frm.doc.custom_exemption_declaration
                },
                callback: function (r) {
                    if (r.message) {
                        frm.set_value("house_rent_payment_amount", r.message.monthly_house_rent || 0);
                        frm.set_value("rented_in_metro_city", r.message.rented_in_metro_city);
                        frm.set_value("rented_from_date", r.message.custom_from_date);
                        frm.set_value("rented_to_date", r.message.custom_to_date);

                        frm.set_value("custom_income_tax_slab", r.message.custom_income_tax);
                        frm.set_value("custom_tax_regime", r.message.custom_tax_regime);
                        frm.set_value("custom_hra_received_annual", r.message.salary_structure_hra);
                        frm.set_value("custom_hra_received_monthly", r.message.custom_hra_received_monthly);
                        frm.set_value("custom_basic_received_annual", r.message.custom_basic);
                        frm.set_value("custom_basic_received_monthly", r.message.custom_basic_received_monthly);
                        frm.set_value("custom_basic_as_per_salary_structure_10", r.message.custom_basic_as_per_salary_structure);
                        frm.set_value("custom_address_line1", r.message.custom_address_line1);
                        frm.set_value("custom_address_line2", r.message.custom_address_line2);
                        frm.set_value("custom_pan", r.message.custom_pan);

                        frm.set_value("custom_annual_hra_exemption", r.message.annual_hra_exemption);
                        frm.set_value("monthly_hra_exemption", r.message.monthly_hra_exemption);
                        frm.set_value("custom_hra_received", r.message.custom_hra_received_annual);
                        frm.set_value("custom_rent_paid__10_of_basic_annual", r.message.custom_rent_paid__10_of_basic_annual);
                        frm.set_value("custom_50_of_basic_metro", r.message.custom_50_of_basic_metro);



                        frm.clear_table("custom_hra_breakup");

                        if (r.message.custom_hra_breakup) {
                            r.message.custom_hra_breakup.forEach(row => {
                                let child = frm.add_child("custom_hra_breakup");
                                child.month = row.month;
                                child.rent_paid = row.rent_paid;
                                child.earned_basic = row.earned_basic;
                                child.hra_received = row.hra_received;
                                child.excess_of_rent_paid = row.excess_of_rent_paid;
                            });
                        }

                        frm.refresh_field("custom_hra_breakup");

                    }
                }
            });
        }
    }
});
