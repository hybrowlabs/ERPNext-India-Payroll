frappe.listview_settings["Tax Declaration History"] = {
    add_fields: ["tax_regime", "payroll_period", "company", "posting_date"],
    filters: [["docstatus", "!=", 2]],

    get_indicator: function (doc) {
        const regime = doc.tax_regime || __("Unknown");
        if (doc.docstatus === 1) return [regime, "blue", "tax_regime,=," + doc.tax_regime];
        return [__("Draft"), "grey", "docstatus,=,0"];
    },
};
