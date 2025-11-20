frappe.ui.form.on("Salary Slip", {
    posting_date: function(frm) {
        if (frm.doc.posting_date > frappe.datetime.get_today()) {
            frappe.msgprint(__('Posting date cannot be in the future.'));
            frm.set_value('posting_date', null);
        }
    },

    refresh: function (frm) {

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



            frm.add_custom_button(__('Salary Slip'), function() {
                let print_format = "Salary Slip"; // <-- your format name
                let url = frappe.urllib.get_full_url(
                    `/printview?doctype=Salary Slip&name=${frm.doc.name}&trigger_print=0&format=${print_format}&no_letterhead=0`
                );
                window.open(url);
            }, __("View"));

    }


    }

});
