final_array = [];

frappe.ui.form.on('Salary Appraisal Calculation', {
    refresh(frm) {},

    employee: function(frm) {
        if (frm.doc.employee) {
            get_old_new_structure(frm, function() {
            get_salary_slip(frm);
            get_reimbursements(frm);
            get_bonus(frm);
            });
        } 
        else 
        {
            frm.clear_table("old_structure_child");
            frm.refresh_field("old_structure_child");
            frm.clear_table("salary_arrear_components");
            frm.refresh_field("salary_arrear_components");

            frm.set_value("old_salary_structure", undefined);
            frm.set_value("new_salary_structure", undefined);

            frm.clear_table("reimbursement_components");
            frm.refresh_field("reimbursement_components");
            frm.clear_table("bonus_components");
            frm.refresh_field("bonus_components");
        }
    }
});

function get_old_new_structure(frm, callback) {
    let old_component_dict = [];
    let new_component_dict = [];

    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Salary Structure Assignment",
            filters: { employee: frm.doc.employee, 'docstatus': 1 },
            fields: ["*"],
            limit: 2,
            order_by: "from_date desc"
        },
        callback: function(res) {
            if (res.message && res.message.length > 1) {
                frm.set_value("old_salary_structure", res.message[1].name);
                frm.set_value("new_salary_structure", res.message[0].name);

                let old_salary_structure = res.message[1].salary_structure;
                let old_from_date = res.message[1].from_date;

                let new_salary_structure = res.message[0].salary_structure;
                let new_from_date = res.message[0].from_date;

                fetchOldSalaryComponents(frm, old_salary_structure, old_from_date, old_component_dict, () => {
                    fetchNewSalaryComponents(frm, new_salary_structure, new_from_date, new_component_dict, () => {
                        let combinedDict = {};
                        old_component_dict.forEach(item => {
                            combinedDict[item.component] = {
                                component: item.component,
                                old_amount: item.value,
                                new_amount: 0
                            };
                        });

                        new_component_dict.forEach(item => {
                            if (combinedDict[item.component]) {
                                combinedDict[item.component].new_amount = item.value;
                            } else {
                                combinedDict[item.component] = {
                                    component: item.component,
                                    old_amount: 0,
                                    new_amount: item.value
                                };
                            }
                        });

                        final_array = Object.values(combinedDict);
                        // console.log(final_array,"final_arrayfinal_array")

                        frm.clear_table("old_structure_child");
                        final_array.forEach(item => {
                            let child = frm.add_child("old_structure_child");
                            frappe.model.set_value(child.doctype, child.name, "salary_component", item.component);
                            frappe.model.set_value(child.doctype, child.name, "old_amount", item.old_amount);
                            frappe.model.set_value(child.doctype, child.name, "new_amount", item.new_amount);
                        });

                        frm.refresh_field("old_structure_child");
                        if (typeof callback === 'function') callback();
                    });
                });
            }
            else{
                msgprint("Please Create New Salary Structure Assignment")
            }
        }
    });
}

function fetchOldSalaryComponents(frm, salary_structure, from_date, old_component_dict, callback) {
    frappe.call({
        method: "hrms.payroll.doctype.salary_structure.salary_structure.make_salary_slip",
        args: {
            source_name: salary_structure,
            employee: frm.doc.employee,
            print_format: 'Salary Slip Standard for CTC',
            docstatus: 1,
            posting_date: from_date
        },
        callback: function(response) {
            if (response.message) {
                let ctc_old_array = [
                    ...(response.message.earnings || []).map(v => ({
                        salary_component: v.salary_component,
                        amount: v.amount
                    })),
                    ...(response.message.deductions || []).map(v => ({
                        salary_component: v.salary_component,
                        amount: v.amount
                    }))
                ];
                fetchSalaryComponentDetails(frm, ctc_old_array, old_component_dict, callback);
            }
        }
    });
}

function fetchNewSalaryComponents(frm, salary_structure, from_date, new_component_dict, callback) {
    frappe.call({
        method: "hrms.payroll.doctype.salary_structure.salary_structure.make_salary_slip",
        args: {
            source_name: salary_structure,
            employee: frm.doc.employee,
            print_format: 'Salary Slip Standard for CTC',
            docstatus: 1,
            posting_date: from_date
        },
        callback: function(response) {
            if (response.message) {
                let ctc_new_array = [
                    ...(response.message.earnings || []).map(v => ({
                        salary_component: v.salary_component,
                        amount: v.amount
                    })),
                    ...(response.message.deductions || []).map(v => ({
                        salary_component: v.salary_component,
                        amount: v.amount
                    }))
                ];
                fetchSalaryComponentDetails(frm, ctc_new_array, new_component_dict, callback);
            }
        }
    });
}

function fetchSalaryComponentDetails(frm, ctc_array, component_dict, callback) {
    let fetchDetails = (index) => {

        
        if (index < ctc_array.length) {
            let item = ctc_array[index];
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Salary Component",
                    name: item.salary_component
                },
                callback: function(res) {
                    if (res.message && res.message.custom_is_part_of_appraisal == 1) {
                        component_dict.push({
                            component: res.message.name,
                            value: item.amount
                        });
                    }
                    fetchDetails(index + 1);

                   
                }
            });
        } 
        else 
        {
            callback();
        }
    };
    fetchDetails(0);
}





function get_salary_slip(frm) {
    if (frm.doc.posting_date) {
        let final_mapped_array = [];

        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Salary Structure Assignment",
                filters: { employee: frm.doc.employee, 'docstatus': 1 },
                fields: ["*"],
                limit: 2,
                order_by: "from_date desc"
            },
            callback: function(res) {
                if (res.message && res.message.length > 1) {
                    let date = res.message[1].from_date;
                    if (date) {
                        frappe.call({
                            method: "frappe.client.get_list",
                            args: {
                                doctype: "Salary Slip",
                                filters: {
                                    employee: frm.doc.employee,
                                    start_date: ['between', [date, frm.doc.posting_date]]
                                },
                                fields: ["*"]
                            },
                            callback: function(res) {
                                

                                res.message.forEach(v => {
                                    frappe.call({
                                        method: "frappe.client.get",
                                        args: {
                                            doctype: "Salary Slip",
                                            name: v.name
                                        },
                                        callback: function(kes) {
                                            kes.message.earnings.forEach(k => {
                                                let matchedComponent = final_array.find(item => item.component === k.salary_component);

                                                if (matchedComponent) {
                                                    final_mapped_array.push({
                                                        "salary_component": matchedComponent.component,
                                                        "salary_slip": v.name,
                                                        "month": v.custom_month,
                                                        "old_amount": k.amount,
                                                        "new_amount": matchedComponent.new_amount,
                                                        "working_days":v.total_working_days,
                                                        "lop":v.leave_without_pay
                                                    });
                                                }
                                            });

                                            kes.message.deductions.forEach(m => {
                                                let matchedComponent = final_array.find(item => item.component === m.salary_component);
                                                if (matchedComponent) {
                                                    final_mapped_array.push({
                                                        "salary_component": matchedComponent.component,
                                                        "salary_slip": v.name,
                                                        "month": v.custom_month,
                                                        "old_amount": m.amount,
                                                        "new_amount": matchedComponent.new_amount,
                                                        "working_days":v.total_working_days,
                                                        "lop":v.leave_without_pay
                                                    });
                                                }
                                            });

                                            frm.clear_table("salary_arrear_components");
                                            frm.refresh_field("salary_arrear_components");
                                            
                                            final_mapped_array.forEach(b => {
                                                
                                                let child = frm.add_child("salary_arrear_components");
                                                let expected_amount = (b.new_amount / b.working_days) * (b.working_days - b.lop);
                                                frappe.model.set_value(child.doctype, child.name, "salary_slip_id", b.salary_slip);
                                                frappe.model.set_value(child.doctype, child.name, "salary_component", b.salary_component);
                                                frappe.model.set_value(child.doctype, child.name, "month", b.month);
                                                frappe.model.set_value(child.doctype, child.name, "old_amount", b.old_amount);
                                                frappe.model.set_value(child.doctype, child.name, "expected_amount", expected_amount);
                                                frappe.model.set_value(child.doctype, child.name, "working_days", b.working_days);
                                                frappe.model.set_value(child.doctype, child.name, "lop_days", b.lop);
                                                frappe.model.set_value(child.doctype, child.name, "difference", expected_amount - b.old_amount);

                                            });

                                            frm.refresh_field("salary_arrear_components");
                                        }
                                    });
                                });
                            }
                        });
                    }
                }
            }
        });
    }
}









function get_bonus(frm) {
    if (frm.doc.posting_date) {
        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Salary Structure Assignment",
                filters: { employee: frm.doc.employee, docstatus: 1 },
                fields: ["*"],
                limit: 2,
                order_by: "from_date desc"
            },
            callback: function (res_assignment) {
                if (res_assignment.message && res_assignment.message.length > 1) {
                    let date = res_assignment.message[1].from_date;
                    let latest_bonus_amount;

                    if (date) {
                        frappe.call({
                            method: "hrms.payroll.doctype.salary_structure.salary_structure.make_salary_slip",
                            args: {
                                source_name: res_assignment.message[0].salary_structure,
                                employee: frm.doc.employee,
                                print_format: 'Salary Slip Standard for CTC',
                                docstatus: 1,
                                posting_date: res_assignment.message[0].from_date
                            },
                            callback: function (structure_response) {
                                if (structure_response.message) {

                                    let bonusPromises = structure_response.message.earnings.map(bonus => {
                                        return new Promise((resolve, reject) => {
                                            frappe.call({
                                                method: "frappe.client.get",
                                                args: {
                                                    doctype: "Salary Component",
                                                    filters: { "name": bonus.salary_component }
                                                },
                                                callback: function (mes) {
                                                    if (mes.message.custom_is_accrual == 1) {
                                                        latest_bonus_amount = bonus.amount;
                                                        console.log(mes.message.name)
                                                        
                                                    }
                                                    
                                                    resolve();
                                                }
                                            });
                                        });
                                    });

                                    Promise.all(bonusPromises).then(() => {
                                        frappe.call({
                                            method: "frappe.client.get_list",
                                            args: {
                                                doctype: "Employee Bonus Accrual",
                                                filters: {
                                                    employee: frm.doc.employee,
                                                    accrual_date: ['between', [date, frm.doc.posting_date]]
                                                },
                                                fields: ["*"]
                                            },
                                            callback: function (res_bonus) {
                                                
                                                frm.clear_table("bonus_components");
                                                frm.refresh_field("bonus_components");

                                                $.each(res_bonus.message, function (i, d) {
                                                    if (d.salary_slip) {
                                                        frappe.call({
                                                            method: "frappe.client.get",
                                                            args: {
                                                                doctype: "Salary Slip",
                                                                name: d.salary_slip
                                                            },
                                                            callback: function (slip_response) {
                                                                if (slip_response.message) {

                                                                    
                                                                    let child = frm.add_child("bonus_components");
                                                                    let expected_bonus_amount = (latest_bonus_amount / slip_response.message.total_working_days) * (slip_response.message.total_working_days - slip_response.message.leave_without_pay);
                                                                    

                                                                    frappe.model.set_value(child.doctype, child.name, "salary_slip_id", d.salary_slip);
                                                                    frappe.model.set_value(child.doctype, child.name, "salary_component", d.salary_component);
                                                                    frappe.model.set_value(child.doctype, child.name, "month", slip_response.message.custom_month);
                                                                    frappe.model.set_value(child.doctype, child.name, "old_amount", d.amount);
                                                                    frappe.model.set_value(child.doctype, child.name, "working_days", slip_response.message.total_working_days);
                                                                    frappe.model.set_value(child.doctype, child.name, "lop_days", slip_response.message.leave_without_pay);
                                                                    frappe.model.set_value(child.doctype, child.name, "expected_amount", expected_bonus_amount);
                                                                    frappe.model.set_value(child.doctype, child.name, "difference", expected_bonus_amount - d.amount);
                                                                 }
                                                                frm.refresh_field("bonus_components");
                                                            }
                                                        });
                                                    }

                                                    else{
                                                        // need to work
                                                    }


                                                });
                                            }
                                        });
                                    });
                                }
                            }
                        });
                    }
                }
            }
        });
    }
}


// function get_reimbursements(frm) {
//     if (frm.doc.posting_date) {
//         let latest_structure_reimbursement_component = [];

//         frappe.call({
//             method: "frappe.client.get_list",
//             args: {
//                 doctype: "Salary Structure Assignment",
//                 filters: { employee: frm.doc.employee, docstatus: 1 },
//                 fields: ["*"],
//                 limit: 2,
//                 order_by: "from_date desc"
//             },
//             callback: function(res) {
//                 if (res.message && res.message.length > 1) {
//                     let date = res.message[1].from_date;

//                     if (date) {
//                         frappe.call({
//                             method: "frappe.client.get",
//                             args: {
//                                 doctype: "Salary Structure Assignment",
//                                 name: res.message[0].name
//                             },
//                             callback: function(mes) {
//                                 if (mes.message) {
                                    

//                                     $.each(mes.message.custom_employee_reimbursements, function(i, reimbursement) {
//                                         latest_structure_reimbursement_component.push({
//                                             "component": reimbursement.reimbursements,
//                                             "amount": reimbursement.monthly_total_amount
//                                         });
//                                     });

//                                     console.log(latest_structure_reimbursement_component,"latest_structure_reimbursement_componentlatest_structure_reimbursement_component")

//                                     frappe.call({
//                                         method: "frappe.client.get_list",
//                                         args: {
//                                             doctype: "Employee Benefit Accrual",
//                                             filters: {
//                                                 employee: frm.doc.employee,
//                                                 benefit_accrual_date: ['between', [date, frm.doc.posting_date]]
//                                             },
//                                             fields: ["*"]
//                                         },
//                                         callback: function(res) {
//                                                 frm.clear_table("reimbursement_components");
//                                                 frm.refresh_field("reimbursement_components");
//                                             res.message.forEach(v => {
//                                                 latest_structure_reimbursement_component.forEach(component => {
//                                                     if (v.salary_component == component.component) {
//                                                         frappe.call({
//                                                             method: "frappe.client.get",
//                                                             args: {
//                                                                 doctype: "Salary Slip",
//                                                                 name: v.salary_slip
//                                                             },
//                                                             callback: function(slip_response) {
//                                                                 if (slip_response.message) {
//                                                                     let child = frm.add_child("reimbursement_components");
//                                                                     frappe.model.set_value(child.doctype, child.name, "salary_slip_id", v.salary_slip);
//                                                                     frappe.model.set_value(child.doctype, child.name, "salary_component", v.salary_component);
//                                                                     frappe.model.set_value(child.doctype, child.name, "old_amount", v.amount);
//                                                                     frappe.model.set_value(child.doctype, child.name, "expected_amount", component.amount);
//                                                                     frappe.model.set_value(child.doctype, child.name, "difference", component.amount - v.amount);
//                                                                     frappe.model.set_value(child.doctype, child.name, "month", slip_response.message.custom_month);
//                                                                     frappe.model.set_value(child.doctype, child.name, "working_days", slip_response.message.total_working_days);
//                                                                     frappe.model.set_value(child.doctype, child.name, "lop_days", slip_response.message.leave_without_pay);
//                                                                 }
//                                                                 frm.refresh_field("reimbursement_components");
//                                                             }
//                                                         });
//                                                     }
//                                                 });
//                                             });
                                           
//                                         }
//                                     });
//                                 }
//                             }
//                         });
//                     }
//                 }
//             }
//         });
//     }
// }



function get_reimbursements(frm) {
    if (frm.doc.posting_date) {
        let latest_structure_reimbursement_component = [];

        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Salary Structure Assignment",
                filters: { employee: frm.doc.employee, docstatus: 1 },
                fields: ["*"],
                limit: 2,
                order_by: "from_date desc"
            },
            callback: function(res) {
                if (res.message && res.message.length > 1) {
                    let date = res.message[1].from_date;

                    if (date) {
                        frappe.call({
                            method: "frappe.client.get",
                            args: {
                                doctype: "Salary Structure Assignment",
                                name: res.message[0].name
                            },
                            callback: function(mes) {
                                if (mes.message) {
                                    $.each(mes.message.custom_employee_reimbursements, function(i, reimbursement) {
                                        latest_structure_reimbursement_component.push({
                                            "component": reimbursement.reimbursements,
                                            "amount": reimbursement.monthly_total_amount
                                        });
                                    });

                                    frappe.call({
                                        method: "frappe.client.get_list",
                                        args: {
                                            doctype: "Employee Benefit Accrual",
                                            filters: {
                                                employee: frm.doc.employee,
                                                benefit_accrual_date: ['between', [date, frm.doc.posting_date]]
                                            },
                                            fields: ["*"]
                                        },
                                        callback: function(res) {
                                            frm.clear_table("reimbursement_components");
                                            frm.refresh_field("reimbursement_components");

                                            res.message.forEach(v => {
                                                let component = latest_structure_reimbursement_component.find(comp => comp.component === v.salary_component);
                                                
                                                frappe.call({
                                                    method: "frappe.client.get",
                                                    args: {
                                                        doctype: "Salary Slip",
                                                        name: v.salary_slip
                                                    },
                                                    callback: function(slip_response) {
                                                        if (slip_response.message) {
                                                            let expected_amount = component ? component.amount : 0;
                                                            let totalamount = (expected_amount / slip_response.message.total_working_days) * (slip_response.message.total_working_days - slip_response.message.leave_without_pay);


                                                            let difference = totalamount - v.amount;

                                                            let child = frm.add_child("reimbursement_components");
                                                            frappe.model.set_value(child.doctype, child.name, "salary_slip_id", v.salary_slip);
                                                            frappe.model.set_value(child.doctype, child.name, "salary_component", v.salary_component);
                                                            frappe.model.set_value(child.doctype, child.name, "old_amount", v.amount);
                                                            frappe.model.set_value(child.doctype, child.name, "expected_amount", totalamount);
                                                            frappe.model.set_value(child.doctype, child.name, "difference", difference);
                                                            frappe.model.set_value(child.doctype, child.name, "month", slip_response.message.custom_month);
                                                            frappe.model.set_value(child.doctype, child.name, "working_days", slip_response.message.total_working_days);
                                                            frappe.model.set_value(child.doctype, child.name, "lop_days", slip_response.message.leave_without_pay);

                                                            frm.refresh_field("reimbursement_components");
                                                        }
                                                    }
                                                });
                                            });
                                        }
                                    });
                                }
                            }
                        });
                    }
                }
            }
        });
    }
}





