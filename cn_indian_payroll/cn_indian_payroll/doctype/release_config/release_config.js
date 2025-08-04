frappe.ui.form.on("Release Config", {
    refresh: function (frm) {
        if (frm.fields_dict.date_config) {
            frm.fields_dict.date_config.$wrapper.html(`
                <div style="display: grid; grid-template-columns: 1fr 1fr auto; gap: 20px; align-items: end; width: 100%; max-width: 100%; margin-bottom: 20px;">
                    <div>
                        <label for="start_date"><strong>Start Date:</strong></label>
                        <input type="date" id="start_date" class="form-control">
                    </div>
                    <div>
                        <label for="end_date"><strong>End Date:</strong></label>
                        <input type="date" id="end_date" class="form-control">
                    </div>
                    <div>
                        <button class="btn btn-primary" id="apply_btn" style="margin-top: 8px; width: 100%;">Apply</button>
                    </div>
                </div>
            `);

            $('#apply_btn').click(function () {
                const start = $('#start_date').val();
                const end = $('#end_date').val();

                if (!start || !end) {
                    frappe.msgprint("Please select both start and end dates.");
                    return;
                }

                frappe.call({
                    method: "cn_indian_payroll.cn_indian_payroll.overrides.release_config.get_date_format",
                    args: {
                        start_date: start,
                        end_date: end,
                        payroll_period: frm.doc.payroll_period,
                        docname: frm.doc.name
                    },
                    callback: function (res) {
                        frappe.msgprint("Child table updated successfully.");
                        frm.reload_doc();
                    }
                });
            });
        }

        frm.fields_dict['locking_period_months'].grid.wrapper.find('.grid-add-row').hide();

    }
});
