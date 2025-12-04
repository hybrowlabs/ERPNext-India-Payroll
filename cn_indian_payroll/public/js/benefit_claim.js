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

    refresh: function(frm) {
       if(frm.doc.docstatus==1)
       {
        frm.add_custom_button("Benefit Payslip", function () {
            if (!frm.doc.employee || !frm.doc.custom_payroll_period) {
                frappe.msgprint(__('Please set Employee and Payroll Period first.'));
                return;
            }

            frappe.call({
                method: "cn_indian_payroll.cn_indian_payroll.overrides.tds_printer.get_benefit_payslip_pdf",
                args: {
                    id: frm.doc.name
                },
                callback: function (r) {
                    if (!r.message || !r.message.html) {
                        frappe.msgprint(__('No HTML generated'));
                        return;
                    }
                    const w = window.open("", "_blank");
                    w.document.open();
                    w.document.write(r.message.html);
                    w.document.close();
                }
            });
        });
       }
    },

    // claim_date: function(frm) {
    //     if (frm.doc.claim_date < frappe.datetime.now_date()) {
    //         frm.set_value("claim_date", undefined);
    //         frappe.msgprint(__('Claim date cannot be in the past.'));
    //     }
    // }
});

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
                                filters: { name: ["in", []] }
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

                    console.log(response.message,"44444444444444")

                    let amount = response.message[0].value;
                    frm.set_value("custom_max_amount", amount);
                }
            }
        });
    }
}
