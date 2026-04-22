frappe.listview_settings["Tax Declaration History"] = {
	add_fields: ["company", "payroll_period", "posting_date", "tax_regime"],

	get_indicator(doc) {
		if (doc.tax_regime) {
			return [__(doc.tax_regime), "blue", `tax_regime,=,${doc.tax_regime}`];
		}
		return [__("History"), "gray", "name,like,%"];
	},

	onload(listview) {
		add_quick_filters(listview);
	},

	refresh(listview) {
		add_quick_filters(listview);
	},

	formatters: {
		posting_date(value) {
			return format_relative_date(value);
		},
	},
};

function add_quick_filters(listview) {
	const default_company = frappe.defaults.get_user_default("Company");

	if (default_company) {
		listview.page.add_action_item(__("My Company"), () => {
			listview.filter_area.clear();
			listview.filter_area.add([["Tax Declaration History", "company", "=", default_company]]);
		});
	}
}

function format_relative_date(value) {
	if (!value) return "";
	return comment_when(`${value} 00:00:00`) || frappe.datetime.str_to_user(value);
}
