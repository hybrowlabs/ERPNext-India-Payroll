var eligible_amount=0


frappe.ui.form.on('Employee Benefit Claim', {
	refresh(frm) {
		
	},


    employee:function(frm)
    {
        if(frm.doc.employee)
            {
                var reimbursements_component=[]

                frappe.call({
                    "method": "frappe.client.get_list",
                    args: {
                        doctype: "Company",
                        filters: { "name":frm.doc.company},
                        fields: ["*"],
                       
                    },
                    callback: function(kes) {

                        if(kes.message.length>0)
                        {
                            var company=kes.message[0].custom_lta_component
                        }

                        console.log(company,"-------")





                frappe.call({
                    "method": "frappe.client.get_list",
                    args: {
                        doctype: "Salary Structure Assignment",
                        filters: { employee: frm.doc.employee ,docstatus:1},
                        fields: ["*"],
                        order_by: "from_date desc",
                        limit: 1
                    },
                    callback: function(res) {
                        if (res.message && res.message.length > 0) {

                            frappe.call({
                                method: "frappe.client.get",
                                args: {
                                    doctype: "Salary Structure Assignment",
                                    filters: { "employee": frm.doc.employee,"docstatus":1,"name":res.message[0].name},
                                    fields: ["*"],
                                    
                                },
                                callback: function(tes) {
                                    if (tes.message) {
                                       
                                        $.each(tes.message.custom_employee_reimbursements,function(i,v)
                                            {
                                                if(v.reimbursements!=company)
                                                {
                                                    reimbursements_component.push(v.reimbursements)

                                                }
                                                
                                               

                                            })

                                            // console.log(reimbursements_component)

                                            frm.set_query("earning_component", function() {
                                                return {
                                                    filters: { name: ["in", reimbursements_component] }
                                                };
                                            });



                                        }
                                    }
                                })


                        }
                    }
                })

            }
        })

            }

        else{

            frm.set_query("earning_component", function() {
                return {
                    filters: { name: ["in", reimbursements_component] }
                };
            });

        }

    },


    earning_component: function(frm) 
    
    {



        if (frm.doc.earning_component && frm.doc.employee) {

            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Salary Structure Assignment",
                    filters: { "employee": frm.doc.employee,"docstatus":1},
                    fields: ["*"],
                    limit: 99999999
                },
                callback: function(res) {
                    if (res.message) {

                        frappe.call({
                            method: "frappe.client.get",
                            args: {
                                doctype: "Salary Structure Assignment",
                                filters: { "employee": frm.doc.employee,"docstatus":1,"name":res.message[0].name},
                                fields: ["*"],
                                
                            },
                            callback: function(tes) {
                                if (tes.message) {
                                   
                                    $.each(tes.message.custom_employee_reimbursements,function(i,v)
                                        {
                                            
                                            if(v.reimbursements==frm.doc.earning_component)
                                                {
                                                    eligible_amount=v.monthly_total_amount
                                                    frappe.call({
                                                        method: "frappe.client.get_list",
                                                        args: {
                                                            doctype: "Employee Benefit Accrual",
                                                            filters: { "employee": frm.doc.employee, "salary_component": frm.doc.earning_component,"docstatus":1},
                                                            fields: ["name", "amount"],
                                                            limit: 99999999
                                                        },
                                                        callback: function(res) {
                                                            if (res.message) {
                                                               
                                            
                                                                var sum = 0;
                                                                $.each(res.message, function(i, v) {
                                                                    
                                                                    sum += v.amount; 
                                                                });
                                            
                                                               
                                                               frappe.call({
                                                                    method: "frappe.client.get_list",
                                                                    args: {
                                                                        doctype: "Employee Benefit Claim",
                                                                        filters: { "employee": frm.doc.employee, "earning_component": frm.doc.earning_component ,"docstatus": 1},
                                                                        fields: ["name", "claimed_amount"],
                                                                        limit: 99999999,
                                                                        
                                                                    },
                                                                    callback: function(kes) {
                                                                        if (kes.message) {
                                        
                                                                            
                                                                            if(kes.message.length>0)
                                                                                {
                                                                                    var total_sum = 0;
                                                                                        $.each(kes.message, function(i, k) {
                                                                                           
                                                                                            total_sum += k.claimed_amount; // Corrected sum calculation
                                                                                        });
                                        
                                        
                                        
                                                                                        frm.set_value("custom_max_amount",sum-total_sum+(eligible_amount))
                                        
                                                                                }
                                        
                                        
                                                                            else
                                                                            {
                                                                                frm.set_value("custom_max_amount",sum+eligible_amount)
                                                                            }
                                        
                                                                        }
                                                                    }
                                                                })
                                        
                                        
                                        
                                        
                                                            }
                                                        }
                                                    });
                                                    
                                                }
                                        })

                                }
                            }
                        })




                    }
                }
            })



            // frappe.call({
            //     method: "frappe.client.get_list",
            //     args: {
            //         doctype: "Employee Benefit Accrual",
            //         filters: { "employee": frm.doc.employee, "salary_component": frm.doc.earning_component,"docstatus":1},
            //         fields: ["name", "amount"],
            //         limit: 99999999
            //     },
            //     callback: function(res) {
            //         if (res.message) {
                       
    
            //             var sum = 0;
            //             $.each(res.message, function(i, v) {
            //                 // console.log(v.amount);
            //                 sum += v.amount; 
            //             });
    
            //             // console.log(sum);


            //             frappe.call({
            //                 method: "frappe.client.get_list",
            //                 args: {
            //                     doctype: "Employee Benefit Claim",
            //                     filters: { "employee": frm.doc.employee, "earning_component": frm.doc.earning_component ,"docstatus": 1},
            //                     fields: ["name", "claimed_amount"],
            //                     limit: 99999999,
                                
            //                 },
            //                 callback: function(kes) {
            //                     if (kes.message) {

            //                         // console.log(kes.message,"ppp")
            //                         if(kes.message.length>0)
            //                             {
            //                                 var total_sum = 0;
            //                                     $.each(kes.message, function(i, k) {
                                                   
            //                                         total_sum += k.claimed_amount; // Corrected sum calculation
            //                                     });

            //                                     // console.log(total_sum,"total_sumtotal_sum")


            //                                     frm.set_value("custom_max_amount",sum-total_sum)

            //                             }


            //                         else
            //                         {
            //                             frm.set_value("custom_max_amount",sum)
            //                         }

            //                     }
            //                 }
            //             })




            //         }
            //     }
            // });
        }
    },

    // claim_date: function(frm) {
    //     if (frm.doc.claim_date < frappe.datetime.now_date()) {
    //         frm.set_value("claim_date", undefined);
    //         frappe.msgprint(__('Claim date cannot be in the past.'));
    //     }
    // }
    
    
    

    
})