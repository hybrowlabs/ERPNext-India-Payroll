frappe.ui.form.on('Employee Promotion', {
	refresh(frm) {


        if (!frm.is_new() && frm.doc.custom_status === "Payroll Configured") {
            frm.add_custom_button("Calculate Arrears", function() {
                if (frm.doc.custom_additional_salary_date) {

                    // Show initial progress
                    frappe.show_progress('Loading...', 0, 100, 'Please wait');

                    // Simulate progress over time
                    let progress = 0;
                    let interval = setInterval(function() {
                        progress += 10; // Increment progress

                        if (progress < 100) {
                            frappe.show_progress('Loading...', progress, 100, 'Please wait');
                        } else {
                            // Final progress state
                            // frappe.show_progress('Completed...', 100, 100, 'Please wait');
                            // clearInterval(interval);

                            // Hide progress bar after a short delay to ensure it shows completed state
                            setTimeout(function() {
                                frappe.hide_progress();
                            }, 500); // Adjust delay as necessary
                        }
                    }, 500); // 500ms interval, adjust as needed

                    // Call your function to get old and new structure
                    get_old_new_structure(frm);

                } else {
                    frappe.msgprint("Please Select Additional Salary Date");
                }
            });
        }
        
        
        
        

        frm.change_custom_button_type('Calculate Arrears', null, 'primary');
		
	},

})


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
                let old_salary_structure = res.message[1].salary_structure;
                let old_from_date = res.message[1].from_date;
                let old_ssa_id = res.message[1].name;

                let new_salary_structure = res.message[0].salary_structure;
                let new_from_date = res.message[0].from_date;
                let new_ssa_id = res.message[0].name;

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

                        let final_array = Object.values(combinedDict);

                        if (final_array.length > 0) {
                            fetchSalarySlipsAndInsertAppraisal(frm, final_array, old_salary_structure, old_from_date, old_ssa_id, new_salary_structure, new_from_date, new_ssa_id);
                        } else {
                            frappe.msgprint("No salary components found.");
                        }
                    });
                });
            } else {
                frappe.msgprint("Please Create New Salary Structure Assignment");
            }
        }
    });







}




async function fetchSalarySlipsAndInsertAppraisal(frm, final_array, old_salary_structure, old_from_date, old_ssa_id, new_salary_structure, new_from_date, new_ssa_id) {
    let final_mapped_array = [];
    let latest_structure_reimbursement_component = [];
    let reimbursement_array = [];
    let bonus_array = [];
    let latest_bonus_amount = 0;

    try {
        // Fetch the latest Salary Structure Assignment
        let res = await frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Salary Structure Assignment",
                filters: { employee: frm.doc.employee, docstatus: 1 },
                fields: ["*"],
                limit: 1,
                order_by: "from_date desc"
            }
        });

        if (res.message && res.message.length > 0) {
            let date = res.message[0].from_date;

            if (date) {
                // Fetch Salary Slips from the given date
                let salary_slips = await frappe.call({
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "Salary Slip",
                        filters: {
                            employee: frm.doc.employee,
                            end_date: ['>=', date]
                        },
                        fields: ["*"]
                    }
                });

                if (salary_slips.message) {
                    let salary_slip_calls = salary_slips.message.map(v => {
                        return new Promise((resolve) => {
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
                                                "working_days": v.total_working_days,
                                                "lop": v.leave_without_pay
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
                                                "working_days": v.total_working_days,
                                                "lop": v.leave_without_pay
                                            });
                                        }
                                    });

                                    resolve();
                                }
                            });
                        });
                    });

                    await Promise.all(salary_slip_calls);
                }

                // Fetch latest structure reimbursement components
                let latest_structure = await frappe.call({
                    method: "frappe.client.get",
                    args: {
                        doctype: "Salary Structure Assignment",
                        name: res.message[0].name
                    }
                });

                if (latest_structure.message) {
                    latest_structure.message.custom_employee_reimbursements.forEach(function(reimbursement) {
                        latest_structure_reimbursement_component.push({
                            "component": reimbursement.reimbursements,
                            "amount": reimbursement.monthly_total_amount
                        });
                    });

                    // Fetch Employee Benefit Accruals
                    let accruals = await frappe.call({
                        method: "frappe.client.get_list",
                        args: {
                            doctype: "Employee Benefit Accrual",
                            filters: {
                                employee: frm.doc.employee,
                                benefit_accrual_date: ['>=', date]
                            },
                            fields: ["*"]
                        }
                    });

                    if (accruals.message) {
                        let accrual_calls = accruals.message.map(v => {
                            return new Promise((resolve) => {
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

                                            reimbursement_array.push({
                                                "salary_slip_id": v.salary_slip,
                                                "salary_component": v.salary_component,
                                                "old_amount": v.amount,
                                                "expected_amount": totalamount,
                                                "difference": difference,
                                                "month": slip_response.message.custom_month,
                                                "working_days": slip_response.message.total_working_days,
                                                "lop_days": slip_response.message.leave_without_pay
                                            });
                                        }
                                        resolve();
                                    }
                                });
                            });
                        });

                        await Promise.all(accrual_calls);
                    }

                    // Fetch latest bonus components
                    let structure_response = await frappe.call({
                        method: "hrms.payroll.doctype.salary_structure.salary_structure.make_salary_slip",
                        args: {
                            source_name: latest_structure.message.salary_structure,
                            employee: frm.doc.employee,
                            print_format: 'Salary Slip Standard for CTC',
                            docstatus: 1,
                            posting_date: date
                        }
                    });

                    if (structure_response.message) {
                        let bonusPromises = structure_response.message.earnings.map(bonus => {
                            return new Promise((resolve, reject) => {
                                frappe.call({
                                    method: "frappe.client.get",
                                    args: {
                                        doctype: "Salary Component",
                                        filters: { "name": bonus.salary_component }
                                    },
                                    callback: function(mes) {
                                        if (mes.message.custom_is_accrual == 1) {
                                            latest_bonus_amount = bonus.amount;
                                        }
                                        resolve();
                                    }
                                });
                            });
                        });

                        await Promise.all(bonusPromises);

                        // Fetch Employee Bonus Accruals
                        let res_bonus = await frappe.call({
                            method: "frappe.client.get_list",
                            args: {
                                doctype: "Employee Bonus Accrual",
                                filters: {
                                    employee: frm.doc.employee,
                                    accrual_date: ['>=', date]
                                },
                                fields: ["*"]
                            }
                        });

                        if (res_bonus.message) {
                            for (let d of res_bonus.message) {
                                if (d.salary_slip) {
                                    let slip_response = await frappe.call({
                                        method: "frappe.client.get",
                                        args: {
                                            doctype: "Salary Slip",
                                            name: d.salary_slip
                                        }
                                    });

                                    if (slip_response.message) {
                                        let expected_bonus_amount = (latest_bonus_amount / slip_response.message.total_working_days) * (slip_response.message.total_working_days - slip_response.message.leave_without_pay);
                                        bonus_array.push({
                                            "salary_slip_id": d.salary_slip,
                                            "salary_component": d.salary_component,
                                            "month": slip_response.message.custom_month,
                                            "old_amount": d.amount,
                                            "working_days": slip_response.message.total_working_days,
                                            "lop_days": slip_response.message.leave_without_pay,
                                            "expected_amount": expected_bonus_amount,
                                            "difference": expected_bonus_amount - d.amount
                                        });
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        // Insert Salary Appraisal Calculation document
      
        
        await frappe.db.insert({
            "doctype": "Salary Appraisal Calculation",
            "employee": frm.doc.employee,
            "employee_name": frm.doc.employee_name,
            "company": frm.doc.company,
            "posting_date": frm.doc.custom_additional_salary_date,
            "employee_promotion_id": frm.doc.name,
            "old_salary_structure": old_salary_structure,
            "new_salary_structure": new_salary_structure,
            "old_from_date": old_from_date,
            "new_from_date": new_from_date,
            "old_salary_structure_assignment_id": old_ssa_id,
            "new_salary_structure_assignment_id": new_ssa_id,
            "old_structure_child": final_array.map(row => ({
                "salary_component": row.component,
                "old_amount": row.old_amount,
                "new_amount": row.new_amount
            })),
            "salary_arrear_components": final_mapped_array.map(row => ({
                "salary_slip_id": row.salary_slip,
                "salary_component": row.salary_component,
                "month": row.month,
                "working_days": row.working_days,
                "lop_days": row.lop,
                "old_amount": row.old_amount,
                "expected_amount": row.new_amount,
                "difference": row.new_amount - row.old_amount
            })),
            "reimbursement_components": reimbursement_array.map(row => ({
                "salary_slip_id": row.salary_slip_id,
                "salary_component": row.salary_component,
                "month": row.month,
                "working_days": row.working_days,
                "lop_days": row.lop_days,
                "old_amount": row.old_amount,
                "expected_amount": row.expected_amount,
                "difference": row.difference
            })),
            "bonus_components": bonus_array.map(row => ({
                "salary_slip_id": row.salary_slip_id,
                "salary_component": row.salary_component,
                "month": row.month,
                "working_days": row.working_days,
                "lop_days": row.lop_days,
                "old_amount": row.old_amount,
                "expected_amount": row.expected_amount,
                "difference": row.difference
            })),
            // Uncomment this if you want to submit the document immediately
            "docstatus": 1,

            

        });
        


        frm.set_value("custom_status","Arrears Calculated")
        frm.save()
        // 

        


    } catch (error) {
        console.error("Error in fetching and inserting appraisal data:", error);
    }


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