frappe.listview_settings['Payroll Entry'] = {
    refresh(listview) {

        // Parent dropdown button
        listview.page.add_inner_button(
            __('Declaration Release'),
            function () {
                frappe.msgprint('Rule A clicked');
            },
            __('Payroll Rules Engine')
        );

        listview.page.add_inner_button(
            __('Delete Extra Payroll Entries'),
            function () {
                frappe.msgprint('Rule B clicked');
            },
            __('Payroll Rules Engine')
        );

        listview.page.add_inner_button(
            __('Delete Payslips'),
            function () {
                frappe.msgprint('Rule C clicked');
            },
            __('Payroll Rules Engine')
        );

        listview.page.add_inner_button(
            __('Delete Form16'),
            function () {
                frappe.msgprint('Rule C clicked');
            },
            __('Payroll Rules Engine')
        );
    }
};
