frappe.ui.form.on("Salary Slip", {
    posting_date: function(frm) {
        if (frm.doc.posting_date > frappe.datetime.get_today()) {
            frappe.msgprint(__('Posting date cannot be in the future.'));
            frm.set_value('posting_date', null);
        }
    },
    
});
