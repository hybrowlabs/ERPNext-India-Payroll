

frappe.ui.form.on('Salary Structure Assignment', {
    

    // employee:function(frm)
    // {
    //     if(frm.doc.employee)

    //         {

    //             frappe.call({
    //                 method: "frappe.client.get",
    //                 args: {
    //                     doctype: "Employee",
    //                     filters: { name: frm.doc.employee },
    //                     fields: ["*"]
    //                 },
    //                 callback: function(res) {
    //                     if (res.message)
    //                     {

    //                         console.log(res.message,"222")

    //                         frm.clear_table("custom_additional_component");
    //                         frm.refresh_field("custom_additional_component");

    //                         $.each(res.message.custom_additional_salary_component,function(i,v)
    //                             {

    //                                 console.log(v.amount)

    //                                 let child = frm.add_child("custom_additional_component");
    //                                 frappe.model.set_value(child.doctype, child.name, "salary_component", v.salary_component);
    //                                 frappe.model.set_value(child.doctype, child.name, "amount", v.amount);

                                
                            
                                
                                    
    //                             })

    //                             frm.refresh_field("custom_additional_component");

    //                     }
    //                 }

    //             })

    //         }

    // },


    refresh(frm)
    {

       

       
        var array=[];
        var array1=[];
        var totalMonthlyEarnings = 0
        let totalAnnualEarnings = 0;

        let totalMonthlyEarnings1 = 0
        let totalAnnualEarnings1 = 0;
    
        let totalMonthlyDeductions = 0;
        let totalAnnualDeductions = 0;
        if (!frm.is_new()) {


        if (frm.doc.employee && frm.doc.salary_structure && frm.doc.docstatus==1) {
            
        
            let salary_breakup = `
                <table class="table table-bordered small"> 
                    <thead> 
                        <tr> 
                            <th style="width: 16%">Salary Component (Earnings)</th> 
                            <th style="width: 16%" class="text-right">Monthly Amount</th> 
                            <th style="width: 16%" class="text-right">Annual Amount</th> 
                        </tr> 
                    </thead> 
                    <tbody id="salary_breakup_body">   
                    </tbody>
                    <tfoot>
                       
                    </tfoot>
                </table>`;
        
            let deduction_breakup = `
                <table class="table table-bordered small"> 
                    <thead> 
                        <tr> 
                            <th style="width: 16%">Salary Component (Deduction)</th> 
                            <th style="width: 16%" class="text-right">Monthly Amount</th> 
                            <th style="width: 16%" class="text-right">Annual Amount</th> 
                        </tr> 
                    </thead> 
                    <tbody id="deduction_breakup_body">   
                    </tbody>
                    <tfoot>
                        <tr>
                            <th>Total (Cost to Company)</th>
                            <th id="total_monthly_deductions" class="text-right"></th>
                            <th id="total_annual_deductions" class="text-right"></th>
                        </tr>
                    </tfoot>
                </table>`;
        
            document.getElementById("ctc_preview").innerHTML = salary_breakup;
            document.getElementById("deduction_preview").innerHTML = deduction_breakup;
        
            let tableBody = document.getElementById("salary_breakup_body");
            let tableBody1 = document.getElementById("deduction_breakup_body");
        
           
        
            frappe.call({
                method: "hrms.payroll.doctype.salary_structure.salary_structure.make_salary_slip",
                args: {
                    source_name: frm.doc.salary_structure,
                    employee: frm.doc.employee,
                    print_format: 'Salary Slip Standard for CTC',
                    docstatus:frm.doc.docstatus
                },
                callback: function(response) {
                    $.each(response.message.earnings, function(i, v) {
                         

                         var detail = {
                            salary_component: v.salary_component,
                            amount: v.amount
                        };
                        array.push(detail);

                    })

                   
                    function fetchSalaryComponentDetails(index) {
                        if (index < array.length) {
                            var salaryComponent = array[index].salary_component;
            
                            frappe.call({
                                method: "frappe.client.get",
                                args: {
                                    doctype: "Salary Component",
                                    filters: { name: salaryComponent },
                                    fields: ["*"]
                                },
                                callback: function(res) {
                                    if (res.message && res.message.custom_is_part_of_ctc == 1) {
                                       
            
                                        
                                        let newRow = tableBody.insertRow();
            
                                       
                                        let componentCell = newRow.insertCell();
                                        componentCell.textContent = res.message.name;
            
                                        let formattedAmount = array[index].amount.toLocaleString();
                                        let amountCell = newRow.insertCell();
                                        amountCell.className = "text-right";
                                        amountCell.textContent = formattedAmount;

                                        let annualAmount = array[index].amount * 12;
                                        let formattedAnnualAmount = annualAmount.toLocaleString();

                                        
                                        let annualAmountCell = newRow.insertCell();
                                        annualAmountCell.className = "text-right";
                                        annualAmountCell.textContent = formattedAnnualAmount;

                                       

                                        totalMonthlyEarnings += array[index].amount;
                                        

                                        
            
                                        
                                        fetchSalaryComponentDetails(index + 1);

                                       
                                       
                                    } 
                                    else 
                                    {
                                       
                                        fetchSalaryComponentDetails(index + 1);
                                    }
                                }
                            });
                        }
                    }
            
                   
                    fetchSalaryComponentDetails(0);



        
                    $.each(response.message.deductions, function(i, k) {


                        var detail1 = {
                            salary_component: k.salary_component,
                            amount: k.amount
                        };
                        array1.push(detail1);

                    });

                   
                    function fetchSalaryComponentDetailsDeduction(index) {
                        if (index < array1.length) {
                            var salaryComponent = array1[index].salary_component;
            
                            frappe.call({
                                method: "frappe.client.get",
                                args: {
                                    doctype: "Salary Component",
                                    filters: { name: salaryComponent },
                                    fields: ["*"]
                                },
                                callback: function(res) {
                                    if (res.message && res.message.custom_is_part_of_ctc == 1) {
                                       
            
                                        
                                        let newRow = tableBody1.insertRow();
                                        let componentCell = newRow.insertCell();
                                        componentCell.textContent = res.message.name;
                                        
            
                                        let formattedAmount = array1[index].amount.toLocaleString();
                                       

                                        let amountCell = newRow.insertCell();
                                        amountCell.className = "text-right";
                                        amountCell.textContent = formattedAmount;



                                        let annualAmount = array1[index].amount * 12;
                                        let formattedAnnualAmount = annualAmount.toLocaleString();
                                        let annualAmountCell = newRow.insertCell();
                                        annualAmountCell.className = "text-right";
                                        annualAmountCell.textContent = formattedAnnualAmount;

                                        totalMonthlyDeductions+=array1[index].amount
                                        totalAnnualDeductions += array1[index].amount * 12;

                                        

                                        

                                        



                                        
            


                                        fetchSalaryComponentDetailsDeduction(index + 1);
                                    } 
                                    else 
                                    {
                                       
                                        fetchSalaryComponentDetailsDeduction(index + 1);
                                    }
                                }
                            });

                            
                            


                        }


                                        document.getElementById("total_monthly_deductions").textContent = (frm.doc.base / 12).toLocaleString();
                                        document.getElementById("total_annual_deductions").textContent =  frm.doc.base.toLocaleString();
                        
                    }

                    
            
                   
                     fetchSalaryComponentDetailsDeduction(0);


                    


                     


                    
                   
        
                    if (frm.doc.custom_statistical_amount > 0) {
                        let reimbursement_breakup = `
                            <table class="table table-bordered small"> 
                                <thead> 
                                    <tr> 
                                        <th style="width: 16%">Reimbursements</th> 
                                        <th style="width: 16%" class="text-right">Monthly Amount</th> 
                                        <th style="width: 16%" class="text-right">Annual Amount</th> 
                                    </tr> 
                                </thead> 
                                <tbody id="reimbursement_breakup_body">   
                                </tbody>
                                <tfoot>
                                   
                                </tfoot>
                            </table>`;
                        document.getElementById("reimbursement_preview").innerHTML = reimbursement_breakup;
        
                        let tableBody2 = document.getElementById("reimbursement_breakup_body");
                       


                                 $.each(frm.doc.custom_employee_reimbursements, function(i, component) {
                                    
                                    let newRow = tableBody2.insertRow();
                                    let componentCell = newRow.insertCell();
                                    componentCell.textContent = component.reimbursements;
                                    
                        
                                    let amountCell = newRow.insertCell();
                                    amountCell.className = "text-right";
                                    amountCell.textContent = component.monthly_total_amount.toLocaleString();
                        
                                    let annualAmountCell = newRow.insertCell();
                                    annualAmountCell.className = "text-right";
                                    annualAmountCell.textContent = (component.monthly_total_amount * 12).toLocaleString();
                        
                                    totalMonthlyEarnings1+=component.monthly_total_amount;
                                    totalAnnualEarnings1 += component.monthly_total_amount * 12;

                                    // console.log(totalMonthlyEarnings1)



                                   
                                });

                                
                    }






                    if (frm.doc.custom_is_special_hra || frm.doc.custom_is_special_conveyance || frm.doc.custom_is_car_allowance) {
                        let additional_component = `
                            <table class="table table-bordered small"> 
                                <thead> 
                                    <tr> 
                                        <th style="width: 16%">Additional Component</th> 
                                        <th style="width: 16%" class="text-right">Monthly Amount</th> 
                                        <th style="width: 16%" class="text-right">Annual Amount</th> 
                                    </tr> 
                                </thead> 
                                <tbody id="additional_breakup_body">   
                                </tbody>
                                <tfoot>
                                </tfoot>
                            </table>`;
                        document.getElementById("additional_component").innerHTML = additional_component;
                    
                        let tableBody3 = document.getElementById("additional_breakup_body");
                    
                        let component = [];
                        let component_amount = [];
                    
                        if (frm.doc.custom_is_special_hra == 1) {
                            component.push("Special HRA");
                            component_amount.push(frm.doc.custom_special_hra_amount_annual);
                        }
                    
                        if (frm.doc.custom_is_special_conveyance == 1) {
                            component.push("Special Conveyance");
                            component_amount.push(frm.doc.custom_special_conveyance_amount_annual);
                        }
                    
                        if (frm.doc.custom_is_car_allowance == 1) {
                            component.push("Car Allowance");
                            component_amount.push(frm.doc.custom_car_allowance_amount_annual);
                        }
                    
                        console.log(component);
                        console.log(component_amount);
                    
                        $.each(component, function (i, b) {
                            let newRow = tableBody3.insertRow();
                            let componentCell = newRow.insertCell();
                            componentCell.textContent = b;
                    
                            let amountCell = newRow.insertCell();
                            amountCell.className = "text-right";
                            let monthlyAmount = component_amount[i] / 12;
                            amountCell.textContent = monthlyAmount.toLocaleString();
                    
                            let annualAmountCell = newRow.insertCell();
                            annualAmountCell.className = "text-right";
                            annualAmountCell.textContent = component_amount[i].toLocaleString();
                        });
                    }
                    

                    
                }
            });



            


            


           

           

            
        }
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


// function additional_component(frm)
// {

//     if(frm.is_new())
//             {
//                 frm.clear_table("custom_additional_component");
//                 frm.refresh_field("custom_additional_component");
            
//                 let additional_component_array = ["Car Allowance", "Special HRA", "Special Conveyance"];
            
//                 $.each(additional_component_array, function(i, v) {
//                     let child = frm.add_child("custom_additional_component");
//                     frappe.model.set_value(child.doctype, child.name, "salary_component", v);
//                 });
            
//                 frm.refresh_field("custom_additional_component");
//             }

// }

