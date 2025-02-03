frappe.ui.form.on('Form 16', {
	refresh(frm) {
		
	},

    employee:function(frm)
    {
        if(frm.doc.employee)
        {


            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Salary Structure Assignment",
                    filters: {
                        employee: frm.doc.employee,
                        docstatus: 1
                    },
                    fields: ["*"],
                    limit: 1,
                    order_by: "from_date desc"
                },
                callback: function (res) {
                    if (res.message && res.message.length > 0) {
                        const payrollPeriod = res.message[0].custom_payroll_period;
    
                        if (payrollPeriod) {






            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Employee Tax Exemption Proof Submission",
                    filters: {
                        employee: frm.doc.employee,
                        
                        docstatus: ["in", [0, 1]] 
                    },
                    fields: ["*"],
                    limit_page_length: 0
                },
                callback: function (proof_response) {
                    if (proof_response.message) {
                        
            
                            if (proof_response.message[0].name) {
                                frappe.call({
                                    method: "frappe.client.get",
                                    args: {
                                        doctype: "Employee Tax Exemption Proof Submission",
                                        name: proof_response.message[0].name
                                    },
                                    callback: function (each_response_data) {
                                        if (each_response_data.message.tax_exemption_proofs) {

                                            frm.clear_table("tax_exemption_proofs");
                                            frm.refresh_field("tax_exemption_proofs");

                                            $.each(each_response_data.message.tax_exemption_proofs,function(i,v)
                                            {

                                                let child = frm.add_child('tax_exemption_proofs');
                                                child.exemption_sub_category = v.exemption_sub_category; // Replace 'benefit_accrual_date' if required
                                                child.exemption_category = v.exemption_category; 
                                                child.max_amount = v.max_amount;
                                                child.amount = v.amount; 




                                                
                                            })

                                            frm.refresh_field('tax_exemption_proofs');


                                            frm.set_value("exemption_amount",each_response_data.message.exemption_amount)
                                            frm.set_value("total_actual_amount",each_response_data.message.total_actual_amount)
                                            frm.set_value("house_rent_payment_amount",each_response_data.message.house_rent_payment_amount)
                                            frm.set_value("rented_in_metro_city",each_response_data.message.rented_in_metro_city)
                                            frm.set_value("rented_from_date",each_response_data.message.rented_from_date)
                                            frm.set_value("rented_to_date",each_response_data.message.rented_to_date)
                                            frm.set_value("monthly_house_rent",each_response_data.message.monthly_house_rent)
                                            frm.set_value("monthly_eligible_amount",each_response_data.message.monthly_eligible_amount)
                                            frm.set_value("total_eligible_hra_exemption",each_response_data.message.total_eligible_hra_exemption)
                                         

                                           


                                            
                                        }
                                        
                                    }
                                });
                            } 
                            
                            
                        }
                    }

                        });

                        }
                    }
                
                }
            })





        }

        else{
            frm.clear_table("tax_exemption_proofs");
            frm.refresh_field("tax_exemption_proofs");

        }
    }
})