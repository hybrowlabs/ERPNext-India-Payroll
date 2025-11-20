

frappe.ui.form.on('Salary Structure Assignment', {


    refresh(frm)
    {
        if(frm.doc.docstatus==1)

        {

        frm.add_custom_button(__('View CTC BreakUp'), async function() {
            frappe.call({
                method: "cn_indian_payroll.cn_indian_payroll.overrides.salary_structure_assignment.generate_ctc_pdf",
                args: {
                    employee: frm.doc.employee,
                    salary_structure: frm.doc.salary_structure,
                    print_format: 'Salary Slip Standard',
                    posting_date: frm.doc.from_date,
                    employee_benefits: frm.doc.employee_benefits
                },
                callback: function(r) {
                    if (r.message && r.message.pdf_url) {
                        window.open(r.message.pdf_url, '_blank');
                    } else {
                        frappe.msgprint("Failed to generate PDF");
                    }
                }
            });
        }, __('Actions'));


        }

        frm.set_query("custom_lwf_state", function() {
            return {
                filters: {
                    lwf_frequency: 1
                }
            };
        });



    },


    custom_lwf_state: function(frm) {
        if (frm.doc.custom_lwf_state) {
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "State",
                    name: frm.doc.custom_lwf_state
                },
                callback: function(res) {
                    if (res.message && res.message.lwf_frequency_list) {
                        let frequency_array = res.message.lwf_frequency_list.map(row => row.frequency_type);
                        frm.set_value("custom_frequency", frequency_array[0]);
                        frm.set_query("custom_frequency", function() {
                            return {
                                filters: {
                                    name: ["in", frequency_array]
                                }
                            };
                        });
                    }
                }
            });
        }
    },

})
