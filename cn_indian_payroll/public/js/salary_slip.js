frappe.ui.form.on("Salary Slip", {
    refresh(frm) {
      frm.add_custom_button("Annual Statement", function () {
        if (!frm.doc.employee || !frm.doc.custom_payroll_period) {
          frappe.msgprint(__('Please set Employee and Payroll Period first.'));
          return;
        }

        frappe.call({
          method: "cn_indian_payroll.cn_indian_payroll.overrides.tds_printer.get_annual_statement_pdf",
          args: {
            employee: frm.doc.employee,
            payroll_period: frm.doc.custom_payroll_period
          },
          callback: function (r) {
            if (!r.message || !r.message.html) {
              frappe.msgprint(__('No HTML generated'));
              return;
            }
            const w = window.open("", "_blank");
            w.document.open();
            w.document.write(r.message.html);   // load full HTML into popup
            w.document.close();
          }
        });
      });
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
