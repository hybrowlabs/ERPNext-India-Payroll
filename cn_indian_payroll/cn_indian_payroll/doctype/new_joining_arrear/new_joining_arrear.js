frappe.ui.form.on("New Joining Arrear", {
	refresh(frm) {
        if(frm.is_new())
        {
		frappe.call({
			method: "frappe.client.get",
			args: {
				doctype: "Payroll Settings"
			},
			callback: function (res) {
				if (res.message && res.message.payroll_based_on) {
					let message = "";
					if (res.message.payroll_based_on === "Attendance") {
						message = "You can mention the future or advance days from attendance cycle end date to month end days.";
					} else if (res.message.payroll_based_on === "Leave") {
						message = "You can mention the present days from joining day to month end day.";
					}

					const styledMessage = `
						<div style="
							font-weight: bold;
							font-size: 16px;
							background-color: #fffae6;
							color: #333;
							padding: 10px;
							border-left: 4px solid #facc15;
							border-radius: 4px;
						">
							${message}
						</div>
					`;

					frm.set_df_property("description", "options", styledMessage);
					frm.refresh_field("description");
				}
			}
		});
    }
	}
});
