frappe.listview_settings['Salary Slip'] = {
    refresh: function (listview) {

        listview.page.add_inner_button(
            __('Send Bulk E-Sign'),
            function () {

                frappe.call({
                    method: "frappe.client.get",
                    args: {
                        doctype: "Payroll Settings",
                        name: "Payroll Settings"
                    },
                    callback: function (res) {
                        if (!res.message) return;

                        let payroll_setting = res.message;
                        console.log("Payroll Settings:", payroll_setting);

                        // Collect allowed employment types
                        let employment_types = [];

                        if (payroll_setting.custom_hide_salary_structure_configuration) {
                            $.each(
                                payroll_setting.custom_hide_salary_structure_configuration,
                                function (i, v) {
                                    if (v.employment_type) {
                                        employment_types.push(v.employment_type);
                                    }
                                }
                            );
                        }

                        let dialog = new frappe.ui.Dialog({
                            title: __('Send Bulk E-Sign'),
                            fields: [
                                {
                                    fieldname: 'month',
                                    label: __('Month'),
                                    fieldtype: 'Select',
                                    options: [
                                        'January', 'February', 'March', 'April',
                                        'May', 'June', 'July', 'August',
                                        'September', 'October', 'November', 'December'
                                    ],
                                    reqd: 1
                                },
                                {
                                    fieldname: 'company',
                                    label: __('Company'),
                                    fieldtype: 'Link',
                                    options: 'Company',
                                    reqd: 1
                                },

                                {
                                    fieldname: 'payroll_period',
                                    label: __('Payroll Period'),
                                    fieldtype: 'Link',
                                    options: 'Payroll Period',
                                    reqd: 1
                                },
                                {
                                    fieldname: 'employment_type',
                                    label: __('Employment Type'),
                                    fieldtype: 'Link',
                                    options: 'Employment Type',
                                    reqd: 1,
                                    get_query: function () {
                                        return {
                                            filters: {
                                                name: ['in', employment_types]
                                            }
                                        };
                                    }
                                }
                            ],
                            primary_action_label: __('Send'),
                            primary_action(values) {

                                frappe.call({
                                    method: "cn_indian_payroll.cn_indian_payroll.overrides.leegality.send_bulk_salary_slip_for_esign",
                                    args: {
                                        month: values.month,
                                        company: values.company,
                                        employment_type: values.employment_type,
                                        payroll_period: values.payroll_period
                                    },
                                    freeze: true,
                                    callback: function (r) {
                                        if (!r.exc) {
                                            frappe.msgprint(__('Bulk e-Sign request sent successfully'));
                                            dialog.hide();
                                        }
                                    }
                                });
                            }
                        });

                        dialog.show();
                    }
                });
            }
        );
    }
};
