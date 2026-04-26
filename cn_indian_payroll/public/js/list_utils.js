// Shared list-view utilities for cn_indian_payroll doctypes.

/**
 * Renders a date field as a human-relative string (e.g. "3 days ago").
 * Falls back to the localised date string when the relative label is unavailable.
 * comment_when() expects a datetime string, so midnight is appended to bare dates.
 */
window.cn_payroll_format_relative_date = function (value) {
	if (!value) return "";
	return comment_when(`${value} 00:00:00`) || frappe.datetime.str_to_user(value);
};

/**
 * Adds a "My Company" quick-filter action to any list view.
 * @param {object} listview  - The Frappe list-view instance.
 * @param {string} doctype   - The DocType name used in the filter condition.
 */
window.cn_payroll_add_company_quick_filter = function (listview, doctype) {
	const default_company = frappe.defaults.get_user_default("Company");
	if (!default_company) return;

	listview.page.add_action_item(__("My Company"), () => {
		listview.filter_area.clear();
		listview.filter_area.add([[doctype, "company", "=", default_company]]);
	});
};
