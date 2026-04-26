frappe.listview_settings["Tax Declaration History"] = {
	add_fields: ["company", "payroll_period", "posting_date", "tax_regime"],

	get_indicator(doc) {
		if (doc.tax_regime) {
			return [__(doc.tax_regime), "blue", `tax_regime,=,${doc.tax_regime}`];
		}
		return [__("History"), "gray", "name,like,%"];
	},

	onload(listview) {
		cn_payroll_add_company_quick_filter(listview, "Tax Declaration History");
	},

	refresh(listview) {
		cn_payroll_add_company_quick_filter(listview, "Tax Declaration History");
	},

	formatters: {
		posting_date(value) {
			return cn_payroll_format_relative_date(value);
		},
	},
};
