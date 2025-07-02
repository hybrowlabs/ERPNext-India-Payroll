frappe.listview_settings['Employee Bonus Accrual'] = {
    onload: function(listview) {
        listview.page.clear_primary_action();
    },
     refresh: function(listview) {
        listview.page.clear_primary_action();
    }
};
