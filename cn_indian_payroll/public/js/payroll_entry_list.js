frappe.listview_settings['Payroll Entry'] = {
    refresh(listview) {

        // Parent dropdown button
        listview.page.add_inner_button(
            __('Declaration Release'),
            function () {
            },
            __('Payroll Rules Engine')
        );

        listview.page.add_inner_button(
            __('Delete Extra Payroll Entries'),
            function () {
            },
            __('Payroll Rules Engine')
        );

        listview.page.add_inner_button(
            __('Delete Payslips'),
            function () {
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
                
            },
            __('Payroll Rules Engine')
        );

        listview.page.add_inner_button(
            __('Bulk Download'),
            function () {
            },
            __('Payroll Rules Engine')
        );

        listview.page.add_inner_button(
            __('Batch Process Taxsheet'),
            function () {
            },
            __('Payroll Rules Engine')
        );

        listview.page.add_inner_button(
            __('Batch Process Annual Taxsheet'),
            function () {
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
