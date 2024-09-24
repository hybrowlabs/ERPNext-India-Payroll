

frappe.ui.form.on('Salary Structure Assignment', {



    onload:function(frm)
    {

        if (frm.doc.custom_promotion_id)
        {

            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: "Employee Promotion",
                    filters:{"name":frm.doc.custom_promotion_id}
                },
                callback: function(r) {
                    if (r.message) {

                        console.log(r.message,"1111")

                        frm.set_value("from_date",r.message.promotion_date)
                        
                    }
                }
            });

        }

    },
    

    


    refresh(frm)
    {

        if(frm.doc.docstatus==1)
            {

           
                    change_regime(frm)
                    
            }


           
                setTimeout(() => {
                    
                    frm.remove_custom_button('Payroll Entry', 'Create');
                    // frm.remove_custom_button('Preview Salary Slip', 'Actions');
                    // frm.remove_custom_button('Chose Regime');
                    
                }, 10);



                if (frm.doc.employee && frm.doc.salary_structure && frm.doc.docstatus==1 )
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
        
    },

    
    custom_nps_percentage(frm) {


        
        if (frm.doc.custom_is_nps==1 )
        
        {
        
                if(frm.doc.custom_nps_percentage <= 10) 
                {
    
    
                        var amount = (frm.doc.base / 12 * 35) / 100;
                        
                        
                        
                        var nps_value=(amount*frm.doc.custom_nps_percentage)/100
                        //  console.log(nps_value,"ppp")
                        frm.set_value("custom_nps_amount",nps_value)
                    
                }
        
                else
                {
                    msgprint("you cant put percentage greater than 10")
                   
                    frm.set_value("custom_nps_amount",undefined)
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




custom_nps_amount(frm) {
    if (frm.doc.custom_is_nps == 1 && frm.doc.custom_nps_amount) {
        var amount = (frm.doc.base / 12 * 35) / 100;
        var nps_value = (amount * 10) / 100;

        if (frm.doc.custom_nps_amount > nps_value) {
            msgprint("Please enter an amount less than or equal to " + nps_value);
            frm.set_value("custom_nps_amount", 0);
            frm.set_value("custom_nps_percentage", 0);
        } else {
            // Calculate custom NPS percentage
            var custom_percentage = (frm.doc.custom_nps_amount / amount) * 100;
            frm.set_value("custom_nps_percentage", custom_percentage);
        }
    }
},

})




function change_regime(frm)
{
    if(!frm.is_new() && frm.doc.income_tax_slab)
    {
        frm.add_custom_button("Switch Regime", function() {

            let d = new frappe.ui.Dialog({
                title: 'Enter details',
                fields: [
                   
                    {
                        label: 'Select Regime',
                        fieldname: 'select_regime',
                        fieldtype: 'Link',
                        options:'Income Tax Slab',
                        reqd:1,
                        default:frm.doc.income_tax_slab
                    }
                ],
                size: 'small', // small, large, extra-large 
                primary_action_label: 'Submit',
                primary_action(values) {
                    console.log(values);

                    frappe.call({

                        "method":"cn_indian_payroll.cn_indian_payroll.overrides.declaration.switch_regime",
                        args:{

                            doc_id: frm.doc.name,
                            employee:frm.doc.employee,
                            regime:values.select_regime

                        },
                        callback :function(res)
                        {
                            frm.reload_doc();
                           

                        }

            })



                    d.hide();
                }
            });
            
            d.show();
            

        });
        frm.change_custom_button_type('Switch Regime', null, 'primary');
    }
}

function send_to_employee(frm)
{
    frm.add_custom_button("Send To Employee", function() {


    })
    frm.change_custom_button_type('Send To Employee', null, 'primary');

}


async function processSalaryComponents(frm) {

    var total_ctc=[]
    const response = await frappe.call({
        method: "hrms.payroll.doctype.salary_structure.salary_structure.make_salary_slip",
        args: {
            source_name: frm.doc.salary_structure,
            employee: frm.doc.employee,
            print_format: 'Salary Slip Standard for CTC',
            docstatus: frm.doc.docstatus,
            posting_date: frm.doc.from_date
        }
    });

    if (response.message) {
        // Define the tables for earnings, reimbursements, deductions, and additional components
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

        // Processing earnings components
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

                total_ctc.push(v.amount)
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

                // Accumulate totals
                totalMonthlyEarnings += roundedAmount;
                totalAnnualEarnings += annualAmount;
            }
        }

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

                total_ctc.push(component.monthly_total_amount)

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

                total_ctc.push(v.amount)
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

                // Accumulate totals
                totalMonthlyDeductions += roundedAmount;
                totalAnnualDeductions += annualAmount;
            }
        }

        var sum = total_ctc.reduce(function(accumulator, currentValue) {
            return accumulator + currentValue;
        }, 0);
        
        console.log(sum);


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


       
        

        
    }
}
