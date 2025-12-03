

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

        frm.fields_dict['custom_other_perquisite_components'].grid.get_field('component').get_query = function(doc, cdt, cdn) {
            var child = locals[cdt][cdn];

            return {
                filters:[
                    ['custom_perquisite', '=', 1]
                ]
            }
        }



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

        frm.trigger('consultant_gst')






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


    consultant_gst:function(frm)
    {

        if (frm.doc.employee && frm.doc.docstatus!=2) {
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Employee",
                    name: frm.doc.employee
                },
                callback: function (res) {
                    if (res.message && res.message.employment_type) {
                        console.log(res.message.employment_type,"11111")
                        frappe.db.get_value("Employment Type", res.message.employment_type, "employee_type_name")
                            .then(r => {
                                if (r.message && r.message.employee_type_name) {

                                    console.log(r.message.employee_type_name,"2222222222")
                                    if (r.message.employee_type_name === "Consultant" || r.message.employee_type_name === "Consultants") {
                                        frm.set_df_property("custom_gst_applicable_consultants", "hidden", 0);
                                        frm.set_df_property("custom_gst_eligible", "hidden", 0);
                                        frm.set_df_property("custom_gst_percentage", "hidden", 0);
                                    } else {
                                        frm.set_df_property("custom_gst_applicable_consultants", "hidden", 1);
                                        frm.set_df_property("custom_gst_eligible", "hidden", 1);
                                        frm.set_df_property("custom_gst_percentage", "hidden", 1);

                                    }
                                }
                            });
                    }
                }
            });
        }
    }


})


async function processSalaryComponents(frm) {

    var total_ctc=[]
    var total_annual_ctc=[]
    const response = await frappe.call({
        method: "hrms.payroll.doctype.salary_structure.salary_structure.make_salary_slip",
        args: {
            source_name: frm.doc.salary_structure,
            employee: frm.doc.employee,
            print_format: 'Salary Slip Standard',
            docstatus: frm.doc.docstatus,
            posting_date: frm.doc.from_date,
            for_preview: 1,
        }
    });

    if (response.message) {
        let salaryBreakup = `
            <table class="table table-bordered small">
                <thead>
                    <tr>
                        <th style="width: 16%">Salary Component (Earnings)</th>
                        <th style="width: 16%" class="text-right">Monthly Amount</th>
                        <th style="width: 16%" class="text-right">Annual Amount</th>
                    </tr>
                </thead>
                <tbody id="salary_breakup_body"></tbody>
            </table>`;

        document.getElementById("ctc_preview").innerHTML = salaryBreakup;
        let tableBody = document.getElementById("salary_breakup_body");

        let totalMonthlyEarnings = 0;
        let totalAnnualEarnings = 0;


        for (const v of response.message.earnings) {
            const res = await frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Salary Component",
                    filters: { name: v.salary_component },
                    fields: ["*"]
                }
            });

            if (res.message && res.message.custom_is_part_of_ctc == 1) {

                total_ctc.push(Math.round(v.amount))
                total_annual_ctc.push(Math.round(v.amount*12))
                let newRow = tableBody.insertRow();

                let componentCell = newRow.insertCell();
                componentCell.textContent = res.message.name;

                let roundedAmount = Math.round(v.amount);
                let formattedAmount = roundedAmount.toLocaleString();
                let amountCell = newRow.insertCell();
                amountCell.className = "text-right";
                amountCell.textContent = formattedAmount;

                let annualAmount = Math.round(v.amount*12);
                let formattedAnnualAmount = annualAmount.toLocaleString();
                let annualAmountCell = newRow.insertCell();
                annualAmountCell.className = "text-right";
                annualAmountCell.textContent = formattedAnnualAmount;


                totalMonthlyEarnings += roundedAmount;
                totalAnnualEarnings += annualAmount;
            }
        }


        if (frm.doc.custom_total_reimbursement_amount > 0) {
            let reimbursementBreakup = `
                <table class="table table-bordered small">
                    <thead>
                        <tr>
                            <th style="width: 16%">Reimbursements</th>
                            <th style="width: 16%" class="text-right">Monthly Amount</th>
                            <th style="width: 16%" class="text-right">Annual Amount</th>
                        </tr>
                    </thead>
                    <tbody id="reimbursement_breakup_body"></tbody>
                </table>`;

            document.getElementById("reimbursement_preview").innerHTML = reimbursementBreakup;
            let reimbursementTableBody = document.getElementById("reimbursement_breakup_body");

            $.each(frm.doc.custom_employee_reimbursements, function(i, component) {
                let newRow = reimbursementTableBody.insertRow();

                let componentCell = newRow.insertCell();
                componentCell.textContent = component.reimbursements;

                let amountCell = newRow.insertCell();
                amountCell.className = "text-right";
                amountCell.textContent = component.monthly_total_amount.toLocaleString();

                total_ctc.push(Math.round(component.monthly_total_amount))
                total_annual_ctc.push(Math.round(component.monthly_total_amount * 12))

                let annualAmountCell = newRow.insertCell();
                annualAmountCell.className = "text-right";
                annualAmountCell.textContent = (component.monthly_total_amount * 12).toLocaleString();

                totalMonthlyEarnings += component.monthly_total_amount;
                totalAnnualEarnings += component.monthly_total_amount * 12;
            });
        }


        let deductionBreakup = `
            <table class="table table-bordered small">
                <thead>
                    <tr>
                        <th style="width: 16%">Salary Component (Deductions)</th>
                        <th style="width: 16%" class="text-right">Monthly Amount</th>
                        <th style="width: 16%" class="text-right">Annual Amount</th>
                    </tr>
                </thead>
                <tbody id="deduction_breakup_body"></tbody>

            </table>`;

        document.getElementById("deduction_preview").innerHTML = deductionBreakup;
        let deductionTableBody = document.getElementById("deduction_breakup_body");

        let totalMonthlyDeductions = 0;
        let totalAnnualDeductions = 0;

        for (const v of response.message.deductions) {
            const res = await frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Salary Component",
                    filters: { name: v.salary_component },
                    fields: ["*"]
                }
            });

            if (res.message && res.message.custom_is_part_of_ctc == 1) {

                total_ctc.push(Math.round(v.amount))
                total_annual_ctc.push(Math.round(v.amount*12))
                let newRow = deductionTableBody.insertRow();

                let componentCell = newRow.insertCell();
                componentCell.textContent = res.message.name;

                let roundedAmount = Math.round(v.amount);
                let formattedAmount = roundedAmount.toLocaleString();
                let amountCell = newRow.insertCell();
                amountCell.className = "text-right";
                amountCell.textContent = formattedAmount;

                let annualAmount = Math.round(v.amount * 12);
                let formattedAnnualAmount = annualAmount.toLocaleString();
                let annualAmountCell = newRow.insertCell();
                annualAmountCell.className = "text-right";
                annualAmountCell.textContent = formattedAnnualAmount;


                totalMonthlyDeductions += roundedAmount;
                totalAnnualDeductions += annualAmount;
            }
        }

        var sum = total_ctc.reduce(function(accumulator, currentValue) {
            return accumulator + currentValue;
        }, 0);

        console.log(sum);
        var sum_annual = total_annual_ctc.reduce(function(accumulator, currentValue) {
            return accumulator + currentValue;
        }, 0);


        if (frm.doc.base) {

            let total_ctcTable = `
                <table class="table table-bordered small">
                    <thead>
                        <tr>
                            <th style="width: 16%">Total</th>
                            <th style="width: 16%" class="text-right">Monthly</th>
                            <th style="width: 16%" class="text-right">Annual</th>
                        </tr>
                    </thead>
                    <tbody id="ctc_breakup_body"></tbody>
                </table>`;


            document.getElementById("total_ctc").innerHTML = total_ctcTable;
            let ctc_body = document.getElementById("ctc_breakup_body");


            let newRow = ctc_body.insertRow();


            let componentCell = newRow.insertCell();
            componentCell.textContent = "Total CTC";

            let monthlyAmount = Math.round(sum);
            let annualAmount = Math.round(sum_annual);



            let formattedMonthlyAmount = monthlyAmount.toLocaleString();
            let amountCell = newRow.insertCell();
            amountCell.className = "text-right";
            amountCell.textContent = formattedMonthlyAmount;

            let formattedAnnualAmount = annualAmount.toLocaleString();
            let annualAmountCell = newRow.insertCell();
            annualAmountCell.className = "text-right";
            annualAmountCell.textContent = formattedAnnualAmount;
        }






    }
}
