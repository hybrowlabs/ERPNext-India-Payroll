frappe.ui.form.on('Employee Promotion', {
	refresh(frm) {


        if (frm.doc.docstatus === 0) {
            if (frm.doc.custom_status === "Completed") {
                frm.page.set_primary_action(__('Submit'), () => {
                    frm.save('Submit');
                });
            } else {
                frm.page.clear_primary_action(); // removes the default button
            }
        }




        if(!frm.is_new() && frm.doc.custom_status=="In Planning")
            {

            frm.add_custom_button("Assign CTC",function()
                {
                    if(frm.doc.employee)
                    {

                    frappe.route_options = {"employee": frm.doc.employee,"custom_promotion_id":frm.doc.name};

                    frappe.set_route("Form", "Salary Structure Assignment", 'new-salary-structure-assignment');

                    }
                    else{
                        msgprint("Please select employee first")
                    }


                })

                frm.change_custom_button_type('Assign CTC', null, 'primary');

            }

            if (!frm.is_new() && frm.doc.custom_status === "Payroll Configured") {

            frm.add_custom_button("Calculate Appraisal Arrears",function()
                {
                    if (frm.doc.custom_additional_salary_date) {

                    frappe.call({
                        "method":"cn_indian_payroll.cn_indian_payroll.overrides.salary_appraisal_calculation.appraisal_calculation",
                        args:{
                            promotion_id :frm.doc.name,
                            employee_id:frm.doc.employee,
                            company:frm.doc.company,
                            date:frm.doc.custom_additional_salary_date,
                            effective_from:frm.doc.promotion_date

                        },
                        callback: function(res)
                        {




                        }
                    })

                    frm.set_value("custom_status","Arrears Calculated")
                    frm.save()

                }

                else {
                    frappe.msgprint("Please Select Additional Salary Date");
                }

                })

            }

        frm.change_custom_button_type('Calculate Appraisal Arrears', null, 'primary');

	},

    onload(frm) {
        if (frm.is_new()) {
            frm.set_value("custom_status", "In Planning");
        }
    },



    employee:function(frm)
    {
        if(frm.doc.employee)
        {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Salary Structure Assignment",
                    filters: { employee: frm.doc.employee, 'docstatus': 1 },
                    fields: ["*"],
                    limit: 1,
                    order_by: "from_date desc"
                },
                callback: function(res) {
                    if (res.message && res.message.length > 0) {
                        frm.set_value("custom_current_salary_structure_reference",res.message[0].name)
                        frm.set_value("custom_current_effective_from_date",res.message[0].from_date)
                        frm.set_value("current_ctc",res.message[0].base)
                        frm.set_value("custom_current_structure",res.message[0].salary_structure)
                    }

                    }
                })

        }
    }



})
