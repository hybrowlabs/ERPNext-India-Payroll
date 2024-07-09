

var array=[]
frappe.ui.form.on('LOP Reversal', {
	onload:function(frm) {

        if(frm.doc.payroll_entry && frm.doc.payroll_entry)
            {
                frappe.call({
        
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "Salary Slip",
                        filters: { "employee": frm.doc.employee, "payroll_entry":frm.doc.payroll_entry},
                        fields: ["*"],
                        
                       
                    },
                    callback: function(res) {


                        if(res.message.length>0)
                            {
                                var date=res.message[0].start_date
                               
                                var date = new Date(date);

                                var month = date.getMonth() + 1;
                                
                                var monthNames = [
                                  "January", "February", "March", "April", "May", "June",
                                  "July", "August", "September", "October", "November", "December"
                                ];
                                var monthName = monthNames[date.getMonth()];

                                frm.set_df_property('lop_month_reversal', 'options', [monthName]);
                                frm.refresh_field('lop_month_reversal');
                            }
                        }
                    })

                }

       

		
	},

    payroll_entry:function(frm)
    {
        if(frm.doc.payroll_entry && frm.doc.employee)
            {
                frappe.call({
        
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "Salary Slip",
                        filters: { "employee": frm.doc.employee, "payroll_entry":frm.doc.payroll_entry},
                        fields: ["*"],
                        
                       
                    },
                    callback: function(res) {


                        if(res.message.length>0)
                            {
                                var date=res.message[0].start_date
                               
                                var date = new Date(date);

                                var month = date.getMonth() + 1;
                                
                                var monthNames = [
                                  "January", "February", "March", "April", "May", "June",
                                  "July", "August", "September", "October", "November", "December"
                                ];
                                var monthName = monthNames[date.getMonth()];

                                frm.set_df_property('lop_month_reversal', 'options', [monthName]);
                                frm.refresh_field('lop_month_reversal');

                                frm.set_value("number_of_days",res.message[0].leave_without_pay)
                                frm.set_value("working_days",res.message[0].total_working_days)
                                frm.set_value("salary_structure",res.message[0].salary_structure)
                                frm.set_value("company",res.message[0].company)


                                
                            }


                        else
                        {
                            frm.set_df_property('lop_month_reversal', 'options', [" "]);
                            frm.refresh_field('lop_month_reversal');
                            frm.set_value("number_of_days",0)
                            frm.set_value("working_days",0)
                            frm.set_value("salary_structure",undefined)
                        }


                    }
                })

            }
    },

    employee:function(frm)
    {

        if(frm.doc.payroll_entry && frm.doc.employee)
            {
                frappe.call({
        
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "Salary Slip",
                        filters: { "employee": frm.doc.employee, "payroll_entry":frm.doc.payroll_entry},
                        fields: ["*"],
                        
                       
                    },
                    callback: function(res) {


                        if(res.message.length>0)
                            {
                                var date=res.message[0].start_date
                               
                                var date = new Date(date);

                                var month = date.getMonth() + 1;
                                
                                var monthNames = [
                                  "January", "February", "March", "April", "May", "June",
                                  "July", "August", "September", "October", "November", "December"
                                ];
                                var monthName = monthNames[date.getMonth()];

                                frm.set_df_property('lop_month_reversal', 'options', [monthName]);
                                frm.refresh_field('lop_month_reversal');

                                frm.set_value("number_of_days",res.message[0].leave_without_pay)
                                frm.set_value("working_days",res.message[0].total_working_days)
                                frm.set_value("salary_structure",res.message[0].salary_structure)
                                
                            }


                        else
                        {
                            frm.set_df_property('lop_month_reversal', 'options', [" "]);
                            frm.refresh_field('lop_month_reversal');
                            frm.set_value("number_of_days",0)
                            frm.set_value("working_days",0)
                            frm.set_value("salary_structure",undefined)
                        }


                    }
                })

            }

    },

   


    before_save: function(frm) {

        frm.clear_table("arrear_breakup");
        frm.refresh_field("arrear_breakup");

        frm.clear_table("arrear_deduction_breakup");
        frm.refresh_field("arrear_deduction_breakup");


        
    
        if (frm.doc.employee && frm.doc.working_days && frm.doc.salary_structure) {



            frappe.call({
                method: "hrms.payroll.doctype.salary_structure.salary_structure.make_salary_slip",
                args: {
                    source_name: frm.doc.salary_structure,
                    employee: frm.doc.employee,
                    print_format: 'Salary Slip Standard for CTC',
                },
                callback: function(response) {
                    console.log(response.message.earnings, "111");
                    
                    var array = [];

                    var array1=[];
                    
                    $.each(response.message.earnings, function(i, v) {
                        var detail = {
                            salary_component: v.salary_component,
                            amount: v.amount
                        };
                        array.push(detail);
                    });

                    $.each(response.message.deductions, function(i, k) {


                        var detail1 = {
                            salary_component: k.salary_component,
                            amount: k.amount
                        };
                        array1.push(detail1);

                    });

    
                    function fetchSalaryComponentDetails(index) {
                        if (index < array.length) {
                            var salaryComponent = array[index].salary_component;
    
                            frappe.call({
                                method: "frappe.client.get_list",
                                args: {
                                    doctype: "Salary Component",
                                    filters: { "custom_is_arrear": 1, "custom_component": salaryComponent },
                                    fields: ["*"]
                                },
                                callback: function(res) {
                                    if (res.message[0]) {
                                        
    
                                        
    
                                        var child = frm.add_child("arrear_breakup");
    
                                        frappe.model.set_value(child.doctype, child.name, "salary_component", res.message[0].name);
                                        var amount = (array[index].amount / frm.doc.working_days) * frm.doc.number_of_days;
                                        var roundedAmount = Math.round(amount);

                                        frappe.model.set_value(child.doctype, child.name, "amount", roundedAmount);
                                        
                                        frm.refresh_field("arrear_breakup");
                                    }
                                    fetchSalaryComponentDetails(index + 1);
                                }
                            });
                        }
                    }
                    fetchSalaryComponentDetails(0);



                    function fetchSalaryComponentDetailsDeduction(index) {
                        if (index < array1.length) {
                            var salaryComponent = array1[index].salary_component;
            
                            frappe.call({
                                method: "frappe.client.get_list",
                                args: {
                                    doctype: "Salary Component",
                                    filters: { "custom_is_arrear": 1, "custom_component": salaryComponent },
                                    fields: ["*"]
                                },
                                callback: function(res) {
                                    if (res.message[0]) {
                                        
    
                                        
    
                                        var child = frm.add_child("arrear_deduction_breakup");
    
                                        frappe.model.set_value(child.doctype, child.name, "salary_component", res.message[0].name);
                                        var amount = (array1[index].amount / frm.doc.working_days) * frm.doc.number_of_days;
                                        var roundedAmount = Math.round(amount);

                                        frappe.model.set_value(child.doctype, child.name, "amount", roundedAmount);
                                        
                                        frm.refresh_field("arrear_deduction_breakup");
                                    }
                                    fetchSalaryComponentDetailsDeduction(index + 1);
                                }
                            })
                        }
                    }

                    fetchSalaryComponentDetailsDeduction(0)




                }
            });


        }
    }
    
    
    
   

})