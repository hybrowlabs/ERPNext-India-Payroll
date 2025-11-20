frappe.ui.form.on('Payroll Entry', {
    refresh(frm) {
        if (frm.doc.docstatus == 1 && frm.doc.status == "Submitted") {
            frm.add_custom_button(__("View Salary Register"), function () {
                frappe.set_route("query-report", "Salary Book Register");
            });
        }

    }
});
