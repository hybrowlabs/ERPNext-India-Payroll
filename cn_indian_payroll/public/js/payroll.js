frappe.ui.form.on('Payroll Entry', {
    setup(frm) {
        frappe.templates["employees_with_unmarked_attendance"] = `
{% if (data.length) { %}
<div class="form-message yellow">
    <div>
        {{
            __(
                "Attendance is pending for these employees between the selected payroll dates. Mark attendance to proceed. Refer {0} for details.",
                ["<a href='/app/query-report/Monthly%20Attendance%20Sheet'>Monthly Attendance Sheet</a>"]
            )
        }}
    </div>
</div>
<table class="table table-bordered small">
    <thead>
        <tr>
            <th style="width: 14%" class="text-left">{{ __("Employee") }}</th>
            <th style="width: 18%" class="text-left">{{ __("Employee Name") }}</th>
            <th style="width: 10%" class="text-left">{{ __("Unmarked Days") }}</th>
            <th style="width: 30%" class="text-left">{{ __("Unmarked Dates") }}</th>
        </tr>
    </thead>
    <tbody>
        {% for (var i = 0, l = data.length; i < l; i++) { %}
            <tr>
                <td class="text-left"> {{ data[i].employee }} </td>
                <td class="text-left"> {{ data[i].employee_name }} </td>
                <td class="text-left"> {{ data[i].unmarked_days }} </td>
                <td class="text-left"> {{ data[i].unmarked_dates || "" }} </td>
            </tr>
        {% } %}
    </tbody>
</table>
{% } else { %}
<div class="form-message green">
    <div>{{ __("Attendance has been marked for all the employees between the selected payroll dates.") }}</div>
</div>
{% } %}
        `;
    },

    refresh(frm)
    {
        if(frm.doc.docstatus==1 && frm.doc.status=="Submitted")
            {
                frm.add_custom_button(__("View Salary Register"),function(frm)
                {

                    frappe.set_route("query-report", "Salary Book Register");
                })
            }

            if(frm.doc.custom_bonus_payment_mode=="Bonus Payout")

                {
                    if( frm.doc.custom_additional_salary_submitted==0)
                        {

                            frm.page.clear_primary_action();

                        }

                }






        if (frm.doc.custom_bonus_payment_mode == "Bonus Payout")

            {

                if(frm.doc.custom_additional_salary_created==0 && frm.doc.custom_additional_salary_submitted==0&&frm.doc.employees.length>0)

                {

                    frm.add_custom_button(__('Create Additional Salary'), function() {

                            frappe.call({

                                method: 'cn_indian_payroll.cn_indian_payroll.overrides.additional_salary.get_additional_salary',
                                args: {
                                    payroll_id:frm.doc.name,
                                    company:frm.doc.company
                                },
                                callback: function(response) {

                                    if(response.message)
                                    {
                                        frm.set_value("custom_additional_salary_created",1)
                                        frm.save();
                                    }
                               }
                            });
                        // }
                    });

                }
        }



        if (frm.doc.custom_bonus_payment_mode == "Bonus Payout")

            {

                if(frm.doc.custom_additional_salary_created==1 &&frm.doc.custom_additional_salary_submitted==0 &&frm.doc.employees.length>0)

                {

                    frm.add_custom_button(__("Submit Additional Salary"),function()
                    {


                        frappe.call({

                            "method":"cn_indian_payroll.cn_indian_payroll.overrides.additional_salary.additional_salary_submit",
                            args:{

                                additional: frm.doc.name

                            },
                            callback :function(res)
                            {


                                        frm.set_value("custom_additional_salary_submitted",1)
                                        frm.save();

                            }

                        })

                    })




                }
            }


    },



});
