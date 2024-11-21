
var month_array=[]
var payroll_entry_array=[]
var payroll_entry_array1=[" "]
frappe.ui.form.on('LOP Reversal', {

    employee: function(frm) {
        if (frm.doc.employee) {


            let salary_slips = [];

                frappe.call({
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "Salary Slip",
                        filters: [
                            ["employee", "=", frm.doc.employee],
                            ["docstatus", "=", 1],
                            ["leave_without_pay", ">", 0]
                        ],
                        fields: ["*"],
                    },
                    callback: function (res1) {
                        if (res1.message) {
                            salary_slips = res1.message; // Add first set of results
                        }

                        // Second call for absent_days
                        frappe.call({
                            method: "frappe.client.get_list",
                            args: {
                                doctype: "Salary Slip",
                                filters: [
                                    ["employee", "=", frm.doc.employee],
                                    ["docstatus", "=", 1],
                                    ["absent_days", ">", 0]
                                ],
                                fields: ["*"],
                            },
                            callback: function (res2) {
                                if (res2.message) {
                                    // Combine both results
                                    salary_slips = salary_slips.concat(res2.message);
                                }

                                // Remove duplicates (if necessary)
                                let unique_slips = [...new Map(salary_slips.map(item => [item.name, item])).values()];

                                // Process the final unique list
                                console.log(unique_slips);

                                if(unique_slips.length>0)
                                {

                                var total_lop=0
                                var month_array = [];

                                            $.each(unique_slips, function(i, v) {

                                                total_lop=v.leave_without_pay+v.absent_days

                                                if(v.total_lop!=v.custom_lop_reversal_days)
                                                {
                                                    month_array.push(v.start_date);
                                                }
                                               
                                            });

                                                        var month_names = [];
    
                        
                                                        var month_map = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
                                    
                                                        
                                                        month_array.forEach(function(date_str) {
                                                            var date = new Date(date_str);
                                                            var month_name = month_map[date.getMonth()];
                                                            month_names.push(month_name);
                                                        });

                                                         console.log(month_names,"22222")

                                                        frm.set_df_property('lop_month_reversal', 'options', month_names.join('\n'));
                                                        frm.refresh_field('lop_month_reversal');
                                    
                                                        
                                                    } 

                                                
                                                    else 
                                                    {
                                                    
                                                        frm.set_df_property('lop_month_reversal', 'options', "");
                                                        frm.refresh_field('lop_month_reversal');
                                                        
                                                    }



                                            
                            }
                        });
                    }
                });







            // frappe.call({
            //     method: "frappe.client.get_list",
            //     args: {
            //         doctype: "Salary Slip",
            //         filters: [
            //             ["employee", "=", frm.doc.employee],
            //             ["docstatus", "=", 1],
                        
            //            [["leave_without_pay", ">", 0],|| 
                            
            //             ["absent_days", ">", 0]]
                        
            //         ],
            //         fields: ["*"],
            //     },
            //     callback: function(res) {
            //         var month_array = [];

            //         console.log(res.message,"111111")
    
            //         // if (res.message.length > 0) {

                        
            //         //     $.each(res.message, function(i, v) {

            //         //         // if(v.leave_without_pay!=v.custom_lop_reversal_days)
            //         //         // {
            //         //             month_array.push(v.start_date);
            //         //         // }
            //         //     });
    
            //         //     var month_names = [];
    
                        
            //         //     var month_map = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    
                        
            //         //     month_array.forEach(function(date_str) {
            //         //         var date = new Date(date_str);
            //         //         var month_name = month_map[date.getMonth()];
            //         //         month_names.push(month_name);
            //         //     });
    
                        
    
                        
            //         //     frm.set_df_property('lop_month_reversal', 'options', month_names.join('\n'));
            //         //     frm.refresh_field('lop_month_reversal');
    
                        
            //         // } 
            //         // else 
            //         // {
                       
            //         //     frm.set_df_property('lop_month_reversal', 'options', "");
            //         //     frm.refresh_field('lop_month_reversal');
                        
            //         // }
            //     }
            // });
        }
    },

    lop_month_reversal:function(frm)
    {




        var month = frm.doc.lop_month_reversal;




                frappe.call({
        
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "Salary Slip",
                        filters: { "employee": frm.doc.employee,"docstatus":1,"custom_month":month},
                        fields: ["*"],
                        
                       
                    },
                    callback: function(res) {


                        if(res.message.length>0)
                            {

                                var total_lop=res.message[0].leave_without_pay+res.message[0].absent_days

                                var salary_slip=res.message[0].name


                                frappe.call({
        
                                    method: "frappe.client.get_list",
                                    args: {
                                        doctype: "LOP Reversal",
                                        filters: { "employee": frm.doc.employee,"docstatus":1,"salary_slip":salary_slip},
                                        fields: ["*"],
                                        
                                       
                                    },
                                    callback: function(kes) {
                
                                        var days=0
                                        
                                        if(kes.message.length>0)
                                        {
                                            $.each(kes.message,function(i,v)
                                            {
                                                days=days+v.number_of_days
                                                

                                                
                                            })



                                            frm.set_value("salary_slip",salary_slip)
                                            frm.set_value("payroll_entry",res.message[0].payroll_entry)
                                            frm.set_value("working_days",res.message[0].payment_days)
                                            // frm.set_value("max_lop_days",res.message[0].leave_without_pay-days)
                                            frm.set_value("max_lop_days",total_lop-days)
                                            frm.set_value("absent_days",res.message[0].absent_days)
                                            frm.set_value("lop_days",res.message[0].leave_without_pay)

                                            


                                        }
                                        else{
                                            frm.set_value("salary_slip",salary_slip)
                                            frm.set_value("payroll_entry",res.message[0].payroll_entry)
                                            frm.set_value("working_days",res.message[0].payment_days)
                                            frm.set_value("max_lop_days",res.message[0].leave_without_pay+res.message[0].absent_days)
                                            frm.set_value("absent_days",res.message[0].absent_days)
                                            frm.set_value("lop_days",res.message[0].leave_without_pay)
                                        }
                                    }
                                })





                                
                               
                                

                            }
                        }
                    })


    },


    number_of_days:function(frm)
    {
        if(frm.doc.number_of_days && frm.doc.number_of_days>frm.doc.max_lop_days)
            {
                msgprint("You can't enter days greater than maximum LOP days")
                frm.set_value("number_of_days",undefined)
            }


    },

    refresh:function(frm)
    {
        
            if (frm.doc.employee && frm.doc.salary_slip) {
                frappe.call({
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "Salary Slip",
                        filters: [
                            ["employee", "=", frm.doc.employee],
                            ["name", "=", frm.doc.salary_slip],
                            
                            
                            ["docstatus", "=", 1],
                        ],
                        fields: ["*"],
                    },
                    callback: function(res) {
                        var month_array = [];
        
                        if (res.message.length > 0) {
    
                            
                            $.each(res.message, function(i, v) {
                                
                                month_array.push(v.start_date);
                                
                            });
        
                            var month_names = [];
        
                            
                            var month_map = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        
                            
                            month_array.forEach(function(date_str) {
                                var date = new Date(date_str);
                                var month_name = month_map[date.getMonth()];
                                month_names.push(month_name);
                            });
        
                            
        
                            
                            frm.set_df_property('lop_month_reversal', 'options', month_names.join('\n'));
                            frm.refresh_field('lop_month_reversal');
        
                            
                        } 
                        else 
                        {
                           
                            frm.set_df_property('lop_month_reversal', 'options', "");
                            frm.refresh_field('lop_month_reversal');
                            
                        }
                    }
                });
            }
        
    }
    

    
   

})