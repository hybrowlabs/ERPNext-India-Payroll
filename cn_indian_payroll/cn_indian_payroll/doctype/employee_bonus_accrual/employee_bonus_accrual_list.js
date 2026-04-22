frappe.listview_settings["Employee Bonus Accrual"] = {
	add_fields: ["company", "payroll_period", "accrual_date", "bonus_paid_date", "is_paid"],

	get_indicator(doc) {
		if (cint(doc.is_paid)) return [__("Paid"), "green", "is_paid,=,1"];
		return [__("Unpaid"), "orange", "is_paid,=,0"];
	},

	onload(listview) {
		add_quick_filters(listview);
	},

	refresh(listview) {
		add_quick_filters(listview);
	},

	formatters: {
		accrual_date(value) {
			return format_relative_date(value);
		},
		bonus_paid_date(value) {
			return format_relative_date(value);
		},
	},
};

function add_quick_filters(listview) {
	const default_company = frappe.defaults.get_user_default("Company");

	listview.page.add_action_item(__("Unpaid"), () => {
		listview.filter_area.clear();
		listview.filter_area.add([["Employee Bonus Accrual", "is_paid", "=", 0]]);
		if (default_company) {
			listview.filter_area.add([["Employee Bonus Accrual", "company", "=", default_company]]);
		}
	});

	listview.page.add_action_item(__("Paid"), () => {
		listview.filter_area.clear();
		listview.filter_area.add([["Employee Bonus Accrual", "is_paid", "=", 1]]);
		if (default_company) {
			listview.filter_area.add([["Employee Bonus Accrual", "company", "=", default_company]]);
		}
	});

	if (default_company) {
		listview.page.add_action_item(__("My Company"), () => {
			listview.filter_area.clear();
			listview.filter_area.add([["Employee Bonus Accrual", "company", "=", default_company]]);
		});
	}
}

function format_relative_date(value) {
	if (!value) return "";
	return comment_when(`${value} 00:00:00`) || frappe.datetime.str_to_user(value);
}
