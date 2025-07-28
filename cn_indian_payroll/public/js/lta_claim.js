

frappe.ui.form.on('LTA Claim', {

    employee: function(frm) {
        if (frm.doc.employee) {

            find_tax_regime(frm)
            get_max_amount(frm)


        }
    },

    amount:function(frm)
    {
        if(frm.doc.amount>frm.doc.max_eligible_amount)
        {
            frm.set_value("amount",undefined)
            msgprint("you cant enter amount greater than eligible amount")
        }
    },


    claim_date: function(frm) {
        get_max_amount(frm)


        // if (frm.doc.claim_date && frm.doc.claim_date <frappe.datetime.now_date()) {
        //     frm.set_value("claim_date", null);
        //     frappe.msgprint(__("You can't select a past date."));
        // }
    }





});


function find_tax_regime(frm)
{
    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Salary Structure Assignment",
            filters: { employee: frm.doc.employee, docstatus: 1,from_date: ["<=", frm.doc.claim_date] },
            fields: ["*"],
            order_by: "from_date desc",
            limit: 1
        },
        callback: function(response) {
            if (response.message && response.message.length > 0) {

                frm.set_value("income_tax_regime",response.message[0].custom_tax_regime)

            }
        }
    })

}


function get_max_amount(frm) {
    if (frm.doc.employee) {
        frappe.call({
            method: "cn_indian_payroll.cn_indian_payroll.overrides.lta_claim.get_max_amount",
            args: {
                doc: frm.doc
            },
            callback: function (r) {
                if (r.message) {
                    frm.set_value("max_eligible_amount", r.message.max_amount);
                    frm.set_value("payroll_period", r.message.payroll_period);
                }
            }
        });
    }
}
