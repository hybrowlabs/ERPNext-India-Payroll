frappe.listview_settings["Employee Bonus Accrual"] = {
    add_fields: ["is_paid", "payroll_period", "company"],
    filters: [["docstatus", "!=", 2]],

    get_indicator: function (doc) {
        if (doc.is_paid) return [__("Paid"), "green", "is_paid,=,1"];
        return [__("Unpaid"), "orange", "is_paid,=,0"];
    },
};
