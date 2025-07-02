// Copyright (c) 2025, Hybrowlabs Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("LOP Reversal Request", {
	refresh(frm) {
		frm.trigger("load_lwp_months");

        if (frm.doc.docstatus === 1) {
			frm.add_custom_button("LOP Reversal", function () {
				let new_doc = frappe.model.get_new_doc("LOP Reversal");
				new_doc.employee = frm.doc.employee;
				new_doc.payroll_period = frm.doc.payroll_period;
				new_doc.company = frm.doc.company;
				new_doc.salary_slip = frm.doc.salary_slip;
				new_doc.custom_lop_reversal_request = frm.doc.name;
				// new_doc.lop_month_reversal = frm.doc.select_the_month_to_reverse;
				new_doc.number_of_days = frm.doc.number_of_days_planning_to_reverse;

				frappe.set_route("Form", "LOP Reversal", new_doc.name);
			}, __("Create"));


		}

	},

	employee(frm) {
		frm.trigger("load_lwp_months");
	},

	payroll_period(frm) {
		frm.trigger("load_lwp_months");
	},

	load_lwp_months(frm) {
		if (!(frm.doc.employee && frm.doc.payroll_period && frm.doc.company)) {
			frm.set_value("select_the_month_to_reverse", undefined);
			return;
		}

		frappe.call({
			method: "frappe.client.get_list",
			args: {
				doctype: "Salary Slip",
				filters: {
					employee: frm.doc.employee,
					docstatus: 1,
					custom_payroll_period: frm.doc.payroll_period,
					company: frm.doc.company,
				},
				fields: [
					"name",
					"absent_days",
					"leave_without_pay",
					"end_date",
					"total_working_days",
				],
			},
			callback(res) {
				let slips = res.message || [];
				let month_set = new Set();
				frm.lwp_array = [];

				slips.forEach((d) => {
					if ((d.absent_days || 0) > 0 || (d.leave_without_pay || 0) > 0) {
						let month_name = new Date(d.end_date).toLocaleString("default", {
							month: "long",
						});
						month_set.add(month_name);

						frm.lwp_array.push({
							salary_slip: d.name,
							absent_days: parseInt(d.absent_days) || 0,
							leave_without_pay: parseInt(d.leave_without_pay) || 0,
							posting_date: d.end_date,
							month_name,
							working_days: d.total_working_days,
						});
					}
				});

				frm.set_df_property(
					"select_the_month_to_reverse",
					"options",
					[""].concat([...month_set].sort()).join("\n")
				);
				frm.refresh_field("select_the_month_to_reverse");
			},
		});
	},

	select_the_month_to_reverse(frm) {

		let selected_entry = (frm.lwp_array || []).find(
			(e) => e.month_name === frm.doc.select_the_month_to_reverse
		);

		if (selected_entry) {
			frm.set_value("salary_slip", selected_entry.salary_slip);
            frm.set_value("max_days", selected_entry.leave_without_pay + selected_entry.absent_days);
		}

		if (frm.doc.days_to_reverse && frm.doc.docstatus === 0) {
			frm.set_value("days_to_reverse", 0);
		}
	},

    number_of_days_planning_to_reverse(frm) {
		let value = frm.doc.number_of_days_planning_to_reverse;
        let total = frm.doc.max_days || 0;


		if (value && value <= 0) {
			frappe.msgprint({
				title: __("Invalid Number of Days"),
				message: __("The number of days to reverse must be a positive number."),
				indicator: "red",
			});

			frm.set_value("number_of_days_planning_to_reverse", "");
		}

		if (value > total) {
			frappe.msgprint({
				title: __("Invalid Number of Days"),
				message: __(
					"The number of days planned for reversal cannot exceed the total Max days.",
				),
				indicator: "red",
			});

			frm.set_value("number_of_days_planning_to_reverse", "");
		}
	},
});
