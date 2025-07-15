frappe.ui.form.on("LOP Reversal", {
	lwp_array: [],

	refresh(frm) {
		frm.trigger("load_lwp_months");
	},
	employee(frm) {
		frm.trigger("load_lwp_months");
	},
	payroll_period(frm) {
		frm.trigger("load_lwp_months");
	},

	load_lwp_months(frm) {
		if (!(frm.doc.employee && frm.doc.payroll_period && frm.doc.company)) {
			frm.set_value("lop_month_reversal", undefined);
			[
				"salary_slip",
				"absent_days",
				"working_days",
				"lop_days",
				"max_lop_days",
			].forEach((f) => frm.set_value(f, undefined));
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
					"lop_month_reversal",
					"options",
					[""].concat([...month_set].sort()).join("\n"),
				);
				frm.refresh_field("lop_month_reversal");
			},
		});
	},

	lop_month_reversal(frm) {
		let selected_entry = frm.lwp_array.find(
			(e) => e.month_name === frm.doc.lop_month_reversal,
		);

		if (selected_entry) {
			frm.set_value("salary_slip", selected_entry.salary_slip);
			frm.set_value("absent_days", selected_entry.absent_days);
			frm.set_value("working_days", selected_entry.working_days);
			frm.set_value("lop_days", selected_entry.leave_without_pay);
			frm.set_value(
				"max_lop_days",
				selected_entry.absent_days + selected_entry.leave_without_pay,
			);
		}

		if (frm.doc.days_to_reverse && frm.doc.docstatus === 0) {
			frm.set_value("days_to_reverse", 0);
		}
	},

	days_to_reverse(frm) {
		let value = frm.doc.days_to_reverse;
		let total = frm.doc.max_lop_days || 0;

		if (value && value <= 0) {
			frappe.msgprint({
				title: __("Invalid Number of Days"),
				message: __("The number of days to reverse must be a positive number."),
				indicator: "red",
			});

			frm.set_value("days_to_reverse", "");
		}

		if (value > total) {
			frappe.msgprint({
				title: __("Invalid Number of Days"),
				message: __(
					"The number of days planned for reversal cannot exceed the total LWP days.",
				),
				indicator: "red",
			});

			frm.set_value("days_to_reverse", "");
		}
	},
});
