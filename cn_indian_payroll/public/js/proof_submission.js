



       frappe.ui.form.on('Employee Tax Exemption Proof Submission', {
	refresh(frm) {
		          if(frm.doc.docstatus==1)
       {
        frm.add_custom_button("Form 12 B", function () {
            if (!frm.doc.employee || !frm.doc.payroll_period) {
                frappe.msgprint(__('Please set Employee and Payroll Period first.'));
                return;
            }

            frappe.call({
                method: "cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.tds_projection.get_form12b_pdf",
                args: {
                    docname: frm.doc.name,
                    doctype: frm.doc.doctype,
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
        });
       }


       
            frm.add_custom_button("Print TDS Projection", () => {
                window.open(
                    `/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.tds_projection.download_tds_poi_projection_pdf?proof_id=${frm.doc.name}`
                );
            });
        
	}
})