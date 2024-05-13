frappe.ui.form.on('Employee', {
    refresh(frm) {
        
        frm.add_custom_button(__("Tax Excemption Declaration"),function()
            {
                
                 frappe.set_route("Form", "Employee Tax Exemption Declaration", 'new-employee-tax-exemption-declaration');
                
            })
        // Your code here
    },
    
    custom_nps_percent(frm) {
        if (frm.doc.custom_is_nps == 1 && frm.doc.custom_nps_percent )
        
        {
        
        if(frm.doc.custom_nps_percent <= 10) 
        {
            base_value(frm, function(amount) 
            {
                
                
                // console.log(amount, "99");
                
                var nps_value=(amount*frm.doc.custom_nps_percent)/100
                frm.set_value("custom_nps_values",nps_value)
            });
        }
        
        else
        {
            msgprint("you cant put percentage greater than 10")
            frm.set_value("custom_nps_values",undefined)
            frm.set_value("custom_nps_percent",undefined)
        }
        
        }
    },
    
    // custom_nps_values(frm) {
    //     if (frm.doc.custom_is_nps == 1 && frm.doc.custom_nps_values) {
            
            
    //         base_value(frm, function(amount)
    //         {
            
    //         // var amount=43750
                
    //             console.log(amount)
                
    //             var nps_value=(amount/10)
    //             console.log(nps_value,"oo")
                
    //             if(frm.doc.custom_nps_values>nps_value)
    //             {
    //                 msgprint("You cant enter amount greater than "+nps_value)
    //                 frm.set_value("custom_nps_values",undefined)
    //                 frm.set_value("custom_nps_percent",undefined)
                    
    //             }
                
    //             else
    //             {
    //                 // console.log(amount)
                    
    //                 if(frm.doc.custom_nps_values==nps_value)
    //                 {
    //                     console.log("matching")
                        
                    
    //                     // console.log(percentage,10)
                    
    //                     frm.set_value("custom_nps_percent",10)
    //                 }
                    
    //                 else
    //                 {
    //                     msgprint("amount is not the 10% of basic")
    //                     frm.set_value("custom_nps_values",undefined)
    //                 // frm.set_value("custom_nps_percent",undefined)
    //                 }
                    
                    

    //             }
                
                
    //         })
            
            
    //         // Perform operations if needed
    //     }
    // },
    
    
    
    custom_cubic_capacity_of_company(frm)
    {
       
        
            if(frm.doc.custom_cubic_capacity_of_company=="Car < 1600 CC" )
            {
                frm.set_value("custom_car_perquisite_as_per_rules",1800)
                
            }
            
            else if (frm.doc.custom_cubic_capacity_of_company=="Car > 1600 CC")
            {
                
                 frm.set_value("custom_car_perquisite_as_per_rules",2400)
                
            }
        

    },
    
    
    custom_is_driver_provided_by_company(frm)
    {
        if(frm.doc.custom_is_driver_provided_by_company==1)
        {
            frm.set_value("custom_driver_perquisite_as_per_rules",900)
        }
        else
        {
            frm.set_value("custom_driver_perquisite_as_per_rules",undefined) 
        }
    }
});

function base_value(frm, callback) 
{
    frappe.call({
        
        method: "frappe.client.get_list",
        args: {
            doctype: "Salary Structure Assignment",
            filters: { "employee": frm.doc.employee, "docstatus": 1 },
            fields: ["name", "base"],
            limit: 1,
            order_by: "from_date desc",
        },
        callback: function(res) {
            if (res.message && res.message.length > 0) {
                var amount = (res.message[0].base / 12 * 35) / 100;
                callback(amount);
            } else {
                frappe.msgprint("Please create a salary structure assignment before assigning NPS");
            }
        }
    });
}
