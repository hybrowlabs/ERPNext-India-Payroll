frappe.ui.form.on('Employee Advance', {
    refresh(frm) {



        if(frm.doc.custom_type=="Salary Advance")

            {


        frm.set_query("custom_deduction_component", function() {
            return {
                "filters": {
                    "type": "Deduction"
                }
            };
        });

        if (!frm.is_new() && frm.doc.docstatus!=2) {
            frappe.call({
                method: 'cn_indian_payroll.cn_indian_payroll.overrides.employee_advance.get_advance_dashboard_erp',
                args: {
                    id: frm.doc.name,
                    employee: frm.doc.employee,
                    company: frm.doc.company,
                    posting_date: frm.doc.posting_date
                },
                callback: function (r) {
                    if (r.message && r.message.length > 0) {
                        const data = r.message[0];   // First advance record
                        const repayments = data.repayments || [];

                    const dashboard_html = `
                        <div class="row text-center mb-4">

                            <!-- Advance Type -->
                            <div class="col-md-3">
                                <div class="p-3" style="border-radius:15px;
                                                        box-shadow:0 4px 12px rgba(0,0,0,0.1);
                                                        background:linear-gradient(135deg,#f9f9f9,#f1f1f1);
                                                        border:1px solid #ddd;">
                                    <div style="font-size:28px; margin-bottom:5px; color:#007bff;">📑</div>
                                    <h6 class="text-muted">Advance Type</h6>
                                    <h5><b>${data.advance_type}</b></h5>
                                </div>
                            </div>

                            <!-- Total Advance Amount -->
                            <div class="col-md-3">
                                <div class="p-3" style="border-radius:15px;
                                                        box-shadow:0 4px 12px rgba(0,0,0,0.1);
                                                        background:linear-gradient(135deg,#f9f9f9,#f1f1f1);
                                                        border:1px solid #ddd;">
                                    <div style="font-size:28px; margin-bottom:5px; color:#28a745;">💰</div>
                                    <h6 class="text-muted">Total Advance</h6>
                                    <h5><b>₹${(data.total_advance_amount || 0).toLocaleString()}</b></h5>
                                </div>
                            </div>

                            <!-- Total Paid -->
                            <div class="col-md-3">
                                <div class="p-3" style="border-radius:15px;
                                                        box-shadow:0 4px 12px rgba(0,0,0,0.1);
                                                        background:linear-gradient(135deg,#f9f9f9,#f1f1f1);
                                                        border:1px solid #ddd;">
                                    <div style="font-size:28px; margin-bottom:5px; color:#17a2b8;">✅</div>
                                    <h6 class="text-muted">Total Paid</h6>
                                    <h5><b>₹${(data.total_paid_amount || 0).toLocaleString()}</b></h5>
                                </div>
                            </div>

                            <!-- Balance -->
                            <div class="col-md-3">
                                <div class="p-3" style="border-radius:15px;
                                                        box-shadow:0 4px 12px rgba(0,0,0,0.1);
                                                        background:linear-gradient(135deg,#f9f9f9,#f1f1f1);
                                                        border:1px solid #ddd;">
                                    <div style="font-size:28px; margin-bottom:5px; color:#dc3545;">📉</div>
                                    <h6 class="text-muted">Balance</h6>
                                    <h5><b>₹${(data.balance_amount || 0).toLocaleString()}</b></h5>
                                </div>
                            </div>

                        </div>
                    `;



                        const has_payroll_manager_role = frappe.user_roles.includes("Payroll Manager");




                        let table_html = `
                            <table id="repayments-table"
                                   style="width:100%; border-collapse:collapse; text-align:center; border-radius:10px; overflow:hidden; box-shadow:0 4px 12px rgba(0,0,0,0.1);">
                                <thead style="background-color:grey; color:white;">
                                    <tr>
                                        <th style="padding:10px;">Sl. No.</th>
                                        <th style="padding:10px;">Payment Date</th>
                                        <th style="padding:10px;">Payment Amount</th>
                                        <th style="padding:10px;">Balance</th>
                                        <th style="padding:10px;">Additional Salary ID</th>
                                        <th style="padding:10px;">Deducted</th>

                                        <th style="padding:10px; color:${(frm.doc.docstatus === 1 && frm.doc.custom_final_status === "Approved") };">
                                            ${(frm.doc.docstatus === 1 && frm.doc.custom_final_status === "Approved") ? 'Hold Deduction' : ''}
                                        </th>

                                        <th style="padding:10px; color:${(frm.doc.docstatus === 1 && frm.doc.custom_final_status === "Approved")};">
                                            ${(frm.doc.docstatus === 1 && frm.doc.custom_final_status === "Approved") ? 'Edit Amount' : ''}
                                        </th>

                                    </tr>
                                </thead>
                                <tbody style="background-color:#fefefe;">
                        `;



                        repayments.forEach(rp => {
                            const is_deducted = rp.deducted === 1 || rp.deducted === true;
                            table_html += `
                                <tr style="border-bottom:1px solid #ddd;">
                                    <td style="padding:10px;">${rp.idx}</td>
                                    <td style="padding:10px;" class="payment-date">${frappe.format(rp.payment_date, {fieldtype:"Date"})}</td>
                                    <td style="padding:10px;">₹${(rp.payment_amount || 0).toLocaleString()}</td>
                                    <td style="padding:10px;">₹${(rp.balance_amount || 0).toLocaleString()}</td>
                                    <td style="padding:10px;" class="additional-salary-id">${rp.additional_salary_id || "-"}</td>
                                   <td style="padding:10px;">
                                        <input type="checkbox" class="deducted-checkbox" ${is_deducted ? "checked" : ""} style="pointer-events:none;"/>
                                    </td>


                                  <td style="padding:10px;">
                                        ${
                                            (has_payroll_manager_role && frm.doc.custom_final_status === "Approved" && frm.doc.docstatus === 1 && !is_deducted && rp.additional_salary_id)
                                            ? `<button class="btn btn-xs btn-primary hold-btn">Hold</button>`
                                            : ``
                                        }
                                    </td>

                                    <td style="padding:10px;">
                                        ${
                                            (has_payroll_manager_role && frm.doc.custom_final_status === "Approved" && frm.doc.docstatus === 1 && !is_deducted && rp.additional_salary_id)
                                            ? `<button class="btn btn-xs btn-primary edit-btn">Edit</button>`
                                            : ``
                                        }
                                    </td>


                                </tr>
                            `;
                        });

                        let settlement_html = "";

                        if (frm.doc.custom_settlement_date) {

                            settlement_html = `
                                <table id="settlement-table"
                                    style="width:100%; border-collapse:collapse; text-align:center; border-radius:10px;
                                           overflow:hidden; box-shadow:0 4px 12px rgba(0,0,0,0.1); margin-top:20px;">
                                    <thead style="background-color:grey; color:white;">
                                        <tr>
                                            <th style="padding:10px;">Settlement Date</th>
                                            <th style="padding:10px;">Settlement Amount</th>
                                            <th style="padding:10px;">Remarks</th>
                                        </tr>
                                    </thead>
                                    <tbody style="background-color:#fefefe;">
                                        <tr>
                                            <td style="padding:8px;">${frappe.format(frm.doc.custom_settlement_date, {fieldtype:"Date"})}</td>
                                            <td style="padding:8px;">₹${(frm.doc.custom_total_paid_amount || 0).toLocaleString()}</td>
                                            <td style="padding:8px;">${frm.doc.custom_remarks || "-"}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            `;
                        }






                        table_html += `</tbody></table>`;


                        const full_html = dashboard_html + table_html+settlement_html;


                        frm.fields_dict.custom_repayment_dashboard.$wrapper.html(full_html);

                            frm.fields_dict.custom_repayment_dashboard.$wrapper
                                .find(".hold-btn")
                                .on("click", function () {
                                    if (!frappe.user.has_role("Payroll Manager")) {
                                        frappe.msgprint("You do not have permission to hold installments.");
                                        return;
                                    }

                                    let row = $(this).closest("tr");
                                    let date = row.find(".payment-date").text().trim();
                                    let additional_salary_id = row.find(".additional-salary-id").text().trim();
                                    let deducted = row.find(".deducted-checkbox").prop("checked");



                                    if (deducted) {
                                        frappe.msgprint("This installment is already deducted. Editing disabled.");
                                        return;
                                    }

                                    let parts = date.split("-");
                                    let formattedDate = `${parts[2]}-${parts[1]}-${parts[0]}`;

                                    let total_installments = $("#repayments-table tbody tr").length;


                                    let row_index = parseInt(row.find("td:first").text());
                                    let remaining_installments = total_installments - row_index;

                                    let d = new frappe.ui.Dialog({
                                        title: "Hold Installment",
                                        size: "large",
                                        fields: [
                                            { fieldtype: "Section Break" },
                                            {
                                                label: "Hold Option",
                                                fieldname: "hold_option",
                                                fieldtype: "Select",
                                                options: [
                                                    "Recover Pending in Next Month",
                                                    "Distribute Across Future Months",
                                                    "Extend Repayment Period"
                                                ],
                                                default: "Distribute Across Future Months"
                                            },
                                            { fieldtype: "Column Break" },
                                            {
                                                label: "Number of Months to Hold",
                                                fieldname: "number_of_months",
                                                fieldtype: "Int",
                                                default: 1,
                                                reqd: 1
                                            },
                                            { fieldtype: "Section Break" },
                                            {
                                                label: "Holding Date",
                                                fieldname: "holding_date",
                                                fieldtype: "Date",
                                                default: formattedDate,
                                                read_only: 1
                                            },
                                            {
                                                label: "Additional Salary ID",
                                                fieldname: "additional_salary_id",
                                                fieldtype: "Data",
                                                default: additional_salary_id,
                                                read_only: 1
                                            }
                                        ],
                                        primary_action_label: "Submit",
                                        primary_action(values) {

                                            console.log(values)



                                            if (values.number_of_months < 1) {
                                                frappe.msgprint("Number of months to hold must be at least 1.");
                                                return;
                                            }

                                            if (values.number_of_months > total_installments) {
                                                frappe.msgprint("Number of months to hold cannot exceed total installments.");
                                                return;
                                            }

                                            if (values.number_of_months > remaining_installments) {
                                                frappe.msgprint(
                                                    `Only ${remaining_installments} installment(s) are pending. You cannot hold ${values.number_of_months} months.`
                                                );
                                                return;
                                            }

                                            let row_amount = row.find("td:eq(2)").text().replace(/[₹,]/g, "").trim() || 0;
                                            let row_id = additional_salary_id;

                                            frappe.call({
                                                method: "cn_indian_payroll.cn_indian_payroll.overrides.employee_advance.hold_installments",
                                                args: {
                                                    repayments: repayments,        // full table data
                                                    idx: row_index,                // current row index
                                                    hold_months: values.number_of_months,
                                                    hold_option: values.hold_option,
                                                    installment_id: row_id,        // selected row’s Additional Salary ID
                                                    installment_amount: row_amount ,// selected row’s amount (cleaned)
                                                    employee:frm.doc.employee,
                                                    component:frm.doc.custom_deduction_component,
                                                    doc_id:frm.doc.name,
                                                    company:frm.doc.company
                                                },
                                                callback: function (r) {
                                                    if (r.message === "success") {
                                                        frappe.msgprint("Installment updated successfully.");
                                                        d.hide();
                                                        frm.reload_doc();
                                                    } else {
                                                        frappe.msgprint("Error updating installment. Please try again.");
                                                    }
                                                }
                                            });
                                        }
                                    });
                                    d.show();
                                });



        // --- EDIT BUTTON ---
        frm.fields_dict.custom_repayment_dashboard.$wrapper
        .find(".edit-btn")
        .on("click", function () {
            if (!frappe.user.has_role("Payroll Manager")) {
                frappe.msgprint("You do not have permission to edit installments.");
                return;
            }

            let row = $(this).closest("tr");
            let date = row.find(".payment-date").text().trim();
            let additional_salary_id = row.find(".additional-salary-id").text().trim();
            let row_amount = row.find("td:eq(2)").text().replace(/[₹,]/g, "").trim() || 0;

            let parts = date.split("-");
            let formattedDate = `${parts[2]}-${parts[1]}-${parts[0]}`;

            let total_installments = $("#repayments-table tbody tr").length;
            let row_index = parseInt(row.find("td:first").text());
            let remaining_installments = total_installments - row_index;

            let d = new frappe.ui.Dialog({
                title: "Edit Installment Amount",
                size: "large",
                fields: [

                    { fieldtype: "Section Break" },
                    {
                        label: "Hold Option",
                        fieldname: "hold_option",
                        fieldtype: "Select",
                        options: [
                            "Recover Pending in Next Month",
                            "Distribute Across Future Months",
                        ],
                        default: "Distribute Across Future Months"
                    },
                    { fieldtype: "Column Break" },
                    {
                        label: "Number of Months to Hold",
                        fieldname: "number_of_months",
                        fieldtype: "Int",
                        default: 1,
                        reqd: 1
                    },
                    { fieldtype: "Section Break" },
                    {
                        label: "Deduction Amount",
                        fieldname: "deduction_amount",
                        fieldtype: "Currency",
                        default: row_amount,
                        reqd: 1
                    },
                    {
                        label: "Payment Date",
                        fieldname: "payment_date",
                        fieldtype: "Date",
                        default: formattedDate,
                        read_only: 1
                    },
                    {
                        label: "Additional Salary ID",
                        fieldname: "additional_salary_id",
                        fieldtype: "Data",
                        default: additional_salary_id,
                        read_only: 1
                    }
                ],
                primary_action_label: "Submit",
                primary_action(values) {



                    if (values.number_of_months < 1) {
                        frappe.msgprint("Number of months to Edit must be at least 1.");
                        return;
                    }

                    if (values.number_of_months > total_installments) {
                        frappe.msgprint("Number of months to Edit cannot exceed total installments.");
                        return;
                    }

                    if (values.number_of_months > remaining_installments) {
                        frappe.msgprint(
                            `Only ${remaining_installments} installment(s) are pending. You cannot hold ${values.number_of_months} months.`
                        );
                        return;
                    }



                    frappe.call({
                        method: "cn_indian_payroll.cn_indian_payroll.overrides.employee_advance.edit_installment",
                        args: {
                            repayments: repayments,
                            idx: row_index,
                            hold_months: values.number_of_months,
                            hold_option: values.hold_option,
                            installment_id: additional_salary_id,
                            installment_amount: values.deduction_amount,
                            employee: frm.doc.employee,
                            component: frm.doc.custom_deduction_component,
                            doc_id: frm.doc.name,
                            company: frm.doc.company
                        },
                        callback: function (r) {
                            if (r.message === "success") {
                                frappe.msgprint("Installment updated successfully.");
                                d.hide();
                                frm.reload_doc();
                            } else {
                                frappe.msgprint("Error updating installment. Please try again.");
                            }
                        }
                    });
                }
            });
            d.show();
        });









                    }
                }
            });


            if(!frm.doc.custom_settlement_date)
            {


            frm.add_custom_button(__('Settle Amount'), function () {
                let d = new frappe.ui.Dialog({
                    title: "One-Time Settlement",
                    fields: [
                        {
                            label: "Settlement Date",
                            fieldname: "settlement_date",
                            fieldtype: "Date",
                            reqd: 1
                        },
                        {
                            label: "Settlement Amount",
                            fieldname: "settlement_amount",
                            fieldtype: "Currency",
                            reqd: 1
                        },
                        {
                            label: "Remarks",
                            fieldname: "remarks",
                            fieldtype: "Small Text",
                            reqd: 1
                        }
                    ],
                    primary_action_label: "Submit",
                    primary_action(values) {
                        if (frm.doc.custom_total_balance_amount == values.settlement_amount) {
                            frappe.call({
                                method: "cn_indian_payroll.cn_indian_payroll.overrides.employee_advance.delete_un_deducted_additional_salaries",
                                args: {
                                    employee: frm.doc.employee,
                                    id: frm.doc.name,
                                    company: frm.doc.company,
                                    settlement_date: values.settlement_date,
                                    remarks: values.remarks,
                                    settlement_amount: values.settlement_amount,
                                    balance_amount: frm.doc.custom_total_balance_amount
                                },
                                callback: function (r) {

                                    console.log(r.message.status)
                                    if (r.message.status == "success") {
                                        frappe.msgprint("Settlement updated successfully.");
                                        d.hide();
                                        frm.reload_doc();
                                    }
                                    else {
                                        frappe.msgprint("Error updating settlement. Please try again.");
                                    }
                                }
                            });
                        }

                        else {
                            frappe.msgprint(
                                `You can’t settle the amount. Balance amount is ${frm.doc.custom_total_balance_amount}`
                            );
                        }
                    }
                });

                d.show();
            });

        }








        }

        if (frm.is_new()) {
            frm.set_value("custom_repayment_dashboard", undefined);

            // Clear the dashboard wrapper so it doesn't show old data
            if (frm.fields_dict.custom_repayment_dashboard) {
                frm.fields_dict.custom_repayment_dashboard.wrapper.innerHTML = "";
            }
        }


    }




    },


    custom_repayment_type(frm)
    {
        if(frm.doc.custom_repayment_type=="One Time")
        {
            frm.set_value("custom_repayment_methods",undefined)
            frm.set_value("custom_monthly_repayment_amount",undefined)
            frm.set_value("custom_repayment_period_in_months",undefined)
        }

    },

    custom_advance_type(frm)
    {
        if(frm.doc.employee && frm.doc.custom_advance_type && frm.doc.custom_type=="Salary Advance")
        {
            frappe.call({
                "method":"cn_indian_payroll.cn_indian_payroll.overrides.employee_advance.get_advance_amount_checking",
                args:{
                    employee:frm.doc.employee,
                    advance_type:frm.doc.custom_advance_type,
                    posting_date:frm.doc.posting_date,
                    company:frm.doc.company
                },
                callback:function(r)
                {
                    if(r.message)
                    {
                        frm.set_value("advance_amount",r.message.amount)

                    }
                }
            })
        }
    },


    custom_type:function(frm)
    {
        if(frm.doc.custom_type=="Reimbursement / Expense Advance")
        {
            frm.set_value("custom_repayment_type",undefined)
            frm.set_value("custom_repayment_methods",undefined)
            frm.set_value("custom_repayment_start_date",undefined)
            frm.set_value("custom_repayment_period_in_months",undefined)
            frm.set_value("custom_monthly_repayment_amount",undefined)

        }
    }

});
