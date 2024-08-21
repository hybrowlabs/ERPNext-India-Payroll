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
                        doctype: "Salary Component",
                        filters: { "component_type":"LTA Reimbursement"},
                        fields: ["*"],
                       
                    },
                    callback: function(kes) {

                        if(kes.message.length>0)
                        {
                            var company=kes.message[0].name
                        }

                        // console.log(company,"-------")





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

                            frm.set_value("custom_payroll_period",res.message[0].custom_payroll_period)

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
                    order_by: "from_date desc",
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
                                                    console.log(eligible_amount,"eligible_amount")

                                                    frappe.call({
                                                        method: "frappe.client.get",
                                                        args: {
                                                            doctype: "Salary Component",
                                                            filters: { "name": frm.doc.earning_component},
                                                           
                                                            
                                                        },
                                                        callback: function(earning_component) {
                                                        if(earning_component.message && earning_component.message.component_type!="Vehicle Maintenance Reimbursement")

                                                            {

                                                                // console.log(earning_component.message.name)


                                                    frappe.call({
                                                        method: "frappe.client.get_list",
                                                        args: {
                                                            doctype: "Employee Benefit Accrual",
                                                            filters: { "employee": frm.doc.employee, "salary_component": frm.doc.earning_component,"docstatus":1,"payroll_period":frm.doc.custom_payroll_period},
                                                            fields: ["*"],
                                                            limit: 99999999
                                                        },
                                                        callback: function(res) {
                                                            if (res.message) {
                                                               
                                            
                                                                var sum = 0;
                                                                $.each(res.message, function(i, v) {
                                                                    
                                                                    sum += v.amount; 
                                                                    // console.log(v.amount)
                                                                });

                                                                console.log(sum,"77777")
                                            
                                                               
                                                               frappe.call({
                                                                    method: "frappe.client.get_list",
                                                                    args: {
                                                                        doctype: "Employee Benefit Claim",
                                                                        filters: { "employee": frm.doc.employee, "earning_component": frm.doc.earning_component ,"docstatus": 1,"custom_payroll_period":frm.doc.custom_payroll_period},
                                                                        fields: ["*"],
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

                                                else if(earning_component.message && earning_component.message.component_type=="Vehicle Maintenance Reimbursement")

                                                {
                                                    frappe.call({
                                                        method: "frappe.client.get_list",
                                                        args: {
                                                            doctype: "Employee Benefit Accrual",
                                                            filters: { "employee": frm.doc.employee, "salary_component": frm.doc.earning_component,"docstatus":1,"payroll_period":frm.doc.custom_payroll_period},
                                                            fields: ["*"],
                                                            limit: 99999999
                                                        },
                                                        callback: function(accrual_data) {
                                                            if (accrual_data.message) {
                                                               
                                            
                                                                var accrual_sum = 0;
                                                                $.each(accrual_data.message, function(i, v) {
                                                                    
                                                                    accrual_sum += v.amount; 
                                                                    
                                                                });

                                                                future_month_count=12-accrual_data.message.length
                                                                // console.log(future_month_count,"future_month_count")
                                                                future_amount=future_month_count*eligible_amount
                                                                // console.log(future_amount,"future_amount")
                                                                frappe.call({
                                                                    method: "frappe.client.get_list",
                                                                    args: {
                                                                        doctype: "Employee Benefit Claim",
                                                                        filters: { "employee": frm.doc.employee, "earning_component": frm.doc.earning_component ,"docstatus": 1,"custom_payroll_period":frm.doc.custom_payroll_period},
                                                                        fields: ["*"],
                                                                        limit: 99999999,
                                                                        
                                                                    },
                                                                    callback: function(kies) {
                                                                        if (kies.message) {
                                        
                                                                            
                                                                            if(kies.message.length>0)
                                                                                {
                                                                                    var total_sum = 0;
                                                                                        $.each(kies.message, function(i, k) {
                                                                                           
                                                                                            total_sum += k.claimed_amount; // Corrected sum calculation
                                                                                        });
                                        
                                        
                                        
                                                                                        frm.set_value("custom_max_amount",(future_amount+accrual_sum)-total_sum)
                                        
                                                                                }
                                        
                                        
                                                                            else
                                                                            {
                                                                                frm.set_value("custom_max_amount",future_amount+accrual_sum)
                                                                            }
                                        
                                                                        }
                                                                    }
                                                                })

                                                            }
                                                        }
                                                    })
                                                   
                                                }
                                                }
                                            })
                                                    
                                                }
                                        })

                                }
                            }
                        })




                    }
                }
            })



            
        }

        
    },

    // claim_date: function(frm) {
    //     if (frm.doc.claim_date < frappe.datetime.now_date()) {
    //         frm.set_value("claim_date", undefined);
    //         frappe.msgprint(__('Claim date cannot be in the past.'));
    //     }
    // }
    
    
    

    
})