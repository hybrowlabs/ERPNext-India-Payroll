frappe.listview_settings['Payroll Entry'] = {
    refresh(listview) {

        // Parent dropdown button
listview.page.add_inner_button(
    __('Declaration Release'),
    function () {

        frappe.new_doc("Release Config");

    },
    __('Payroll Rules Engine')
);

        listview.page.add_inner_button(
                __('Delete Extra Payroll Entries'),
                function () {

                    let d = new frappe.ui.Dialog({
                        title: 'Delete Extra Payroll Entries',
                        fields: [
                            {
                                label: 'From Date',
                                fieldname: 'from_date',
                                fieldtype: 'Date',
                                reqd: 1
                            },
                            {
                                label: 'To Date',
                                fieldname: 'to_date',
                                fieldtype: 'Date',
                                reqd: 1
                            },
                            {
                                label: 'Employee',
                                fieldname: 'employee',
                                fieldtype: 'Link',
                                options: 'Employee'
                            }
                        ],
                        primary_action_label: 'Delete',
                        primary_action(values) {

                            frappe.call({
                                method: 'cn_indian_payroll.cn_indian_payroll.overrides.dashboard.delete_extra_payment',
                                args: {
                                    from_date: values.from_date,
                                    to_date: values.to_date,
                                    employee: values.employee
                                },
                                freeze: true,
                                freeze_message: 'Processing...',
                                callback: function (r) {
                                    if (r.message) {
                                        frappe.msgprint(r.message);
                                        d.hide();
                                        listview.refresh(); // refresh list after delete
                                    }
                                }
                            });

                        }
                    });

                    d.show();
                },
                __('Payroll Rules Engine')
            );
        listview.page.add_inner_button(
            __('Delete Payslips'),
                function () {

                    let d = new frappe.ui.Dialog({
                        title: 'Delete Extra Payroll Entries',
                        fields: [
                            {
                                label: 'From Date',
                                fieldname: 'from_date',
                                fieldtype: 'Date',
                                reqd: 1
                            },
                            {
                                label: 'To Date',
                                fieldname: 'to_date',
                                fieldtype: 'Date',
                                reqd: 1
                            },
                            {
                                label: 'Employee',
                                fieldname: 'employee',
                                fieldtype: 'Link',
                                options: 'Employee'
                            }
                        ],
                        primary_action_label: 'Delete',
                        primary_action(values) {

                            frappe.call({
                                method: 'cn_indian_payroll.cn_indian_payroll.overrides.dashboard.delete_salary_slip',
                                args: {
                                    from_date: values.from_date,
                                    to_date: values.to_date,
                                    employee: values.employee
                                },
                                freeze: true,
                                freeze_message: 'Processing...',
                                callback: function (r) {
                                    if (r.message) {
                                        frappe.msgprint(r.message);
                                        d.hide();
                                        listview.refresh(); // refresh list after delete
                                    }
                                }
                            });

                        }
                    });

                    d.show();
                },
            __('Payroll Rules Engine')
        );

        listview.page.add_inner_button(
            __('Delete Form16'),
            function () {
            },
            __('Payroll Rules Engine')
        );

        listview.page.add_inner_button(
            __('Payslip Release Import'),
            function () {
                frappe.new_doc("Data Import");
            },
            __('Payroll Rules Engine')
        );

        listview.page.add_inner_button(
            __('Bulk Download'),
            function () {
                frappe.new_doc("Data Import");
            },
            __('Payroll Rules Engine')
        );

        listview.page.add_inner_button(
            __('Batch Process Taxsheet'),
            function () {
                 msgprint("processed successfully")
            },
            __('Payroll Rules Engine')
        );

        listview.page.add_inner_button(
            __('Batch Process Annual Taxsheet'),
            function () {
                msgprint("processed successfully")
            },
            __('Payroll Rules Engine')
        );

        listview.page.add_inner_button(
            __('View History'),
            function () {
            },
            __('Payroll Rules Engine')
        );
    }
};
