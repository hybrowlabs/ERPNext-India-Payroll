frappe.ui.form.on('Employee', {
    refresh: function(frm) {
        // Main button group: "Details"
        frm.add_custom_button('Details', null, 'Actions');

        // Sub-buttons under "Details"
        if (frappe.user.has_role("HR Manager") || frappe.user.has_role("Payroll Manager")) {
            frm.add_custom_button('Assign New CTC', function() {

            frappe.route_options = {"employee": frm.doc.name};

            frappe.set_route("Form", "Salary Structure Assignment", 'new-salary-structure-assignment');


            }, 'Details');
        }

        frm.add_custom_button('View Latest CTC', function() {


            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Salary Structure Assignment",
                    filters: {
                        "employee": frm.doc.employee,
                        "docstatus": 1,
                        "company": frm.doc.company
                    },
                    fields: ["name"],
                    limit: 1,
                    order_by: "from_date desc"
                },
                callback: function(res) {

                    if (res.message && res.message.length > 0) {
                        frappe.set_route("Form", "Salary Structure Assignment", res.message[0].name);
                    } else {
                        frappe.msgprint("No Salary Structure Assignment found.");
                    }
                }
            });




        }, 'Details');


        frm.add_custom_button('View Exemption Declaration', function () {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Salary Structure Assignment",
                    filters: {
                        "employee": frm.doc.employee,
                        "docstatus": 1,
                        "company": frm.doc.company
                    },
                    fields: ["*"],
                    limit: 1,
                    order_by: "from_date desc"
                },
                callback: function (res) {
                    if (res.message && res.message.length > 0) {
                        let ssa = res.message[0];
                        frappe.call({
                            method: "frappe.client.get_list",
                            args: {
                                doctype: "Employee Tax Exemption Declaration",
                                filters: {
                                    "employee": frm.doc.employee,
                                    "docstatus": 1,
                                    "company": frm.doc.company,
                                    "payroll_period": ssa.custom_payroll_period
                                },
                                fields: ["name"],
                                limit: 1
                            },
                            callback: function (response) {
                                if (response.message && response.message.length > 0) {
                                    frappe.set_route("Form", "Employee Tax Exemption Declaration", response.message[0].name);
                                } else {
                                    frappe.msgprint("No Employee Tax Exemption Declaration found.");
                                }
                            }
                        });
                    } else {
                        frappe.msgprint("No Salary Structure Assignment found.");
                    }
                }
            });
        },'Details');

    }

});
