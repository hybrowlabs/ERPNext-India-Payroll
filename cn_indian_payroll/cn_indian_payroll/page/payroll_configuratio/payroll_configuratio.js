
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

    // Create a container to hold the table
    const container = $('<div>').appendTo(page.main);

    // Create the table element
    const table = $('<table class="table table-bordered">').appendTo(container);
    const thead = $('<thead>').appendTo(table);
    const tbody = $('<tbody>').appendTo(table);

    // Create the table header
    $('<tr>')
        .append('<th>Salary Component</th>')
        .append('<th>Abbr</th>')  
        .append('<th>Condition</th>')
        .append('<th>Formula</th>')
        .append('<th>Action</th>')  
        .appendTo(thead);

    // Fetch data from "Payroll Configuration"
    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Salary Component Library Item",
            filters: { "disabled": 0 },
            fields: ["*"],
            // order_by: "sequence asc" 
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

                    // Create the Add button
                    const addButton = $('<button>', {
                        text: 'Add',
                        class: 'btn btn-success',
                        click: function() {
                            const rowData = {
                                salary_component: componentInput.val(),
                                abbr: abbrInput.val(),
                                condition: conditionInput.val(),
                                formula: formulaInput.val(),
                                

								depends_on_payment_days:item.depends_on_payment_days,
								is_tax_applicable:item.is_tax_applicable,
								round_to_the_nearest_integer:item.round_to_the_nearest_integer,
								do_not_include_in_total:item.do_not_include_in_total,
								remove_if_zero_valued:item.remove_if_zero_valued,
								is_part_of_gross_pay:item.is_part_of_gross_pay,
								disabled:item.disabled,
								is_part_of_ctc:item.is_part_of_ctc,
								perquisite: item.perquisite,
								is_accrual: item.is_accrual,
								type: item.component_type,
								reimbursement: item.is_reimbursement,
                                component_type: item.type,
								is_arrear:item.is_arrear,
								component:item.component,
								is_part_of_appraisal:item.is_part_of_appraisal,
								tax_applicable_based_on_regime:item.tax_applicable_based_on_regime,
								regime:item.regime,
								multi_insert:item.multi_select,
								sequence:item.sequence,
                                
                                
                            };

							

							let Child_custom_field = [];
							const custom_field = [];

							const salary_component_array = []; 

							salary_component_array.push({
								"component": rowData.salary_component,
								"abbr":rowData.abbr,
								"type":rowData.component_type,
								"formula":rowData.formula,
								"condition":rowData.condition
							});

							if(rowData.is_arrear)
							{
								salary_component_array.push({
									"component": `${rowData.salary_component}(Arrear)`,
									"abbr": `${rowData.abbr}Arrear`,
									"type":rowData.component_type,
									"formula":"",
									"condition":""
								});

							}

							
							
							if (rowData.multi_insert == 1) {
								custom_field = [
									{
										doctype: "Salary Structure Assignment",
										label: rowData.salary_component,
										field_type: "Check",
										field_name: rowData.salary_component.toLowerCase().replace(/[^a-z]/g, '')+ rowData.abbr.toLowerCase().replace(/[^a-z]/g, ''),
										depends: "",
										insert_after: "custom_allowances",
									},
									{
										doctype: "Salary Structure Assignment",
										label: `${rowData.salary_component} Value`,
										field_type: "Data",
										field_name: `${rowData.salary_component.toLowerCase().replace(/[^a-z]/g, '')}${rowData.abbr.toLowerCase().replace(/[^a-z]/g, '')}_value`,										depends: rowData.salary_component.toLowerCase().replace(/[^a-z]/g, '')+ rowData.abbr.toLowerCase().replace(/[^a-z]/g, ''),
										insert_after: rowData.salary_component.toLowerCase().replace(/[^a-z]/g, '')+ rowData.abbr.toLowerCase().replace(/[^a-z]/g, ''),
									}
								];
								
							}
							
							if (rowData.multi_insert !== 1) {
								frappe.call({
									method: "frappe.client.get",
									args: {
										doctype: "Salary Component Library Item",
										filters: { "name": rowData.salary_component },
										fields: ["name"],
									},
									callback: function (current_res) {
										if (current_res.message) {
											try {
												if (Array.isArray(current_res.message.custom_field_child) && current_res.message.custom_field_child.length > 0) {
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
											} catch (error) {
												console.error("Error processing child fields:", error);
												frappe.msgprint(__('Failed to process child fields. Please check console for details.'));
											}
										} else {
											frappe.msgprint(__('No data received from the server.'));
										}
							
										// Now create the dialog after fetching child fields
										createAndShowDialog();
									},
									error: function (err) {
										console.error("Server error:", err);
										frappe.msgprint(__('Failed to fetch data. Please try again later.'));
									},
								});
							}
							
							
							
							else 
							
							{
								// If multi_insert is 1, no need to fetch, create the dialog immediately
								createAndShowDialog();
							}


							
							function createAndShowDialog() {
							
							
								const dialogFields = [
									
									{
										label: 'The following components have been added to the salary component.',
										fieldname: 'heading',
										fieldtype: 'Heading',
									},
									{
										label: 'Salary Component Details',
										fieldname: 'salary_components_table',
										fieldtype: 'Table',
										cannot_add_rows: 1,
										in_place_edit: 0,
										fields: [
											{ label: 'Salary Component', fieldname: 'salary_component', fieldtype: 'Data', in_list_view: 1, read_only: 1 },
											{ label: 'Abbreviation', fieldname: 'abbr', fieldtype: 'Data', in_list_view: 1, read_only: 1 },
											{ label: 'Type', fieldname: 'type', fieldtype: 'Select', options: 'Earning\nDeduction', in_list_view: 1, read_only: 1 },
											{ label: 'Formula', fieldname: 'formula', fieldtype: 'Data', in_list_view: 1, read_only: 1 },
											{ label: 'Condition', fieldname: 'condition', fieldtype: 'Data', in_list_view: 1, read_only: 1 }
										]
									}
								];
							
								if (custom_field.length > 0 || Child_custom_field.length > 0) {
									dialogFields.push(
										
										{
											label: 'The following custom fields have been added to the Salary Structure Assignment',
											fieldname: 'custom_field_heading',
											fieldtype: 'Heading',
										},
										{
											label: 'Custom Field Details',
											fieldname: 'custom_field_table',
											fieldtype: 'Table',
											cannot_add_rows: 1,
											in_place_edit: 0,
											fields: [
												{ label: 'Doctype', fieldname: 'doctype', fieldtype: 'Data', in_list_view: 1, read_only: 1 },
												{ label: 'Label', fieldname: 'label', fieldtype: 'Data', in_list_view: 1, read_only: 1 },
												{ label: 'Field Name', fieldname: 'field_name', fieldtype: 'Data', in_list_view: 1, read_only: 1 },
												{ label: 'Field Type', fieldname: 'field_type', fieldtype: 'Data', in_list_view: 1, read_only: 1 },
												{ label: 'Depends', fieldname: 'depends', fieldtype: 'Data', in_list_view: 1, read_only: 1 },
												{ label: 'insert after', fieldname: 'insert_after', fieldtype: 'Data', hidden: 1, read_only: 1 }
											]
										}
									);
								}
							
								let d = new frappe.ui.Dialog({
									title: 'Follow The Details',
									fields: dialogFields,
									size: 'large',
									primary_action_label: 'Submit',
									primary_action(values) {
										



										frappe.call({
                                        method: "cn_indian_payroll.cn_indian_payroll.overrides.payroll_configuration.get_salary_component",
                                        args: {
                                            data: rowData,
                                            component: values.salary_components_table,
                                            custom_field: values.custom_field_table,
                                        },
										callback:function(response)
										{

											 if(response && response.exc) {
												     frappe.msgprint(__('Server returned an error: ') + response.exc);
												   } else {
												     frappe.msgprint(__('Operation completed successfully.'));
												   }

										}
                                    });










										d.hide();
									}
								});
							
								d.show();
							
								let tableField = d.fields_dict.salary_components_table;
								if (!tableField.df.data) {
									tableField.df.data = [];
								}

								

								if (salary_component_array.length > 0) {
									salary_component_array.forEach(field => {
										tableField.df.data.push({
											salary_component: field.component,
											abbr: field.abbr,
											type: field.type,
											formula: field.formula,
											condition: field.condition,
										});
									});
									tableField.grid.refresh();
								}


							
								let CustomtableField = d.fields_dict.custom_field_table;
								if (!CustomtableField.df.data) {
									CustomtableField.df.data = [];
								}
							
								if (custom_field.length > 0) {
									custom_field.forEach(field => {
										CustomtableField.df.data.push({
											doctype: field.doctype,
											label: field.label,
											field_name: field.field_name,
											field_type: field.field_type,
											depends: field.depends,
											insert_after:field.insert_after,
										});
									});
									CustomtableField.grid.refresh();
								}
							
								if (Child_custom_field.length > 0) {
									Child_custom_field.forEach(field => {
										CustomtableField.df.data.push({
											doctype: field.doctype,
											label: field.label,
											field_name: field.field_name,
											field_type: field.field_type,
											depends: field.depends,
											insert_after:field.insert_after,
											
										});
									});
									CustomtableField.grid.refresh();
								}
							}
							
							
							
							
							





   
                        }
                    });

                    // Disable the button initially if the component is already added
                    if (item.component_added == 1) {
                        addButton.prop('disabled', true).text('Added');
                    }

                    // Append the button to the row
                    $('<td>').append(addButton).appendTo(row);



				
                });

				
            }
        }
    });
};




							



									
									
		



