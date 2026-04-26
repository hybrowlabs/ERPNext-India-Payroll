frappe.listview_settings["New Joining Arrear"] = {
    add_fields: ["payout_date", "docstatus"],
    filters: [["docstatus", "!=", 2]],

    get_indicator: function (doc) {
        if (doc.docstatus === 0) return [__("Draft"), "grey", "docstatus,=,0"];
        if (doc.docstatus === 1) return [__("Submitted"), "blue", "docstatus,=,1"];
    },
};
