

frappe.ui.form.on('Salary Structure Assignment', {






    custom_meal_card:function(frm)
    {
        if(frm.doc.custom_meal_card)
        {
            frm.trigger('get_meal_card_amount');
        }

    },

    custom_telecom_wallet:function(frm)
    {
        if(frm.doc.custom_telecom_wallet)
        {
            frm.trigger('get_telecom_amount');
        }
    },
    custom_attire_wallet:function(frm)
    {
        if(frm.doc.custom_attire_wallet)
        {
            frm.trigger('get_attire_wallet');
        }
    },
    custom_fuel_wallet:function(frm)
    {
        if(frm.doc.custom_fuel_wallet)
        {
            frm.trigger('get_fuel_wallet');
        }
    },
    custom_gift_wallet:function(frm)
    {
        if(frm.doc.custom_gift_wallet)
        {
            frm.trigger('get_gift_wallet');
        }
    },


    get_meal_card_amount: function(frm) {

        if(frm.doc.custom_meal_card)
        {

            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Salary Component",
                    filters: {
                        "custom_variable_name": "custom_meal_card_amount_annual",
                        "disabled": 0
                    },
                    fields: ["custom_variable_name", "custom_value"],
                },
                callback: function(res) {
                    if (res.message && res.message.length > 0) {
                        let value = res.message[0].custom_value || "";
                        let values_array = [];
                        value.split(",").forEach(function(item) {
                            values_array.push(item.trim());
                        });
                         frm.set_df_property('custom_meal_card_amount_annual', 'options', values_array.join("\n"));
                        frm.refresh_field('custom_meal_card_amount_annual');
                    } else {
                        frappe.msgprint("No Meal Card data found.");
                    }
                }
            });

        }

    },

    get_telecom_amount: function(frm) {
        if(frm.doc.custom_telecom_wallet)
            {

            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Salary Component",
                    filters: {
                        "custom_variable_name": "custom_telecom_wallet_amount_annual",
                        "disabled": 0
                    },
                    fields: ["custom_variable_name", "custom_value"],
                },
                callback: function(res) {
                    if (res.message && res.message.length > 0) {
                        let value = res.message[0].custom_value || "";
                        let values_array = [];
                        value.split(",").forEach(function(item) {
                            values_array.push(item.trim());
                        });
                         frm.set_df_property('custom_telecom_wallet_amount_annual', 'options', values_array.join("\n"));
                        frm.refresh_field('custom_telecom_wallet_amount_annual');
                    } else {
                        frappe.msgprint("No Telecom data found.");
                    }
                }
            });
        }

    },

    get_attire_wallet: function(frm) {

        if(frm.doc.custom_attire_wallet)
            {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Salary Component",
                    filters: {
                        "custom_variable_name": "custom_attire_wallet_amountannual",
                        "disabled": 0
                    },
                    fields: ["custom_variable_name", "custom_value"],
                },
                callback: function(res) {
                    if (res.message && res.message.length > 0) {
                        let value = res.message[0].custom_value || "";
                        let values_array = [];
                        value.split(",").forEach(function(item) {
                            values_array.push(item.trim());
                        });
                         frm.set_df_property('custom_attire_wallet_amountannual', 'options', values_array.join("\n"));
                        frm.refresh_field('custom_attire_wallet_amountannual');
                    } else {
                        frappe.msgprint("No data found. please mention variable name as custom_attire_wallet_amountannual in Salary Component");
                    }
                }
            });
        }

    },
    get_fuel_wallet: function(frm) {
        if(frm.doc.custom_fuel_wallet)
            {

            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Salary Component",
                    filters: {
                        "custom_variable_name": "custom_fuel_wallet_amount_annual",
                        "disabled": 0
                    },
                    fields: ["custom_variable_name", "custom_value"],
                },
                callback: function(res) {
                    if (res.message && res.message.length > 0) {
                        let value = res.message[0].custom_value || "";
                        let values_array = [];
                        value.split(",").forEach(function(item) {
                            values_array.push(item.trim());
                        });
                         frm.set_df_property('custom_fuel_wallet_amount_annual', 'options', values_array.join("\n"));
                        frm.refresh_field('custom_fuel_wallet_amount_annual');
                    } else {
                        frappe.msgprint("No data found. please mention variable name as custom_fuel_wallet_amount_annual in Salary Component");
                    }
                }
            });
        }

    },

    get_gift_wallet: function(frm) {
        if(frm.doc.custom_gift_wallet)
            {

            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Salary Component",
                    filters: {
                        "custom_variable_name": "custom_gift_wallet_amountannual",
                        "disabled": 0
                    },
                    fields: ["custom_variable_name", "custom_value"],
                },
                callback: function(res) {
                    if (res.message && res.message.length > 0) {
                        let value = res.message[0].custom_value || "";
                        let values_array = [];
                        value.split(",").forEach(function(item) {
                            values_array.push(item.trim());
                        });
                         frm.set_df_property('custom_gift_wallet_amountannual', 'options', values_array.join("\n"));
                        frm.refresh_field('custom_gift_wallet_amountannual');
                    } else {
                        frappe.msgprint("No data found. please mention variable name as custom_gift_wallet_amountannual in Salary Component");
                    }
                }
            });
        }

    },







    onload: function(frm) {
            if (frm.doc.custom_promotion_id && frm.is_new()) {
                frappe.call({
                    method: 'frappe.client.get',
                    args: {
                        doctype: "Employee Promotion",
                        filters: { "name": frm.doc.custom_promotion_id }
                    },
                    callback: function(r) {
                        if (r.message) {
                            frappe.after_ajax(() => {
                                setTimeout(() => {
                                    frm.set_value("salary_structure", r.message.custom_current_structure);
                                    frm.set_value("from_date",r.message.promotion_date)
                                    frm.set_value("currency",r.message.custom_currency)


                                }, 100);
                            });
                        }
                    }
                });
            }


            frm.trigger('consultant_gst')


    },


    refresh(frm)
    {



        frm.trigger('get_meal_card_amount');
        frm.trigger('get_telecom_amount');
        frm.trigger('get_attire_wallet');
        frm.trigger('get_fuel_wallet');
        frm.trigger('get_gift_wallet');
        frm.trigger('consultant_gst')

        if (frm.doc.custom_promotion_id) {
            frm.add_custom_button(__('View Employee Promotion'), function() {
                frappe.set_route('Form', 'Employee Promotion', frm.doc.custom_promotion_id);
            }, __('Actions'));
        }


        if (frm.doc.employee && frm.doc.docstatus==1)
            {
                    processSalaryComponents(frm)
            }


        frm.fields_dict['custom_employee_reimbursements'].grid.get_field('reimbursements').get_query = function(doc, cdt, cdn) {
            var child = locals[cdt][cdn];

            return {
                filters:[
                    ['custom_is_reimbursement', '=', 1]
                ]
            }
        }

        // frm.fields_dict['custom_other_perquisite_components'].grid.get_field('component').get_query = function(doc, cdt, cdn) {
        //     var child = locals[cdt][cdn];

        //     return {
        //         filters:[
        //             ['custom_perquisite', '=', 1]
        //         ]
        //     }
        // }



        if (frm.doc.custom_lwf_state) {
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "State Master",
                    name: frm.doc.custom_lwf_state
                },
                callback: function(res) {
                    if (res.message && res.message.frequency) {


                        let frequency_array = res.message.frequency.map(row => row.frequency);


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


        frm.set_query("custom_lwf_state", function() {
            return {
                filters: {
                   "lwf_applicable":1
                }
            };
        });








    },

    custom_lwf:function(frm)
    {
        if(frm.doc.custom_lwf==0)
        {
            frm.set_value("custom_lwf_state",undefined)
            // frm.set_default_property("custom_frequency","hidden",1)
        }

    },


    custom_cubic_capacity_of_company(frm)
    {

            if(frm.doc.custom_cubic_capacity_of_company=="Car < 1600 CC" )
            {
                frm.set_value("custom_car_perquisite_as_per_rules",1800)
            }

            else if (frm.doc.custom_cubic_capacity_of_company=="Car > 1600 CC")
            {
                frm.set_value("custom_car_perquisite_as_per_rules",2400)
            }


    },

    custom_lwf_state: function(frm) {
        if (frm.doc.custom_lwf_state) {
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "State Master",
                    name: frm.doc.custom_lwf_state
                },
                callback: function(res) {
                    if (res.message && res.message.frequency) {


                        let frequency_array = res.message.frequency.map(row => row.frequency);


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




    custom_driver_provided_by_company(frm)
    {
        if(frm.doc.custom_driver_provided_by_company==1)
        {
            frm.set_value("custom_driver_perquisite_as_per_rules",900)
        }
        else
        {
            frm.set_value("custom_driver_perquisite_as_per_rules",undefined)
        }
    },


    custom__car_perquisite(frm)
    {
        if (frm.doc.custom__car_perquisite==1)
            {
                if(frm.doc.custom_cubic_capacity_of_company=="Car > 1600 CC")
                    {

                        frm.set_value("custom_car_perquisite_as_per_rules",2400)
                    }

            }

            else
            {
                frm.set_value("custom_car_perquisite_as_per_rules",undefined)

            }
    },


    consultant_gst: function(frm) {

        if (frm.doc.employee) {

            let employment_type = [];

            // Fetch Payroll Settings
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Payroll Settings",
                    name: "Payroll Settings"
                },
                callback: function(res) {

                    if (res.message) {
                        console.log(res.message, "Payroll Settings Loaded");

                        let config = res.message.custom_hide_salary_structure_configuration;

                        if (config && config.length > 0) {
                            $.each(config, function(i, d) {
                                if (d.employment_type) {
                                    employment_type.push(d.employment_type);
                                }
                            });
                        }

                        console.log("Employment Types:", employment_type);

                        // Fetch Employee Doc
                        frappe.call({
                            method: "frappe.client.get",
                            args: {
                                doctype: "Employee",
                                name: frm.doc.employee
                            },
                            callback: function(emp_res) {

                                if (emp_res.message && emp_res.message.employment_type) {

                                    let emp_type = emp_res.message.employment_type;
                                    console.log("Employee Type:", emp_type);

                                    if (employment_type.includes(emp_type)) {

                                        console.log("Match found - hiding GST fields");

                                        frm.set_df_property("custom_gst_applicable_consultants", "hidden", 0);
                                        frm.set_df_property("custom_gst_eligible", "hidden", 0);
                                        frm.set_df_property("custom_gst_percentage", "hidden", 0);

                                        frm.set_df_property("custom_minimum_wages_applicable", "hidden", 1);
                                        frm.set_df_property("custom_manual_input_values", "hidden", 1);
                                        frm.set_df_property("custom_allowance", "hidden", 1);

                                        frm.set_df_property("custom_epf", "hidden", 1);
                                        frm.set_df_property("custom_nps", "hidden", 1);
                                        frm.set_df_property("custom_lwf_labour_welfare_fund_", "hidden", 1);
                                        frm.set_df_property("custom_esic", "hidden", 1);
                                        frm.set_df_property("custom_perquisite", "hidden", 1);
                                        frm.set_df_property("custom_reimbursements", "hidden", 1);
                                        frm.set_df_property("custom_section_break_qbdc8", "hidden", 1);

                                    } else {

                                        console.log("No match - showing GST fields");

                                        frm.set_df_property("custom_gst_applicable_consultants", "hidden", 0);
                                        frm.set_df_property("custom_gst_eligible", "hidden", 0);
                                        frm.set_df_property("custom_gst_percentage", "hidden", 0);
                                        frm.set_df_property("custom_minimum_wages_applicable", "hidden", 0);

                                        frm.set_df_property("custom_minimum_wages_applicable", "hidden", 0);
                                        frm.set_df_property("custom_manual_input_values", "hidden", 0);
                                        frm.set_df_property("custom_allowance", "hidden", 0);

                                        frm.set_df_property("custom_epf", "hidden", 0);
                                        frm.set_df_property("custom_nps", "hidden", 0);
                                        frm.set_df_property("custom_lwf_labour_welfare_fund_", "hidden", 0);
                                        frm.set_df_property("custom_esic", "hidden", 0);
                                        frm.set_df_property("custom_perquisite", "hidden", 0);
                                        frm.set_df_property("custom_reimbursements", "hidden", 0);
                                        frm.set_df_property("custom_section_break_qbdc8", "hidden", 0);
                                    }
                                }

                            }
                        });
                    }

                }
            });
        }
    },
    employee:function(frm)
    {
        frm.trigger('consultant_gst')

        console.log("Employee field changed - triggering state fetch");


        if (frm.doc.employee) {
            frappe.call({
                method: "cn_indian_payroll.cn_indian_payroll.overrides.tds_projection_calculation.get_state_from_branch",
                args: {

                        employee: frm.doc.employee,
                        company: frm.doc.company
                },
                callback: function (r) {
                    if (r.message) {


                        frm.set_value("custom_state", r.message);
                        frm.set_value("custom_lwf_state", r.message);


                    }
                }
            });

            frappe.call({
                method: "cn_indian_payroll.cn_indian_payroll.overrides.tds_projection_calculation.fetch_last_ctc_details",
                args: {

                        employee: frm.doc.employee,
                        company: frm.doc.company,
                        doctype:"Salary Structure Assignment",

                },
                callback: function (r) {
                    if (r.message) {
                   
                        let data = r.message.response;
                        let reimbursements = r.message.response.custom_employee_reimbursements || [];

                        frm.set_value("salary_structure",data.salary_structure)
                        frm.set_value("from_date",data.from_date)
                        frm.set_value("income_tax_slab",data.income_tax_slab)
                        frm.set_value("custom_payroll_period",data.custom_payroll_period)
                        frm.set_value("custom_fixed_gross_annual",data.custom_fixed_gross_annual)
                        frm.set_value("custom_basic",data.custom_basic)
                        frm.set_value("custom_basic_annual",data.custom_basic_annual)

                        frm.set_value("custom_special_allowance",data.custom_special_allowance)
                        frm.set_value("custom_special_allowance_annual",data.custom_special_allowance_annual)
                        frm.set_value("custom_esic_employee",data.custom_esic_employee)
                        frm.set_value("custom_esic_employee_annual",data.custom_esic_employee_annual)

                        frm.set_value("custom_hra",data.custom_hra)
                        frm.set_value("custom_hra_annual",data.custom_hra_annual)

                        frm.set_value("custom_epf_employee",data.custom_epf_employee)
                        frm.set_value("custom_epf_employee_annual",data.custom_epf_employee_annual)

                        frm.set_value("custom_esic_employer",data.custom_esic_employer)
                        frm.set_value("custom_esic_employer_annual",data.custom_esic_employer_annual)

                        frm.set_value("custom_lta",data.custom_lta)
                        frm.set_value("custom_lta_annual",data.custom_lta_annual)

                        frm.set_value("custom_epf_employer",data.custom_epf_employer)
                        frm.set_value("custom_epf_employer_annual",data.custom_epf_employer_annual)

                        frm.set_value("custom_nps_value",data.custom_nps_value)
                        frm.set_value("custom_nps_annual",data.custom_nps_annual)

                        frm.set_value("custom_meal_card",data.custom_meal_card)
                        frm.set_value("custom_meal_card_amount_annual",data.custom_meal_card_amount_annual)

                        frm.set_value("custom_telecom_wallet",data.custom_telecom_wallet)
                        frm.set_value("custom_telecom_wallet_amount_annual",data.custom_telecom_wallet_amount_annual)
                        frm.set_value("custom_fuel_wallet",data.custom_fuel_wallet)
                        frm.set_value("custom_fuel_wallet_amount_annual",data.custom_fuel_wallet_amount_annual)
                        
                        frm.set_value("custom_attire_wallet",data.custom_attire_wallet)
                        frm.set_value("custom_attire_wallet_amountannual",data.custom_attire_wallet_amountannual)

                        frm.set_value("custom_gift_wallet",data.custom_gift_wallet)
                        frm.set_value("custom_gift_wallet_amountannual",data.custom_gift_wallet_amountannual)

                        frm.set_value("custom_is_epf",data.custom_is_epf)
                        frm.set_value("custom_epf_type",data.custom_epf_type)

                        frm.set_value("custom_is_nps",data.custom_is_nps)
                        frm.set_value("custom_nps_percentage",data.custom_nps_percentage)

                        frm.set_value("custom_lwf",data.custom_lwf)
                        frm.set_value("custom_lwf_state",data.custom_lwf_state)

                        frm.set_value("custom_frequency",data.custom_frequency)
                        frm.set_value("custom_lwf_designation",data.custom_lwf_designation)

                        frm.set_value("custom_state",data.custom_state)
                        
                        frm.clear_table("custom_employee_reimbursements");

                        frm.clear_table("custom_employee_reimbursements");

                        reimbursements.forEach(row => {

                            let child = frm.add_child("custom_employee_reimbursements");

                            child.reimbursements = row.reimbursements;
                            child.monthly_total_amount = row.monthly_total_amount;

                           
                        });

                        frm.refresh_field("custom_employee_reimbursements");



                    }
                }
            });

            frappe.call({
                method: "cn_indian_payroll.cn_indian_payroll.overrides.tds_projection_calculation.fetch_gst_details",
                args: {

                        employee: frm.doc.employee,
                        company: frm.doc.company,
                        

                },
                callback: function (r) {
                    if (r.message) {

                        if(r.message.status=="No")
                        {
                            frm.set_value("custom_gst_eligible",0)

                        }
                        else
                        {
                            frm.set_value("custom_gst_eligible",1)


                        }



                    }
                }
            });

            


        

    }
    }



})



// async function processSalaryComponents(frm) {

       

//     let total_ctc = [];
//     let total_annual_ctc = [];

//     const response = await frappe.call({
//         method: "hrms.payroll.doctype.salary_structure.salary_structure.make_salary_slip",
//         args: {
//             source_name: frm.doc.salary_structure,
//             employee: frm.doc.employee,
//             print_format: "Salary Slip Standard",
//             docstatus: frm.doc.docstatus,
//             posting_date: frm.doc.from_date,
//             for_preview: 1,
//         }
//     });

//     if (!response.message) return;

//     let table = `
//         <table class="table table-bordered small">
//             <thead>
//                 <tr>
//                      <th width="60%">Salary Component (Earnings)</th>
//                     <th width="20%" class="text-right">Monthly Amount</th>
//                     <th width="20%" class="text-right">Annual Amount</th>
//                 </tr>
//             </thead>
//             <tbody id="salary_breakup_body"></tbody>
//         </table>`;

//     document.getElementById("ctc_preview").innerHTML = table;
//     let tableBody = document.getElementById("salary_breakup_body");

//     let totalMonthlyEarnings = 0;
//     let totalAnnualEarnings = 0;

//     /* =========================
//        Earnings
//     ========================== */

//     for (const v of response.message.earnings) {

//         const component = await frappe.db.get_doc("Salary Component", v.salary_component);

//         if (component.custom_is_part_of_ctc == 1) {

//             let monthly = Math.round(v.amount);
//             let annual = monthly * 12;

//             total_ctc.push(monthly);
//             total_annual_ctc.push(annual);

//             let row = tableBody.insertRow();

//             row.insertCell().textContent = component.name;

//             let monthlyCell = row.insertCell();
//             monthlyCell.className = "text-right";
//             monthlyCell.textContent = monthly.toLocaleString();

//             let annualCell = row.insertCell();
//             annualCell.className = "text-right";
//             annualCell.textContent = annual.toLocaleString();

//             totalMonthlyEarnings += monthly;
//             totalAnnualEarnings += annual;
//         }
//     }

//     let fixed_gross_table = `
//         <table class="table table-bordered small">
//             <thead>
//                 <tr>
//                     <th width="60%">Fixed Gross</th>
//                     <th width="20%" class="text-right">Monthly Amount</th>
//                     <th width="20%" class="text-right">Annual Amount</th>
//                 </tr>
//             </thead>
//             <tbody id="salary_fixed_body"></tbody>
//         </table>`;

//     document.getElementById("fixed_gross").innerHTML = fixed_gross_table;
//     let fixedtableBody = document.getElementById("salary_fixed_body");

        
//     // =========================
//     // Fixed Gross Calculation
//     // =========================

//     if (totalMonthlyEarnings > 0) {

//         let row = fixedtableBody.insertRow();

//         row.insertCell().textContent = "Fixed Gross";

//         let monthlyCell = row.insertCell();
//         monthlyCell.className = "text-right";
//         monthlyCell.textContent = Math.round(totalMonthlyEarnings).toLocaleString();

//         let annualCell = row.insertCell();
//         annualCell.className = "text-right";
//         annualCell.textContent = Math.round(totalAnnualEarnings).toLocaleString();
//     }





//     /* =========================
//        Reimbursements
//     ========================== */

//     if (frm.doc.custom_employee_reimbursements?.length) {

//         let reimbursementTable = `
//             <table class="table table-bordered small">
//                 <thead>
//                     <tr>
//                         <th width="60%">Reimbursements</th>
//                         <th width="20%" class="text-right">Monthly Amount</th>
//                         <th width="20%" class="text-right">Annual Amount</th>
//                     </tr>
//                 </thead>
//                 <tbody id="reimbursement_breakup_body"></tbody>
//             </table>`;

//         document.getElementById("reimbursement_preview").innerHTML = reimbursementTable;

//         let body = document.getElementById("reimbursement_breakup_body");

//         frm.doc.custom_employee_reimbursements.forEach(component => {

//             let monthly = Math.round(component.monthly_total_amount);
//             let annual = monthly * 12;

//             total_ctc.push(monthly);
//             total_annual_ctc.push(annual);

//             let row = body.insertRow();

//             row.insertCell().textContent = component.reimbursements;

//             let m = row.insertCell();
//             m.className = "text-right";
//             m.textContent = monthly.toLocaleString();

//             let a = row.insertCell();
//             a.className = "text-right";
//             a.textContent = annual.toLocaleString();
//         });
//     }




//     /* =========================
//        Deductions
//     ========================== */

//     let deductionTable = `
//         <table class="table table-bordered small">
//             <thead>
//                 <tr>
//                     <th width="60%">Salary Component (Deductions)</th>
//                     <th width="20%" class="text-right">Monthly Amount</th>
//                     <th width="20%" class="text-right">Annual Amount</th>
//                 </tr>
//             </thead>
//             <tbody id="deduction_breakup_body"></tbody>
//         </table>`;

//     document.getElementById("deduction_preview").innerHTML = deductionTable;

//     let deductionBody = document.getElementById("deduction_breakup_body");

//     for (const v of response.message.deductions) {

//         const component = await frappe.db.get_doc("Salary Component", v.salary_component);

//         if (component.custom_is_part_of_ctc == 1) {

//             let monthly = Math.round(v.amount);
//             let annual = monthly * 12;

//             total_ctc.push(monthly);
//             total_annual_ctc.push(annual);

//             let row = deductionBody.insertRow();

//             row.insertCell().textContent = component.name;

//             let m = row.insertCell();
//             m.className = "text-right";
//             m.textContent = monthly.toLocaleString();

//             let a = row.insertCell();
//             a.className = "text-right";
//             a.textContent = annual.toLocaleString();
//         }
//     }


// /* =========================
//    Variable Pay (Include in CTC)
// ========================= */

// if (frm.doc.custom_variable_pay_components?.length) {

//     // Check if any component should be included in CTC
//     const hasIncludedComponent = frm.doc.custom_variable_pay_components.some(
//         component => component.part_of_ctc == 1
//     );

//     if (hasIncludedComponent) {

//         let includeTable = `
//             <table class="table table-bordered small">
//                 <thead>
//                     <tr>
//                         <th>Variable Pay (Included in CTC)</th>
//                         <th class="text-right">Annual Amount</th>
//                     </tr>
//                 </thead>
//                 <tbody id="variable_include_body"></tbody>
//             </table>`;

//         document.getElementById("variable_pay_include_ctc").innerHTML = includeTable;

//         let includeBody = document.getElementById("variable_include_body");

//         frm.doc.custom_variable_pay_components.forEach(component => {

//             if (component.part_of_ctc == 1) {

//                 let amount = Math.round(component.amount);

//                 total_annual_ctc.push(amount);

//                 let row = includeBody.insertRow();

//                 row.insertCell().textContent = component.variable_name;

//                 let amountCell = row.insertCell();
//                 amountCell.className = "text-right";
//                 amountCell.textContent = amount.toLocaleString();
//             }

//         });
//     }
// }




//     /* =========================
//        Total CTC
//     ========================== */

//     let sum = total_ctc.reduce((a, b) => a + b, 0);
//     let sumAnnual = total_annual_ctc.reduce((a, b) => a + b, 0);

//     if (frm.doc.base) {

//         let totalTable = `
//             <table class="table table-bordered small">
//                 <thead>
//                     <tr>
//                         <th>Total</th>
//                         <th class="text-right">Monthly</th>
//                         <th class="text-right">Annual</th>
//                     </tr>
//                 </thead>
//                 <tbody id="ctc_breakup_body"></tbody>
//             </table>`;

//         document.getElementById("total_ctc").innerHTML = totalTable;

//         let body = document.getElementById("ctc_breakup_body");

//         let row = body.insertRow();

//         row.insertCell().textContent = "Total CTC";

//         let m = row.insertCell();
//         m.className = "text-right";
//         m.textContent = Math.round(sum).toLocaleString();

//         let a = row.insertCell();
//         a.className = "text-right";
//         a.textContent = Math.round(sumAnnual).toLocaleString();
//     }



// if (frm.doc.custom_variable_pay_components?.length) {

//     // Check if any component is excluded from CTC
//     const hasExcludedComponent = frm.doc.custom_variable_pay_components.some(
//         component => component.part_of_ctc == 0
//     );

//     if (hasExcludedComponent) {

//         let excludeTable = `
//             <table class="table table-bordered small">
//                 <thead>
//                     <tr>
//                         <th>Variable Pay (Excluded from CTC)</th>
//                         <th class="text-right">Annual Amount</th>
//                     </tr>
//                 </thead>
//                 <tbody id="variable_exclude_body"></tbody>
//             </table>`;

//         document.getElementById("variable_pay_exclude_ctc").innerHTML = excludeTable;

//         let excludeBody = document.getElementById("variable_exclude_body");

//         frm.doc.custom_variable_pay_components.forEach(component => {

//             if (component.part_of_ctc == 0) {

//                 let amount = Math.round(component.amount);

//                 let row = excludeBody.insertRow();

//                 row.insertCell().textContent = component.variable_name;

//                 let amountCell = row.insertCell();
//                 amountCell.className = "text-right";
//                 amountCell.textContent = amount.toLocaleString();
//             }

//         });
//     }
// }

// }



async function processSalaryComponents(frm) {

    const r = await frappe.call({
        method: "cn_indian_payroll.cn_indian_payroll.overrides.salary_structure.get_ctc_breakup",
        args: { doc: frm.doc }
    });

    if (!r.message) return;

    let data = r.message;

    console.log("CTC Breakup Data:", data);


    let html = `
    <table class="table table-bordered small">
        <thead>
            <tr>
                <th>Component</th>
                <th class="text-right">Monthly</th>
                <th class="text-right">Annual</th>
            </tr>
        </thead>
        <tbody>
            ${data.earnings.map(e => `
                <tr>
                    <td  width="60%">${e.component}</td>
                    <td class="text-right"  width="20%">${e.monthly.toLocaleString()}</td>
                    <td class="text-right"  width="20%">${e.annual.toLocaleString()}</td>
                </tr>
            `).join("")}
        </tbody>
    </table>`;

    document.getElementById("ctc_preview").innerHTML = html;



    let fixed_gross_html = `
    <table class="table table-bordered small">
        <tbody>
           
                <tr>
                    <td  width="60%"><b>Fixed Gross</b></td>
                    <td class="text-right"  width="20%">${data.fixed_gross.toLocaleString()}</td>
                    <td class="text-right"  width="20%">${data.fixed_gross_annual.toLocaleString()}</td>
                </tr>
           
        </tbody>
    </table>`;

    document.getElementById("fixed_gross").innerHTML = fixed_gross_html;
                   



    let reimbursement_html = `
    <table class="table table-bordered small">
        <tbody>
            ${data.reimbursements.map(r => `
                <tr>
                    <td  width="60%">${r.component}</td>
                    <td class="text-right"  width="20%">${r.monthly.toLocaleString()}</td>
                    <td class="text-right"  width="20%">${r.annual.toLocaleString()}</td>
                </tr>
            `).join("")}
        </tbody>
    </table>`;

    document.getElementById("reimbursement_preview").innerHTML = reimbursement_html;


                   



    let deduction_html = `
    <table class="table table-bordered small">
        <tbody>
            ${data.deductions.map(d => `
                <tr>
                    <td  width="60%">${d.component}</td>
                    <td class="text-right"  width="20%">${d.monthly.toLocaleString()}</td>
                    <td class="text-right"  width="20%">${d.annual.toLocaleString()}</td>
                </tr>
            `).join("")}
        </tbody>
    </table>`;

    document.getElementById("deduction_preview").innerHTML = deduction_html;


    let variable_ctc_html = `
    <table class="table table-bordered small">
        <tbody>
            ${data.variable_include.map(v => `
                <tr>
                    <td  width="70%">${v.component}</td>
                    <td class="text-right"  width="20%">${v.amount.toLocaleString()}</td>
                   
                </tr>
            `).join("")}
        </tbody>
    </table>`;

    document.getElementById("variable_pay_include_ctc").innerHTML = variable_ctc_html;

    let total_ctc_html = `
    <table class="table table-bordered small">
        <tbody>
            
                <tr>
                   <td  width="60%"><b>Total CTC</b></td>
                    <td class="text-right"  width="20%">${data.total_monthly.toLocaleString()}</td>
                    <td class="text-right"  width="20%">${data.total_annual.toLocaleString()}</td>
                   
                </tr>
         
        </tbody>
    </table>`;

    document.getElementById("total_ctc").innerHTML = total_ctc_html;


    let variable_exclude_ctc_html = `
    <table class="table table-bordered small">
        <tbody>
            ${data.variable_exclude.map(k => `
                <tr>
                    <td  width="70%">${k.component}</td>
                    <td class="text-right"  width="20%">${k.amount.toLocaleString()}</td>
                   
                </tr>
            `).join("")}
        </tbody>
    </table>`;

    document.getElementById("variable_pay_exclude_ctc").innerHTML = variable_exclude_ctc_html;

    

}