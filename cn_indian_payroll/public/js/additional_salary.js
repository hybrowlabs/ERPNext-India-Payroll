frappe.ui.form.on("Additional Salary", {
    custom_is_off_cycle_payment: function(frm) {
        if (frm.doc.custom_is_off_cycle_payment) {
            frm.set_value("custom_is_regular_payment", 0);
            frm.set_value("custom_is_reimbursement", 0);
        }
    },
    custom_is_regular_payment: function(frm) {
        if (frm.doc.custom_is_regular_payment) {
            frm.set_value("custom_is_off_cycle_payment", 0);
            frm.set_value("custom_is_reimbursement", 0);
        }
    },
    custom_is_reimbursement: function(frm) {
        if (frm.doc.custom_is_reimbursement) {
            frm.set_value("custom_is_off_cycle_payment", 0);
            frm.set_value("custom_is_regular_payment", 0);
        }
    },

    custom_component_type: function(frm) {

        if (frm.doc.custom_component_type == "Taxable" && frm.doc.custom_is_off_cycle_payment) {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Salary Component",
                    fields: ["name", "do_not_include_in_total", "custom_is_part_of_gross_pay"],
                    filters: {
                        "do_not_include_in_total": 1,
                        "custom_is_part_of_gross_pay": 0,
                        "is_tax_applicable":1
                    },
                    limit_page_length: 9999
                },
                callback: function(r) {
                    if (r.message) {
                        // Extract names into array
                        let component_list = r.message.map(d => d.name);

                        // Apply as filter on salary_component field
                        frm.set_query("salary_component", function() {
                            return {
                                filters: {
                                    "name": ["in", component_list]
                                }
                            };
                        });

                        // optional: clear previous value if not in list
                        if (frm.doc.salary_component && !component_list.includes(frm.doc.salary_component)) {
                            frm.set_value("salary_component", "");
                        }
                    }
                }
            });
        }
        else if (frm.doc.custom_component_type == "Non Taxable" && frm.doc.custom_is_off_cycle_payment) {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Salary Component",
                    fields: ["name", "do_not_include_in_total", "custom_is_part_of_gross_pay"],
                    filters: {
                        "do_not_include_in_total": 1,
                        "custom_is_part_of_gross_pay": 0,
                        "is_tax_applicable":0
                    },
                    limit_page_length: 9999
                },
                callback: function(r) {
                    if (r.message) {
                        // Extract names into array
                        let component_list = r.message.map(d => d.name);

                        // Apply as filter on salary_component field
                        frm.set_query("salary_component", function() {
                            return {
                                filters: {
                                    "name": ["in", component_list]
                                }
                            };
                        });

                        // optional: clear previous value if not in list
                        if (frm.doc.salary_component && !component_list.includes(frm.doc.salary_component)) {
                            frm.set_value("salary_component", "");
                        }
                    }
                }
            });
        }
        else if (frm.doc.custom_component_type == "Taxable" && frm.doc.custom_is_regular_payment) {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Salary Component",
                    fields: ["name", "do_not_include_in_total", "custom_is_part_of_gross_pay"],
                    filters: {
                        "do_not_include_in_total": 0,
                        "custom_is_part_of_gross_pay": 1,
                        "is_tax_applicable":1
                    },
                    limit_page_length: 9999
                },
                callback: function(r) {
                    if (r.message) {
                        // Extract names into array
                        let component_list = r.message.map(d => d.name);

                        // Apply as filter on salary_component field
                        frm.set_query("salary_component", function() {
                            return {
                                filters: {
                                    "name": ["in", component_list]
                                }
                            };
                        });

                        // optional: clear previous value if not in list
                        if (frm.doc.salary_component && !component_list.includes(frm.doc.salary_component)) {
                            frm.set_value("salary_component", "");
                        }
                    }
                }
            });
        }

        else if (frm.doc.custom_component_type == "Non Taxable" && frm.doc.custom_is_regular_payment) {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Salary Component",
                    fields: ["name", "do_not_include_in_total", "custom_is_part_of_gross_pay"],
                    filters: {
                        "do_not_include_in_total": 0,
                        "custom_is_part_of_gross_pay": 1,
                        "is_tax_applicable":0
                    },
                    limit_page_length: 9999
                },
                callback: function(r) {
                    if (r.message) {
                        // Extract names into array
                        let component_list = r.message.map(d => d.name);

                        // Apply as filter on salary_component field
                        frm.set_query("salary_component", function() {
                            return {
                                filters: {
                                    "name": ["in", component_list]
                                }
                            };
                        });

                        // optional: clear previous value if not in list
                        if (frm.doc.salary_component && !component_list.includes(frm.doc.salary_component)) {
                            frm.set_value("salary_component", "");
                        }
                    }
                }
            });
        }
    }
});
