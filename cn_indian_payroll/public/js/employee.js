frappe.ui.form.on('Employee', {
    refresh(frm) {

        

       

        if(!frm.is_new())
            {
        
            frm.add_custom_button(__("Tax Exemption Declaration"),function()
            {

                frappe.call({
        
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "Employee Tax Exemption Declaration",
                        filters: { "employee": frm.doc.employee, "docstatus": ["in", [0, 1]]},
                        fields: ["name"],
                        limit: 1,
                       
                    },
                    callback: function(res) {

                       
                        if (res.message.length>0)
                        {
                            frappe.set_route("Form", "Employee Tax Exemption Declaration", res.message[0].name);

                        }
                        else{
                            msgprint("Please Create Employee Tax Exemption Declaration")
                        }
                       

                    }
                })



                
                //  frappe.set_route("Form", "Employee Tax Exemption Declaration", 'new-employee-tax-exemption-declaration');
                
            })

            if (frappe.user.has_role("HR Manager")) 
                {

                        frm.add_custom_button(__("Assign CTC"),function()
                        {

                            frappe.call({
                    
                                method: "frappe.client.get_list",
                                args: {
                                    doctype: "Salary Structure Assignment",
                                    filters: { "employee": frm.doc.employee, "docstatus": 1 },
                                    fields: ["name"],
                                    limit: 1,
                                
                                },
                                callback: function(res) {

                                    
                                    if (res.message.length>0)
                                    {
                                        frappe.set_route("Form", "Salary Structure Assignment", res.message[0].name);
                                        

                                    }
                                    else
                                    {

                                    

                                        frappe.route_options = {"employee": frm.doc.name};

                                        frappe.set_route("Form", "Salary Structure Assignment", 'new-salary-structure-assignment');
                                    }
                                

                                }
                            })



                            
                        
                            
                        })

                }


        }
    },
    
    
    
  
   
    
    
    
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

function additional_component(frm) {
   

    frm.clear_table("custom_additional_component");
    frm.refresh_field("custom_additional_component");

    let additional_component_array = ["Car Allowance", "Special HRA", "Special Conveyance"];

    $.each(additional_component_array, function(i, v) {
        let child = frm.add_child("custom_additional_component");
        frappe.model.set_value(child.doctype, child.name, "salary_component", v);
    });

    frm.refresh_field("custom_additional_component");
}
