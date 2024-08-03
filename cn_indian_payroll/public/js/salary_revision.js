final_array = [];

frappe.ui.form.on('Salary Appraisal Calculation', {
    refresh(frm) {},

    employee: function(frm) {
        if (frm.doc.employee) {
            get_old_new_structure(frm, function() {
            get_salary_slip(frm);
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
                    if (res.message && res.message.custom_is_part_of_ctc == 1) {
                        component_dict.push({
                            component: res.message.name,
                            value: item.amount
                        });
                    }
                    fetchDetails(index + 1);
                }
            });
        } else {
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
                                frm.clear_table("salary_arrear_components");
                                frm.refresh_field("salary_arrear_components");

                                res.message.forEach(v => {
                                    frappe.call({
                                        method: "frappe.client.get",
                                        args: {
                                            doctype: "Salary Slip",
                                            name: v.name
                                        },
                                        callback: function(kes) {
                                            kes.message.earnings.forEach(k => {
                                                console.log
                                                let matchedComponent = final_array.find(item => item.salary_component === k.salary_component);
                                                if (matchedComponent) {

                                                    console.log(matchedComponent.salary_component)

                                                    final_mapped_array.push({
                                                        "salary_component": matchedComponent.salary_component,
                                                        "salary_slip": k.name,
                                                        "month": v.custom_month,
                                                        "old_amount": k.amount,
                                                        "new_amount": matchedComponent.new_amount
                                                    });
                                                }
                                            });

                                            // console.log(final_mapped_array,"---------")

                                            // kes.message.deductions.forEach(m => {
                                            //     let matchedComponent = final_array.find(item => item.salary_component === m.salary_component);
                                            //     if (matchedComponent) {
                                            //         final_mapped_array.push({
                                            //             "salary_component": matchedComponent.salary_component,
                                            //             "salary_slip": m.name,
                                            //             "month": v.custom_month,
                                            //             "old_amount": m.amount,
                                            //             "new_amount": matchedComponent.new_amount
                                            //         });
                                            //     }
                                            // });

                                            // console.log(final_mapped_array)

                                            // final_mapped_array.forEach(b => {
                                            //     let child = frm.add_child("salary_arrear_components");
                                            //     frappe.model.set_value(child.doctype, child.name, "salary_slip_id", b.salary_slip);
                                            //     frappe.model.set_value(child.doctype, child.name, "salary_component", b.salary_component);
                                            //     frappe.model.set_value(child.doctype, child.name, "month", b.month);
                                            //     frappe.model.set_value(child.doctype, child.name, "old_amount", b.old_amount);
                                            //     frappe.model.set_value(child.doctype, child.name, "expected_amount", b.new_amount);
                                            //     frappe.model.set_value(child.doctype, child.name, "difference", b.new_amount - b.old_amount);
                                            // });

                                            // frm.refresh_field("salary_arrear_components");
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
