frappe.ui.form.on('Full and Final Statement', {
    refresh(frm) {
        // Logic for refreshing the form if needed
    },

    employee(frm) {

        if(frm.doc.employee)
        {



            get_accrued_components(frm)




        }

        else{
            frm.clear_table("custom_emplloyee_tax_deduction");
            frm.refresh_field("custom_emplloyee_tax_deduction");

        }

    }
});



frappe.ui.form.on('Leave Encashment Child', {
    encashment_days: function (frm, cdt, cdn) {
        var d = locals[cdt][cdn];

        console.log(d,"1111")




        if (d.encashment_days)
        {
            console.log(d.encashment_days)
            frappe.call({
                method: "cn_indian_payroll.cn_indian_payroll.overrides.full_and_final_settlement.get_encashment_amount",
                args: {
                    employee: frm.doc.employee,
                    company: frm.doc.company,
                },
                callback: function (response) {
                    if (response.message) {

                        console.log(response.message)

                        var per_day_amount = response.message;
                        d.amount = ( per_day_amount / 30 ) * d.encashment_days
                        d.basic_amount=per_day_amount

                    }
                }
            });

        }





    },



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

            // frm.clear_table('custom_calculated_amount');
            // frm.clear_table('custom_calculated_amount');

            frm.clear_table('custom_emplloyee_tax_deduction');
            frm.clear_table('custom_emplloyee_tax_deduction');





            if (response.message) {
                const bonusList = response.message.bonus_list || [];
                const reimbursementList = response.message.reimbursement_list || [];
                const final_arrayList = response.message.final_array || [];

                // const leave_encashment_list=response.message.leave_encashment||[]

                const tax_list=response.message.tax_list||[]




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


                    const child = frm.add_child('custom_accrued_component_summary');
                    child.salary_component = row.component;
                    child.total_accrued_amount = row.accrued_amount;
                    child.total_settled_amount = row.claimed_amount;
                    child.balance_amount = row.balance_amount;
                });



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
            // frm.refresh_field('custom_calculated_amount');
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
