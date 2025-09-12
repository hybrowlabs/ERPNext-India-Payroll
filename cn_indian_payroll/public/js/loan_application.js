// frappe.ui.form.on('Loan Application', {
//     refresh: function (frm) {
//         if (!frm.doc.applicant || !frm.doc.name) {
//             return;
//         }

//         // build static loan table
//         const tableHtml = `
//         <div style="overflow:auto; padding: 6px; background: #fff; margin-bottom: 15px;">
//           <table class="table table-bordered" style="width:100%; border-collapse:collapse; font-size:13px;">
//             <thead>
//               <tr style="background:#f5f5f5;">
//                 <th>Loan ID</th>
//                 <th>Employee</th>
//                 <th>Loan Type</th>
//                 <th>Approved</th>
//                 <th>EMI</th>
//                 <th>Start Date</th>
//                 <th>Tenure (mo)</th>
//                 <th>Status</th>
//               </tr>
//             </thead>
//             <tbody>
//               <tr>
//                 <td>ACC-LOAN-2025-00001</td>
//                 <td>Shinil N</td>
//                 <td>Personal</td>
//                 <td style="text-align:right;">₹ 500,000</td>
//                 <td style="text-align:right;">₹ 3,000</td>
//                 <td>2025-01-01</td>
//                 <td>60</td>
//                 <td>Approved</td>
//               </tr>
//             </tbody>
//           </table>
//         </div>
//         `;

//         // dashboard 7 boxes
//         const dashboardHtml = `
//         <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-top: 10px; margin-bottom: 15px;">
//           <div class="dash-box"><div class="dash-title">Monthly Repayment</div><div class="dash-value">₹ 3,000</div></div>
//           <div class="dash-box"><div class="dash-title">Total Months</div><div class="dash-value">60</div></div>
//           <div class="dash-box"><div class="dash-title">Paid Months</div><div class="dash-value">12</div></div>
//           <div class="dash-box"><div class="dash-title">Remaining Months</div><div class="dash-value">48</div></div>
//           <div class="dash-box"><div class="dash-title">Total Loan Amount</div><div class="dash-value">₹ 500,000</div></div>
//           <div class="dash-box"><div class="dash-title">Total Paid</div><div class="dash-value">₹ 36,000</div></div>
//           <div class="dash-box"><div class="dash-title">Remaining Amount</div><div class="dash-value">₹ 464,000</div></div>
//           <div class="dash-box"><div class="dash-title">Remaining Amount</div><div class="dash-value">₹ 464,000</div></div>

//           </div>

//         <style>
//           .dash-box {
//             background:#f8f9fa; padding:12px; border-radius:6px; border:1px solid #ddd;
//           }
//           .dash-title {
//             font-size:12px; color:#666;
//           }
//           .dash-value {
//             font-size:14px; font-weight:bold; color:#333;
//           }
//         </style>
//         `;

//         // reimbursement / repayment schedule table (collapsible)
//         const reimbursementHtml = `
//         <div style="margin-top:20px; border:1px solid #ddd; border-radius:6px;">
//           <div style="background:#f5f5f5; padding:10px; cursor:pointer; display:flex; justify-content:space-between; align-items:center;"
//                onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'none' ? 'block' : 'none'">
//             <span style="font-weight:bold;">Reimbursement / Repayment Schedule</span>
//             <span style="font-size:12px; color:#666;">▼</span>
//           </div>
//           <div style="display:none; padding:10px;">
//             <table class="table table-bordered" style="width:100%; border-collapse:collapse; font-size:13px;">
//               <thead>
//                 <tr style="background:#f5f5f5;">
//                   <th>Payment Date</th>
//                   <th>Principal Amount</th>
//                   <th>Interest Amount</th>
//                   <th>Total Payment</th>
//                   <th>Balance Loan Amount</th>
//                 </tr>
//               </thead>
//               <tbody>
//                 <tr>
//                   <td>2025-02-01</td>
//                   <td style="text-align:right;">₹ 2,500</td>
//                   <td style="text-align:right;">₹ 500</td>
//                   <td style="text-align:right;">₹ 3,000</td>
//                   <td style="text-align:right;">₹ 497,500</td>
//                 </tr>
//                 <tr>
//                   <td>2025-03-01</td>
//                   <td style="text-align:right;">₹ 2,520</td>
//                   <td style="text-align:right;">₹ 480</td>
//                   <td style="text-align:right;">₹ 3,000</td>
//                   <td style="text-align:right;">₹ 494,980</td>
//                 </tr>
//               </tbody>
//             </table>
//           </div>
//         </div>
//         `;

//         // combine all
//         const finalHtml = tableHtml + dashboardHtml + reimbursementHtml;

//         // display in custom field
//         if (frm.fields_dict.custom_loan_dashboard) {
//             frm.fields_dict.custom_loan_dashboard.wrapper.innerHTML = finalHtml;
//         } else {
//             frm.set_df_property("custom_loan_dashboard", "options", finalHtml);
//         }
//     }
// });



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
                console.log("Loan Dashboard Response:", loan);

                function makeDashBox(title, value) {
                    return `
                      <div style="
                          background: #f9f9f9;

                          border-radius: 8px;
                          padding: 12px;
                          text-align: center;
                          box-shadow: 0 1px 3px rgba(0,0,0,0.08);
                          border:1px solid #000;
                      ">
                        <div style="font-size: 13px; color: #666; margin-bottom: 6px;">${title}</div>
                        <div style="font-size: 16px; font-weight: bold; color: #333;">${value}</div>
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


                // Dashboard 7 Boxes
                let dashboardHtml = `
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-top: 10px; margin-bottom: 15px;">
                  ${makeDashBox("Monthly Repayment", "₹ " + (loan.monthly_repayment_amount || 0))}
                  ${makeDashBox("Total Months", loan.total_months || 0)}
                  ${makeDashBox("Paid Months", loan.paid_months || 0)}
                  ${makeDashBox("Remaining Months", loan.remaining_months || 0)}
                  ${makeDashBox("Total Loan Amount", "₹ " + (loan.total_loan_amount || 0))}
                  ${makeDashBox("Total Paid", "₹ " + (loan.total_paid_amount || 0))}
                  ${makeDashBox("Remaining Amount", "₹ " + (loan.remaining_amount || 0))}
                  ${makeDashBox("Total Interest", "₹ " + (loan.remaining_amount || 0))}
                </div>
                `;


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
                                <button class="btn btn-sm btn-primary hold-btn"
                                        data-row-id="${i + 1}"
                                        data-date="${row.payment_date}"
                                        data-amount="${row.total_payment}">
                                    Hold
                                </button>
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



            // Attach event listeners for Hold buttons
            $(frm.fields_dict.custom_loan_dashboard.wrapper)
                .find(".hold-btn")
                .on("click", function () {
                    const rowId = $(this).data("row-id");
                    const paymentDate = $(this).data("date");
                    const amount = $(this).data("amount");

                    // Open Dialog
                    let d = new frappe.ui.Dialog({
                        title: "Hold Repayment",
                        fields: [
                            {
                                label: "Payment Date",
                                fieldname: "payment_date",
                                fieldtype: "Date",
                                default: paymentDate,
                                read_only: 1
                            },
                            {
                                label: "Days to Hold",
                                fieldname: "days_to_hold",
                                fieldtype: "Int",
                                reqd: 1
                            },
                            {
                                label: "Amount",
                                fieldname: "amount",
                                fieldtype: "Currency",
                                default: amount,
                                read_only: 1
                            }
                        ],
                        primary_action_label: "Submit",
                        primary_action(values) {
                            console.log("Row ID:", rowId);
                            console.log("Payment Date:", values.payment_date);
                            console.log("Amount:", values.amount);
                            console.log("Days to Hold:", values.days_to_hold);
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


    }


});
