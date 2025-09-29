// Copyright (c) 2025, Hybrowlabs technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Resettlement", {
	refresh(frm) {

	},


    employee: function(frm) {
        if (frm.doc.employee) {

            // ✅ Get Employee document first
            frappe.db.get_doc("Employee", frm.doc.employee)
                .then(employee => {
                    if (!employee.relieving_date) {
                        frappe.msgprint("Relieving date is mandatory");
                    }

                    frappe.call({
                        method: "frappe.client.get_list",
                        args: {
                            doctype: "Salary Slip",
                            filters: {
                                employee: frm.doc.employee,
                                salary_withholding: ["!=", ""]
                            },
                            fields: ["name", "posting_date", "custom_net_pay_amount"]
                        },
                        callback: function(res) {
                            if (res && res.message && res.message.length > 0) {

                                // Clear existing child table rows
                                frm.clear_table("salary_slip_detail");

                                $.each(res.message, function(i, v) {
                                    let child = frm.add_child("salary_slip_detail");
                                    child.salary_slip = v.name;
                                    child.date = v.posting_date;
                                    child.amount = v.custom_net_pay_amount;
                                });

                                frm.refresh_field("salary_slip_detail");

                            } else {
                                console.log("No salary slips found with withholding for this employee.");
                            }
                        }
                    });

                    frappe.call({
                        method: "cn_indian_payroll.cn_indian_payroll.overrides.full_and_final_settlement.get_accrued_components",
                        args: {
                            employee: frm.doc.employee,
                            company: frm.doc.company,
                            relieving_date: frm.doc.relieving_date,
                        },
                        callback: function (response) {
                            frm.clear_table('payable_earnings');
                            frm.clear_table('receivable_deductions');


                            if (response.message) {
                                const reimbursementList = response.message.reimbursement_list || [];
                                const final_arrayList = response.message.final_array || [];


                                console.log(final_arrayList,"8888888888888")

                                final_arrayList.forEach(row => {
                                    let child = frm.add_child('payable_earnings');

                                    child.salary_component = row.component;
                                    child.amount = row.balance_amount;
                                });
                                frm.refresh_field("payable_earnings");





                            }
                        }
                        })

                });


        }
    }





});
