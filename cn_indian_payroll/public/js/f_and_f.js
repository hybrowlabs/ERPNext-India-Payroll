frappe.ui.form.on('Full and Final Statement', {
    refresh(frm) {
    },

    employee(frm) {

        if(frm.doc.employee)
        {

            get_accrued_components(frm)


        }

        else{
            frm.clear_table("custom_emplloyee_tax_deduction");
            frm.refresh_field("custom_emplloyee_tax_deduction");

            frm.clear_table('custom_accrued_benefit');
            frm.clear_table('custom_accrued_component_summary');

            frm.clear_table('custom_calculated_amount');
            frm.clear_table('custom_calculated_amount');

            frm.clear_table('custom_emplloyee_tax_deduction');
            frm.clear_table('custom_emplloyee_tax_deduction');

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

        if (frm.doc.custom_calculated_amount && frm.doc.custom_calculated_amount.length > 0) {
            $.each(frm.doc.custom_calculated_amount, function(i, row) {
                total += row.amount || 0;
            });
        }

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

                        frm.doc.payables.forEach((v) => {
                            if (v.custom_reference_component === target_component) {
                                frappe.model.set_value(v.doctype, v.name, "amount", total);
                            }
                        });

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

        if (frm.doc.custom_calculated_amount && frm.doc.custom_calculated_amount.length > 0) {
            $.each(frm.doc.custom_calculated_amount, function(i, row) {
                total += row.amount || 0;
            });
        }

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
                        frm.doc.payables.forEach((v) => {
                            if (v.custom_reference_component === target_component) {
                                frappe.model.set_value(v.doctype, v.name, "amount", total);
                            }
                        });

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

                                frm.doc.payables.forEach((v, i) => {
                                    if (v.custom_reference_component === target_component) {
                                        frappe.model.set_value(v.doctype, v.name, "amount", totalAmount);

                                    }
                                });

                                frm.refresh_field("payables");
                            }
                        }
                    });
                }

                bonusList.forEach(row => {
                    let child = frm.add_child('custom_accrued_benefit');
                    child.date = row.date;
                    child.payment_days = row.payment_days;
                    child.salary_slip_id = row.salary_slip_id;
                    child.salary_component = row.salary_component;
                    child.accrued_amount = row.accrued_amount;
                });

                reimbursementList.forEach(row => {
                    let child = frm.add_child('custom_accrued_benefit');
                    child.date = row.date;
                    child.payment_days = row.payment_days;
                    child.salary_slip_id = row.salary_slip_id;
                    child.salary_component = row.salary_component;
                    child.accrued_amount = row.accrued_amount;
                    child.claimed_amount = row.claimed_amount;
                });

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
