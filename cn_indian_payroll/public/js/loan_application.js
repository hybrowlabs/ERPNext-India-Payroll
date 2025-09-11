frappe.ui.form.on('Loan Application', {
	refresh(frm) {
		frappe.call({
            "method": "cn_indian_payroll.cn_indian_payroll.overrides.loan_dashboard.print_loan_dashboard",
            args: {

                    employee: frm.doc.applicant

            },
            callback: function(res) {
                if (res.message && res.message) {
                   console.log(res.message)
            }
        }
    })
	}
})
