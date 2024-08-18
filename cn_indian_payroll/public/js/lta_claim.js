

frappe.ui.form.on('LTA Claim', {
    refresh(frm) {
        
                    // frm.set_query('employee', function() {
                    //     return {
                    //         filters: {
                    //             "custom_lta_applicable":1
                    //         }
                    //     };
                    // });


                
         
    },

    employee: function(frm) {
        if (frm.doc.employee) {

            find_tax_regime(frm)

            show_max_lta_amount(frm)


            // show_max_lta_amount(frm)
    
            // function futureAndProcessData() {
            //     return new Promise((resolve, reject) => {
            //         var component = [];
            //         var reimbursement_amount = [];
                    
            //         frappe.call({
            //             method: "frappe.client.get_list",
            //             args: {
            //                 doctype: "Company",
            //                 filters: { "name": frm.doc.company },
            //                 fields: ["*"]
            //             },
            //             callback: function(companyData) {
            //                 if (companyData.message && companyData.message.length > 0) {
            //                     const customLTAComponent = companyData.message[0].custom_lta_component;
                
            //                     if (customLTAComponent) {
            //                         component.push(customLTAComponent);
                
            //                         frappe.call({
            //                             method: "frappe.client.get_list",
            //                             args: {
            //                                 doctype: "Fiscal Year",
            //                                 fields: ["*"],
            //                                 order_by: "year_start_date desc",
            //                                 limit: 1
            //                             },
            //                             callback: function(kes) {
            //                                 if (kes.message && kes.message.length > 0) {
            //                                     const t1 = new Date(kes.message[0].year_end_date);
            //                                     const t2 = new Date(frm.doc.claim_date);
                
            //                                     const years = t1.getFullYear() - t2.getFullYear();
            //                                     const months = t1.getMonth() - t2.getMonth();
            //                                     const days = t1.getDate() - t2.getDate();
                
            //                                     let monthDifference = ((years * 12) + months)+1;

            //                                     // console.log(monthDifference,"-----------")
                
            //                                     if (days < 0) {
            //                                         monthDifference -= 1;
            //                                         console.log(monthDifference,"++++++++++")
            //                                     }
    
            //                                     frappe.call({
            //                                         method: "frappe.client.get_list",
            //                                         args: {
            //                                             doctype: "Salary Structure Assignment",
            //                                             filters: { employee: frm.doc.employee, docstatus: 1 },
            //                                             fields: ["*"],
            //                                             order_by: "from_date desc",
            //                                             limit: 1
            //                                         },
            //                                         callback: function(res) {
            //                                             if (res.message && res.message.length > 0) {
            //                                                 frappe.call({
            //                                                     method: "frappe.client.get",
            //                                                     args: {
            //                                                         doctype: "Salary Structure Assignment",
            //                                                         filters: { name: res.message[0].name },
            //                                                         fields: ["*"]
            //                                                     },
            //                                                     callback: function(employee_data) {
            //                                                         if (employee_data.message) {
            //                                                             $.each(employee_data.message.custom_employee_reimbursements, function(i, v) {
            //                                                                 if (v.reimbursements === customLTAComponent) {
            //                                                                     reimbursement_amount.push(v.monthly_total_amount * monthDifference);
            //                                                                 }
            //                                                             });
    
            //                                                             const futureTotal = reimbursement_amount.reduce((acc, curr) => acc + curr, 0);
            //                                                             resolve(futureTotal);
            //                                                         } else {
            //                                                             resolve(0);
            //                                                         }
            //                                                     }
            //                                                 });
            //                                             } else {
            //                                                 resolve(0);
            //                                             }
            //                                         }
            //                                     });
            //                                 } else {
            //                                     resolve(0);
            //                                 }
            //                             }
            //                         });
            //                     } else {
            //                         resolve(0);
            //                     }
            //                 } else {
            //                     resolve(0);
            //                 }
            //             }
            //         });
            //     });
            // }
    
            // function fetchAndProcessData() {
            //     return new Promise((resolve, reject) => {
            //         var accrual_data_array = [];
                
            //         frappe.call({
            //             method: "frappe.client.get_list",
            //             args: {
            //                 doctype: "Company",
            //                 filters: { "name": frm.doc.company },
            //                 fields: ["*"]
            //             },
            //             callback: function(companyData) {
            //                 if (companyData.message && companyData.message.length > 0) {
            //                     const customLTAComponent = companyData.message[0].custom_lta_component;
                
            //                     if (customLTAComponent) {
            //                         frappe.call({
            //                             method: "frappe.client.get_list",
            //                             args: {
            //                                 doctype: "Employee Benefit Accrual",
            //                                 filters: {
            //                                     "employee": frm.doc.employee,
            //                                     "docstatus": 1,
            //                                     "salary_component": customLTAComponent
            //                                 },
            //                                 fields: ["*"]
            //                             },
            //                             callback: function(accrual_data) {
            //                                 if (accrual_data.message && accrual_data.message.length > 0) {
            //                                     $.each(accrual_data.message, function(i, g) {
            //                                         accrual_data_array.push(g.amount);
            //                                     });
    
            //                                     const sum = accrual_data_array.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
            //                                     resolve(sum);
            //                                 } else {
            //                                     resolve(0);
            //                                 }
            //                             }
            //                         });
            //                     } else {
            //                         resolve(0);
            //                     }
            //                 } else {
            //                     resolve(0);
            //                 }
            //             }
            //         });
            //     });
            // }
    
            // function claimedAndProcessData() {
            //     return new Promise((resolve, reject) => {
            //         var total_claimed = [];
    
            //         frappe.call({
            //             method: "frappe.client.get_list",
            //             args: {
            //                 doctype: "LTA Claim",
            //                 filters: { "employee": frm.doc.employee },
            //                 fields: ["*"],
            //                 limit: 999999999
            //             },
            //             callback: function(lta_data) {
            //                 if (lta_data.message && lta_data.message.length > 0) {
            //                     $.each(lta_data.message, function(i, m) {
            //                         total_claimed.push(m.amount);
            //                     });
    
            //                     const claimed_total = total_claimed.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
            //                     resolve(claimed_total);
            //                 } else {
            //                     resolve(0);
            //                 }
            //             }
            //         });
            //     });
            // }
    
            // // Call all functions and calculate the final result
            // Promise.all([futureAndProcessData(), fetchAndProcessData(), claimedAndProcessData()])
            //     .then(results => {
            //         const [future_total, accrued_total, claimed_total] = results;
            //         console.log(future_total,"future_total")
            //         console.log(accrued_total,"accrued_total")
            //         console.log(claimed_total,"claimed_total")

            //         const final_result = accrued_total + future_total - claimed_total;
            //         console.log(final_result, "Final Result");
            //         frm.set_value("max_eligible_amount",final_result)
            //     })
            //     .catch(error => {
            //         console.error("Error in processing data:", error);
            //     });
        }
    },

    amount:function(frm)
    {
        if(frm.doc.amount>frm.doc.max_eligible_amount)
        {
            frm.set_value("amount",undefined)
            msgprint("you cant enter amount greater than eligible amount")
        }
    },
    claim_date: function(frm) {
        if (frm.doc.claim_date && frm.doc.claim_date <frappe.datetime.now_date()) {
            frm.set_value("claim_date", null);
            frappe.msgprint(__("You can't select a past date."));
        }
    }
    


    

});




function show_max_lta_amount(frm) {
    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Salary Component",
            filters: { "component_type": "LTA Reimbursement" },
            fields: ["*"],
        },
        callback: function(res) {
            if (res.message && res.message.length > 0) {
                var reimbursement_amount = [];

                frappe.call({
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "Salary Structure Assignment",
                        filters: { employee: frm.doc.employee, docstatus: 1 },
                        fields: ["*"],
                        order_by: "from_date desc",
                        limit: 1
                    },
                    callback: function(response) {
                        if (response.message && response.message.length > 0) {
                            frappe.call({
                                method: "frappe.client.get",
                                args: {
                                    doctype: "Salary Structure Assignment",
                                    name: response.message[0].name
                                },
                                callback: function(employee_data) {
                                    if (employee_data.message) {
                                        $.each(employee_data.message.custom_employee_reimbursements, function(i, v) {
                                            if (v.reimbursements === res.message[0].name) {
                                                reimbursement_amount.push(v.monthly_total_amount);
                                            }
                                            
                                        });

                                        console.log(reimbursement_amount, "-----");

                                        if (reimbursement_amount.length > 0) {
                                            frappe.call({
                                                method: "frappe.client.get_list",
                                                args: {
                                                    doctype: "Payroll Period",
                                                    filters: {
                                                        "company": frm.doc.company,
                                                        "start_date": ["<=", frm.doc.posting_date],
                                                        "end_date": [">=", frm.doc.posting_date]
                                                    },
                                                    fields: ["start_date", "end_date"],
                                                    limit: 1
                                                },
                                                callback: function(payroll_data) {
                                                    if (payroll_data.message && payroll_data.message.length > 0) {
                                                        // console.log(payroll_data.message);

                                                        frappe.call({
                                                            method: "frappe.client.get_list",
                                                            args: {
                                                                doctype: "LTA Claim",
                                                                filters: {
                                                                    "company": frm.doc.company,
                                                                    "claim_date": ["between", payroll_data.message[0].start_date, payroll_data.message[0].end_date],                                                                    
                                                                    "employee": frm.doc.employee,
                                                                    
                                                                },
                                                                fields: ["*"],
                                                            },
                                                            callback: function(lta_data) {
                                                                var total_amount=[]
                                                                if (lta_data.message && lta_data.message.length > 0) {
                                                                    console.log(lta_data.message);
                                                                    $.each(lta_data.message,function(i,k)
                                                                        {
                                                                            total_amount.push(k.amount)
                                                                            
                                                                        })
                                                                    const sum1 = total_amount.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

                                                                    console.log(sum1,"88888")


                                                                    var accrual_data_array = [];

                                                                    frappe.call({
                                                                        method: "frappe.client.get_list",
                                                                        args: {
                                                                            doctype: "Employee Benefit Accrual",
                                                                            filters: {
                                                                                "employee": frm.doc.employee,
                                                                                "docstatus": 1,
                                                                                "salary_component": res.message[0].name,
                                                                                "payroll_period":payroll_data.message[0].name
                                                                            },
                                                                            fields: ["*"]
                                                                        },
                                                                        callback: function(accrual_data) {
                                                                            if (accrual_data.message && accrual_data.message.length > 0) {

                                                                                // console.log(accrual_data.message)
                                                                                $.each(accrual_data.message, function(i, g) {
                                                                                    accrual_data_array.push(g.amount);
                                                                                });

                                                                                const sum = accrual_data_array.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

                                                                                console.log(sum,"99999")
                                                                                var future_value = 12-accrual_data.message.length
                                                                                
                                                                                var future_amount=future_value*reimbursement_amount[0]
                                                                                console.log(future_amount)
                                                                                var max_eligible_amount=(future_amount+sum)-sum1
                                                                                frm.set_value("max_eligible_amount",max_eligible_amount)








                                                                            }
                                                                        }
                                                                    })




                                                                } 
                                                                else 
                                                                {

                                                                    var accrual_data_array = [];

                                                                    frappe.call({
                                                                        method: "frappe.client.get_list",
                                                                        args: {
                                                                            doctype: "Employee Benefit Accrual",
                                                                            filters: {
                                                                                "employee": frm.doc.employee,
                                                                                "docstatus": 1,
                                                                                "salary_component": res.message[0].name,
                                                                                "payroll_period":payroll_data.message[0].name
                                                                            },
                                                                            fields: ["*"]
                                                                        },
                                                                        callback: function(accrual_data) {
                                                                            if (accrual_data.message && accrual_data.message.length > 0) {

                                                                                console.log(accrual_data.message)
                                                                                $.each(accrual_data.message, function(i, g) {
                                                                                    accrual_data_array.push(g.amount);
                                                                                });

                                                                                const sum = accrual_data_array.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
                                                                                // console.log(sum, "Total Accrued Amount");

                                                                                var future_value = 12-accrual_data.message.length
                                                                                var future_amount=future_value*reimbursement_amount[0]
                                                                                frm.set_value("max_eligible_amount",future_amount+sum)

                                                                                // console.log(future_amount, "Future Value of LTA");

                                                                            } 
                                                                            else 
                                                                            {
                                                                                console.log("No accruals found for this salary component.");
                                                                            }
                                                                        }
                                                                    });
                                                                }
                                                            }
                                                        });
                                                    } else {
                                                        frappe.msgprint("This date is not included in the latest payroll period. Please create a payroll period.");
                                                    }
                                                }
                                            });
                                        }
                                    }
                                }
                            });
                        }
                    }
                });
            } else {
                frappe.msgprint("There is no salary component with component type LTA Reimbursement.");
            }
        }
    });
}


function find_tax_regime(frm)
{
    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Salary Structure Assignment",
            filters: { employee: frm.doc.employee, docstatus: 1 },
            fields: ["*"],
            order_by: "from_date desc",
            limit: 1
        },
        callback: function(response) {
            if (response.message && response.message.length > 0) {

                frm.set_value("income_tax_regime",response.message[0].income_tax_slab)

            }
        }
    })

}
