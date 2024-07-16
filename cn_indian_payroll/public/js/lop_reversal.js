
var month_array=[]
var payroll_entry_array=[]
var payroll_entry_array1=[" "]
frappe.ui.form.on('LOP Reversal', {

    employee: function(frm) {
        if (frm.doc.employee) {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Salary Slip",
                    filters: [
                        ["employee", "=", frm.doc.employee],
                        ["leave_without_pay", ">", 0],
                        ["custom_lop_updated", "=", 0],
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
    },

    lop_month_reversal:function(frm)
    {

        
var month_map = {
    "January": 0,
    "February": 1,
    "March": 2,
    "April": 3,
    "May": 4,
    "June": 5,
    "July": 6,
    "August": 7,
    "September": 8,
    "October": 9,
    "November": 10,
    "December": 11
};


var month = frm.doc.lop_month_reversal;

var current_date = new Date();
var year = current_date.getFullYear();

var month_number = month_map[month];

var start_date = new Date(year, month_number, 1);

var start_date_str = start_date.getFullYear() + '-' + String(start_date.getMonth() + 1).padStart(2, '0') + '-01';
console.log(start_date_str);



                frappe.call({
        
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "Salary Slip",
                        filters: { "employee": frm.doc.employee,"docstatus":1,"start_date":start_date_str},
                        fields: ["*"],
                        
                       
                    },
                    callback: function(res) {


                        if(res.message.length>0)
                            {

                                console.log(res.message[0].name,"1111")

                               
                                frm.set_value("salary_slip",res.message[0].name)
                                frm.set_value("payroll_entry",res.message[0].payroll_entry)
                                frm.set_value("working_days",res.message[0].payment_days)
                                frm.set_value("max_lop_days",res.message[0].leave_without_pay)
                                

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
    

   


    before_save: function(frm) {

        frm.clear_table("arrear_breakup");
        frm.refresh_field("arrear_breakup");

        frm.clear_table("arrear_deduction_breakup");
        frm.refresh_field("arrear_deduction_breakup");


        
    
        if (frm.doc.employee && frm.doc.working_days && frm.doc.salary_slip) {



            frappe.call({

                method: "frappe.client.get",
                    args: {
                        doctype: "Salary Slip",
                        filters: { "employee": frm.doc.employee, "name":frm.doc.salary_slip},
                        fields: ["*"],
                        
                       
                    },

                callback: function(response) {
                   
                    
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