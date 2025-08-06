frappe.listview_settings['Employee Benefit Accrual'] = {
    onload: function(listview) {
        listview.page.clear_primary_action();
    },
     refresh: function(listview) {
        listview.page.clear_primary_action();
    }
};
