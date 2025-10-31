

frappe.ui.form.on('Salary Structure Assignment', {


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
    },


    refresh(frm)
    {

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
                    doctype: "State",
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
                    doctype: "State",
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


})


async function processSalaryComponents(frm) {
    var total_ctc = 0; // only Basic component value

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
        // Earnings Table
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

        for (const v of response.message.earnings) {
            const res = await frappe.db.get_value("Salary Component", v.salary_component, "custom_is_part_of_ctc");

            if (res && res.message && res.message.custom_is_part_of_ctc == 1) {
                let newRow = tableBody.insertRow();
                let componentCell = newRow.insertCell();
                componentCell.textContent = v.salary_component;

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

                // ✅ Only Basic component goes into total_ctc
                if (v.salary_component.toLowerCase() === "basic") {
                    total_ctc = roundedAmount;
                }
            }
        }

        // Deductions Table
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

        for (const v of response.message.deductions) {
            const res = await frappe.db.get_value("Salary Component", v.salary_component, "custom_is_part_of_ctc");
            if (res && res.message && res.message.custom_is_part_of_ctc == 1) {
                let newRow = deductionTableBody.insertRow();
                let componentCell = newRow.insertCell();
                componentCell.textContent = v.salary_component;

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
            }
        }

        // ✅ Total CTC section (only Basic)
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
        componentCell.textContent = "Basic CTC";

        let formattedMonthly = total_ctc.toLocaleString();
        let monthlyCell = newRow.insertCell();
        monthlyCell.className = "text-right";
        monthlyCell.textContent = formattedMonthly;

        let annualAmount = total_ctc * 12;
        let formattedAnnual = annualAmount.toLocaleString();
        let annualCell = newRow.insertCell();
        annualCell.className = "text-right";
        annualCell.textContent = formattedAnnual;
    }
}
