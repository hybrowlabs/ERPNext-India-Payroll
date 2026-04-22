frappe.listview_settings["New Joining Arrear"] = {
	add_fields: ["company", "posting_date", "payout_date", "docstatus", "employee_name", "payroll_period"],

	get_indicator(doc) {
		if (doc.docstatus === 0) {
			if (doc.payout_date && frappe.datetime.get_diff(doc.payout_date, frappe.datetime.nowdate()) < 0) {
				return [__("Draft (Overdue)"), "red", "docstatus,=,0"];
			}
			return [__("Draft"), "orange", "docstatus,=,0"];
		}
		if (doc.docstatus === 1) return [__("Submitted"), "green", "docstatus,=,1"];
		if (doc.docstatus === 2) return [__("Cancelled"), "red", "docstatus,=,2"];
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
		payout_date(value) {
			return format_relative_date(value);
		},
	},
};

function add_quick_filters(listview) {
	const default_company = frappe.defaults.get_user_default("Company");

	listview.page.add_action_item(__("Draft"), () => {
		listview.filter_area.clear();
		listview.filter_area.add([["New Joining Arrear", "docstatus", "=", 0]]);
		if (default_company) {
			listview.filter_area.add([["New Joining Arrear", "company", "=", default_company]]);
		}
	});

	listview.page.add_action_item(__("Submitted"), () => {
		listview.filter_area.clear();
		listview.filter_area.add([["New Joining Arrear", "docstatus", "=", 1]]);
		if (default_company) {
			listview.filter_area.add([["New Joining Arrear", "company", "=", default_company]]);
		}
	});

	if (default_company) {
		listview.page.add_action_item(__("My Company"), () => {
			listview.filter_area.clear();
			listview.filter_area.add([["New Joining Arrear", "company", "=", default_company]]);
		});
	}
}

function format_relative_date(value) {
	if (!value) return "";
	// comment_when expects datetime; Date fields can be treated as midnight.
	return comment_when(`${value} 00:00:00`) || frappe.datetime.str_to_user(value);
}
