frappe.pages['payroll-configuratio'].on_page_load = function(wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Component Library',
        single_column: true,
    });

    // Add CSS to make all rows white
    $('<style>').text(`
        table.table tbody tr {
            background-color: white !important;
        }
    `).appendTo('head');

    const container = $('<div>').appendTo(page.main);
    const table = $('<table class="table table-bordered">').appendTo(container);
    const thead = $('<thead>').appendTo(table);
    const tbody = $('<tbody>').appendTo(table);

    $('<tr>')
        .append('<th>Salary Component</th>')
        .append('<th>Abbr</th>')
        .append('<th>Condition</th>')
        .append('<th>Formula</th>')
        .append('<th>Action</th>')
        .appendTo(thead);

    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Salary Component Library Item",
            filters: { "disabled": 0 },
            fields: ["*"],
			limit_page_length: 0  // <- this returns all records
        },
        callback: function(res) {
            if (res.message && res.message.length > 0) {
                var data = res.message;
                data.sort((a, b) => Number(a.sequence) - Number(b.sequence));

                data.forEach(function(item) {
                    const row = $('<tr>').appendTo(tbody).css("background-color", "white");

                    const isComponentEditable = item.multi_select === 1;
                    const isFieldsEditable = item.visibility_type === "Not Fixed";

                    const componentInput = $('<input>', {
                        type: 'text',
                        class: 'form-control',
                        value: item.salary_component,
                        readonly: !isComponentEditable
                    }).appendTo($('<td>').appendTo(row));

                    const abbrInput = $('<input>', {
                        type: 'text',
                        class: 'form-control',
                        value: item.abbr || "",
                        readonly: !isComponentEditable
                    }).appendTo($('<td>').appendTo(row));

                    const conditionInput = $('<input>', {
                        type: 'text',
                        class: 'form-control',
                        value: isFieldsEditable ? item.condition || "" : item.condition,
                        readonly: !isFieldsEditable,
                        style: isFieldsEditable ? "" : "background-color: #f0f0f0; color: #888;"
                    }).appendTo($('<td>').appendTo(row));

                    const formulaInput = $('<input>', {
                        type: 'text',
                        class: 'form-control',
                        value: isFieldsEditable ? item.formula || "" : item.formula,
                        readonly: !isFieldsEditable,
                        style: isFieldsEditable ? "" : "background-color: #f0f0f0; color: #888;"
                    }).appendTo($('<td>').appendTo(row));

                    const addButton = $('<button>', {
                        text: 'Add',
                        class: 'btn btn-success',
                        click: function () {
                            const rowData = {
                                salary_component: componentInput.val(),
                                abbr: abbrInput.val(),
                                condition: conditionInput.val(),
                                formula: formulaInput.val(),

                                depends_on_payment_days: item.depends_on_payment_days,
                                is_tax_applicable: item.is_tax_applicable,
                                round_to_the_nearest_integer: item.round_to_the_nearest_integer,
                                do_not_include_in_total: item.do_not_include_in_total,
                                remove_if_zero_valued: item.remove_if_zero_valued,
                                is_part_of_gross_pay: item.is_part_of_gross_pay,
                                disabled: item.disabled,
                                is_part_of_ctc: item.is_part_of_ctc,
                                perquisite: item.perquisite,
                                is_accrual: item.is_accrual,
                                type: item.component_type,
                                reimbursement: item.is_reimbursement,
                                component_type: item.type,
                                is_arrear: item.is_arrear,
                                component: item.component,
                                is_part_of_appraisal: item.is_part_of_appraisal,
                                tax_applicable_based_on_regime: item.tax_applicable_based_on_regime,
                                regime: item.regime,
                                multi_insert: item.multi_select,
                                sequence: item.sequence,
								visibility_type: item.visibility_type,
								multi_select: item.multi_select,
                            };

							console.log("Row Data: ", rowData);

                            const salary_component_array = [{
                                component: rowData.salary_component,
                                abbr: rowData.abbr,
                                type: rowData.component_type,
                                formula: rowData.formula,
                                condition: rowData.condition
                            }];

                            if (rowData.is_arrear) {
                                salary_component_array.push({
                                    component: `${rowData.salary_component}(Arrear)`,
                                    abbr: `${rowData.abbr}Arrear`,
                                    type: rowData.component_type,
                                    formula: "",
                                    condition: ""
                                });
                            }

                            let custom_field = [];
                            const Child_custom_field = [];

                            if (rowData.multi_insert == 1) {
                                custom_field = [
                                    {
                                        doctype: "Salary Structure Assignment",
                                        label: rowData.salary_component,
                                        field_type: "Check",
                                        field_name: rowData.salary_component.toLowerCase().replace(/[^a-z]/g, '') + rowData.abbr.toLowerCase().replace(/[^a-z]/g, ''),
                                        depends: "",
                                        insert_after: "custom_allowances",
                                    },
                                    {
                                        doctype: "Salary Structure Assignment",
                                        label: `${rowData.salary_component} Value`,
                                        field_type: "Data",
                                        field_name: `${rowData.salary_component.toLowerCase().replace(/[^a-z]/g, '')}${rowData.abbr.toLowerCase().replace(/[^a-z]/g, '')}_value`,
                                        depends: rowData.salary_component.toLowerCase().replace(/[^a-z]/g, '') + rowData.abbr.toLowerCase().replace(/[^a-z]/g, ''),
                                        insert_after: rowData.salary_component.toLowerCase().replace(/[^a-z]/g, '') + rowData.abbr.toLowerCase().replace(/[^a-z]/g, ''),
                                    }
                                ];
                            }

                            function callCreateComponentAPI() {
                                frappe.call({
                                    method: "cn_indian_payroll.cn_indian_payroll.overrides.payroll_configuration.get_salary_component",
                                    args: {
                                        data: rowData,
                                        component: salary_component_array,
                                        custom_field: custom_field.concat(Child_custom_field),
                                    },
                                    callback: function (response) {
                                        if (response && response.exc) {
                                            frappe.msgprint(__('Server returned an error: ') + response.exc);
                                        } else {
                                            frappe.msgprint(__('Component added successfully.'));

											if(rowData.visibility_type=="Fixed" && rowData.multi_insert == 0) {


												addButton.prop('disabled', true).text('Added');

											}


                                        }
                                    },
                                    error: function (err) {
                                        console.error("API call error:", err);
                                        frappe.msgprint(__('Failed to add component. Please check console.'));
                                    }
                                });
                            }

                            if (rowData.multi_insert !== 1) {
                                frappe.call({
                                    method: "frappe.client.get",
                                    args: {
                                        doctype: "Salary Component Library Item",
                                        filters: { "name": rowData.salary_component },
                                        fields: ["name", "custom_field_child"],
                                    },
                                    callback: function (current_res) {
                                        if (current_res.message && Array.isArray(current_res.message.custom_field_child)) {
                                            $.each(current_res.message.custom_field_child, function (i, v) {
                                                Child_custom_field.push({
                                                    doctype: v.dt,
                                                    label: v.label,
                                                    field_name: v.field_name,
                                                    field_type: v.type,
                                                    depends: v.depends_on,
                                                    insert_after: v.insert_after,
                                                });
                                            });
                                        }
                                        callCreateComponentAPI();
                                    }
                                });
                            } else {
                                callCreateComponentAPI();
                            }
                        }
                    });

                    if (item.component_added == 1 &&  item.multi_select == 0) {
                        addButton.prop('disabled', true).text('Added');
                    }

                    $('<td>').append(addButton).appendTo(row);
                });
            }
        }
    });
};
