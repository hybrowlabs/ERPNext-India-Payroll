// frappe.pages['payroll-configuratio'].on_page_load = function(wrapper) {
//     var page = frappe.ui.make_app_page({
//         parent: wrapper,
//         title: 'Payroll Configuration',
//         single_column: true
//     });

//     // Add CSS to make all rows white
//     $('<style>').text(`
//         table.table tbody tr {
//             background-color: white !important;
//         }
//     `).appendTo('head');

//     // Create a container to hold the table
//     var container = $('<div>').appendTo(page.main);

//     // Create the table element
//     var table = $('<table class="table table-bordered">').appendTo(container);
//     var thead = $('<thead>').appendTo(table);
//     var tbody = $('<tbody>').appendTo(table);

//     // Create the table header
//     $('<tr>')
//         .append('<th>Salary Component</th>')
//         .append('<th>Abbr</th>')  
//         .append('<th>Condition</th>')
//         .append('<th>Formula</th>')
//         .append('<th>Action</th>')  
//         .appendTo(thead);

//     // Fetch data from "Payroll Configuration"
//     frappe.call({
//         method: "frappe.client.get",
//         args: {
//             doctype: "Payroll Configuration",
//             fields: ["salary_component_configuration"]
//         },
//         callback: function(res) {
//             if (res.message && res.message.salary_component_configuration) {
//                 var data = res.message.salary_component_configuration;

//                 data.forEach(function(item) {
//                     var row = $('<tr>').appendTo(tbody).css("background-color", "white"); // Ensure white background

//                     var isComponentEditable = item.multi_select == 1;
//                     var isFieldsEditable = item.type === "Not Fixed";

//                     var componentInput = $('<input>', {
//                         type: 'text',
//                         class: 'form-control',
//                         value: item.salary_component,
//                         readonly: !isComponentEditable
//                     }).appendTo($('<td>').appendTo(row));

//                     var abbrInput = $('<input>', {
//                         type: 'text',
//                         class: 'form-control',
//                         value: item.abbr || "",
//                         readonly: !isComponentEditable
//                     }).appendTo($('<td>').appendTo(row));

//                     var conditionInput = $('<input>', {
//                         type: 'text',
//                         class: 'form-control',
//                         value: item.condition || "",
//                         readonly: !isFieldsEditable
//                     }).appendTo($('<td>').appendTo(row));

//                     var formulaInput = $('<input>', {
//                         type: 'text',
//                         class: 'form-control',
//                         value: item.formula || "",
//                         readonly: !isFieldsEditable
//                     }).appendTo($('<td>').appendTo(row));

//                     var addButton = $('<button>', {
//                         text: 'Add',
//                         class: 'btn btn-success',
//                         click: function() {
//                             var rowData = {
//                                 salary_component: componentInput.val(),
//                                 abbr: abbrInput.val(),
//                                 condition: conditionInput.val(),
//                                 formula: formulaInput.val(),
//                             };
//                             console.log(rowData);
//                         }
//                     }).appendTo($('<td>').appendTo(row));
//                 });
//             }
//         }
//     });
// };


// frappe.pages['payroll-configuratio'].on_page_load = function(wrapper) {
//     var page = frappe.ui.make_app_page({
//         parent: wrapper,
//         title: 'Payroll Configuration',
//         single_column: true
//     });

//     // Add CSS to make all rows white
//     $('<style>').text(`
//         table.table tbody tr {
//             background-color: white !important;
//         }
//     `).appendTo('head');

//     // Create a container to hold the table
//     var container = $('<div>').appendTo(page.main);

//     // Create the table element
//     var table = $('<table class="table table-bordered">').appendTo(container);
//     var thead = $('<thead>').appendTo(table);
//     var tbody = $('<tbody>').appendTo(table);

//     // Create the table header
//     $('<tr>')
//         .append('<th>Salary Component</th>')
//         .append('<th>Abbr</th>')  
//         .append('<th>Condition</th>')
//         .append('<th>Formula</th>')
//         .append('<th>Action</th>')  
		
//         .appendTo(thead);

//     // Fetch data from "Payroll Configuration"
//     frappe.call({
//         method: "frappe.client.get",
//         args: {
//             doctype: "Payroll Configuration",
//             fields: ["salary_component_configuration"]
//         },
//         callback: function(res) {
//             if (res.message && res.message.salary_component_configuration) {
//                 var data = res.message.salary_component_configuration;

//                 data.forEach(function(item) {
//                     var row = $('<tr>').appendTo(tbody).css("background-color", "white"); // Ensure white background

//                     var isComponentEditable = item.multi_select == 1;
//                     var isFieldsEditable = item.type === "Not Fixed";

//                     var componentInput = $('<input>', {
//                         type: 'text',
//                         class: 'form-control',
//                         value: item.salary_component,
//                         readonly: !isComponentEditable
//                     }).appendTo($('<td>').appendTo(row));

//                     var abbrInput = $('<input>', {
//                         type: 'text',
//                         class: 'form-control',
//                         value: item.abbr || "",
//                         readonly: !isComponentEditable
//                     }).appendTo($('<td>').appendTo(row));

//                     var conditionInput;
//                     if (isFieldsEditable) {
//                         conditionInput = $('<input>', {
//                             type: 'text',
//                             class: 'form-control',
//                             value: item.condition || ""
//                         });
//                     } else {
//                         conditionInput = $('<input>', {
//                             type: 'text',
//                             class: 'form-control',
//                             value: "Already Configured",
//                             readonly: true,
//                             style: "background-color: #f0f0f0; color: #888;"
//                         });
//                     }
//                     $('<td>').append(conditionInput).appendTo(row);

//                     var formulaInput;
//                     if (isFieldsEditable) {
//                         formulaInput = $('<input>', {
//                             type: 'text',
//                             class: 'form-control',
//                             value: item.formula || ""
//                         });
//                     } else {
//                         formulaInput = $('<input>', {
//                             type: 'text',
//                             class: 'form-control',
//                             value: "Already Configured",
//                             readonly: true,
//                             style: "background-color: #f0f0f0; color: #888;"
//                         });
//                     }
//                     $('<td>').append(formulaInput).appendTo(row);

//                     var addButton = $('<button>', {
//                         text: 'Add',
//                         class: 'btn btn-success',
//                         click: function() {
//                             var rowData = {
//                                 salary_component: componentInput.val(),
//                                 abbr: abbrInput.val(),
//                                 condition: conditionInput.val(),
//                                 formula: formulaInput.val(),
								
//                             };
//                             console.log(rowData);
//                         }
//                     }).appendTo($('<td>').appendTo(row));
//                 });
//             }
//         }
//     });
// };



// frappe.pages['payroll-configuratio'].on_page_load = function(wrapper) {
//     var page = frappe.ui.make_app_page({
//         parent: wrapper,
//         title: 'Payroll Configuration',
//         single_column: true
//     });

//     // Add CSS to make all rows white
//     $('<style>').text(`
//         table.table tbody tr {
//             background-color: white !important;
//         }
//     `).appendTo('head');

//     // Create a container to hold the table
//     var container = $('<div>').appendTo(page.main);

//     // Create the table element
//     var table = $('<table class="table table-bordered">').appendTo(container);
//     var thead = $('<thead>').appendTo(table);
//     var tbody = $('<tbody>').appendTo(table);

//     // Create the table header
//     $('<tr>')
//         .append('<th>Salary Component</th>')
//         .append('<th>Abbr</th>')  
//         .append('<th>Condition</th>')
//         .append('<th>Formula</th>')
//         .append('<th>Action</th>')  
//         .appendTo(thead);

//     // Fetch data from "Payroll Configuration"
//     frappe.call({
//         method: "frappe.client.get",
//         args: {
//             doctype: "Payroll Configuration",
//             fields: ["salary_component_configuration"]
//         },
//         callback: function(res) {
//             if (res.message && res.message.salary_component_configuration) {
//                 var data = res.message.salary_component_configuration;

//                 data.forEach(function(item) {
//                     var row = $('<tr>').appendTo(tbody).css("background-color", "white"); // Ensure white background

//                     var isComponentEditable = item.multi_select == 1;
//                     var isFieldsEditable = item.type === "Not Fixed";

//                     var componentInput = $('<input>', {
//                         type: 'text',
//                         class: 'form-control',
//                         value: item.salary_component,
//                         readonly: !isComponentEditable
//                     }).appendTo($('<td>').appendTo(row));

//                     var abbrInput = $('<input>', {
//                         type: 'text',
//                         class: 'form-control',
//                         value: item.abbr || "",
//                         readonly: !isComponentEditable
//                     }).appendTo($('<td>').appendTo(row));

//                     var conditionInput;
//                     if (isFieldsEditable) {
//                         conditionInput = $('<input>', {
//                             type: 'text',
//                             class: 'form-control',
//                             value: item.condition || ""
//                         });
//                     } else {
//                         conditionInput = $('<input>', {
//                             type: 'text',
//                             class: 'form-control',
//                             value: "Already Configured",
//                             readonly: true,
//                             style: "background-color: #f0f0f0; color: #888;"
//                         });
//                     }
//                     $('<td>').append(conditionInput).appendTo(row);

//                     var formulaInput;
//                     if (isFieldsEditable) {
//                         formulaInput = $('<input>', {
//                             type: 'text',
//                             class: 'form-control',
//                             value: item.formula || ""
//                         });
//                     } else {
//                         formulaInput = $('<input>', {
//                             type: 'text',
//                             class: 'form-control',
//                             value: "Already Configured",
//                             readonly: true,
//                             style: "background-color: #f0f0f0; color: #888;"
//                         });
//                     }
//                     $('<td>').append(formulaInput).appendTo(row);

//                     var addButton = $('<button>', {
//                         text: 'Add',
//                         class: 'btn btn-success',
//                         click: function() {
//                             var rowData = {
//                                 salary_component: componentInput.val(),
//                                 abbr: abbrInput.val(),
//                                 condition: conditionInput.val(),
//                                 formula: formulaInput.val(),
//                                 component_identification_type: item.component_identification_type // Include is_accrual in console output
//                             };



//                             console.log(rowData,"222222222222222");


// 							if(rowData && rowData.component_identification_type)
// 							{
// 								console.log(rowData.component_identification_type)


// 								if(item.component_identification_type==rowData.component_identification_type)&& (item.salary_component==rowData.salary_component)
// 														{
// 															frappe.call({
// 																method: "frappe.client.get_list",
// 																args: {
// 																	doctype: "Salary Component",
// 																	filters:{"disable":0}
// 																	fields: ["*"]
// 																},
// 																callback: function(component_res) {
// 																	console.log(component_res,message)



// 														}
// 													})











// 							}











//                         }
//                     }).appendTo($('<td>').appendTo(row));
//                 });
//             }
//         }
//     });
// };




// frappe.pages['payroll-configuratio'].on_page_load = function(wrapper) {
//     var page = frappe.ui.make_app_page({
//         parent: wrapper,
//         title: 'Payroll Configuration',
//         single_column: true
//     });

//     // Add CSS to make all rows white
//     $('<style>').text(`
//         table.table tbody tr {
//             background-color: white !important;
//         }
//     `).appendTo('head');

//     // Create a container to hold the table
//     var container = $('<div>').appendTo(page.main);

//     // Create the table element
//     var table = $('<table class="table table-bordered">').appendTo(container);
//     var thead = $('<thead>').appendTo(table);
//     var tbody = $('<tbody>').appendTo(table);

//     // Create the table header
//     $('<tr>')
//         .append('<th>Salary Component</th>')
//         .append('<th>Abbr</th>')  
//         .append('<th>Condition</th>')
//         .append('<th>Formula</th>')
//         .append('<th>Action</th>')  
//         .appendTo(thead);

//     // Fetch data from "Payroll Configuration"
//     frappe.call({
//         method: "frappe.client.get",
//         args: {
//             doctype: "Payroll Configuration",
//             fields: ["salary_component_configuration"]
//         },
//         callback: function(res) {
//             if (res.message && res.message.salary_component_configuration) {
//                 var data = res.message.salary_component_configuration;

//                 data.forEach(function(item) {
//                     var row = $('<tr>').appendTo(tbody).css("background-color", "white"); // Ensure white background

//                     var isComponentEditable = item.multi_select == 1;
//                     var isFieldsEditable = item.type === "Not Fixed";

//                     var componentInput = $('<input>', {
//                         type: 'text',
//                         class: 'form-control',
//                         value: item.salary_component,
//                         readonly: !isComponentEditable
//                     }).appendTo($('<td>').appendTo(row));

//                     var abbrInput = $('<input>', {
//                         type: 'text',
//                         class: 'form-control',
//                         value: item.abbr || "",
//                         readonly: !isComponentEditable
//                     }).appendTo($('<td>').appendTo(row));

//                     var conditionInput;
//                     if (isFieldsEditable) {
//                         conditionInput = $('<input>', {
//                             type: 'text',
//                             class: 'form-control',
//                             value: item.condition || ""
//                         });
//                     } else {
//                         conditionInput = $('<input>', {
//                             type: 'text',
//                             class: 'form-control',
//                             value: "Already Configured",
//                             readonly: true,
//                             style: "background-color: #f0f0f0; color: #888;"
//                         });
//                     }
//                     $('<td>').append(conditionInput).appendTo(row);

//                     var formulaInput;
//                     if (isFieldsEditable) {
//                         formulaInput = $('<input>', {
//                             type: 'text',
//                             class: 'form-control',
//                             value: item.formula || ""
//                         });
//                     } else {
//                         formulaInput = $('<input>', {
//                             type: 'text',
//                             class: 'form-control',
//                             value: "Already Configured",
//                             readonly: true,
//                             style: "background-color: #f0f0f0; color: #888;"
//                         });
//                     }
//                     $('<td>').append(formulaInput).appendTo(row);

//                     var addButton = $('<button>', {
//                         text: 'Add',
//                         class: 'btn btn-success',
//                         click: function() {
//                             var rowData = {
//                                 salary_component: componentInput.val(),
//                                 abbr: abbrInput.val(),
//                                 condition: conditionInput.val(),
//                                 formula: formulaInput.val(),
//                                 component_identification_type: item.component_identification_type,
// 								type: item.component_type,
//                                 is_accrual: item.is_accrual 
//                             };

//                             console.log("Row Data:", rowData);

//                             if (rowData.component_identification_type) {
                                

//                                 // Corrected condition syntax
//                                 if (item.component_identification_type == rowData.component_identification_type && 
//                                     item.salary_component == rowData.salary_component) {

//                                     frappe.call({
//                                         method: "frappe.client.get",
//                                         args: {
//                                             doctype: "Salary Component",
//                                             filters: { "disabled": 0,"name":rowData.salary_component},
//                                             fields: ["*"]
//                                         },
//                                         callback: function(component_res) {
//                                             console.log("Salary Components:", component_res.message);

// 											frappe.db.set_value(component_res.message.condition,"False")
//                                         }
//                                     });
//                                 }

// 								else{
// 									console.log("yyy")
// 								}
//                             }
//                         }
//                     }).appendTo($('<td>').appendTo(row));
//                 });
//             }
//         }
//     });
// };




// frappe.pages['payroll-configuratio'].on_page_load = function(wrapper) {
//     var page = frappe.ui.make_app_page({
//         parent: wrapper,
//         title: 'Payroll Configuration',
//         single_column: true
//     });

//     // Add CSS to make all rows white
//     $('<style>').text(`
//         table.table tbody tr {
//             background-color: white !important;
//         }
//     `).appendTo('head');

//     // Create a container to hold the table
//     var container = $('<div>').appendTo(page.main);

//     // Create the table element
//     var table = $('<table class="table table-bordered">').appendTo(container);
//     var thead = $('<thead>').appendTo(table);
//     var tbody = $('<tbody>').appendTo(table);

//     // Create the table header
//     $('<tr>')
//         .append('<th>Salary Component</th>')
//         .append('<th>Abbr</th>')  
//         .append('<th>Condition</th>')
//         .append('<th>Formula</th>')
//         .append('<th>Action</th>')  
//         .appendTo(thead);

//     // Fetch data from "Payroll Configuration"
//     frappe.call({
//         method: "frappe.client.get",
//         args: {
//             doctype: "Payroll Configuration",
//             fields: ["salary_component_configuration"]
//         },
//         callback: function(res) {
//             if (res.message && res.message.salary_component_configuration) {
//                 var data = res.message.salary_component_configuration;

//                 data.forEach(function(item) {
//                     var row = $('<tr>').appendTo(tbody).css("background-color", "white"); // Ensure white background

//                     var isComponentEditable = item.multi_select == 1;
//                     var isFieldsEditable = item.type === "Not Fixed";

//                     var componentInput = $('<input>', {
//                         type: 'text',
//                         class: 'form-control',
//                         value: item.salary_component,
//                         readonly: !isComponentEditable
//                     }).appendTo($('<td>').appendTo(row));

//                     var abbrInput = $('<input>', {
//                         type: 'text',
//                         class: 'form-control',
//                         value: item.abbr || "",
//                         readonly: !isComponentEditable
//                     }).appendTo($('<td>').appendTo(row));

//                     var conditionInput;
//                     if (isFieldsEditable) {
//                         conditionInput = $('<input>', {
//                             type: 'text',
//                             class: 'form-control',
//                             value: item.condition || ""
//                         });
//                     } else {
//                         conditionInput = $('<input>', {
//                             type: 'text',
//                             class: 'form-control',
//                             value: "Already Configured",
//                             readonly: true,
//                             style: "background-color: #f0f0f0; color: #888;"
//                         });
//                     }
//                     $('<td>').append(conditionInput).appendTo(row);

//                     var formulaInput;
//                     if (isFieldsEditable) {
//                         formulaInput = $('<input>', {
//                             type: 'text',
//                             class: 'form-control',
//                             value: item.formula || ""
//                         });
//                     } else {
//                         formulaInput = $('<input>', {
//                             type: 'text',
//                             class: 'form-control',
//                             value: "Already Configured",
//                             readonly: true,
//                             style: "background-color: #f0f0f0; color: #888;"
//                         });
//                     }
//                     $('<td>').append(formulaInput).appendTo(row);

//                     var addButton = $('<button>', {
//                         text: 'Add',
//                         class: 'btn btn-success',
//                         click: function() {
//                             var rowData = {
//                                 salary_component: componentInput.val(),
//                                 abbr: abbrInput.val(),
//                                 condition: conditionInput.val(),
//                                 formula: formulaInput.val(),
//                                 component_identification_type: item.component_identification_type,
//                                 type: item.component_type,
//                                 is_accrual: item.is_accrual 
//                             };

//                             console.log("Row Data:", rowData);

//                             if (rowData.component_identification_type ) {
//                                 if (item.component_identification_type === rowData.component_identification_type && 
//                                     item.salary_component === rowData.salary_component) {

//                                     frappe.call({
//                                         method: "frappe.client.get_list",
//                                         args: {
//                                             doctype: "Salary Component",
//                                             filters: { "disabled": 0, "name": rowData.salary_component,"type":rowData.type},
//                                             fields: ["name", "condition"]
//                                         },
//                                         callback: function(component_res) {
//                                             if (component_res.message.length > 0) {
//                                                 var component = component_res.message[0];
//                                                 console.log("Salary Component Found:", component);

//                                                 frappe.db.set_value("Salary Component", component.name, {
// 													"condition": rowData.condition,
// 													"formula": rowData.formula
// 												})
//                                                     .then(() => {
//                                                         console.log("Condition updated successfully for:", component.name);
//                                                     })
//                                                     .catch((err) => {
//                                                         console.error("Error updating condition:", err);
//                                                     });
//                                             } else {
//                                                 console.log("No matching Salary Component found.");
//                                             }
//                                         }
//                                     });
//                                 } 
// 								else
								 
// 								{
// 									console.log(rowData.salary_component,"vvv")
//                                     console.log("Component Identification Type does not match.");
//                                 }
//                             } else {
//                                 console.log("No Component Identification Type found in row data.");
//                             }
//                         }
//                     }).appendTo($('<td>').appendTo(row));
//                 });
//             }
//         }
//     });
// };




frappe.pages['payroll-configuratio'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Payroll Configuration',
        single_column: true
    });

    // Add CSS to make all rows white
    $('<style>').text(`
        table.table tbody tr {
            background-color: white !important;
        }
    `).appendTo('head');

    // Create a container to hold the table
    var container = $('<div>').appendTo(page.main);

    // Create the table element
    var table = $('<table class="table table-bordered">').appendTo(container);
    var thead = $('<thead>').appendTo(table);
    var tbody = $('<tbody>').appendTo(table);

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
        method: "frappe.client.get",
        args: {
            doctype: "Payroll Configuration",
            fields: ["salary_component_configuration"]
        },
        callback: function(res) {
            if (res.message && res.message.salary_component_configuration) {
                var data = res.message.salary_component_configuration;

                data.forEach(function(item) {
                    var row = $('<tr>').appendTo(tbody).css("background-color", "white");

                    var isComponentEditable = item.multi_select == 1;
                    var isFieldsEditable = item.type === "Not Fixed";

                    var componentInput = $('<input>', {
                        type: 'text',
                        class: 'form-control',
                        value: item.salary_component,
                        readonly: !isComponentEditable
                    }).appendTo($('<td>').appendTo(row));

                    var abbrInput = $('<input>', {
                        type: 'text',
                        class: 'form-control',
                        value: item.abbr || "",
                        readonly: !isComponentEditable
                    }).appendTo($('<td>').appendTo(row));

                    var conditionInput = $('<input>', {
                        type: 'text',
                        class: 'form-control',
                        value: isFieldsEditable ? item.condition || "" : "Already Configured",
                        readonly: !isFieldsEditable,
                        style: isFieldsEditable ? "" : "background-color: #f0f0f0; color: #888;"
                    }).appendTo($('<td>').appendTo(row));

                    var formulaInput = $('<input>', {
                        type: 'text',
                        class: 'form-control',
                        value: isFieldsEditable ? item.formula || "" : "Already Configured",
                        readonly: !isFieldsEditable,
                        style: isFieldsEditable ? "" : "background-color: #f0f0f0; color: #888;"
                    }).appendTo($('<td>').appendTo(row));

                    var addButton = $('<button>', {
                        text: 'Add',
                        class: 'btn btn-success',
                        click: function() {
                            var rowData = {
                                salary_component: componentInput.val(),
                                abbr: abbrInput.val(),
                                condition: conditionInput.val(),
                                formula: formulaInput.val(),
                                component_identification_type: item.component_identification_type,
                                type: item.component_type,
                                is_accrual: item.is_accrual
                            };

                            console.log("Row Data:", rowData);

							if(rowData.condition !="Already Configured" && rowData.formula!="Already Configured" && rowData.component_identification_type=="Standard")							{
                                frappe.call({
                                    method: "frappe.client.get_list",
                                    args: {
                                        doctype: "Salary Component",
                                        filters: { "disabled": 0, "name": rowData.salary_component, "type": rowData.type},
                                        fields: ["*"]
                                    },
                                    callback: function(standard_component_res) {
                                        if (standard_component_res.message.length > 0) {
                                            var component = standard_component_res.message[0];
                                            console.log("Salary Component Found:", component);

                                            // If "Already Configured", update with that value
                                            var updatedCondition = rowData.condition !== "Already Configured" ? rowData.condition : component.condition;
                                            var updatedFormula = rowData.formula !== "Already Configured" ? rowData.formula : component.formula;

                                            frappe.db.set_value("Salary Component", component.name, {
                                                "condition": updatedCondition,
                                                "formula": updatedFormula
                                            })
                                            .then(() => {
                                                msgprint("Condition and Formula updated successfully");
                                            })
                                            .catch((err) => {
                                                console.error("Error updating Salary Component:", err);
                                            });

                                        } 
										
										else 
										
										{

											frappe.db.insert({
												doctype: "Salary Component",
												salary_component :rowData.salary_component,
												name: rowData.salary_component,
												type: rowData.type,
												salary_component_abbr: rowData.abbr,
												
												depends_on_payment_days:1,
												is_tax_applicable:1,
												do_not_include_in_total:0,
												custom_is_part_of_gross_pay:1,
												custom_is_part_of_ctc:1,
												custom_is_part_of_appraisal:1,
												custom_tax_exemption_applicable_based_on_regime:1,
												custom_regime:"All",
												formula:rowData.formula,
												condition:rowData.condition,
												

												accounts: [
													{
														company: "Minix Holdings Private Limited",
														account: "Salary - MHPL",
														parentfield: "accounts"  // Ensure correct linkage
													}
												]
												

											}).then((doc) => {
												msgprint("Salary Component inserted successfully:", doc.name);

												

													frappe.db.insert({
														doctype: "Salary Component",
														salary_component :rowData.salary_component+"ARREAR",
														name: rowData.salary_component+"ARREAR",
														type: rowData.type,
														salary_component_abbr: rowData.abbr+"ARREAR",
														
														depends_on_payment_days:0,
														is_tax_applicable:1,
														do_not_include_in_total:0,
														custom_is_part_of_gross_pay:1,
														custom_is_part_of_ctc:0,
														custom_is_part_of_appraisal:0,
														custom_tax_exemption_applicable_based_on_regime:1,
														custom_regime:"All",
														custom_is_arrear:1,
														custom_component:rowData.salary_component,
														accounts: [
															{
																company: "Minix Holdings Private Limited",
																account: "Salary - MHPL",
																parentfield: "accounts"  // Ensure correct linkage
															}
														]
														
		
													})

												

											})








                                            
                                        }
                                    }
                                });
                            } 
							


							if(rowData.condition =="Already Configured" && rowData.formula=="Already Configured" && rowData.component_identification_type=="Standard")
							{
								// console.log(rowData.salary_component,"1111")
								// console.log(item.salary_component,"22222")

								    frappe.call({
                                    method: "frappe.client.get_list",
                                    args: {
                                        doctype: "Salary Component",
                                        filters: { "disabled": 0, "name": rowData.salary_component, "type": rowData.type },
                                        fields: ["name"]
                                    },
                                    callback: function(component_res) {
                                        if (component_res.message.length == 0) {


											frappe.db.insert({
												doctype: "Salary Component",
												salary_component :item.salary_component,
												name: item.salary_component,
												type: item.component_type,
												salary_component_abbr: rowData.abbr,
												component_type:item.special_type,
												depends_on_payment_days:item.depends_on_payment_days,
												is_tax_applicable:item.is_tax_applicable,
												do_not_include_in_total:item.do_not_include_in_total,
												custom_is_part_of_gross_pay:item.is_part_of_gross_pay,
												custom_is_part_of_ctc:item.is_part_of_ctc,
												custom_is_part_of_appraisal:item.is_part_of_appraisal,
												custom_tax_exemption_applicable_based_on_regime:item.tax_applicable_based_on_regime,
												custom_regime:item.regime,
												formula:item.formula,
												condition:item.condition,
												variable_based_on_taxable_salary:item.variable_based_on_taxable_salary,
												is_income_tax_component:item.is_income_tax_component,

												accounts: [
													{
														company: "Minix Holdings Private Limited",
														account: "Salary - MHPL",
														parentfield: "accounts"  // Ensure correct linkage
													}
												]
												

											}).then((doc) => {
												msgprint("Salary Component inserted successfully:", doc.name);

												if(item.is_arrear && item.component)
												{

													frappe.db.insert({
														doctype: "Salary Component",
														salary_component :item.component,
														name: item.component,
														type: item.component_type,
														salary_component_abbr: rowData.abbr+"ARREAR",
														component_type:item.special_type,
														depends_on_payment_days:0,
														is_tax_applicable:item.is_tax_applicable,
														do_not_include_in_total:item.do_not_include_in_total,
														custom_is_part_of_gross_pay:item.is_part_of_gross_pay,
														custom_is_part_of_ctc:0,
														custom_is_part_of_appraisal:0,
														custom_tax_exemption_applicable_based_on_regime:item.tax_applicable_based_on_regime,
														custom_regime:item.regime,
														custom_is_arrear:1,
														custom_component:item.salary_component,
														accounts: [
															{
																company: "Minix Holdings Private Limited",
																account: "Salary - MHPL",
																parentfield: "accounts"  // Ensure correct linkage
															}
														]
														
		
													})

												}

											})





										}

										else{

											msgprint("Component Already Added")

										}
									}
								})


							}


							if(rowData.condition =="Already Configured" && rowData.formula=="Already Configured" && rowData.component_identification_type=="Reimbursement")
								{
									
									frappe.call({
										method: "frappe.client.get_list",
										args: {
											doctype: "Salary Component",
											filters: { "disabled": 0, "name": rowData.salary_component, "type": rowData.type },
											fields: ["name"]
										},
										callback: function (reimbursement_component_res) {
											if (reimbursement_component_res.message.length == 0) {
									
												let taxablePromise = Promise.resolve();
												let nonTaxablePromise = Promise.resolve();
									
												// Insert LTA Taxable Component if applicable
												if (item.special_type == "LTA Reimbursement" && item.lta_taxable_component) {
													taxablePromise = frappe.db.insert({
														doctype: "Salary Component",
														salary_component: item.lta_taxable_component,
														name: item.lta_taxable_component,
														type: item.component_type,
														salary_component_abbr: rowData.abbr + "TAX",
														component_type: "LTA Taxable",
														depends_on_payment_days: 0,
														do_not_include_in_total: item.do_not_include_in_total,
														custom_is_part_of_gross_pay: item.is_part_of_gross_pay,
														custom_is_part_of_ctc: 0,
														custom_is_part_of_appraisal: 0,
														is_tax_applicable: 1,
														accounts: [
															{
																company: "Minix Holdings Private Limited",
																account: "Salary - MHPL",
																parentfield: "accounts"
															}
														]
													});
												}
									
												// Insert LTA Non-Taxable Component if applicable
												if (item.special_type == "LTA Reimbursement" && item.lta_non_taxable_component) {
													nonTaxablePromise = frappe.db.insert({
														doctype: "Salary Component",
														salary_component: item.lta_non_taxable_component,
														name: item.lta_non_taxable_component,
														type: item.component_type,
														salary_component_abbr: rowData.abbr + "NON TAX",
														component_type: "LTA Non Taxable",
														depends_on_payment_days: 0,
														is_tax_applicable: 0,
														do_not_include_in_total: item.do_not_include_in_total,
														custom_is_part_of_gross_pay: item.is_part_of_gross_pay,
														custom_is_part_of_ctc: 0,
														accounts: [
															{
																company: "Minix Holdings Private Limited",
																account: "Salary - MHPL",
																parentfield: "accounts"
															}
														]
													});
												}
									
												// Insert LTA Reimbursement Component only after taxable and non-taxable components are created
												Promise.all([taxablePromise, nonTaxablePromise]).then(() => {
													if (item.special_type == "LTA Reimbursement") {
														frappe.db.insert({
															doctype: "Salary Component",
															salary_component: item.salary_component,
															name: item.salary_component,
															type: item.component_type,
															salary_component_abbr: rowData.abbr,
															component_type: "LTA Reimbursement",
															depends_on_payment_days: 0,
															is_tax_applicable: 0,
															do_not_include_in_total: item.do_not_include_in_total,
															custom_is_part_of_gross_pay: item.is_part_of_gross_pay,
															custom_is_part_of_ctc: 0,
															custom_lta_taxable_component: item.lta_taxable_component,
															custom_lta_non_taxable_component: item.lta_non_taxable_component,
															accounts: [
																{
																	company: "Minix Holdings Private Limited",
																	account: "Salary - MHPL",
																	parentfield: "accounts"
																}
															]
														});
													}
												});
									
												// Insert other salary components if not LTA Reimbursement
												if (item.special_type != "LTA Reimbursement") {
													frappe.db.insert({
														doctype: "Salary Component",
														salary_component: item.salary_component,
														name: item.salary_component,
														type: item.component_type,
														salary_component_abbr: rowData.abbr,
														component_type: item.special_type,
														depends_on_payment_days: item.depends_on_payment_days,
														is_tax_applicable: item.is_tax_applicable,
														do_not_include_in_total: item.do_not_include_in_total,
														custom_is_part_of_gross_pay: item.is_part_of_gross_pay,
														custom_is_part_of_ctc: item.is_part_of_ctc,
														custom_is_part_of_appraisal: item.is_part_of_appraisal,
														custom_tax_exemption_applicable_based_on_regime: item.tax_applicable_based_on_regime,
														custom_regime: item.regime,
														formula: item.formula,
														condition: item.condition,
														variable_based_on_taxable_salary: item.variable_based_on_taxable_salary,
														is_income_tax_component: item.is_income_tax_component,
														custom_is_reimbursement: item.is_reimbursement,
														is_flexible_benefit: 1,
														pay_against_benefit_claim: 1,
														max_benefit_amount: 9999,
														create_separate_payment_entry_against_benefit_claim: 1,
														accounts: [
															{
																company: "Minix Holdings Private Limited",
																account: "Salary - MHPL",
																parentfield: "accounts"
															}
														]
													}).then((doc) => {
														msgprint("Salary Component inserted successfully: " + doc.name);
													});
												}
									
											} else {
												msgprint("Component Already Added");
											}
										}
									});
									
									
	
	
								}

								if(rowData.condition =="Already Configured" && rowData.formula=="Already Configured" && rowData.component_identification_type=="Perquisite")
									{
										
		
											frappe.call({
											method: "frappe.client.get_list",
											args: {
												doctype: "Salary Component",
												filters: { "disabled": 0, "name": rowData.salary_component, "type": rowData.type },
												fields: ["name"]
											},
											callback: function(per_component_res) {
												if (per_component_res.message.length == 0) {
		
		
													frappe.db.insert({
														doctype: "Salary Component",
														salary_component :item.salary_component,
														name: item.salary_component,
														type: item.component_type,
														salary_component_abbr: rowData.abbr,
														component_type:item.special_type,
														depends_on_payment_days:item.depends_on_payment_days,
														is_tax_applicable:item.is_tax_applicable,
														do_not_include_in_total:item.do_not_include_in_total,
														custom_is_part_of_gross_pay:item.is_part_of_gross_pay,
														custom_is_part_of_ctc:item.is_part_of_ctc,
														custom_is_part_of_appraisal:item.is_part_of_appraisal,
														custom_tax_exemption_applicable_based_on_regime:item.tax_applicable_based_on_regime,
														custom_regime:item.regime,
														formula:item.formula,
														condition:item.condition,
														custom_perquisite:item.perquisite,
														
		
														accounts: [
															{
																company: "Minix Holdings Private Limited",
																account: "Salary - MHPL",
																parentfield: "accounts"  // Ensure correct linkage
															}
														]
														
		
													}).then((doc) => {
														msgprint("Salary Component inserted successfully:", doc.name);
		

		
													})
		
		
		
		
		
												}
		
												else{
		
													msgprint("Component Already Added")
		
												}
											}
										})
		
		
									}


									if(rowData.component_identification_type=="Accrual")
										{
											
											frappe.call({
												method: "frappe.client.get_list",
												args: {
													doctype: "Salary Component",
													filters: { "disabled": 0, "name": rowData.salary_component, "type": rowData.type },
													fields: ["name"]
												},
												callback: function (accrual_component_res) {
													if (accrual_component_res.message.length == 0) {
											
														let taxablePromise = Promise.resolve();
														
											
														// Insert LTA Taxable Component if applicable
														if (item.is_accrual == 1 && item.paidout_component) {
															taxablePromise = frappe.db.insert({
																doctype: "Salary Component",
																salary_component: rowData.salary_component+"(Payout)",
																name: rowData.salary_component+"(Payout)",
																type: item.component_type,
																salary_component_abbr: rowData.abbr,
																
																depends_on_payment_days: 0,
																do_not_include_in_total: item.do_not_include_in_total,
																custom_is_part_of_gross_pay: item.is_part_of_gross_pay,
																custom_is_part_of_ctc: 0,
																custom_is_part_of_appraisal: 0,
																is_tax_applicable: 1,
																condition:item.condition,
																formula:item.formula,
																accounts: [
																	{
																		company: "Minix Holdings Private Limited",
																		account: "Salary - MHPL",
																		parentfield: "accounts"
																	}
																]
															});
														}
											
														
											
														Promise.all([taxablePromise]).then(() => {
															if (item.is_accrual == 1 ) {
																frappe.db.insert({
																	doctype: "Salary Component",
																	salary_component: rowData.salary_component,
																	name: rowData.salary_component,
																	type: item.component_type,
																	salary_component_abbr: rowData.abbr,
																	
																	depends_on_payment_days: 0,
																	is_tax_applicable: 0,
																	do_not_include_in_total: item.do_not_include_in_total,
																	custom_is_part_of_gross_pay: item.is_part_of_gross_pay,
																	custom_is_part_of_ctc: item.is_part_of_ctc,
																	custom_is_accrual:1,
																	custom_paidout_component:rowData.salary_component+"(Payout)",
																	
																	accounts: [
																		{
																			company: "Minix Holdings Private Limited",
																			account: "Salary - MHPL",
																			parentfield: "accounts"
																		}
																	]
																});
															}
														});
											
														
											
													} else {
														msgprint("Component Already Added");
													}
												}
											});
											
											
			
			
										}

								


							
                        }
                    }).appendTo($('<td>').appendTo(row));
                });
            }
        }
    });
};



