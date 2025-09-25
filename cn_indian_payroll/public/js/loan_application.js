


frappe.ui.form.on('Loan Application', {
    refresh: function (frm) {


        if(frm.doc.docstatus === 1&& !frm.is_new())

            {

        frappe.call({
            method: "cn_indian_payroll.cn_indian_payroll.overrides.loan_dashboard.print_loan_dashboard_erp",
            args: {
                employee: frm.doc.applicant,
                id: frm.doc.name
            },
            callback: function (r) {
                if (!r.message || r.message.length === 0) {
                    frm.fields_dict.custom_loan_dashboard.wrapper.innerHTML =
                        "<div style='padding:10px; color:#888;'>No Loan Dashboard Data Available</div>";
                    return;
                }

                const loan = r.message[0]; // since 1 loan at a time
                console.log("Loan Dashboard Response:", loan.repayment_schedule);


                function makeDashBox(icon, title, value) {
                  return `
                    <div style="
                      background: white;
                      padding: 15px;
                      border-radius: 12px;
                      border: 1px solid #e5e7eb;
                      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.68);
                      display: flex;
                      align-items: center;
                      gap: 14px;
                      transition: transform 0.2s ease, box-shadow 0.2s ease;
                    "
                    onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 6px 14px rgba(0,0,0,0.15)';"
                    onmouseout="this.style.transform='none'; this.style.boxShadow='0 2px 6px rgba(0,0,0,0.08)';"
                    >
                      <div style="
                        background: #f3f4f6;
                        font-size: 22px;
                        padding: 10px;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        min-width: 48px;
                        min-height: 48px;
                        color: #374151;
                      ">
                        ${icon}
                      </div>
                      <div>
                        <div style="font-size: 14px; color: #4b5563; font-weight: 500;">${title}</div>
                        <div style="font-size: 18px; font-weight: 700; color: #111827;">${value}</div>
                      </div>
                    </div>
                  `;
                }



                // Loan Table
                let tableHtml = `
                    <div style="overflow:auto; padding: 6px; background: #fff; margin-bottom: 15px;">
                    <table class="table" style="width:100%; border-collapse:collapse; font-size:13px; border:1px solid #000;">
                        <thead>
                        <tr style="background:#f5f5f5;">


                            <th style="border:1px solid #000;">Loan Type</th>
                            <th style="border:1px solid #000;">EMI Type</th>
                            <th style="border:1px solid #000;">Approved Amount</th>
                            <th style="border:1px solid #000;">EMI Amount</th>
                            <th style="border:1px solid #000;">Rate of Iterest</th>
                            <th style="border:1px solid #000;">Start Date</th>
                            <th style="border:1px solid #000;">Tenure (month)</th>
                            <th style="border:1px solid #000;">Status</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr>


                            <td style="border:1px solid #000;">${loan.loan_type || ""}</td>
                             <td style="border:1px solid #000;">${loan.emi_type || ""}</td>
                            <td style="text-align:right; border:1px solid #000;">₹ ${loan.loan_approved_amount || 0}</td>
                            <td style="text-align:right; border:1px solid #000;">₹ ${loan.monthly_repayment_amount || 0}</td>
                            <td style="text-align:right; border:1px solid #000;">${loan.rate_of_interest || 0}%</td>
                            <td style="border:1px solid #000;">${loan.loan_start_date || ""}</td>
                            <td style="border:1px solid #000;">${loan.loan_tenure || 0}</td>
                            <td style="border:1px solid #000;">${loan.status || ""}</td>
                        </tr>
                        </tbody>
                    </table>
                    </div>
                    `;




                let dashboardHtml = `
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-top: 10px; margin-bottom: 15px;">
                ${makeDashBox("📑", "Loan Type", loan.loan_type || "")}
                ${makeDashBox("💰", "Total Loan Amount", "₹ " + (loan.total_loan_amount || 0))}
                ${makeDashBox("📈", "Standard Rate of Interest", (loan.standard_interest || 0) + "%")}
                ${makeDashBox("📉", "Rate of Interest", (loan.rate_of_interest || 0) + "%")}
                ${makeDashBox("🗓️", "Total Months", loan.total_months || 0)}
                ${makeDashBox("⏳", "Remaining Months", loan.remaining_months || 0)}
                ${makeDashBox("📊", "Paid Months", loan.paid_months || 0)}
                ${makeDashBox("💸", "Monthly Repayment", "₹ " + (loan.monthly_repayment_amount || 0))}

                ${makeDashBox("💰", "Total Payable Amount", "₹ " + (loan. total_payment|| 0))}
                ${makeDashBox("📈", "Total Interest Payable", "₹ " + (loan. total_interest_payable|| 0))}
                ${makeDashBox("🏦", "Total Principal Paid", "₹ " + (loan. total_principal_paid|| 0))}
                ${makeDashBox("✅", "Total Paid", "₹ " + (loan.total_paid_amount || 0))}

                </div>
                `;




                const has_payroll_manager_role = frappe.user_roles.includes("Payroll Manager");


                let scheduleRows = "";
                if (loan.repayment_schedule && loan.repayment_schedule.length > 0) {
                    loan.repayment_schedule.forEach((row, i) => {
                      scheduleRows += `
                      <tr>
                          <td style="text-align:center; border:1px solid #000;">${i + 1}</td>
                          <td style="border:1px solid #000;">${frappe.datetime.str_to_user(row.payment_date)}</td>
                          <td style="text-align:right; border:1px solid #000;">₹ ${(row.principal_amount || 0).toFixed(2)}</td>
                          <td style="text-align:right; border:1px solid #000;">₹ ${(row.interest_amount || 0).toFixed(2)}</td>
                          <td style="text-align:right; border:1px solid #000;">₹ ${(row.total_payment || 0).toFixed(2)}</td>
                          <td style="text-align:right; border:1px solid #000;">₹ ${(row.balance_loan_amount || 0).toFixed(2)}</td>
                          <td style="text-align:center; border:1px solid #000;">
                            <input type="checkbox" disabled ${row.deducted ? "checked" : ""}>
                          </td>
                          <td style="text-align:center; border:1px solid #000;">
                              ${(row.deducted === 0 && has_payroll_manager_role)
                                  ? `<button class="btn btn-xs btn-primary hold-btn"
                                            data-row-id="${i + 1}"
                                            data-date="${row.payment_date}"
                                            data-amount="${row.total_payment}">
                                        Hold
                                    </button>`
                                  : ""}
                            </td>
                      </tr>
                      `;

                   });
                }


                let reimbursementHtml = `
                <div style="margin-top:20px; border:1px solid #000;">
                  <div style="background:#f5f5f5; padding:10px; cursor:pointer; display:flex; justify-content:space-between; align-items:center;"
                       onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'none' ? 'block' : 'none'">
                    <span style="font-weight:bold;">Repayment Schedule</span>
                    <span style="font-size:12px; color:#666;">▼</span>
                  </div>
                  <div style="display:none; padding:10px;">
                    <table class="table"
                           style="width:100%; border-collapse:collapse; font-size:13px; border:1px solid #000;">
                      <thead>
                        <tr style="background:#f5f5f5;">
                          <th style="border:1px solid #000;">Sl. No.</th>
                          <th style="border:1px solid #000;">Payment Date</th>
                          <th style="border:1px solid #000;">Principal Amount</th>
                          <th style="border:1px solid #000;">Interest Amount</th>
                          <th style="border:1px solid #000;">Total Payment</th>
                          <th style="border:1px solid #000;">Balance Loan Amount</th>
                          <th style="border:1px solid #000;">Deducted</th>

                          <th style="border:1px solid #000;">Hold</th>
                        </tr>
                      </thead>
                      <tbody>
                        ${scheduleRows}
                      </tbody>
                    </table>
                  </div>
                </div>
              `;



                // Combine All
                const finalHtml = tableHtml + dashboardHtml + reimbursementHtml;

                // Render inside custom field
                if (frm.fields_dict.custom_loan_dashboard) {
                    frm.fields_dict.custom_loan_dashboard.wrapper.innerHTML = finalHtml;
                }


            $(frm.fields_dict.custom_loan_dashboard.wrapper)
                .find(".hold-btn")
                .on("click", function () {
                  let row = $(this).closest("tr");
                    const rowId = $(this).data("row-id");
                    const paymentDate = $(this).data("date");
                    const amount = $(this).data("amount");


                    let row_index = parseInt(row.find("td:first").text());


                    let remaining_installments = loan.loan_tenure - row_index;


                    let d = new frappe.ui.Dialog({
                        title: "Hold Repayment",
                        size: "large",
                        fields: [
                            {
                                label: "Payment Date",
                                fieldname: "payment_date",
                                fieldtype: "Date",
                                default: paymentDate,
                                read_only: 1
                            },
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

                        ],
                        primary_action_label: "Submit",
                        primary_action(values) {



                          if (values.number_of_months < 1) {
                            frappe.msgprint("Number of months to hold must be at least 1.");
                            return;
                        }

                        if (values.number_of_months > loan.loan_tenure) {
                            frappe.msgprint("Number of months to hold cannot exceed total installments.");
                            return;
                        }



                        if (values.number_of_months > remaining_installments) {
                              frappe.msgprint(
                                  `Only ${remaining_installments} installment(s) are pending. You cannot hold ${values.number_of_months} months.`
                              );
                              return;
                          }



                          frappe.call({
                            method: "cn_indian_payroll.cn_indian_payroll.overrides.loan_application.hold_installments",
                            args: {

                                payment_date:values.payment_date,
                                employee:frm.doc.applicant,
                                company:frm.doc.company,
                                type:values.hold_option,
                                number_of_months:values.number_of_months,
                                doc_id:frm.doc.name,
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
        });

        // helper to create dashboard boxes
        function makeDashBox(title, value) {
            return `
              <div class="dash-box">
                <div class="dash-title">${title}</div>
                <div class="dash-value">${value}</div>
              </div>
            `;
        }

        // styles
        const style = `
        <style>
          .dash-box {
            background:#f8f9fa; padding:12px; border-radius:6px; border:1px solid #ddd;
          }
          .dash-title {
            font-size:12px; color:#666;
          }
          .dash-value {
            font-size:14px; font-weight:bold; color:#333;
          }
        </style>
        `;
        $(frm.fields_dict.custom_loan_dashboard.wrapper).append(style);

    }
    if (frm.is_new()) {
        frm.set_value("custom_loan_dashboard", undefined);

        // Clear the dashboard wrapper so it doesn't show old data
        if (frm.fields_dict.custom_loan_dashboard) {
            frm.fields_dict.custom_loan_dashboard.wrapper.innerHTML = "";
        }
    }


    },

    applicant:function(frm)
    {
      if(frm.doc.applicant_type=="Employee")
      {
        frm.set_value("custom_employee",frm.doc.applicant)
      }
    }


});
