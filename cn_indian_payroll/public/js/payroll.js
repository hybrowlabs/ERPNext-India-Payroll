frappe.ui.form.on('Payroll Entry', {


    

    refresh(frm) 
    {

        
        
            // frm.add_custom_button(__("test"),function(frm)
            //     {
            //         frappe.call({
            //             method: 'payrollset',
            //             // doc: frm.doc,
            //             args: {
            //                 value1: frm.doc.name
            //             },
            //             callback: function(r) {
            //                 if (r.message) {
            //                     frappe.msgprint(r.message);
            //                 }
            //             }
            //         });
                    
            //     })



            





            if(frm.doc.custom_bonus_payment_mode=="Bonus Payout")

                {
                    if( frm.doc.custom_additional_salary_submitted==0)
                        {
                            
                            frm.page.clear_primary_action();

                        }
                    
                }










        if(frm.doc.salary_slips_created==1)
            {



        if (frm.doc.custom_bonus_payment_mode == "Bonus Accrual" && frm.doc.custom_bonus_accrual_created == 0)
            
            
            {

                create_bonus_accrual_entry(frm)



             


            }


        }

    if(frm.doc.custom_bonus_accrual_created==1 && frm.doc.custom_bonus_accrual_submit==0)
        {

            if (frm.doc.custom_bonus_payment_mode == "Bonus Accrual" )
            {

            frm.add_custom_button(__("Sumbit Bonus Accrual"),function()
                {

                     frappe.call({

                        "method":"meril.meril.overrides.accrual_bonus.get_submit",
                        args:{

                            payroll_entry: frm.doc.name

                        },
                        callback :function(res)
                        {
                            // console.log(res.message,"111111")
                            if(res.message)
                                {
                                    frm.set_value("custom_bonus_accrual_submit",1)
                                    frm.save('Update');
                                }

                        }

            })
                    
                })

            }

           

        }



        if (frm.doc.custom_bonus_payment_mode == "Bonus Payout") 
            
            {

                if(frm.doc.custom_additional_salary_created==0 && frm.doc.custom_additional_salary_submitted==0&&frm.doc.employees.length>0)

                {





                    frm.add_custom_button(__('Create Additional Salary'), function() {
                    
                            frappe.call({
                                // method: 'meril.payroll.get_additional_salary',
                                method: 'meril.meril.overrides.additional_salary.get_additional_salary',
                                args: {
                                    payroll_id:frm.doc.name
                                },
                                callback: function(response) {
                                    // Process the response if needed
                                    console.log(response.message);

                                    
                                }
                            });
                        // }
                    });

                }
        }



        if (frm.doc.custom_bonus_payment_mode == "Bonus Payout") 
            
            {

                if(frm.doc.custom_additional_salary_created==1 &&frm.doc.custom_additional_salary_submitted==0 &&frm.doc.employees.length>0)

                {

                    frm.add_custom_button(__("Sumbit Additional Salary"),function()
                    {
    
                        frappe.call({
    
                            "method":"meril.meril.overrides.additional_salary.additional_salary_submit",
                            args:{
    
                                additional: frm.doc.name
    
                            },
                            callback :function(res)
                            {
                                // console.log(res.message,"111111")
                                if(res.message)
                                    {
                                        // frm.set_value("custom_bonus_accrual_submit",1)
                                        // frm.save('Update');
                                    }
    
                            }
    
                        })
                        
                    })




                }
            }


    },


    after_save(frm)
    {
        if(frm.doc.custom_bonus_accrual_created==1 && frm.doc.custom_bonus_accrual_submit==0)
            {
                msgprint("Employee Bonus Accrual Created")


            }


            if(frm.doc.custom_bonus_accrual_submit==1)
                {
                    msgprint("Employee Bonus Accrual Submitted")
    
    
                }
    }
});



function create_bunus(frm)
{
    console.log("hiii")
    frm.add_custom_button(__("Create Bonus Accrual Entry"), function() {
                if (frm.doc.employees.length > 0) {
                    $.each(frm.doc.employees, function(i, v) {
                        frappe.call({
                            "method": "frappe.client.get_list",
                            args: {
                                doctype: "Salary Structure Assignment",
                                filters: { employee: v.employee ,docstatus:1},
                                fields: ["name", "from_date", "employee", "salary_structure", "company", "currency", "base"],
                                order_by: "from_date desc",
                                limit: 1
                            },
                            callback: function(res) {
                                if (res.message && res.message.length > 0) {
                                    var salaryStructure = res.message[0];
                                    // console.log(salaryStructure)
                                    console.log(res.message[0].name)


                                    if (salaryStructure.company)
                                         {
                                           

                                        frappe.call({
                                            "method": "frappe.client.get",
                                            args: {
                                                doctype: "Company",
                                                filters: { name: salaryStructure.company },
                                                fields: ["name", "custom_bonus_salary_component"],
                                            },
                                            callback: function(companyData) {
                                                if (companyData.message && companyData.message.custom_bonus_salary_component) {
                                                    
                                                    console.log(companyData.message.custom_bonus_salary_component)

                                                    
                                                    
                                                    frappe.call({
                                                        "method": "frappe.client.get_list",
                                                        args: {
                                                            doctype: "Salary Slip",
                                                            filters: {"employee": v.employee, "payroll_entry": frm.doc.name },
                                                            fields: ["name"],
                                                        },
                                                        callback: function(salaryslip) {
                                                            if (salaryslip.message && salaryslip.message.length > 0) {
                                                                console.log(salaryslip.message[0].name, "111");

                                                                frappe.call
                                                                ({
                                                                    "method": "frappe.client.get",
                                                                    args: {
                                                                        doctype: "Salary Slip",
                                                                        filters: { name: salaryslip.message[0].name },
                                                                        
                                                                    },
                                                                    callback: function(slipdate) {

                                                                       

                                                                        $.each(slipdate.message.earnings, function(i, component) {

                                                                         




                                                                            if(component.salary_component==companyData.message.custom_bonus_salary_component)
                                                                                {
                                                                                    console.log(component.amount)
                                                                                    
                                                                                       frappe.db.insert({
                                                                                          "doctype": "Employee Bonus Accrual",
                                                                                          "employee": v.employee,
                                                                                          "company":  frm.doc.company,
                                                                                          "accrual_date": frm.doc.posting_date,
                                                                                          "salary_component": companyData.message.custom_bonus_salary_component,
                                                                                          "salary_structure":slipdate.message.salary_structure ,
                                                                                          "salary_structure_assignment": res.message[0].name,
                                                                                          "bonus_paid_date":frm.doc.posting_date,
                                                                                          "payroll_entry":frm.doc.name,
                                                                                        
                                                                                          "amount": component.amount
                                                                                    });


                                                                                    frm.set_value("custom_bonus_accrual_created",1)
                                                                                    frm.save('Update');


                                                                                    
                                                                                    




                                                                                }

                                                                        })



                                                                        
                                                                    }

                                                                })



                                                            }
                                                        }
                                                    });
                                                }
                                            }
                                        });
                                    }
                                }
                            }
                        });
                    });

                    // msgprint("Employee Bonus Accrual Created")
                }
                    


            });






}

function create_bonus_accrual_entry(frm)
{
    frm.add_custom_button(__("Create Bonus Accrual Entry"),function()
    {

         frappe.call({

            "method":"meril.meril.overrides.accrual_bonus.accrual_created",
            args:{

                payroll_entry_doc_id: frm.doc.name,
                company_name :frm.doc.company

            },
            callback: function(res)
            {
                // console.log(res.message,"9999")


                msgprint("Bonus Accrual is Created")
                frm.set_value("custom_bonus_accrual_created",1)
                frm.save('Update');
                
            }
            

            })
        
    })


}

