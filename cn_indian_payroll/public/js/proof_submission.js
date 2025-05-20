frappe.ui.form.on('Employee Tax Exemption Proof Submission', {
    onload(frm) {
        if (frm.doc.custom_declaration) {
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Employee Tax Exemption Declaration",
                    name: frm.doc.custom_declaration
                },
                callback: function (r) {
                    if (r.message && r.message.declarations) {
                        const declarations = r.message.declarations;

                        // Update only if lengths match
                        if (declarations.length === frm.doc.tax_exemption_proofs.length) {
                            for (let i = 0; i < declarations.length; i++) {
                                frm.doc.tax_exemption_proofs[i].custom_declaration_amount = declarations[i].amount;
                            }
                            frm.refresh_field('tax_exemption_proofs');
                        } else {
                            frappe.msgprint(__('Number of declaration rows do not match. Manual review needed.'));
                        }
                    }
                }
            });
        }
    }
});
