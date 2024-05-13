frappe.ui.form.on('Employee Benefit Claim', {
	refresh(frm) {
		// your code here
	},


    earning_component: function(frm) 
    
    {
        if (frm.doc.earning_component) {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Employee Benefit Accrual",
                    filters: { "employee": frm.doc.employee, "salary_component": frm.doc.earning_component },
                    fields: ["name", "amount"],
                    limit: 99999999
                },
                callback: function(res) {
                    if (res.message) {
                        // console.log(res.message);
    
                        var sum = 0;
                        $.each(res.message, function(i, v) {
                            console.log(v.amount);
                            sum += v.amount; // Corrected sum calculation
                        });
    
                        console.log(sum);


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

                                    // console.log(kes.message,"ppp")
                                    if(kes.message.length>0)
                                        {
                                            var total_sum = 0;
                                                $.each(kes.message, function(i, k) {
                                                   
                                                    total_sum += k.claimed_amount; // Corrected sum calculation
                                                });

                                                console.log(total_sum,"total_sumtotal_sum")


                                                frm.set_value("custom_max_amount",sum-total_sum)

                                        }


                                    else
                                    {
                                        frm.set_value("custom_max_amount",sum)
                                    }

                                }
                            }
                        })




                    }
                }
            });
        }
    }
    
    
    

    
})