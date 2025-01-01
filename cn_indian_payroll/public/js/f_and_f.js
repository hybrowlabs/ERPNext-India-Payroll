frappe.ui.form.on('Full and Final Statement', {
    refresh(frm) {
        // Logic for refreshing the form if needed
    },

    employee(frm) {
        get_outstanding_benefits(frm);
    }
});

function get_outstanding_benefits(frm) {
    if (frm.doc.employee) {
        // Fetch the latest Salary Structure Assignment for the employee
        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Salary Structure Assignment",
                filters: {
                    employee: frm.doc.employee,
                    docstatus: 1
                },
                fields: ["*"],
                limit: 1,
                order_by: "from_date desc"
            },
            callback: function (res) {
                if (res.message && res.message.length > 0) {
                    const payrollPeriod = res.message[0].custom_payroll_period;

                    if (payrollPeriod) {


                        frappe.call({
                            method: "frappe.client.get_list",
                            args: {
                                doctype: "Employee Benefit Accrual",
                                filters: {
                                    employee: frm.doc.employee,
                                    docstatus: ["in", [0, 1]],
                                    payroll_period: payrollPeriod
                                },
                                fields: ["*"],
                                limit_page_length: 0
                            },
                            callback: function (response) {
                                if (response.message && response.message.length > 0) {
                        
                                    // Create a map to group components
                                    let componentGroups = {};
                        
                                    // Group components by their salary_component
                                    $.each(response.message, function (i, v) {
                                        if (!componentGroups[v.salary_component]) {
                                            componentGroups[v.salary_component] = [];
                                        }
                                        componentGroups[v.salary_component].push(v);
                                    });
                        
                                    // Iterate through the grouped components in the desired order
                                    Object.keys(componentGroups).forEach(function (component) {
                                        let group = componentGroups[component];
                                        let componentSum = 0; // To sum the components
                                        let totalSettlement = 0; // To accumulate total settlement for subtraction
                        
                                        // Add each component in the group
                                        $.each(group, function (i, v) {
                                            componentSum += v.amount; // Add the accrued amount
                                            totalSettlement += v.total_settlement; // Add the total settlement
                                        });
                        
                                        // Calculate the final value to be added to payables (sum - total settlement)
                                        let finalAmount = componentSum - totalSettlement;
                        
                                        // Add the result to the child table (payables)
                                        let child = frm.add_child('payables');
                                        child.component = component; // Set the component name (e.g., Bonus, Leave Travel Allowance, etc.)
                                        child.amount = finalAmount; // Set the final calculated amount
                                        frm.refresh_field('payables');
                                    });
                        
                                    console.log(componentGroups, "componentGroups");
                        
                                }
                            }
                        });
                        





                        frappe.call({
                            method: "frappe.client.get_list",
                            args: {
                                doctype: "Employee Benefit Accrual",
                                filters: {
                                    employee: frm.doc.employee,
                                    docstatus: ["in", [0, 1]],
                                    payroll_period: payrollPeriod
                                },
                                fields: ["*"],
                                limit_page_length: 0 
                                },
                            callback: function (response) {
                                if (response.message && response.message.length > 0) {
                                
                                    // Create a map to group components
                                    let componentGroups = {};
                                
                                    // Group components by their salary_component
                                    $.each(response.message, function (i, v) {
                                        if (!componentGroups[v.salary_component]) {
                                            componentGroups[v.salary_component] = [];
                                        }
                                        componentGroups[v.salary_component].push(v);
                                    });
                                
                                    // Iterate through the grouped components in the desired order
                                    Object.keys(componentGroups).forEach(function (component) {
                                        let group = componentGroups[component];
                                
                                        // Add each component in the group to the child table
                                        $.each(group, function (i, v) {
                                            let child = frm.add_child('custom_accrued_benefit');

                                            if(v.salary_slip)
                                            {

                                                frappe.call({
                                                    method: "frappe.client.get",
                                                    args: {
                                                        doctype: "Salary Slip",
                                                        filters: {
                                                            employee: v.employee,
                                                            name: v.salary_slip
                                                           
                                                        },
                                                        
                                                        },
                                                    callback: function (slip_response) {
                                                        if(slip_response.message)
                                                        {
                                                            child.date = v.benefit_accrual_date; // Replace 'benefit_accrual_date' with the correct field
                                                            child.salary_slip_id = v.salary_slip; // Replace 'salary_slip' with the correct field
                                                            child.salary_component = v.salary_component;
                                                            child.accrued_amount = v.amount; // Replace 'amount' with the correct field
                                                            child.claimed_amount = v.total_settlement; // Replace 'total_settlement' with the correct field
                                                            child.payment_days=slip_response.message.payment_days


                                                        }
                                                        frm.refresh_field('custom_accrued_benefit');

                                                    }
                                                })

                                            }
                                            
                                            
                                           
                                        });
                                    });

                                    console.log(componentGroups,"componentGroupscomponentGroups")


                                    

                                    
                                }
                                
                                
                                else 
                                
                                {

                                    
                                }
                            }
                        });



                        //BONUS COMPONENT
                        
                        var bonus_sum=[]
                        frappe.call({
                            method: "frappe.client.get_list",
                            args: {
                                doctype: "Employee Bonus Accrual",
                                filters: {
                                    employee: frm.doc.employee,
                                    docstatus: ["in", [0, 1]],
                                    is_paid:0
                                },
                                fields: ["*"],
                                limit_page_length: 0 
                                },
                            callback: function (bonus_response) {

                                if(bonus_response.message)
                                {
                                    

                                    $.each(bonus_response.message, function (i, k) {

                                        bonus_sum.push(k.amount)


                                        let child = frm.add_child('custom_accrued_benefit');

                                        if(k.salary_slip)
                                        {

                                            frappe.call({
                                                method: "frappe.client.get",
                                                args: {
                                                    doctype: "Salary Slip",
                                                    filters: {
                                                        employee: k.employee,
                                                        name: k.salary_slip
                                                       
                                                    },
                                                    
                                                    },
                                                callback: function (slip_response_data) {
                                                    if(slip_response_data.message)
                                                    {
                                                        
                                                        child.date = k.accrual_date; // Replace 'benefit_accrual_date' with the correct field
                                                        child.salary_slip_id = k.salary_slip; // Replace 'salary_slip' with the correct field
                                                        child.salary_component = k.salary_component;
                                                        child.accrued_amount = k.amount; // Replace 'amount' with the correct field
                                                        child.payment_days=slip_response_data.message.payment_days


                                                    }
                                                    frm.refresh_field('custom_accrued_benefit');

                                                }
                                            })

                                        }
                                        
                                        
                                       
                                    });

                                    console.log(bonus_sum,"BONUS")

                                    let sum = bonus_sum.reduce(function(accumulator, currentValue) {
                                        return accumulator + currentValue;
                                    }, 0); // 0 is the initial value of the accumulator
                                    
                                    
            
                                    let child = frm.add_child('payables');
                                    child.component = "Bonus PaidOut";
                                    child.amount=sum
                                    frm.refresh_field('payables');

                                    
                                     
                                }
                            }
                        })




                        
                        

                        frappe.call({
                            method: "frappe.client.get_list",
                            args: {
                                doctype: "Salary Slip",
                                filters: {
                                    employee: frm.doc.employee,
                                    docstatus: ["in", [0, 1]],
                                    custom_payroll_period: payrollPeriod,
                                    
                                    
                                },
                                fields: ["*"],
                                limit_page_length: 0,
                                order_by: "posting_date asc"
                            },
                            callback: function (salary_slip_response) {
                        
                                if (salary_slip_response.message) {
                                    // Arrays to store PT and Income Tax separately
                                    let ptComponents = [];
                                    let incomeTaxComponents = [];
                        
                                    $.each(salary_slip_response.message, function (i, s) {
                                        frappe.call({
                                            method: "frappe.client.get",
                                            args: {
                                                doctype: "Salary Slip",
                                                filters: {
                                                    name: s.name
                                                }
                                            },
                                            callback: function (each_slip_response_data) {
                                                if (each_slip_response_data.message) {
                                                    $.each(each_slip_response_data.message.deductions, function (i, p) {
                                                        frappe.call({
                                                            method: "frappe.client.get",
                                                            args: {
                                                                doctype: "Salary Component",
                                                                filters: {
                                                                    name: p.salary_component
                                                                }
                                                            },
                                                            callback: function (component_data) {
                                                                if (component_data.message) {
                                                                    // Check if the component is PT or Income Tax and store accordingly
                                                                    if (component_data.message.component_type == "Professional Tax") {
                                                                        ptComponents.push({
                                                                            date: each_slip_response_data.message.posting_date,
                                                                            salary_slip_id: each_slip_response_data.message.name,
                                                                            salary_component: component_data.message.salary_component,
                                                                            amount: p.amount,
                                                                            payment_days: each_slip_response_data.message.payment_days
                                                                        });
                                                                    } else if (component_data.message.is_income_tax_component == 1) {
                                                                        incomeTaxComponents.push({
                                                                            date: each_slip_response_data.message.posting_date,
                                                                            salary_slip_id: each_slip_response_data.message.name,
                                                                            salary_component: component_data.message.salary_component,
                                                                            amount: p.amount,
                                                                            payment_days: each_slip_response_data.message.payment_days
                                                                        });
                                                                    }
                                                                }
                                                            }
                                                        });
                                                    });
                                                }
                                            }
                                        });
                                    });
                        
                                    // After all the data is collected, add PT components first, then Income Tax
                                    frappe.after_ajax(function () {
                                        // Add Professional Tax components first
                                        $.each(ptComponents, function (i, component) {
                                            let child = frm.add_child('custom_emplloyee_tax_deduction');
                                            child.date = component.date;
                                            child.salary_slip_id = component.salary_slip_id;
                                            child.salary_component = component.salary_component;
                                            child.amount = component.amount;
                                            child.payment_days = component.payment_days;
                                        });
                        
                                        // Then add Income Tax components
                                        $.each(incomeTaxComponents, function (i, component) {
                                            let child = frm.add_child('custom_emplloyee_tax_deduction');
                                            child.date = component.date;
                                            child.salary_slip_id = component.salary_slip_id;
                                            child.salary_component = component.salary_component;
                                            child.amount = component.amount;
                                            child.payment_days = component.payment_days;
                                        });
                        
                                        frm.refresh_field('custom_emplloyee_tax_deduction');
                                    });
                        
                                }
                            }
                        });


                        



                        
                                            
                                        



                        

















                    } 
                    
                    else {
                        frappe.msgprint({
                            title: __('Payroll Period Missing'),
                            message: 'No payroll period found in the latest Salary Structure Assignment.',
                            indicator: 'red'
                        });
                    }
                } 
                
                else {
                    frappe.msgprint({
                        title: __('No Assignments Found'),
                        message: 'No Salary Structure Assignment found for the selected employee.',
                        indicator: 'red'
                    });
                }
            }
        });

        var deduction_array = ["Notice Pay Recovery", "PF Recovery","ESIC Recovery","Waive off Recovery"]; // Array with deduction components

        // Iterate through the deduction_array
        for (let i = 0; i < deduction_array.length; i++) {
            let child = frm.add_child('receivables');
            child.component = deduction_array[i]; // Access the component name from the array
            child.amount = 0; // Set the amount as 0

            frm.refresh_field('receivables');
             
            
        }
        deduction_array=[]



    } else {
        frappe.msgprint(__('Please select an Employee.'));
    }
}
