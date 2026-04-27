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
                                    fieldname: 'company',
                                    label: __('Company'),
                                    fieldtype: 'Link',
                                    options: 'Company',
                                    reqd: 1,
                                    onchange: function () {
                                            dialog.set_value('payroll_period', null);
                                            dialog.fields_dict.payroll_period.refresh();
                                        }
                                },

                                {
                                    fieldname: 'payroll_period',
                                    label: __('Payroll Period'),
                                    fieldtype: 'Link',
                                    options: 'Payroll Period',
                                    reqd: 1,
                                    get_query: function () {
                                        return {
                                            filters: {
                                                company: dialog.get_value('company')
                                            }
                                        };
                                    }
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
                                },
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

         listview.page.add_inner_button(
            __('Send Invoice to ERP'),
            function () {

                 let dialog = new frappe.ui.Dialog({
                            title: __('Send Bulk Invoice to ERP'),
                            fields: [
                                
                                {
                                    fieldname: 'company',
                                    label: __('Company'),
                                    fieldtype: 'Link',
                                    options: 'Company',
                                    reqd: 1,
                                    onchange: function () {
                                            dialog.set_value('payroll_period', null);
                                            dialog.fields_dict.payroll_period.refresh();
                                        }
                                },

                                {
                                    fieldname: 'payroll_period',
                                    label: __('Payroll Period'),
                                    fieldtype: 'Link',
                                    options: 'Payroll Period',
                                    reqd: 1,
                                    get_query: function () {
                                        return {
                                            filters: {
                                                company: dialog.get_value('company')
                                            }
                                        };
                                    }
                                },
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
                               
                            ],
                            
                            primary_action_label: __('Send'),
                            primary_action(values) {

                                frappe.call({
                                    method: "cn_indian_payroll.cn_indian_payroll.overrides.leegality.send_bulk_salary_slip_to_erp",
                                    args: {
                                        month: values.month,
                                        company: values.company,
                                        payroll_period: values.payroll_period
                                    },
                                    freeze: true,
                                    callback: function (r) {
                                        if (!r.exc) {
                                            if(r.message && r.message.status === "completed"){
                                                frappe.msgprint(__('Bulk Invoice sent to ERP successfully'));
                                            }
                                            dialog.hide();
                                        }
                                    }
                                });
                            }
                        });

                        dialog.show();




            });

    },
}


