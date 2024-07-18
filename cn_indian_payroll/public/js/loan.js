frappe.ui.form.on('Loan', {
	onload(frm) {

        if(frm.is_new())
        {





            if(frm.doc.applicant_type=="Employee" && frm.doc.loan_product)
                {
                    frappe.call({
                        "method": "frappe.client.get_list",
                        args: {
                            doctype: "Loan Product",
                            filters: { "name":frm.doc.loan_product},
                            fields: ["*"],
                            
                        },
                        callback: function(res) {
                            if (res.message && res.message.length > 0) {
                                console.log(res.message)
                                if(frm.doc.loan_amount>res.message[0].custom_loan_perquisite_threshold_amount)
                                    {
                                        
                                                frm.set_value("custom_loan_perquisite_rate_of_interest",res.message[0].custom_loan_perquisite_rate_of_interest)
                
                                            

                                    }
        
                                
                                    
        
        
                            }
                        }
                    })

                }

                else
                                    {
                                        frm.set_value("custom_loan_perquisite_rate_of_interest",0)
        
        
                                    }

        }
		
	},

    loan_product:function(frm)
    {
        if (frm.doc.loan_product && frm.doc.loan_amount)
        {

            frappe.call({
                "method": "frappe.client.get_list",
                args: {
                    doctype: "Loan Product",
                    filters: { "name":frm.doc.loan_product},
                    fields: ["*"],
                    
                },
                callback: function(res) {
                    if (res.message && res.message.length > 0) {
                        

                        if(frm.doc.loan_amount>res.message[0].custom_loan_perquisite_threshold_amount)
                            {



                                if(frm.doc.applicant_type=="Employee")
                                    {
                                        frm.set_value("custom_loan_perquisite_rate_of_interest",res.message[0].custom_loan_perquisite_rate_of_interest)

                                    }
                                    else
                                    {
                                        frm.set_value("custom_loan_perquisite_rate_of_interest",0)


                                    }

                                }


                    }
                }
            })


        }
    },

    loan_amount:function(frm)
    {
        if (frm.doc.loan_product && frm.doc.loan_amount)
            {
    
                frappe.call({
                    "method": "frappe.client.get_list",
                    args: {
                        doctype: "Loan Product",
                        filters: { "name":frm.doc.loan_product},
                        fields: ["*"],
                        
                    },
                    callback: function(res) {
                        if (res.message && res.message.length > 0) {
                            
    
                            if(frm.doc.loan_amount>res.message[0].custom_loan_perquisite_threshold_amount)
                                {
    
    
    
                                    if(frm.doc.applicant_type=="Employee")
                                        {
                                            frm.set_value("custom_loan_perquisite_rate_of_interest",res.message[0].custom_loan_perquisite_rate_of_interest)
    
                                        }
                                        else
                                        {
                                            frm.set_value("custom_loan_perquisite_rate_of_interest",0)
    
    
                                        }
    
                                }

                                    else
                                        {
                                            frm.set_value("custom_loan_perquisite_rate_of_interest",0)
    
    
                                        }
    
    
                        }
                    }
                })
    
    
            }

    }
})