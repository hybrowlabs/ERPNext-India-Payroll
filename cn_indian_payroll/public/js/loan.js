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


            if(frm.doc.loan_application)
                {
                    frappe.call({
                        "method": "frappe.client.get",
                        args: {
                            doctype: "Loan Application",
                            filters: { "name":frm.doc.loan_application},
                            
                            
                        },
                        callback: function(res) {
                            if (res.message) {
                                // console.log(res.message,"222")
                                frm.set_value("monthly_repayment_amount",res.message.repayment_amount)
                            }
                        }
                    })

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