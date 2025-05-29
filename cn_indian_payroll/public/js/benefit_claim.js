frappe.ui.form.on('Employee Benefit Claim', {


    claimed_amount: function(frm) {
        if (frm.doc.claimed_amount > frm.doc.custom_max_amount) {
            frm.set_value("claimed_amount", undefined);
            frappe.msgprint("You can't enter an amount greater than the eligible amount.");
        }
    },


    claim_date:function(frm)
    {
        get_employee_details(frm);

    },

    employee: function(frm) {
        get_employee_details(frm);
    },

    earning_component: function(frm) {

        get_max_amount(frm);


    },

        // claim_date: function(frm) {
    //     if (frm.doc.claim_date < frappe.datetime.now_date()) {
    //         frm.set_value("claim_date", undefined);
    //         frappe.msgprint(__('Claim date cannot be in the past.'));
    //     }
    // }
});

// Define get_employee_details as a global function
function get_employee_details(frm) {
    if (frm.doc.employee) {
        frappe.call({
            method: "cn_indian_payroll.cn_indian_payroll.overrides.benefit_claim.benefit_claim",
            args: {
                doc: frm.doc
            },
            callback: function(r) {
                if (r.message) {
                    let component_array = r.message.component_array || [];
                    let payroll_period = r.message.payroll_period;

                    frm.set_value("custom_payroll_period", payroll_period);

                    if (component_array.length > 0) {
                        frm.set_query("earning_component", function() {
                            return {
                                filters: { name: ["in", component_array] }
                            };
                        });
                    } else {
                        frm.set_query("earning_component", function() {
                            return {
                                filters: { name: ["in", []] }  // Empty list fallback
                            };
                        });
                    }
                }
            }
        });
    }
}


function get_max_amount(frm)
{
    if (frm.doc.employee) {
        frappe.call({
            method: "cn_indian_payroll.cn_indian_payroll.overrides.benefit_claim.get_max_amount",
            args: {
                doc: frm.doc
            },
            callback: function(response) {
                if (response.message) {

                    let amount = response.message;
                    frm.set_value("custom_max_amount", amount);
                }
            }
        });
    }
}
