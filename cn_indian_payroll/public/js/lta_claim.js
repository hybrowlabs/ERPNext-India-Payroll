

frappe.ui.form.on('LTA Claim', {

    employee: function(frm) {
        if (frm.doc.employee) {

            find_tax_regime(frm)
            get_max_amount(frm)


        }
    },

    amount:function(frm)
    {
        if(frm.doc.amount>frm.doc.max_eligible_amount)
        {
            frm.set_value("amount",undefined)
            msgprint("you cant enter amount greater than eligible amount")
        }
    },


    claim_date: function(frm) {
        get_max_amount(frm)
        // if (frm.doc.claim_date && frm.doc.claim_date <frappe.datetime.now_date()) {
        //     frm.set_value("claim_date", null);
        //     frappe.msgprint(__("You can't select a past date."));
        // }
    }





});




function show_max_lta_amount(frm) {
    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Salary Component",
            filters: { "component_type": "LTA Reimbursement" },
            fields: ["*"],
        },
        callback: function(res) {
            if (res.message && res.message.length > 0) {
                var reimbursement_amount = [];

                frappe.call({
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "Salary Structure Assignment",
                        filters: { employee: frm.doc.employee, docstatus: 1 },
                        fields: ["*"],
                        order_by: "from_date desc",
                        limit: 1
                    },
                    callback: function(response) {
                        if (response.message && response.message.length > 0) {
                            frappe.call({
                                method: "frappe.client.get",
                                args: {
                                    doctype: "Salary Structure Assignment",
                                    name: response.message[0].name
                                },
                                callback: function(employee_data) {
                                    if (employee_data.message) {
                                        $.each(employee_data.message.custom_employee_reimbursements, function(i, v) {
                                            if (v.reimbursements === res.message[0].name) {
                                                reimbursement_amount.push(v.monthly_total_amount);
                                            }

                                        });


                                        if (reimbursement_amount.length > 0) {
                                            frappe.call({
                                                method: "frappe.client.get_list",
                                                args: {
                                                    doctype: "Payroll Period",
                                                    filters: {
                                                        "company": frm.doc.company,
                                                        "start_date": ["<=", frm.doc.posting_date],
                                                        "end_date": [">=", frm.doc.posting_date]
                                                    },
                                                    fields: ["start_date", "end_date"],
                                                    limit: 1
                                                },
                                                callback: function(payroll_data) {
                                                    if (payroll_data.message && payroll_data.message.length > 0) {

                                                        frappe.call({
                                                            method: "frappe.client.get_list",
                                                            args: {
                                                                doctype: "LTA Claim",
                                                                filters: {
                                                                    "company": frm.doc.company,
                                                                    "claim_date": ["between", payroll_data.message[0].start_date, payroll_data.message[0].end_date],
                                                                    "employee": frm.doc.employee,

                                                                },
                                                                fields: ["*"],
                                                            },
                                                            callback: function(lta_data) {
                                                                var total_amount=[]
                                                                if (lta_data.message && lta_data.message.length > 0) {
                                                                    console.log(lta_data.message);
                                                                    $.each(lta_data.message,function(i,k)
                                                                        {
                                                                            total_amount.push(k.amount)

                                                                        })
                                                                    const sum1 = total_amount.reduce((accumulator, currentValue) => accumulator + currentValue, 0);



                                                                    var accrual_data_array = [];

                                                                    frappe.call({
                                                                        method: "frappe.client.get_list",
                                                                        args: {
                                                                            doctype: "Employee Benefit Accrual",
                                                                            filters: {
                                                                                "employee": frm.doc.employee,
                                                                                "docstatus": 1,
                                                                                "salary_component": res.message[0].name,
                                                                                "payroll_period":payroll_data.message[0].name
                                                                            },
                                                                            fields: ["*"]
                                                                        },
                                                                        callback: function(accrual_data) {
                                                                            if (accrual_data.message && accrual_data.message.length > 0) {

                                                                                // console.log(accrual_data.message)
                                                                                $.each(accrual_data.message, function(i, g) {
                                                                                    accrual_data_array.push(g.amount);
                                                                                });

                                                                                const sum = accrual_data_array.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

                                                                                let startDate = new Date(response.message[0].from_date);
                                                                                let endDate = new Date(payroll_data.message[0].end_date);

                                                                                // Calculate year and month difference
                                                                                let yearDifference = endDate.getFullYear() - startDate.getFullYear();
                                                                                let monthDifference = endDate.getMonth() - startDate.getMonth();

                                                                                // Total months difference
                                                                                let totalMonths = yearDifference * 12 + monthDifference;

                                                                                // console.log("Difference in months:", totalMonths-1);

                                                                                var future_value = (totalMonths)

                                                                                var future_amount=future_value*reimbursement_amount[0]

                                                                                var max_eligible_amount=(future_amount+sum)-sum1
                                                                                frm.set_value("max_eligible_amount",max_eligible_amount)








                                                                            }
                                                                        }
                                                                    })




                                                                }
                                                                else
                                                                {

                                                                    var accrual_data_array = [];



                                                                    frappe.call({
                                                                        method: "frappe.client.get_list",
                                                                        args: {
                                                                            doctype: "Employee Benefit Accrual",
                                                                            filters: {
                                                                                "employee": frm.doc.employee,
                                                                                "docstatus": 1,
                                                                                "salary_component": res.message[0].name,
                                                                                "payroll_period":payroll_data.message[0].name
                                                                            },
                                                                            fields: ["*"]
                                                                        },
                                                                        callback: function(accrual_data) {
                                                                            if (accrual_data.message && accrual_data.message.length > 0) {

                                                                                console.log(accrual_data.message)
                                                                                $.each(accrual_data.message, function(i, g) {
                                                                                    accrual_data_array.push(g.amount);
                                                                                });

                                                                                const sum = accrual_data_array.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

                                                                                let startDate = new Date(response.message[0].from_date);
                                                                                let endDate = new Date(payroll_data.message[0].end_date);

                                                                                // Calculate year and month difference
                                                                                let yearDifference = endDate.getFullYear() - startDate.getFullYear();
                                                                                let monthDifference = endDate.getMonth() - startDate.getMonth();

                                                                                // Total months difference
                                                                                let totalMonths = yearDifference * 12 + monthDifference;

                                                                                console.log("Difference in months:", totalMonths-1);

                                                                                var future_value = (totalMonths)
                                                                                var future_amount=future_value*reimbursement_amount[0]
                                                                                frm.set_value("max_eligible_amount",future_amount+sum)

                                                                                // console.log(future_amount, "Future Value of LTA");

                                                                            }
                                                                            else
                                                                            {
                                                                                console.log("No accruals found for this salary component.");
                                                                            }
                                                                        }
                                                                    });
                                                                }
                                                            }
                                                        });
                                                    } else {
                                                        frappe.msgprint("This date is not included in the latest payroll period. Please create a payroll period.");
                                                    }
                                                }
                                            });
                                        }
                                    }
                                }
                            });
                        }
                    }
                });
            } else {
                frappe.msgprint("There is no salary component with component type LTA Reimbursement.");
            }
        }
    });
}


function find_tax_regime(frm)
{
    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Salary Structure Assignment",
            filters: { employee: frm.doc.employee, docstatus: 1,from_date: ["<=", frm.doc.claim_date] },
            fields: ["*"],
            order_by: "from_date desc",
            limit: 1
        },
        callback: function(response) {
            if (response.message && response.message.length > 0) {

                frm.set_value("income_tax_regime",response.message[0].custom_tax_regime)

            }
        }
    })

}


function get_max_amount(frm) {
    if (frm.doc.employee) {
        frappe.call({
            method: "cn_indian_payroll.cn_indian_payroll.overrides.lta_claim.get_max_amount",
            args: {
                doc: frm.doc
            },
            callback: function (r) {
                if (r.message) {
                    frm.set_value("max_eligible_amount", r.message.max_amount);
                    frm.set_value("payroll_period", r.message.payroll_period);
                }
            }
        });
    }
}
