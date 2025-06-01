frappe.ui.form.on('Full and Final Statement', {
    refresh(frm) {
        // Logic for refreshing the form if needed
    },

    employee(frm) {

        if(frm.doc.employee)
        {

            // earning_component(frm).then(() => {
            //     // Ensure payables table is updated BEFORE calling this
            //     get_leave_encashment(frm);
            // });
            // // earning_component(frm)
            // deduction_component(frm)
            // get_outstanding_benefits(frm)
            // get_tax(frm)
            // // get_leave_encashment(frm)

            get_accrued_components(frm)




        }

        else{
            frm.clear_table("custom_emplloyee_tax_deduction");
            frm.refresh_field("custom_emplloyee_tax_deduction");

        }

    }
});



frappe.ui.form.on('Leave Encashment Child', {
    basic_amount: function (frm, cdt, cdn) {
        var d = locals[cdt][cdn];

        if (d.basic_amount) {
            if (d.encashment_days && d.leave_type) {
                frappe.model.set_value(cdt, cdn, "amount", (d.basic_amount / 30) * d.encashment_days);
            }
        }


        let total = 0;

        // Sum amounts in custom_calculated_amount
        if (frm.doc.custom_calculated_amount && frm.doc.custom_calculated_amount.length > 0) {
            $.each(frm.doc.custom_calculated_amount, function(i, row) {
                total += row.amount || 0;
            });
        }

        // Sum amounts in custom_locked_leave
        if (frm.doc.custom_locked_leave && frm.doc.custom_locked_leave.length > 0) {
            $.each(frm.doc.custom_locked_leave, function(i, row) {
                total += row.amount || 0;
            });
        }


        if (total > 0) {
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Company",
                    name: frm.doc.company
                },
                callback: function(res) {
                    if (res && res.message && res.message.custom_leave_encashment_component) {
                        let target_component = res.message.custom_leave_encashment_component;

                        console.log("METCHING")

                        // Loop through payables and update matching component's amount
                        frm.doc.payables.forEach((v) => {
                            if (v.custom_reference_component === target_component) {
                                frappe.model.set_value(v.doctype, v.name, "amount", total);
                            }
                        });

                        // Refresh the payables field in the form UI
                        frm.refresh_field("payables");
                    }
                }
            });
        }
    },

    encashment_days: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];

        if (d.encashment_days) {
            if (d.basic_amount && d.leave_type) {
                frappe.model.set_value(cdt, cdn, "amount", (d.basic_amount / 30) * d.encashment_days);
            }
        }

        let total = 0;

        // Sum amounts in custom_calculated_amount
        if (frm.doc.custom_calculated_amount && frm.doc.custom_calculated_amount.length > 0) {
            $.each(frm.doc.custom_calculated_amount, function(i, row) {
                total += row.amount || 0;
            });
        }

        // Sum amounts in custom_locked_leave
        if (frm.doc.custom_locked_leave && frm.doc.custom_locked_leave.length > 0) {
            $.each(frm.doc.custom_locked_leave, function(i, row) {
                total += row.amount || 0;
            });
        }


        if (total > 0) {
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Company",
                    name: frm.doc.company
                },
                callback: function(res) {
                    if (res && res.message && res.message.custom_leave_encashment_component) {
                        let target_component = res.message.custom_leave_encashment_component;

                        console.log("METCHING")

                        // Loop through payables and update matching component's amount
                        frm.doc.payables.forEach((v) => {
                            if (v.custom_reference_component === target_component) {
                                frappe.model.set_value(v.doctype, v.name, "amount", total);
                            }
                        });

                        // Refresh the payables field in the form UI
                        frm.refresh_field("payables");
                    }
                }
            });
        }
    }

});



function get_accrued_components(frm) {
    if (!frm.doc.employee) return;

    frappe.call({
        method: "cn_indian_payroll.cn_indian_payroll.overrides.full_and_final_settlement.get_accrued_components",
        args: {
            employee: frm.doc.employee,
            company: frm.doc.company,
            relieving_date: frm.doc.relieving_date,
        },
        callback: function (response) {
            frm.clear_table('custom_accrued_benefit');
            frm.clear_table('custom_accrued_component_summary');

            frm.clear_table('custom_calculated_amount');
            frm.clear_table('custom_calculated_amount');

            frm.clear_table('custom_emplloyee_tax_deduction');
            frm.clear_table('custom_emplloyee_tax_deduction');





            if (response.message) {
                const bonusList = response.message.bonus_list || [];
                const reimbursementList = response.message.reimbursement_list || [];
                const final_arrayList = response.message.final_array || [];

                const leave_encashment_list=response.message.leave_encashment||[]

                const tax_list=response.message.tax_list||[]



                let totalAmount = leave_encashment_list.reduce((sum, row) => {
                    return sum + (row.amount || 0);
                }, 0);

                if (totalAmount > 0) {
                    frappe.call({
                        method: "frappe.client.get",
                        args: {
                            doctype: "Company",
                            name: frm.doc.company
                        },
                        callback: function(res) {
                            if (res && res.message && res.message.custom_leave_encashment_component) {
                                let target_component = res.message.custom_leave_encashment_component;

                                // Loop through payables and update matching component's amount
                                frm.doc.payables.forEach((v, i) => {
                                    if (v.custom_reference_component === target_component) {
                                        // Update the amount using frappe.model.set_value for proper change detection
                                        frappe.model.set_value(v.doctype, v.name, "amount", totalAmount);
                                        // If you want to break the loop after first match, you can do it like this:
                                        // return false;
                                    }
                                });

                                // Refresh the payables field in the form UI
                                frm.refresh_field("payables");
                            }
                        }
                    });
                }


                // Add bonus entries
                bonusList.forEach(row => {
                    let child = frm.add_child('custom_accrued_benefit');
                    child.date = row.date;
                    child.payment_days = row.payment_days;
                    child.salary_slip_id = row.salary_slip_id;
                    child.salary_component = row.salary_component;
                    child.accrued_amount = row.accrued_amount;
                });

                // Add reimbursement entries
                reimbursementList.forEach(row => {
                    let child = frm.add_child('custom_accrued_benefit');
                    child.date = row.date;
                    child.payment_days = row.payment_days;
                    child.salary_slip_id = row.salary_slip_id;
                    child.salary_component = row.salary_component;
                    child.accrued_amount = row.accrued_amount;
                    child.claimed_amount = row.claimed_amount;
                });

                // Process final array and update payables
                final_arrayList.forEach(row => {
                    if (row.balance_amount > 0) {
                        frappe.call({
                            method: "frappe.client.get",
                            args: {
                                doctype: "Salary Component",
                                name: row.component
                            },
                            callback: function (res) {
                                if (res.message) {
                                    const component = res.message;

                                    if (
                                        component.custom_is_accrual === 1 &&
                                        component.custom_paidout_component
                                    ) {

                                        console.log(component.custom_paidout_component)
                                        frm.doc.payables.forEach(v => {
                                            if (v.custom_reference_component === component.custom_paidout_component) {
                                                v.amount = row.balance_amount;
                                            }
                                        });
                                        frm.refresh_field('payables');
                                    }
                                }
                            }
                        });

                        frm.doc.payables.forEach(v => {
                            if (v.custom_reference_component === row.component) {
                                v.amount = row.balance_amount;
                            }
                        });
                        frm.refresh_field('payables');
                    }

                    // if (row.balance_amount <= 0) {
                    //     frm.doc.receivables.forEach(v => {
                    //         if (v.custom_reference_component === row.component) {
                    //             v.amount = row.balance_amount;
                    //         }
                    //     });
                    //     frm.refresh_field('receivables');

                    // }

                    // Always add component summary
                    const child = frm.add_child('custom_accrued_component_summary');
                    child.salary_component = row.component;
                    child.total_accrued_amount = row.accrued_amount;
                    child.total_settled_amount = row.claimed_amount;
                    child.balance_amount = row.balance_amount;
                });

                leave_encashment_list.forEach(row=>{

                    let child = frm.add_child('custom_calculated_amount');
                    child.leave_type = row.leave_type;
                    child.encashment_days = row.encashment_days;
                    child.basic_amount = row.basic_amount;
                    child.amount = row.amount;

                })

                tax_list.forEach(row=>{

                    let child = frm.add_child('custom_emplloyee_tax_deduction');
                    child.date = row.date;
                    child.salary_slip_id = row.id;
                    child.payment_days = row.payment_days;
                    child.salary_component = row.salary_component;
                    child.amount = row.amount;

                })


                frm.refresh_field('custom_accrued_component_summary');

            }

            frm.refresh_field('custom_accrued_benefit');
            frm.refresh_field('custom_accrued_component_summary');
            frm.refresh_field('custom_calculated_amount');
            frm.refresh_field('custom_emplloyee_tax_deduction');






        }
    });
}










function get_outstanding_benefits(frm) {
    if (frm.doc.employee) {

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




                        frm.clear_table("custom_accrued_benefit");
                        frm.refresh_field("custom_accrued_benefit");

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

                                            // console.log(v.salary_slip,"11111")
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

                                    // console.log(componentGroups,"componentGroupscomponentGroups")





                                }


                                else

                                {


                                }
                            }
                        });



                        //BONUS COMPONENT

                        var bonus_sum = [];
                        frappe.call({
                            method: "frappe.client.get_list",
                            args: {
                                doctype: "Employee Bonus Accrual",
                                filters: {
                                    employee: frm.doc.employee,
                                    docstatus: ["in", [0, 1]],
                                    is_paid: 0
                                },
                                fields: ["*"],
                                limit_page_length: 0
                            },
                            callback: function (bonus_response) {
                                if (bonus_response.message) {
                                    $.each(bonus_response.message, function (i, k) {
                                        bonus_sum.push(k.amount);

                                        let child = frm.add_child('custom_accrued_benefit');
                                        child.date = k.accrual_date; // Replace 'benefit_accrual_date' if required
                                        child.salary_slip_id = k.salary_slip;
                                        child.salary_component = k.salary_component;
                                        child.accrued_amount = k.amount; // Replace 'amount' if required

                                        if (k.salary_slip) {
                                            frappe.call({
                                                method: "frappe.client.get",
                                                args: {
                                                    doctype: "Salary Slip",
                                                    name: k.salary_slip
                                                },
                                                callback: function (slip_response_data) {
                                                    if (slip_response_data.message) {
                                                        child.payment_days = slip_response_data.message.payment_days;
                                                    }
                                                    frm.refresh_field('custom_accrued_benefit');
                                                }
                                            });
                                        } else {
                                            frm.refresh_field('custom_accrued_benefit');
                                        }
                                    });

                                    // Calculate total bonus sum
                                    let sum = bonus_sum.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

                                    // Check if component exists
                                    let exists = frm.doc.payables.some((row) => row.component === "Bonus PaidOut");

                                    if (!exists) {
                                        let payables_child = frm.add_child('payables');
                                        payables_child.component = "Bonus PaidOut";
                                        payables_child.amount = sum;
                                        frm.refresh_field('payables');
                                    } else {
                                        frm.doc.payables.forEach((row) => {
                                            if (row.component === "Bonus PaidOut") {
                                                row.amount = sum;
                                            }
                                        });
                                        frm.refresh_field('payables');
                                    }
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





    } else {
        frappe.msgprint(__('Please select an Employee.'));
    }
}


function get_tax(frm)
{

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

                                frm.clear_table("custom_emplloyee_tax_deduction");
                                frm.refresh_field("custom_emplloyee_tax_deduction");

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
            }
        }
    })

}

// function deduction_component(frm) {
//     var deduction_array = ["Notice Pay Recovery", "PF Recovery", "ESIC Recovery", "Waive off Recovery"]; // Array with deduction components

//     // Iterate through the deduction_array
//     for (let i = 0; i < deduction_array.length; i++) {
//         let child = frm.add_child('receivables');
//         child.component = deduction_array[i]; // Access the component name from the array
//         child.amount = 0; // Set the amount as 0
//     }

//     // Refresh the field once after the loop
//     frm.refresh_field('receivables');

//     // Clear the array if necessary
//     deduction_array = [];
// }

function deduction_component(frm) {
    var deduction_array = ["Notice Pay Recovery", "PF Recovery", "ESIC Recovery", "Waive off Recovery"]; // Array with deduction components

    frm.clear_table('receivables');

    deduction_array.forEach((component) => {
        // Check if the component already exists in the child table
        let exists = frm.doc.receivables.some((row) => row.component === component);

        // Add the component if it doesn't already exist
        if (!exists) {
            let child = frm.add_child('receivables');
            child.component = component;
            child.amount = 0; // Set the amount as 0
        }
    });

    // Refresh the field after processing all components
    frm.refresh_field('receivables');
}


// function earning_component(frm)
// {
//     frappe.call({
//         method: "frappe.client.get_list",
//         args: {
//             doctype: "Salary Structure Assignment",
//             filters: {
//                 employee: frm.doc.employee,
//                 docstatus: 1
//             },
//             fields: ["*"],
//             limit: 1,
//             order_by: "from_date desc"
//         },
//         callback: function (res) {
//             if (res.message && res.message.length > 0) {
//                 const payrollPeriod = res.message[0].custom_payroll_period;

//                 if (payrollPeriod) {
//                     frappe.call({
//                         method: "frappe.client.get_list",
//                         args: {
//                             doctype: "Employee Benefit Accrual",
//                             filters: {
//                                 employee: frm.doc.employee,
//                                 docstatus: ["in", [0, 1]],
//                                 payroll_period: payrollPeriod
//                             },
//                             fields: ["*"],
//                             limit_page_length: 0
//                         },
//                         callback: function (response) {
//                             if (response.message && response.message.length > 0) {
//                                 // Create a map to group components
//                                 let componentGroups = {};

//                                 // Group components by their salary_component
//                                 $.each(response.message, function (i, v) {
//                                     if (!componentGroups[v.salary_component]) {
//                                         componentGroups[v.salary_component] = [];
//                                     }
//                                     componentGroups[v.salary_component].push(v);
//                                 });

//                                 // Iterate through the grouped components in the desired order
//                                 Object.keys(componentGroups).forEach(function (component) {
//                                     let group = componentGroups[component];
//                                     let componentSum = 0; // To sum the components
//                                     let totalSettlement = 0; // To accumulate total settlement for subtraction

//                                     // Calculate the sums for the component
//                                     group.forEach((v) => {
//                                         componentSum += v.amount; // Add the accrued amount
//                                         totalSettlement += v.total_settlement; // Add the total settlement
//                                     });

//                                     // Calculate the final value to be added to payables (sum - total settlement)
//                                     let finalAmount = componentSum - totalSettlement;

//                                     // Check if the component already exists in payables
//                                     let exists = frm.doc.payables.some((row) => row.component === component);

//                                     if (!exists) {
//                                         // Add the result to the child table (payables)
//                                         let child = frm.add_child('payables');
//                                         child.component = component; // Set the component name
//                                         child.amount = finalAmount; // Set the final calculated amount
//                                     }
//                                 });

//                                 // Refresh the payables field after adding all components
//                                 frm.refresh_field('payables');

//                             }
//                         }
//                     });
//                 }
//             }
//         }
//     });

// }

// function get_leave_encashment(frm) {
//     frappe.call({
//         method: "frappe.client.get_list",
//         args: {
//             doctype: "Leave Encashment",
//             filters: {
//                 employee: frm.doc.employee,
//                 docstatus: 1
//             },
//             fields: ["leave_type", "encashment_days", "custom_basic_amount", "encashment_amount"],
//         },
//         callback: function (r) {
//             if (r.message && r.message.length > 0) {
//                 // Clear the child table before adding new rows
//                 frm.clear_table('custom_calculated_amount');

//                 r.message.forEach(row => {
//                     let child = frm.add_child('custom_calculated_amount');
//                     child.leave_type = row.leave_type;
//                     child.encashment_days = row.encashment_days;
//                     child.basic_amount = row.custom_basic_amount;
//                     child.amount = row.encashment_amount;
//                 });

//                 // Refresh the child table field to show the new rows
//                 frm.refresh_field('custom_calculated_amount');
//             } else {
//                 frappe.msgprint(__('No Leave Encashment records found for this employee.'));
//             }
//         }
//     });
// }


// function earning_component(frm) {
//     frappe.call({
//         method: "frappe.client.get_list",
//         args: {
//             doctype: "Salary Structure Assignment",
//             filters: {
//                 employee: frm.doc.employee,
//                 docstatus: 1
//             },
//             fields: ["*"],
//             limit: 1,
//             order_by: "from_date desc"
//         },
//         callback: function (res) {
//             if (res.message && res.message.length > 0) {
//                 const payrollPeriod = res.message[0].custom_payroll_period;

//                 if (payrollPeriod) {
//                     frappe.call({
//                         method: "frappe.client.get_list",
//                         args: {
//                             doctype: "Employee Benefit Accrual",
//                             filters: {
//                                 employee: frm.doc.employee,
//                                 docstatus: ["in", [0, 1]],
//                                 payroll_period: payrollPeriod
//                             },
//                             fields: ["*"],
//                             limit_page_length: 0
//                         },
//                         callback: function (response) {
//                             if (response.message && response.message.length > 0) {
//                                 // ✅ Clear the payables child table before inserting new rows
//                                 frm.clear_table('payables');

//                                 // Create a map to group components
//                                 let componentGroups = {};

//                                 // Group components by their salary_component
//                                 $.each(response.message, function (i, v) {
//                                     if (!componentGroups[v.salary_component]) {
//                                         componentGroups[v.salary_component] = [];
//                                     }
//                                     componentGroups[v.salary_component].push(v);
//                                 });

//                                 // Iterate through the grouped components
//                                 Object.keys(componentGroups).forEach(function (component) {
//                                     let group = componentGroups[component];
//                                     let componentSum = 0;
//                                     let totalSettlement = 0;

//                                     group.forEach((v) => {
//                                         componentSum += v.amount;
//                                         totalSettlement += v.total_settlement;
//                                     });

//                                     let finalAmount = componentSum - totalSettlement;

//                                     let child = frm.add_child('payables');
//                                     child.component = component;
//                                     child.amount = finalAmount;
//                                 });

//                                 // Refresh the table
//                                 frm.refresh_field('payables');
//                             }
//                         }
//                     });
//                 }
//             }
//         }
//     });
// }
function get_leave_encashment(frm) {
    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Leave Encashment",
            filters: {
                employee: frm.doc.employee,
                docstatus: 1
            },
            fields: ["leave_type", "encashment_days", "custom_basic_amount", "encashment_amount"],
        },
        callback: function (r) {
            if (r.message && r.message.length > 0) {
                // Clear custom_calculated_amount table
                frm.clear_table('custom_calculated_amount');

                let total_encashment = 0;

                r.message.forEach(row => {
                    let child = frm.add_child('custom_calculated_amount');
                    child.leave_type = row.leave_type;
                    child.encashment_days = row.encashment_days;
                    child.basic_amount = row.custom_basic_amount;
                    child.amount = row.encashment_amount;

                    total_encashment += row.encashment_amount || 0;
                });

                frm.refresh_field('custom_calculated_amount');

                // ❌ Remove existing Leave Encashment from payables the right way
                const existing_rows = frm.doc.payables.filter(row => row.component === "Leave Encashment");
                existing_rows.forEach(row => {
                    frm.get_field('payables').grid.grid_rows_by_docname[row.name].remove();
                });

                // ➕ Add new Leave Encashment row
                if (total_encashment > 0) {
                    let payable = frm.add_child('payables');
                    payable.component = "Leave Encashment";
                    payable.amount = total_encashment;
                }

                frm.refresh_field('payables');
            } else {
                frappe.msgprint(__('No Leave Encashment records found for this employee.'));
            }
        }
    });
}


function earning_component(frm) {
    return new Promise((resolve) => {
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
                                    frm.clear_table('payables');

                                    let componentGroups = {};

                                    $.each(response.message, function (i, v) {
                                        if (!componentGroups[v.salary_component]) {
                                            componentGroups[v.salary_component] = [];
                                        }
                                        componentGroups[v.salary_component].push(v);
                                    });

                                    Object.keys(componentGroups).forEach(function (component) {
                                        let group = componentGroups[component];
                                        let componentSum = 0;
                                        let totalSettlement = 0;

                                        group.forEach((v) => {
                                            componentSum += v.amount;
                                            totalSettlement += v.total_settlement;
                                        });

                                        let finalAmount = componentSum - totalSettlement;

                                        let child = frm.add_child('payables');
                                        child.component = component;
                                        child.amount = finalAmount;
                                    });

                                    frm.refresh_field('payables');
                                }
                                resolve(); // ✅ Resolve after everything is done
                            }
                        });
                    } else {
                        resolve();
                    }
                } else {
                    resolve();
                }
            }
        });
    });
}
