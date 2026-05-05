frappe.ui.form.on("Salary Slip", {
    refresh(frm) {


        hide_consultant_fields(frm);


        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Payroll Settings",
                name: "Payroll Settings"
            },
            callback: function (res) {
                if (!res.message) return;

                let payroll_setting = res.message;

                if (payroll_setting.custom_hide_salary_structure_configuration) {
                    $.each(
                        payroll_setting.custom_hide_salary_structure_configuration,
                        function (i, v) {

                            // Check employment type
                            if (
                                v.employment_type &&
                                v.employment_type.includes(frm.doc.custom_employment_type)
                            ) {

                                // Send for e-Sign button
                                if (frm.doc.custom_e_sign_status === "Not Send") {
                                    frm.add_custom_button("Send for e-Sign", () => {
                                        frappe.call({
                                            method: "cn_indian_payroll.cn_indian_payroll.overrides.leegality.send_salary_slip_for_esign",
                                            args: {
                                                salary_slip: frm.doc.name
                                            },
                                            freeze: true,
                                            callback: function (r) {
                                                if (!r.exc) {
                                                    frappe.msgprint("Sent to Leegality successfully");
                                                    frm.reload_doc();
                                                }
                                            }
                                        });
                                    });
                                }

                                                            
                            if (frm.doc.custom_e_sign_status === "Send") {
                                frm.add_custom_button("⬇️ View Signed PDF", () => {

                                    frappe.call({
                                        method: "cn_indian_payroll.cn_indian_payroll.overrides.leegality.view_signed_payslip",
                                        args: {
                                            salary_slip: frm.doc.name
                                        },
                                        freeze: true,
                                        callback: function (r) {
                                            if (!r.exc && r.message.status === "success") {

                                                const file_url = r.message.file_url;

                                                
                                                window.open(file_url, "_blank");

                                            } else {
                                                frappe.msgprint("Failed to fetch signed PDF");
                                            }
                                        }
                                    });

                                });
                            }





                            }
                        }
                    );
                }
            }
        });



        // frm.add_custom_button("Send Invoice to ERP", function () {

        //         frappe.call({
        //             method: "cn_indian_payroll.cn_indian_payroll.overrides.leegality.view_signed_payslip",
        //             args: {
        //                 salary_slip: frm.doc.name
        //             },
        //             freeze: true,
        //             callback: function (r) {

        //                 if (r.message && r.message.status === "success") {
        //                     frappe.msgprint("Purchase Invoice Created Successfully");
        //                 } else {
        //                     frappe.msgprint("Error while creating Purchase Invoice");
        //                 }
        //             }
        //         });

        //     });




        






        // if (frm.doc.docstatus === 1) {
        //     frm.add_custom_button(
        //         __("View Consultant Invoice"),
        //         function () {
        //             frappe.call({
        //                 method: "cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.salary_slip_list.get_consultant_payslip_pdf",
        //                 args: {
        //                     slip_id: frm.doc.name,
        //                 },
        //                 callback: function (r) {
        //                     if (r.message && r.message.html) {
        //                         let win = window.open("", "_blank");
        //                         win.document.write(r.message.html);
        //                         win.document.close();
        //                     } else {
        //                         frappe.msgprint("No invoice data found");
        //                     }
        //                 },
        //             });
        //         },
        //         __("Print")
        //     );
        // }



    //   frm.add_custom_button(__('View Payslip PDF'), function() {
    //     const slip_id = encodeURIComponent(frm.doc.name);
    //     const url = `/api/method/cn_indian_payroll.cn_indian_payroll.overrides.tds_printer.get_benefit_payslip_pdf_html?id=${slip_id}`;

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

        frappe.call({
            method: "cn_indian_payroll.cn_indian_payroll.overrides.tds_printer.get_payslip_pdf",
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












    },

     

  });




function hide_consultant_fields(frm) {

    let fields_to_hide = [
        "custom_e_sign_status",
        "custom_attach",
        "custom_slip_attach",
        "custom_document_id",
        "custom_e_sign_url",

    ];

    frappe.call({
        method: "frappe.client.get",
        args: {
            doctype: "Payroll Settings",
            name: "Payroll Settings"
        },
        callback: function (r) {

            if (!r.message) return;

            let payroll_settings = r.message;

            let employment_types = [];

            if (payroll_settings.custom_hide_salary_structure_configuration) {
                employment_types = payroll_settings.custom_hide_salary_structure_configuration.map(row => row.employment_type);
            }

            
            let should_hide = employment_types.includes(frm.doc.custom_employment_type);

            fields_to_hide.forEach(field => {
                frm.set_df_property(field, "hidden", should_hide ? 0 : 1);
            });
        }
    });
}