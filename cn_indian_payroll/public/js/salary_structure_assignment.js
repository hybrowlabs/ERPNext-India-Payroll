

frappe.ui.form.on('Salary Structure Assignment', {


    refresh(frm)
    {
        if(frm.doc.docstatus==1)

        {

        frm.add_custom_button(__('View CTC BreakUp'), async function() {
            frappe.call({
                method: "cn_indian_payroll.cn_indian_payroll.overrides.salary_structure_assignment.generate_ctc_pdf",
                args: {
                    employee: frm.doc.employee,
                    salary_structure: frm.doc.salary_structure,
                    print_format: 'Salary Slip Standard',
                    posting_date: frm.doc.from_date,
                    employee_benefits: frm.doc.custom_employee_reimbursements
                },
                callback: function(r) {
                    if (r.message && r.message.pdf_url) {
                        window.open(r.message.pdf_url, '_blank');
                    } else {
                        frappe.msgprint("Failed to generate PDF");
                    }
                }
            });
        }, __('Actions'));


        }

        if (frm.doc.employee && frm.doc.docstatus==1)
            {
                    processSalaryComponents(frm)
            }

        frm.set_query("custom_lwf_state", function() {
            return {
                filters: {
                    lwf_frequency: 1
                }
            };
        });



        frm.fields_dict['custom_employee_reimbursements'].grid.get_field('reimbursements').get_query = function(doc, cdt, cdn) {
            var child = locals[cdt][cdn];

            return {
                filters:[
                    ['custom_is_reimbursement', '=', 1]
                ]
            }
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
                    if (res.message && res.message.lwf_frequency_list) {
                        let frequency_array = res.message.lwf_frequency_list.map(row => row.frequency_type);
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

})



async function processSalaryComponents(frm) {

    var total_ctc=[]
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
                let newRow = tableBody.insertRow();

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


                totalMonthlyEarnings += roundedAmount;
                totalAnnualEarnings += annualAmount;
            }
        }


        if (frm.doc.custom_total_amount > 0) {
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






    }
}
