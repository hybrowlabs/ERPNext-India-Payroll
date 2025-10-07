frappe.ui.form.on("Salary Slip", {
    refresh(frm) {



    //   frm.add_custom_button(__('View Payslip PDF'), function() {
    //     const slip_id = encodeURIComponent(frm.doc.name);
    //     const url = `/api/method/cn_indian_payroll.cn_indian_payroll.overrides.tds_printer.get_payslip_pdf_html?id=${slip_id}`;

    //     fetch(url)
    //         .then(response => response.json())
    //         .then(data => {
    //             if (data.content_type === 'text/html' && data.response) {
    //                 const win = window.open('', '_blank'); // open new tab
    //                 win.document.open();
    //                 win.document.write(data.response); // inject the full HTML
    //                 win.document.close();
    //             } else {
    //                 frappe.msgprint(__('No HTML content returned'));
    //             }
    //         })
    //         .catch(err => {
    //             console.error(err);
    //             frappe.msgprint(__('Failed to load payslip'));
    //         });
    // }).addClass('btn-primary');


        if(frm.doc.docstatus==1 || frm.doc.docstatus==0)
        {


      frm.add_custom_button("TDS Sheet", function () {
        if (!frm.doc.employee || !frm.doc.custom_payroll_period) {
          frappe.msgprint(__('Please set Employee and Payroll Period first.'));
          return;
        }

        frappe.call({
          method: "cn_indian_payroll.cn_indian_payroll.overrides.tds_printer.get_annual_statement_pdf",
          args: {
            employee: frm.doc.employee,
            payroll_period: frm.doc.custom_payroll_period,
            end_date: frm.doc.end_date,
            month: frm.doc.custom_month,
            tax_regime:frm.doc.custom_tax_regime,
            id:frm.doc.name,
            income_tax_slab:frm.doc.custom_income_tax_slab
          },
          callback: function (r) {
            if (!r.message || !r.message.html) {
              frappe.msgprint(__('No HTML generated'));
              return;
            }
            const w = window.open("", "_blank");
            w.document.open();
            w.document.write(r.message.html);
            w.document.close();
          }
        });
      },"View");


      frm.add_custom_button("Regular Payslip", function () {
        if (!frm.doc.employee || !frm.doc.custom_payroll_period) {
            frappe.msgprint(__('Please set Employee and Payroll Period first.'));
            return;
        }

        // frappe.call({
        //     method: "cn_indian_payroll.cn_indian_payroll.overrides.tds_printer.get_payslip_pdf",
        //     args: {
        //         id: frm.doc.name   // only need the salary slip name
        //     },
        //     callback: function (r) {
        //         if (!r.message || !r.message.html) {
        //             frappe.msgprint(__('No HTML generated'));
        //             return;
        //         }
        //         const w = window.open("", "_blank");
        //         w.document.open();
        //         w.document.write(r.message.html);
        //         w.document.close();
        //     }
        // });

        frappe.call({
          method: "cn_indian_payroll.cn_indian_payroll.overrides.tds_printer.get_payslip_pdf_json",
          args: { id: frm.doc.name },
          callback: function(r) {
              const w = window.open("", "_blank");
              w.document.write(r.message.html);
          }
      });

    }, "View");




    frm.add_custom_button("Benefit Payslip", function () {
      if (!frm.doc.employee || !frm.doc.custom_payroll_period) {
          frappe.msgprint(__('Please set Employee and Payroll Period first.'));
          return;
      }

      frappe.call({
          method: "cn_indian_payroll.cn_indian_payroll.overrides.tds_printer.get_benefit_payslip_pdf",
          args: {
              id: frm.doc.name
          },
          callback: function (r) {
              if (!r.message || !r.message.html) {
                  frappe.msgprint(__('No HTML generated'));
                  return;
              }
              const w = window.open("", "_blank");
              w.document.open();
              w.document.write(r.message.html);
              w.document.close();
          }
      });
  }, "View");



  frm.add_custom_button("Offcycle Payslip", function () {
    if (!frm.doc.employee || !frm.doc.custom_payroll_period) {
        frappe.msgprint(__('Please set Employee and Payroll Period first.'));
        return;
    }

    frappe.call({
        method: "cn_indian_payroll.cn_indian_payroll.overrides.tds_printer.get_offcycle_payslip_pdf",
        args: {
            id: frm.doc.name   // only need the salary slip name
        },
        callback: function (r) {
            if (!r.message || !r.message.html) {
                frappe.msgprint(__('No HTML generated'));
                return;
            }
            const w = window.open("", "_blank");
            w.document.open();
            w.document.write(r.message.html);
            w.document.close();
        }
    });
}, "View");






    }








    }
  });




// frappe.ui.form.on("Salary Slip", {
//     refresh(frm) {
//       frm.add_custom_button("Annual Statement", function () {
//         if (!frm.doc.employee || !frm.doc.custom_payroll_period) {
//           frappe.msgprint(__('Please set Employee and Payroll Period first.'));
//           return;
//         }

//         frappe.call({
//           method: "cn_indian_payroll.cn_indian_payroll.overrides.tds_printer.get_annual_statement_pdf",
//           args: {
//             employee: frm.doc.employee,
//             payroll_period: frm.doc.custom_payroll_period
//           },
//           callback: function (r) {
//             if (!r.message || !r.message.html) {
//               frappe.msgprint(__('No HTML generated'));
//               return;
//             }

//             // Open new window and inject HTML
//             const w = window.open("", "_blank");
//             w.document.open();
//             w.document.write(r.message.html);

//             // Add print trigger after content is loaded
//             w.document.write(`
//               <script>
//                 window.onload = function() {
//                   window.print();
//                 };
//               <\/script>
//             `);

//             w.document.close();
//           }
//         });
//       });
//     }
//   });
