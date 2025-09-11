frappe.ui.form.on('Employee Advance', {
    refresh(frm) {

        if (frm.doc.status === "Paid" && frm.doc.repay_unclaimed_amount_from_salary) {
            frm.add_custom_button(__('Deduct From Salary'), function() {
                frappe.model.with_doctype("Additional Salary", function() {
                    let new_doc = frappe.model.get_new_doc("Additional Salary");
                    new_doc.employee = frm.doc.employee;
                    new_doc.company = frm.doc.company;
                    new_doc.amount = frm.doc.advance_amount;
                    new_doc.ref_doctype = "Employee Advance";
                    new_doc.ref_docname = frm.doc.name;

                    frappe.set_route("Form", "Additional Salary", new_doc.name);
                });
            }).addClass("btn-primary");
        }







        if (frm.doc.docstatus === 1 && !frm.is_new()) {
            frappe.call({
                method: 'cn_indian_payroll.cn_indian_payroll.overrides.employee_advance.get_advance_details',
                args: {
                    id: frm.doc.name,
                    employee: frm.doc.employee,
                    company: frm.doc.company,
                    posting_date: frm.doc.posting_date
                },
                callback: function (r) {
                    if (r.message) {
                        const data = r.message;

                        // Dashboard HTML
                        const dashboard_html = `
                            <div class="row text-center mb-4">
                                <div class="col-md-3">
                                    <div class="p-3" style="border:1px solid #ddd; border-radius:10px; box-shadow:0 4px 8px rgba(0,0,0,0.1); background-color:#f9f9f9;">
                                        <h6 class="text-muted">Advance Type</h6>
                                        <h5>${data.advance_type}</h5>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="p-3" style="border:1px solid #ddd; border-radius:10px; box-shadow:0 4px 8px rgba(0,0,0,0.1); background-color:#f9f9f9;">
                                        <h6 class="text-muted">Total Advance Amount</h6>
                                        <h5>₹${data.total_loan_amount.toLocaleString()}</h5>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="p-3" style="border:1px solid #ddd; border-radius:10px; box-shadow:0 4px 8px rgba(0,0,0,0.1); background-color:#f9f9f9;">
                                        <h6 class="text-muted">Total Paid</h6>
                                        <h5>₹${data.total_paid.toLocaleString()}</h5>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="p-3" style="border:1px solid #ddd; border-radius:10px; box-shadow:0 4px 8px rgba(0,0,0,0.1); background-color:#f9f9f9;">
                                        <h6 class="text-muted">Balance</h6>
                                        <h5>₹${data.balance_amount.toLocaleString()}</h5>
                                    </div>
                                </div>
                            </div>
                        `;

                        // Table HTML
                        let table_html = `
                            <table id="installments-table"
                                   style="width:100%; border-collapse:collapse; text-align:center; border-radius:10px; overflow:hidden; box-shadow:0 4px 12px rgba(0,0,0,0.1);">
                                <thead style="background-color:grey; color:white;">
                                    <tr>
                                        <th style="padding:10px;">Sl. No.</th>
                                        <th style="padding:10px;">Installment Date</th>
                                        <th style="padding:10px;">Installment Amount</th>
                                        <th style="padding:10px;">Additional Salary ID</th>
                                        <th style="padding:10px;">Deducted</th>
                                        <th style="padding:10px;">Edit</th>
                                    </tr>
                                </thead>
                                <tbody style="background-color:#fefefe;">
                        `;

                        data.installments.forEach(inst => {
                            const is_deducted = inst.deducted === 1 || inst.deducted === true;

                            table_html += `
                                <tr style="border-bottom:1px solid #ddd;">
                                    <td style="padding:10px;">${inst.sl}</td>
                                    <td style="padding:10px;" class="installment-date">${inst.date}</td>
                                    <td style="padding:10px;">₹${inst.amount.toLocaleString()}</td>
                                    <td style="padding:10px;" class="additional-salary-id">${inst.additional_salary_id}</td>
                                    <td style="padding:10px;">
                                        <input type="checkbox" class="deducted-checkbox" ${is_deducted ? "checked disabled" : ""}/>
                                    </td>
                                    <td style="padding:10px;">
                                        <button class="btn btn-xs btn-primary edit-btn" ${is_deducted ? "disabled" : ""}>
                                            Edit/Hold
                                        </button>
                                    </td>
                                </tr>
                            `;
                        });

                        table_html += `</tbody></table>`;

                        const full_html = dashboard_html + table_html;

                        frm.fields_dict.custom_repayment_dashboard.$wrapper.html(full_html);

                        // Attach edit button actions
                        frm.fields_dict.custom_repayment_dashboard.$wrapper
                            .find(".edit-btn")


                            .on("click", function () {


                                if (!frappe.user.has_role("Payroll Manager")) {
                                    frappe.msgprint("You do not have permission to hold installments.");
                                    return;
                                }




                                let row = $(this).closest("tr");
                                let date = row.find(".installment-date").text();
                                let additional_salary_id = row.find(".additional-salary-id").text();
                                let deducted = row.find(".deducted-checkbox").prop("checked");
                                let prev_date = row.prev().find(".installment-date").text() || null;

                                if (deducted) {
                                    frappe.msgprint("This installment is already deducted. Editing disabled.");
                                    return;
                                }

                                let parts = date.split("-");
                                let formattedDate = `${parts[2]}-${parts[1]}-${parts[0]}`;

                                let total_installments = $("#installments-table tbody tr").length;
                                let row_index = parseInt(row.find("td:first").text());

                                let remaining_installments = total_installments - row_index;

                                let d = new frappe.ui.Dialog({
                                    title: "Hold Installment",
                                    size: "large",
                                    fields: [
                                        { fieldtype: "Section Break" },
                                        { label: "Hold Option", fieldname: "hold_option", fieldtype: "Select", options: ["Recover Pending in Next Month", "Distribute Across Future Months", "Extend Repayment Period"], default: "Distribute Across Future Months" },
                                        { fieldtype: "Column Break" },
                                        { label: "Number of Months to Hold", fieldname: "number_of_months", fieldtype: "Int", default: 1, reqd: 1 },
                                        { fieldtype: "Section Break" },
                                        { label: "Holding Date", fieldname: "holding_date", fieldtype: "Date", default: formattedDate,read_only:1 },

                                        { label: "Additional Salary ID", fieldname: "additional_salary_id", fieldtype: "Data", default: additional_salary_id,hidden: 1 },
                                    ],
                                    primary_action_label: "Submit",
                                    primary_action(values) {

                                        if (values.number_of_months > total_installments) {
                                            frappe.msgprint("Number of months to hold cannot exceed total installments.");
                                            return;
                                        }

                                        if (values.number_of_months > remaining_installments) {
                                            frappe.msgprint(`Only ${remaining_installments} installment(s) are pending. You cannot hold ${values.number_of_months} months.`);
                                            return;
                                        }


                                        frappe.call({
                                            method: "cn_indian_payroll.cn_indian_payroll.overrides.employee_advance.hold_installments",
                                            args: {
                                                additional_salary_id: values.additional_salary_id,
                                                previous_date: prev_date,
                                                hold_option: values.hold_option,
                                                holding_date: values.holding_date,
                                                number_of_months: values.number_of_months,
                                                amount: values.amount,
                                                advance_amount: frm.doc.advance_amount,
                                                total_installments: total_installments
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
                                        d.hide();

                                }
                                });
                                d.show();
                            });











                    }
                }
            });
        }
    }
});
