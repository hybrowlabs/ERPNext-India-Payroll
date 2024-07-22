

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
    
            function futureAndProcessData() {
                return new Promise((resolve, reject) => {
                    var component = [];
                    var reimbursement_amount = [];
                    
                    frappe.call({
                        method: "frappe.client.get_list",
                        args: {
                            doctype: "Company",
                            filters: { "name": frm.doc.company },
                            fields: ["*"]
                        },
                        callback: function(companyData) {
                            if (companyData.message && companyData.message.length > 0) {
                                const customLTAComponent = companyData.message[0].custom_lta_component;
                
                                if (customLTAComponent) {
                                    component.push(customLTAComponent);
                
                                    frappe.call({
                                        method: "frappe.client.get_list",
                                        args: {
                                            doctype: "Fiscal Year",
                                            fields: ["*"],
                                            order_by: "year_start_date desc",
                                            limit: 1
                                        },
                                        callback: function(kes) {
                                            if (kes.message && kes.message.length > 0) {
                                                const t1 = new Date(kes.message[0].year_end_date);
                                                const t2 = new Date(frm.doc.claim_date);
                
                                                const years = t1.getFullYear() - t2.getFullYear();
                                                const months = t1.getMonth() - t2.getMonth();
                                                const days = t1.getDate() - t2.getDate();
                
                                                let monthDifference = (years * 12) + months;
                
                                                if (days < 0) {
                                                    monthDifference -= 1;
                                                }
    
                                                frappe.call({
                                                    method: "frappe.client.get_list",
                                                    args: {
                                                        doctype: "Salary Structure Assignment",
                                                        filters: { employee: frm.doc.employee, docstatus: 1 },
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
                                                                    filters: { name: res.message[0].name },
                                                                    fields: ["*"]
                                                                },
                                                                callback: function(employee_data) {
                                                                    if (employee_data.message) {
                                                                        $.each(employee_data.message.custom_employee_reimbursements, function(i, v) {
                                                                            if (v.reimbursements === customLTAComponent) {
                                                                                reimbursement_amount.push(v.monthly_total_amount * monthDifference);
                                                                            }
                                                                        });
    
                                                                        const futureTotal = reimbursement_amount.reduce((acc, curr) => acc + curr, 0);
                                                                        resolve(futureTotal);
                                                                    } else {
                                                                        resolve(0);
                                                                    }
                                                                }
                                                            });
                                                        } else {
                                                            resolve(0);
                                                        }
                                                    }
                                                });
                                            } else {
                                                resolve(0);
                                            }
                                        }
                                    });
                                } else {
                                    resolve(0);
                                }
                            } else {
                                resolve(0);
                            }
                        }
                    });
                });
            }
    
            function fetchAndProcessData() {
                return new Promise((resolve, reject) => {
                    var accrual_data_array = [];
                
                    frappe.call({
                        method: "frappe.client.get_list",
                        args: {
                            doctype: "Company",
                            filters: { "name": frm.doc.company },
                            fields: ["*"]
                        },
                        callback: function(companyData) {
                            if (companyData.message && companyData.message.length > 0) {
                                const customLTAComponent = companyData.message[0].custom_lta_component;
                
                                if (customLTAComponent) {
                                    frappe.call({
                                        method: "frappe.client.get_list",
                                        args: {
                                            doctype: "Employee Benefit Accrual",
                                            filters: {
                                                "employee": frm.doc.employee,
                                                "docstatus": 1,
                                                "salary_component": customLTAComponent
                                            },
                                            fields: ["*"]
                                        },
                                        callback: function(accrual_data) {
                                            if (accrual_data.message && accrual_data.message.length > 0) {
                                                $.each(accrual_data.message, function(i, g) {
                                                    accrual_data_array.push(g.amount);
                                                });
    
                                                const sum = accrual_data_array.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
                                                resolve(sum);
                                            } else {
                                                resolve(0);
                                            }
                                        }
                                    });
                                } else {
                                    resolve(0);
                                }
                            } else {
                                resolve(0);
                            }
                        }
                    });
                });
            }
    
            function claimedAndProcessData() {
                return new Promise((resolve, reject) => {
                    var total_claimed = [];
    
                    frappe.call({
                        method: "frappe.client.get_list",
                        args: {
                            doctype: "LTA Claim",
                            filters: { "employee": frm.doc.employee },
                            fields: ["*"],
                            limit: 999999999
                        },
                        callback: function(lta_data) {
                            if (lta_data.message && lta_data.message.length > 0) {
                                $.each(lta_data.message, function(i, m) {
                                    total_claimed.push(m.amount);
                                });
    
                                const claimed_total = total_claimed.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
                                resolve(claimed_total);
                            } else {
                                resolve(0);
                            }
                        }
                    });
                });
            }
    
            // Call all functions and calculate the final result
            Promise.all([futureAndProcessData(), fetchAndProcessData(), claimedAndProcessData()])
                .then(results => {
                    const [future_total, accrued_total, claimed_total] = results;
                    console.log(future_total,"future_total")
                    console.log(accrued_total,"accrued_total")
                    console.log(claimed_total,"claimed_total")

                    const final_result = accrued_total + future_total - claimed_total;
                    console.log(final_result, "Final Result");
                    frm.set_value("max_eligible_amount",final_result)
                })
                .catch(error => {
                    console.error("Error in processing data:", error);
                });
        }
    }
    

});
