

frappe.ui.form.on('Salary Structure Assignment', {



    onload:function(frm)
    {

        if (frm.doc.custom_promotion_id && frm.is_new())
        {

            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: "Employee Promotion",
                    filters:{"name":frm.doc.custom_promotion_id}
                },
                callback: function(r) {
                    if (r.message) {



                        frm.set_value("from_date",r.message.promotion_date)

                    }
                }
            });

        }

    },







    refresh(frm)
    {





                setTimeout(() => {

                    frm.remove_custom_button('Payroll Entry', 'Create');


                }, 10);



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



    frm.fields_dict['custom_other_perquisites'].grid.get_field('title').get_query = function(doc, cdt, cdn) {
        var child = locals[cdt][cdn];

        return {
            filters:[
                ['custom_perquisite', '=', 1]
            ]
        }
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

    const response = await frappe.call({
        method: "hrms.payroll.doctype.salary_structure.salary_structure.make_salary_slip",
        args: {
            source_name: frm.doc.salary_structure,
            employee: frm.doc.employee,
            print_format: 'Salary Slip Standard',
            docstatus: 1,
            posting_date: frm.doc.from_date,
            for_preview: 1,
        }
    });

    if (response.message) {
        // Arrays to categorize components
        let basicSalaryComponents = [];
        let allowanceComponents = [];
        let statutoryComponents = [];
        let insuranceComponents = [];

        // Process earnings components
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
                let roundedAmount, annualAmount;

                if (res.message.round_to_the_nearest_integer == 0) {
                    roundedAmount = v.default_amount;
                    annualAmount = Math.round(v.default_amount * 12);
                } else {
                    roundedAmount = Math.round(v.default_amount);
                    annualAmount = roundedAmount * 12;
                }

                let componentData = {
                    name: res.message.name,
                    monthly: roundedAmount,
                    annual: annualAmount,
                    sequence: res.message.custom_sequence || v.idx || 999
                };

                // Categorize based on is_basic or adhoc flag
                if (res.message.custom_is_adhoc_or_basic == 1) {
                    basicSalaryComponents.push(componentData);
                } else {
                    allowanceComponents.push(componentData);
                }
            }
        }

        // Process deductions components
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
                let roundedAmount, annualAmount;

                if (res.message.round_to_the_nearest_integer == 0) {
                    roundedAmount = v.default_amount;
                    annualAmount = Math.round(v.default_amount * 12);
                } else {
                    roundedAmount = Math.round(v.default_amount);
                    annualAmount = roundedAmount * 12;
                }

                let componentData = {
                    name: res.message.name,
                    monthly: roundedAmount,
                    annual: annualAmount,
                    sequence: res.message.custom_sequence || v.idx || 999
                };

                // Categorize based on insurance flag
                if (res.message.custom_is_insurance == 1) {
                    insuranceComponents.push(componentData);
                } else {
                    statutoryComponents.push(componentData);
                }
            }
        }

        // Sort components by sequence
        basicSalaryComponents.sort((a, b) => a.sequence - b.sequence);
        allowanceComponents.sort((a, b) => a.sequence - b.sequence);
        statutoryComponents.sort((a, b) => a.sequence - b.sequence);
        insuranceComponents.sort((a, b) => a.sequence - b.sequence);

        // Calculate totals
        let totalBasicMonthly = basicSalaryComponents.reduce((sum, c) => sum + c.monthly, 0);
        let totalBasicAnnual = basicSalaryComponents.reduce((sum, c) => sum + c.annual, 0);

        let totalAllowanceMonthly = allowanceComponents.reduce((sum, c) => sum + c.monthly, 0);
        let totalAllowanceAnnual = allowanceComponents.reduce((sum, c) => sum + c.annual, 0);

        let totalStatutoryMonthly = statutoryComponents.reduce((sum, c) => sum + c.monthly, 0);
        let totalStatutoryAnnual = statutoryComponents.reduce((sum, c) => sum + c.annual, 0);

        let totalInsuranceMonthly = insuranceComponents.reduce((sum, c) => sum + c.monthly, 0);
        let totalInsuranceAnnual = insuranceComponents.reduce((sum, c) => sum + c.annual, 0);

        let grossSalaryMonthly = totalBasicMonthly + totalAllowanceMonthly;
        let grossSalaryAnnual = totalBasicAnnual + totalAllowanceAnnual;

        let totalSalaryMonthly = grossSalaryMonthly + totalStatutoryMonthly + totalInsuranceMonthly;
        let totalSalaryAnnual = grossSalaryAnnual + totalStatutoryAnnual + totalInsuranceAnnual;

        // Helper function to create component rows
        function createComponentRows(components) {
            return components.map(c => `
                <tr>
                    <td class="header-left">${c.name}</td>
                    <td class="data-center text-right">${Math.round(c.monthly).toLocaleString()}</td>
                    <td class="data-center text-right">${Math.round(c.annual).toLocaleString()}</td>
                </tr>
            `).join('');
        }

        // Build complete salary structure table
        let salaryStructureTable = `
            <style>
                .salary-table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }
                .salary-table th, .salary-table td {
                    border: 1px solid #d1d8dd;
                    padding: 8px;
                }
                .salary-table .header-title {
                    background-color: #f5f7fa;
                    text-align: center;
                    font-weight: bold;
                    font-size: 14px;
                }
                .salary-table .header-left {
                    text-align: left;
                    font-weight: 600;
                }
                .salary-table .header-center {
                    text-align: center;
                    font-weight: 600;
                    background-color: #f5f7fa;
                }
                .salary-table .data-center {
                    text-align: center;
                }
                .salary-table .statutory-row {
                    background-color: #e8f4f8;
                }
                .salary-table .statutory-row td {
                    font-weight: bold;
                }
                .salary-table .total-row {
                    background-color: #f0f0f0;
                    font-weight: bold;
                }
                .note-section {
                    margin-top: 20px;
                    font-size: 12px;
                    color: #666;
                }
            </style>
            <table class="salary-table">
                <tr>
                    <th colspan="3" class="header-title">Salary Structure w.e.f. ${frappe.datetime.str_to_user(frm.doc.from_date)}</th>
                </tr>
                <tr>
                    <th class="header-left">COMPENSATION COMPONENTS</th>
                    <th class="header-center">PER MONTH</th>
                    <th class="header-center">PER ANNUM</th>
                </tr>

                <tr class="statutory-row"><td><strong>Basic Salary</strong></td><td></td><td></td></tr>
                ${createComponentRows(basicSalaryComponents)}
                <tr class="total-row">
                    <td><strong>TOTAL BASIC SALARY</strong></td>
                    <td class="data-center text-right"><strong>${Math.round(totalBasicMonthly).toLocaleString()}</strong></td>
                    <td class="data-center text-right"><strong>${Math.round(totalBasicAnnual).toLocaleString()}</strong></td>
                </tr>

                <tr class="statutory-row"><td><strong>Allowances</strong></td><td></td><td></td></tr>
                ${createComponentRows(allowanceComponents)}
                <tr class="total-row">
                    <td><strong>TOTAL ALLOWANCES</strong></td>
                    <td class="data-center text-right"><strong>${Math.round(totalAllowanceMonthly).toLocaleString()}</strong></td>
                    <td class="data-center text-right"><strong>${Math.round(totalAllowanceAnnual).toLocaleString()}</strong></td>
                </tr>

                <tr class="total-row">
                    <td><strong>GROSS SALARY</strong></td>
                    <td class="data-center text-right"><strong>${Math.round(grossSalaryMonthly).toLocaleString()}</strong></td>
                    <td class="data-center text-right"><strong>${Math.round(grossSalaryAnnual).toLocaleString()}</strong></td>
                </tr>

                <tr class="statutory-row"><td><strong>STATUTORY PAYMENTS</strong></td><td></td><td></td></tr>
                ${createComponentRows(statutoryComponents)}
                <tr class="total-row">
                    <td><strong>TOTAL STATUTORY PAYMENTS</strong></td>
                    <td class="data-center text-right"><strong>${Math.round(totalStatutoryMonthly).toLocaleString()}</strong></td>
                    <td class="data-center text-right"><strong>${Math.round(totalStatutoryAnnual).toLocaleString()}</strong></td>
                </tr>

                <tr class="statutory-row"><td><strong>HEALTH INSURANCE</strong></td><td></td><td></td></tr>
                ${createComponentRows(insuranceComponents)}
                <tr class="total-row">
                    <td><strong>TOTAL HEALTH INSURANCE COST</strong></td>
                    <td class="data-center text-right"><strong>${Math.round(totalInsuranceMonthly).toLocaleString()}</strong></td>
                    <td class="data-center text-right"><strong>${Math.round(totalInsuranceAnnual).toLocaleString()}</strong></td>
                </tr>

                <tr class="total-row">
                    <td><strong>TOTAL SALARY</strong></td>
                    <td class="data-center text-right"><strong>${Math.round(totalSalaryMonthly).toLocaleString()}</strong></td>
                    <td class="data-center text-right"><strong>${Math.round(totalSalaryAnnual).toLocaleString()}</strong></td>
                </tr>
            </table>

            <div class="note-section">
                <p>*Gratuity: Gratuity is payable as per the provisions of The Payment of the Gratuity Act, 1972.</p>
            </div>
        `;

        document.getElementById("ctc_preview").innerHTML = salaryStructureTable;
    }
}


// OLD CODE BELOW - KEPT FOR REFERENCE IF NEEDED
/*
        // Handle reimbursements if applicable
        if (frm.doc.custom_statistical_amount > 0) {
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

                let annualAmountCell = newRow.insertCell();
                annualAmountCell.className = "text-right";
                annualAmountCell.textContent = (component.monthly_total_amount * 12).toLocaleString();

                totalMonthlyEarnings += component.monthly_total_amount;
                totalAnnualEarnings += component.monthly_total_amount * 12;
            });
        }

        // Define and handle deductions
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

                if(res.message.round_to_the_nearest_integer == 0)
                    {

                        total_ctc.push(v.default_amount)
                        let newRow = deductionTableBody.insertRow();

                        let componentCell = newRow.insertCell();
                        componentCell.textContent = res.message.name;

                        let roundedAmount = (v.default_amount);
                        let formattedAmount = roundedAmount.toLocaleString();
                        let amountCell = newRow.insertCell();
                        amountCell.className = "text-right";
                        amountCell.textContent = formattedAmount;

                        let annualAmount = Math.round((v.default_amount)*12);
                        let formattedAnnualAmount = annualAmount.toLocaleString();
                        let annualAmountCell = newRow.insertCell();
                        annualAmountCell.className = "text-right";
                        annualAmountCell.textContent = formattedAnnualAmount;

                        // Accumulate totals
                        totalMonthlyDeductions += roundedAmount;
                        totalAnnualDeductions += annualAmount;



                    }
                    else{

                        total_ctc.push(Math.round(v.default_amount))
                        let newRow = deductionTableBody.insertRow();

                        let componentCell = newRow.insertCell();
                        componentCell.textContent = res.message.name;

                        let roundedAmount = Math.round(v.default_amount);
                        let formattedAmount = roundedAmount.toLocaleString();
                        let amountCell = newRow.insertCell();
                        amountCell.className = "text-right";
                        amountCell.textContent = formattedAmount;

                        let annualAmount = Math.round(v.default_amount)*12;
                        let formattedAnnualAmount = annualAmount.toLocaleString();
                        let annualAmountCell = newRow.insertCell();
                        annualAmountCell.className = "text-right";
                        annualAmountCell.textContent = formattedAnnualAmount;

                        // Accumulate totals
                        totalMonthlyDeductions += roundedAmount;
                        totalAnnualDeductions += annualAmount;

                    }
            }
        }

        var sum = total_ctc.reduce(function(accumulator, currentValue) {
            return accumulator + currentValue;
        }, 0);

        // console.log(sum);


        if (frm.doc.base) {
            // Define the table structure with proper HTML syntax and include table headings
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

            // Insert the table structure into the element with id "total_ctc"
            document.getElementById("total_ctc").innerHTML = total_ctcTable;
            let ctc_body = document.getElementById("ctc_breakup_body");

            // Create a new row in the table body
            let newRow = ctc_body.insertRow();

            // Insert cells into the new row
            let componentCell = newRow.insertCell();
            componentCell.textContent = "Total CTC";

            let monthlyAmount = Math.round(sum);
            let annualAmount = Math.round(monthlyAmount*12);



            let formattedMonthlyAmount = monthlyAmount.toLocaleString();
            let amountCell = newRow.insertCell();
            amountCell.className = "text-right";
            amountCell.textContent = formattedMonthlyAmount;

            let formattedAnnualAmount = annualAmount.toLocaleString();
            let annualAmountCell = newRow.insertCell();
            annualAmountCell.className = "text-right";
            annualAmountCell.textContent = formattedAnnualAmount;
        }






        // Handle additional components if applicable
        if (frm.doc.custom_is_special_hra || frm.doc.custom_is_special_conveyance || frm.doc.custom_is_car_allowance || frm.doc.custom_is_incentive || frm.doc.custom_is_extra_driver_salary) {
            let additionalComponentTable = `
                <table class="table table-bordered small">
                    <thead>
                        <tr>
                            <th style="width: 16%">Additional Component</th>
                            <th style="width: 16%" class="text-right">Monthly Amount</th>
                            <th style="width: 16%" class="text-right">Annual Amount</th>
                        </tr>
                    </thead>
                    <tbody id="additional_breakup_body"></tbody>
                </table>`;

            document.getElementById("additional_component").innerHTML = additionalComponentTable;
            let additionalTableBody = document.getElementById("additional_breakup_body");

            let components = [];
            let componentAmounts = [];

            if (frm.doc.custom_is_special_hra) {
                components.push("Special HRA");
                componentAmounts.push(frm.doc.custom_special_hra_amount_annual);
            }

            if (frm.doc.custom_is_special_conveyance) {
                components.push("Special Conveyance");
                componentAmounts.push(frm.doc.custom_special_conveyance_amount_annual);
            }

            if (frm.doc.custom_is_car_allowance) {
                components.push("Car Allowance");
                componentAmounts.push(frm.doc.custom_car_allowance_amount_annual);
            }

            if (frm.doc.custom_is_incentive) {
                components.push("Incentive");
                componentAmounts.push(frm.doc.custom_incentive_amount_annual);
            }

            if (frm.doc.custom_is_extra_driver_salary) {
                components.push("Extra Driver Salary");
                componentAmounts.push(frm.doc.custom_extra_driver_salary_value);
            }



            $.each(components, function (i, componentName) {
                let newRow = additionalTableBody.insertRow();

                let componentCell = newRow.insertCell();
                componentCell.textContent = componentName;




                let monthlyAmount = Math.round(componentAmounts[i] / 12)

                let formattedMonthlyAmount = monthlyAmount.toLocaleString();
                // console.log(formattedMonthlyAmount)
                let amountCell = newRow.insertCell();
                amountCell.className = "text-right";
                amountCell.textContent = formattedMonthlyAmount;

                let formattedAnnualAmount = componentAmounts[i].toLocaleString();
                let annualAmountCell = newRow.insertCell();
                annualAmountCell.className = "text-right";
                annualAmountCell.textContent = formattedAnnualAmount;
            });
        }
*/
