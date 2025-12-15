


frappe.ui.form.on('Employee Tax Exemption Declaration', {
    refresh(frm) {
        frm.trigger("change_tax_regime");
        frm.trigger("display_declaration_form");
        tds_projection_html(frm)

    },

    change_tax_regime(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button("Choose Regime", function () {
                let d = new frappe.ui.Dialog({
                    title: 'Choose Tax Regime',
                    fields: [
                        {
                            label: 'Select Regime',
                            fieldname: 'select_regime',
                            fieldtype: 'Select',
                            options: ['Old Regime', 'New Regime'],
                            reqd: 1,
                            default: frm.doc.custom_tax_regime,
                            description: `Your current tax regime is <strong>${frm.doc.custom_tax_regime}</strong>`
                        }
                    ],
                    size: 'small',
                    primary_action_label: 'Submit',
                    primary_action(values) {
                        frappe.call({
                            method: "cn_indian_payroll.cn_indian_payroll.overrides.declaration.choose_regime",
                            args: {
                                doc_id: frm.doc.name,
                                employee: frm.doc.employee,
                                company: frm.doc.company,
                                payroll_period: frm.doc.payroll_period,
                                regime: values.select_regime
                            },
                            callback: function (res) {
                                frm.reload_doc();
                            }
                        });
                        d.hide();
                    }
                });
                d.show();
            });

            frm.change_custom_button_type('Choose Regime', null, 'primary');
        }
    },

    display_declaration_form(frm) {

        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Employee Tax Exemption Sub Category",
                fields: ["name", "exemption_category", "max_amount", "custom_description", "custom_component_type"],
                filters: {
                    is_active: 1
                },
                order_by: "custom_sequence asc",
                limit_page_length: 999999
            },
            callback: function (r) {
                if (r.message && r.message.length > 0) {

                    let stored_data = {};
                    if (frm.doc.custom_declaration_form_data) {
                        try {
                            stored_data = JSON.parse(frm.doc.custom_declaration_form_data);
                        } catch (e) {}
                    }

                    let rows_html = '';

                    r.message.forEach(row => {
                        const stored_row = Array.isArray(stored_data)
                            ? stored_data.find(item => item.id === row.name || item.sub_category === row.name)
                            : null;

                        // const stored_value = stored_row ? stored_row.max_amount || '' : '';

                        const stored_value = stored_row ? stored_row.amount || '' : '';

                        // const stored_value = stored_row ? stored_row.value || stored_row.amount || '' : '';



                        let is_readonly = false;
                        if (frm.doc.custom_tax_regime === "New Regime") {
                            is_readonly = true;
                        } else if (frm.doc.custom_tax_regime === "Old Regime") {
                            is_readonly = ["NPS", "EPF", "Professional Tax"].includes(row.custom_component_type);
                        }

                        const readonly_attr = is_readonly ? 'readonly' : '';

                        rows_html += `
                            <tr data-id="${row.name}" data-max="${row.max_amount}" data-category="${row.exemption_category}">
                                <td>${row.name}</td>
                                <td>${row.max_amount || ''}</td>
                                <td>${row.exemption_category || ''}</td>
                                <td>${row.custom_description || ''}</td>
                                <td><input type="number" class="input-field" style="width: 100%" value="${stored_value}" ${readonly_attr} /></td>
                            </tr>
                        `;
                    });

                    let info_message = '';
                    if (frm.doc.custom_tax_regime === "New Regime") {
                        info_message = `
                            <div style="
                                background-color: #fff3cd;
                                color: #856404;
                                padding: 12px;
                                margin-bottom: 15px;
                                border: 1px solid #ffeeba;
                                border-radius: 4px;
                            ">
                                <strong>Note:</strong> All exemption input fields are disabled under <strong>New Regime</strong>.
                            </div>
                        `;
                    }

                    const preview= `
                        ${info_message}
                        <style>
                            .styled-declaration-table {
                                width: 100%;
                                border-collapse: collapse;
                                margin-top: 15px;
                            }
                            .styled-declaration-table th, .styled-declaration-table td {
                                padding: 12px;
                                border: 1px solid #ccc;
                                text-align: left;
                            }
                            .styled-declaration-table th {
                                background-color: #f7f7f7;
                            }
                        </style>

                        <table class="styled-declaration-table" id="summary-table">
                            <thead>

                                <tr>
                                    <th>The Selected Tax Regime</th>
                                    <td><b>${frm.doc.custom_tax_regime}</b></td>
                                </tr>
                                <tr>
                                    <th>Annual HRA Exemption</th>
                                    <td><b>${frm.doc.annual_hra_exemption || 0}</b></td>
                                </tr>
                                 <tr>
                                    <th>Total 80D Exemption</th>
                                    <td><b>${frm.doc.custom_total_80d_exemption||0}</b></td>
                                </tr>
                                <tr>
                                    <th>Total Declared Amount</th>
                                    <td><b>${Math.round(frm.doc.total_declared_amount+frm.doc.monthly_house_rent || 0)}</b></td>
                                </tr>
                                <tr>
                                    <th>Total Exemption Eligible Amount</th>
                                    <td><b>${Math.round(frm.doc.total_exemption_amount || 0)}</b></td>
                                </tr>


                            </thead>
                        </table>



                    `;

                    frm.fields_dict.custom_declaration_total_preview.$wrapper.html(preview);
                    frm.fields_dict.custom_declaration_total_preview.$wrapper.css("width", "100%");

                    const html = `
                        ${info_message}




                        <style>
                            .styled-declaration-table {
                                width: 100%;
                                border-collapse: collapse;
                                margin-top: 15px;
                            }
                            .styled-declaration-table,
                            .styled-declaration-table th,
                            .styled-declaration-table td {
                                border: 2px solid #000; /* bold black borders */
                            }
                            .styled-declaration-table th,
                            .styled-declaration-table td {
                                padding: 12px;
                                text-align: left;
                                font-weight: bold; /* bold text inside cells */
                            }
                                .input-field {
                                                width: 100%;
                                                font-weight: bold;
                                                border: 2px solid #000;
                                                padding: 5px;
                                                box-sizing: border-box;
                        </style>



                        <table class="styled-declaration-table" id="declaration-table">
                            <thead>
                                <tr>
                                    <th>Invested Description</th>
                                    <th>Maximum Limit</th>
                                    <th>Section</th>
                                    <th>Narration</th>
                                    <th>Amount</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${rows_html}
                            </tbody>
                        </table>


                    `;

                    frm.fields_dict.custom_declaration_form.$wrapper.html(html);
                    frm.fields_dict.custom_declaration_form.$wrapper.css("width", "100%");

                    const inputs = document.querySelectorAll("#declaration-table tbody tr input");

                    inputs.forEach(input => {
                        if (!input.hasAttribute("readonly")) {
                            input.addEventListener("change", () => {
                                const formData = [];
                                frm.clear_table("declarations");

                                document.querySelectorAll("#declaration-table tbody tr").forEach(row => {
                                    const id = row.getAttribute("data-id");
                                    const max = parseFloat(row.getAttribute("data-max")) || 0;
                                    const exemption_category = row.getAttribute("data-category");
                                    let value = parseFloat(row.querySelector("input").value || 0);


                                    console.log(exemption_category,"value---")



                                    if (value > 0) {
                                        formData.push({
                                            id: id,
                                            sub_category: id,
                                            exemption_category: exemption_category,
                                            max_amount: max > 0 ? max : value,
                                            amount: value,
                                            value: value
                                        });

                                        const d = frm.add_child("declarations");
                                        d.exemption_sub_category = id;
                                        d.exemption_category = exemption_category;
                                        d.max_amount = max > 0 ? max : value;
                                        d.amount = value;
                                    }
                                });

                                frm.set_value("custom_declaration_form_data", JSON.stringify(formData));
                                frm.refresh_field("declarations");
                            });
                        }
                    });
                }
            }
        });

    },

    tds_projection_html(frm) {
        if (frm.doc.docstatus === 1) {
                frappe.call({
                    method: "cn_indian_payroll.cn_indian_payroll.overrides.tds_projection_calculation.calculate_tds_projection",
                    args: {
                        doc: frm.doc
                    },
                    callback: function (res) {
                        if (res.message) {
                            let data = res.message;

                            console.log(data);

                            let oldSlabRows = "";
                                for (let i = 0; i < data.old_regime_from_amounts.length; i++) {
                                    oldSlabRows += `
                                        <tr>
                                            <td style="padding: 6px;">₹ ${data.old_regime_from_amounts[i]}</td>
                                            <td style="padding: 6px; text-align: right;">₹ ${data.old_regime_to_amounts[i]}</td>
                                            <td style="padding: 6px; text-align: right;">${data.old_regime_percentages[i]}%</td>
                                            <td style="padding: 6px; text-align: right;">₹ ${data.old_regime_tax_per_slab[i]}</td>
                                        </tr>
                                    `;
                                }

                                // Build HTML rows for New Regime Slab
                                let newSlabRows = "";
                                for (let i = 0; i < data.new_regime_from_amounts.length; i++) {
                                    newSlabRows += `
                                        <tr>
                                            <td style="padding: 6px;">₹ ${data.new_regime_from_amounts[i]}</td>
                                            <td style="padding: 6px; text-align: right;">₹ ${data.new_regime_to_amounts[i]}</td>
                                            <td style="padding: 6px; text-align: right;">${data.new_regime_percentages[i]}%</td>
                                            <td style="padding: 6px; text-align: right;">₹ ${data.new_regime_tax_per_slab[i]}</td>
                                        </tr>
                                    `;
                                }

                                let old_tax = (
                                    (data.old_regime_education_cess + data.old_regime_surcharge +
                                    (data.old_regime_total_tax - data.old_regime_rebate_amount)) -
                                    data.total_tax_already_paid
                                );

                                let new_tax = (
                                    (data.new_regime_education_cess+data.new_regime_surcharge+
                                    (data.new_regime_total_tax-data.new_regime_rebate_amount)) -
                                    data.total_tax_already_paid
                                );

                                let old_tax_balance = (
                                    (
                                        data.old_regime_education_cess +
                                        data.old_regime_surcharge +
                                        (data.old_regime_total_tax - data.old_regime_rebate_amount)
                                    ) - data.advance_tax
                                ) - data.total_tax_already_paid;


                                let new_tax_balance = (
                                    (
                                        data.new_regime_education_cess +
                                        data.new_regime_surcharge +
                                        (data.new_regime_total_tax - data.new_regime_rebate_amount)
                                    ) - data.advance_tax
                                ) - data.total_tax_already_paid;


                                let monthBase = data.month_count === 0 ? data.num_months : data.month_count+1;

                                let currentTax_old_regime = old_tax / monthBase;
                                let currentTax_new_regime = new_tax / monthBase;

                                let currentTax_old_regime_tax = old_tax_balance / monthBase;
                                let currentTax_new_regime_tax = new_tax_balance / monthBase;


                        const html = `
                                    <table class="table table-bordered" style="width: 100%; border-collapse: collapse; margin-top: 10px;">
                                        <thead style="background-color: #f0f0f0;">
                                            <tr style="background-color:rgba(3, 9, 15, 0.68); color: white;">
                                                <th style="padding: 10px; border: 1px solid #ddd;">Title</th>
                                                <th style="padding: 10px; border: 1px solid #ddd;">Old Regime</th>
                                                <th style="padding: 10px; border: 1px solid #ddd;">New Regime</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td style="padding: 10px; border: 1px solid #ddd;">Taxable Earnings (Current)</td>
                                                <td><div style="text-align: right"> ₹ ${data.current_taxable_earnings_old_regime}</div></td>
                                                <td><div style="text-align: right"> ₹ ${data.current_taxable_earnings_new_regime}</div></td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 10px; border: 1px solid #ddd;">Taxable Earnings (Future)</td>
                                                <td><div style="text-align: right"> ₹ ${data.future_taxable_earnings_old_regime}</div></td>
                                                <td><div style="text-align: right"> ₹ ${data.future_taxable_earnings_new_regime}</div></td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 10px; border: 1px solid #ddd;">Loan Perquisite</td>
                                                <td><div style="text-align: right"> ₹ ${data.loan_perquisite_amount}</div></td>
                                                <td><div style="text-align: right"> ₹ ${data.loan_perquisite_amount}</div></td>
                                            </tr>
                                            <tr style="font-weight: bold; background-color: #e9ecef;">
                                                <td>Total Taxable Earnings (Current+Future+Loan)</td>
                                                <td><div style="text-align: right"> ₹ ${data.total_taxable_earnings_old_regime}</div></td>
                                                <td><div style="text-align: right"> ₹ ${data.total_taxable_earnings_new_regime}</div></td>
                                            </tr>

                                            <tr>
                                                <!-- First column with nested table -->
                                                <td>
                                                    <b>Less: Allowances Exempted U/s 16</b>
                                                    <table style="width: 100%; border-collapse: collapse; margin-top: 5px;" border="1">
                                                        <thead style="background-color: #f0f0f0;">
                                                            <tr>
                                                                <th style="padding: 6px;">Title</th>
                                                                <th style="padding: 6px; text-align: right;">Old Regime</th>
                                                                <th style="padding: 6px; text-align: right;">New Regime</th>
                                                            </tr>
                                                        </thead>
                                                        <tbody>
                                                            <tr>
                                                                <td style="padding: 6px;">Standard Deduction</td>
                                                                <td style="padding: 6px; text-align: right;">₹ ${data.old_regime_standard_value}</td>
                                                                <td style="padding: 6px; text-align: right;">₹ ${data.new_regime_standard_value}</td>
                                                            </tr>
                                                            <tr>
                                                                <td style="padding: 6px;">Professional Tax</td>
                                                                <td style="padding: 6px; text-align: right;">₹ ${data.pt_amount}</td>
                                                                <td style="padding: 6px; text-align: right;">₹ 0</td>
                                                            </tr>

                                                        </tbody>
                                                    </table>
                                                </td>

                                                <!-- Second column: Old Regime Total -->
                                                <td><div style="text-align: right;">₹ ${data.old_regime_standard_value+data.pt_amount}</div></td>

                                                <!-- Third column: New Regime Total -->
                                                <td><div style="text-align: right;">₹ ${data.new_regime_standard_value}</div></td>
                                            </tr>

                                             <tr>
                                                <td style="padding: 10px; border: 1px solid #ddd;">HRA Exemptions</td>
                                                <td><div style="text-align: right"> ₹ ${data.hra_exemptions}</div></td>
                                                <td><div style="text-align: right"> ₹ 0</div></td>
                                            </tr>

                                            <tr>
                                                <td style="padding: 10px; border: 1px solid #ddd;">Total Exemption/Deductions</td>
                                                <td><div style="text-align: right"> ₹ ${data.total_old_regime_deductions}</div></td>
                                                <td><div style="text-align: right"> ₹ ${data.total_new_regime_deductions}</div></td>
                                            </tr>

                                             <tr style="font-weight: bold; background-color: #e9ecef;">
                                                <td style="padding: 10px; border: 1px solid #ddd;">Annual Taxable Income</td>
                                                <td><div style="text-align: right"> ₹ ${data.old_regime_annual_taxable_income}</div></td>
                                                <td><div style="text-align: right"> ₹ ${data.new_regime_annual_taxable_income}</div></td>
                                            </tr>



                                            <tr>
                                                <!-- First column with nested table -->
                                                <td>
                                                    <b>Old Regime Tax Slab</b>
                                                            <table style="width: 100%; border-collapse: collapse; margin-top: 5px;" border="1">
                                                                <thead style="background-color: #f0f0f0;">
                                                                    <tr>
                                                                        <th style="padding: 6px;">From Amount</th>
                                                                        <th style="padding: 6px; text-align: right;">To Amount</th>
                                                                        <th style="padding: 6px; text-align: right;">Percentage</th>
                                                                        <th style="padding: 6px; text-align: right;">Amount</th>
                                                                    </tr>
                                                                </thead>
                                                                <tbody>
                                                                    ${oldSlabRows}
                                                                </tbody>
                                                            </table>

                                                            <br>

                                                            <b>New Regime Tax Slab</b>
                                                            <table style="width: 100%; border-collapse: collapse; margin-top: 5px;" border="1">
                                                                <thead style="background-color: #f0f0f0;">
                                                                    <tr>
                                                                        <th style="padding: 6px;">From Amount</th>
                                                                        <th style="padding: 6px; text-align: right;">To Amount</th>
                                                                        <th style="padding: 6px; text-align: right;">Percentage</th>
                                                                        <th style="padding: 6px; text-align: right;">Amount</th>
                                                                    </tr>
                                                                </thead>
                                                                <tbody>
                                                                    ${newSlabRows}
                                                                </tbody>
                                                            </table>

                                                </td>

                                                <!-- Second column: Old Regime Total -->
                                                <td><div style="text-align: right;">₹ ${data.old_regime_total_tax}</div></td>

                                                <!-- Third column: New Regime Total -->
                                                <td><div style="text-align: right;">₹ ${data.new_regime_total_tax}</div></td>
                                            </tr>



                                             <tr>
                                                <td>
                                                    <b>Rebate</b>
                                                            <table style="width: 100%; border-collapse: collapse; margin-top: 5px;" border="1">
                                                                <thead style="background-color: #f0f0f0;">
                                                                    <tr>
                                                                        <th style="padding: 6px;">Regime</th>
                                                                        <th style="padding: 6px; text-align: right;">Annual Taxable Lessthan</th>
                                                                        <th style="padding: 6px; text-align: right;">Max Amount</th>
                                                                        <th style="padding: 6px; text-align: right;">Marginal Relief</th>
                                                                    </tr>
                                                                </thead>
                                                                <tbody>


                                                                    <tr>
                                                                        <th style="padding: 6px;">Old Regime</th>
                                                                        <th style="padding: 6px; text-align: right;">${data.old_regime_rebate_limit}</th>
                                                                        <th style="padding: 6px; text-align: right;">${data.old_regime_max_amount}</th>
                                                                        <th style="padding: 6px; text-align: right;">${data.old_regime_marginal_relief_min}-${data.old_regime_marginal_relief_max}</th>
                                                                    </tr>

                                                                     <tr>
                                                                        <th style="padding: 6px;">New Regime</th>
                                                                        <th style="padding: 6px; text-align: right;">${data.new_regime_rebate_limit}</th>
                                                                        <th style="padding: 6px; text-align: right;">${data.new_regime_max_amount}</th>
                                                                        <th style="padding: 6px; text-align: right;">${data.new_regime_marginal_relief_min}-${data.new_regime_marginal_relief_max}</th>
                                                                    </tr>

                                                                </tbody>
                                                            </table>


                                                </td>

                                                <td><div style="text-align: right;">₹ ${data.old_regime_rebate_amount}</div></td>

                                                <td><div style="text-align: right;">₹ ${data.new_regime_rebate_amount}</div></td>
                                            </tr>


                                            <tr>
                                                <td style="padding: 10px; border: 1px solid #ddd;">Total Tax on Income</td>
                                                 <td><div style="text-align: right"> ₹ ${data.old_regime_total_tax-data.old_regime_rebate_amount}</div></td>
                                                <td><div style="text-align: right"> ₹ ${data.new_regime_total_tax-data.new_regime_rebate_amount}</div></td>
                                            </tr>

                                            <tr>
                                                <td style="padding: 10px; border: 1px solid #ddd;">Surcharge</td>
                                                 <td><div style="text-align: right"> ₹ ${data.old_regime_surcharge}</div></td>
                                                <td><div style="text-align: right"> ₹ ${data.new_regime_surcharge}</div></td>
                                            </tr>

                                            <tr>
                                                <td style="padding: 10px; border: 1px solid #ddd;">Education Cess</td>
                                                 <td><div style="text-align: right"> ₹ ${data.old_regime_education_cess}</div></td>
                                                <td><div style="text-align: right"> ₹ ${data.new_regime_education_cess}</div></td>
                                            </tr>

                                            <tr style="font-weight: bold; background-color: #e9ecef;">
                                                <td style="padding: 10px; border: 1px solid #ddd;">Tax Payable</td>
                                                 <td><div style="text-align: right"> ₹ ${data.old_regime_education_cess+data.old_regime_surcharge+(data.old_regime_total_tax-data.old_regime_rebate_amount)}</div></td>
                                                <td><div style="text-align: right"> ₹ ${data.new_regime_education_cess+data.new_regime_surcharge+(data.new_regime_total_tax-data.new_regime_rebate_amount)}</div></td>
                                            </tr>

                                            <tr style="font-weight: bold; background-color: #e9ecef;">
                                                <td style="padding: 10px; border: 1px solid #ddd;">Advance Tax Deducted Amount</td>
                                                 <td><div style="text-align: right"> ₹ ${data.advance_tax}</div></td>
                                                <td><div style="text-align: right"> ₹ ${data.advance_tax}</div></td>
                                            </tr>

                                            <tr style="font-weight: bold; background-color: #e9ecef;">
                                                <td style="padding: 10px; border: 1px solid #ddd;">Balance Tax Payable</td>
                                                 <td><div style="text-align: right"> ₹ ${(data.old_regime_education_cess+data.old_regime_surcharge+(data.old_regime_total_tax-data.old_regime_rebate_amount))-(data.advance_tax)}</div></td>
                                                <td><div style="text-align: right"> ₹ ${(data.new_regime_education_cess+data.new_regime_surcharge+(data.new_regime_total_tax-data.new_regime_rebate_amount))-(data.advance_tax)}</div></td>
                                            </tr>

                                            <tr style="font-weight: bold; background-color: #e9ecef;">
                                                <td style="padding: 10px; border: 1px solid #ddd;">Tax Paid</td>
                                                 <td><div style="text-align: right"> ₹ ${data.total_tax_already_paid}</div></td>
                                                <td><div style="text-align: right"> ₹ ${data.total_tax_already_paid}</div></td>
                                            </tr>



                                            <tr style="font-weight: bold; background-color: #e9ecef;">
                                                <td style="padding: 10px; border: 1px solid #ddd;">Current Tax</td>
                                                <td><div style="text-align: right"> ₹ ${Math.round(currentTax_old_regime_tax)}</div></td>
                                                <td><div style="text-align: right"> ₹ ${Math.round(currentTax_new_regime_tax)}</div></td>
                                            </tr>










                                        </tbody>
                                    </table>
                                `;

                            frm.set_df_property("custom_employee_tax_projection", "options", html);
                            frm.refresh_field("custom_employee_tax_projection");




                        }
                    }
                });
            }
        },

    monthly_house_rent(frm) {

    if(frm.doc.monthly_house_rent>0)
        {
            frm.set_value("custom_check",0)

        }

    }



});


function tds_projection_html(frm) {
    if (frm.doc.docstatus == 1) {

        let section10_component = []; // Ensure it's an array
        let section10_amount = []; // Ensure it's an array

        let section80c_component=[]
        let section80c_amount=[]

        let section80d_component=[]
        let section80d_amount=[]
        let section80d_amount_total=[]


        let section80d_other=[]
        let section80d_other_amount=[]

        let other_component=[]
        let other_amount=[]


        let total_array = [];
        let total_value = [];
        let from_amount = [];
        let to_amount = [];
        let percentage = [];
        let difference = [];




        let total_sum_old=0

        frappe.call({
            method: "cn_indian_payroll.cn_indian_payroll.overrides.tds_projection_calculation.get_doc_data",
            args: {
                doc_name: frm.doc.name,
                employee: frm.doc.employee,
                company: frm.doc.company,
                payroll_period: frm.doc.payroll_period
            },
            callback: function (res) {
                if (res.message) {
                    const from_month = res.message.from_month;
                    const to_month = res.message.to_month;
                    const oldValue = Math.round(res.message.current_old_value);
                    const newValue = Math.round(res.message.current_new_value);
                    const old_future_amount = Math.round(res.message.future_old_value);
                    const new_future_amount = Math.round(res.message.future_new_value);

                    const num_months=res.message.num_months
                    const salary_slip_count=res.message.salary_slip_count



                    const old_std=res.message.old_standard
                    const new_std=res.message.new_standard

                    const pt_value=Math.round(res.message.pt)
                    const nps_value=Math.round(res.message.nps)
                    const epf_value=Math.round(res.message.epf)


                    const per_comp = res.message.perquisite_component || [];
                    const per_values = res.message.perquisite_amount || [];

                    const accrued_data=res.message.accrued_data_list||[]



                    const total_per_sum = per_values.reduce((total, value) => total + value, 0);

                    const maxLength = Math.max(per_comp.length, per_values.length);

                    // console.log(accrued_data,"8888888888888888888")
                    const accruedData = accrued_data; // just assign it, no Math.max


                    section80c_component.push("Investments In PF(Auto)")
                    section80c_amount.push(epf_value)

                    let perquisiteRows = "";
                    for (let i = 0; i < maxLength; i++) {
                        let component = per_comp[i] || "-";
                        let oldPer = per_values[i] || "-";
                        let newPer = per_values[i] || "-";
                        perquisiteRows += `<tr><td>${component}</td><td>${"₹" + oldPer}</td><td>${"₹" + newPer}</td></tr>`;
                    }

                    console.log(perquisiteRows,"-----")

                    let accrued_components = "";
                    let total_accrued = 0;
                    let total_future = 0;

                      for (let i = 0; i < accruedData.length; i++) {
                          let component = accruedData[i].component || "-";
                          let accrued = accruedData[i].amount || 0;
                          let future = accruedData[i].future_amount || 0;

                          let row_sum = accrued + future;

                          total_accrued += accrued;
                          total_future += future;

                          accrued_components += `<tr>
                              <td>${component}</td>
                              <td>₹${parseFloat(accrued).toFixed(2)}</td>
                              <td>₹${parseFloat(future).toFixed(2)}</td>
                          </tr>`;
                      }

                      // console.log(accrued_components, "-----");
                      // console.log(`Total Combined Amount: ₹${total_accrued + total_future}`);


                    // console.log(frm.doc.custom_declaration_form_data,"------------------")
                    if (frm.doc.custom_declaration_form_data) {
                      // Parse the JSON field if it's a string
                      let jsonData = typeof frm.doc.custom_declaration_form_data === 'string'
                          ? JSON.parse(frm.doc.custom_declaration_form_data)
                          : frm.doc.custom_declaration_form_data;



                      if (jsonData.amount && jsonData.amount > 0) {
                          section80d_component.push("Mediclaim Self, Spouse & Children (Below 60 years)");
                          section80d_amount.push(jsonData.amount);
                      }

                      if (jsonData.amount3 && jsonData.amount3 > 0) {
                          section80d_component.push("Mediclaim Self (Senior Citizen - 60 years & above)");
                          section80d_amount.push(jsonData.amount3);
                      }

                      if (jsonData.mpAmount3 && jsonData.mpAmount3 > 0) {
                          section80d_component.push("Parents (Below 60 years)");
                          section80d_amount.push(jsonData.mpAmount3);
                      }

                      if (jsonData.mpAmount4 && jsonData.mpAmount4 > 0) {
                          section80d_component.push("Parents (Senior Citizen - 60 years & above)");
                          section80d_amount.push(jsonData.mpAmount4);
                      }

                      if (jsonData.mp5 && jsonData.mp5 > 0) {
                          section80d_component.push("Preventive Checkup (Self + Family)");
                          section80d_amount.push(jsonData.mp5);
                      }

                      if (jsonData.mpAmount6 && jsonData.mpAmount6 > 0) {
                          section80d_component.push("Preventive Checkup (Parents)");
                          section80d_amount.push(jsonData.mpAmount6);
                      }

                      if (jsonData.amount_80d_eligible_amount && jsonData.amount_80d_eligible_amount > 0) {
                        section80d_component.push("Total Eligible Amount");
                        section80d_amount_total.push(jsonData.amount_80d_eligible_amount);
                        section80d_amount.push(jsonData.amount_80d_eligible_amount);
                    }


                  } else {
                      console.log("custom_declaration_form_data is empty or undefined");
                  }









                    // Check if declarations exist
                    if (frm.doc.declarations) {
                        $.each(frm.doc.declarations, function (i, v) {
                            if (v.exemption_category == "Section 10(14)") {
                                section10_component.push(v.exemption_sub_category);
                                section10_amount.push(v.amount);
                            }

                            if(v.exemption_category == "Section 80C" && v.exemption_sub_category!="Investments In PF(Auto)")
                            {
                              section80c_component.push(v.exemption_sub_category)
                              section80c_amount.push(v.amount)





                            }



                              if(v.exemption_category == "Section 80DD" || v.exemption_category == "Section 80E" || v.exemption_category == "Section 80EE"||v.exemption_category == "Section 80U")
                                {


                                  section80d_other.push(v.exemption_sub_category)

                                  section80d_other_amount.push(v.amount)



                                }





                                const validCategories = [

                                  "Section 80DDB",
                                  "Section 80G",
                                  "Section 80CCD(1B)",
                                  "Section 80EEA",
                                  "Section 80EEB",
                                  "Section 80GGC",
                                  "Section 80TTA",
                                  "Section 80TTB",
                                  "Section 80GG",
                                  "Section 80CCG",
                                  "Section 24(b)",



                              ];

                              if (validCategories.includes(v.exemption_category)) {
                                other_component.push(v.exemption_sub_category)
                                other_amount.push(v.amount)


                              }
                        });
                    }


                    const total_section10_sum = section10_amount.reduce((total, value) => total + value, 0);
                    const total_section80C_sum = Math.min(section80c_amount.reduce((total, value) => total + value, 0), 150000);
                    // const total_section80d_sum = section80d_amount_total.reduce ((total, value) => total + value, 0);
                    const total_section80d_sum = [...section80d_amount_total, ...section80d_other_amount].reduce(
                      (total, value) => total + value,
                      0
                    );

                    const total_other_sum = other_amount.reduce((total, value) => total + value, 0);

                    // console.log(total_section80d_sum,"total_section80d_sumtotal_section80d_sum")


                    const section10_maxLength = Math.max(section10_component.length, section10_amount.length);
                    const section80_maxLength = Math.max(section80c_component.length, section80c_amount.length);
                    const section80D_maxLength = Math.max(section80d_component.length, section80d_amount_total.length);
                    const section80DOther_maxLength = Math.max(section80d_other.length, section80d_other_amount.length);
                    const other_maxLength = Math.max(other_component.length, other_amount.length);


                    const annual_hra_exemption=Math.max(frm.doc.annual_hra_exemption)




                    // Create rows for section 10 details
                    let Section10Rows = "";
                    for (let i = 0; i < section10_maxLength; i++) {
                        let Section10component = section10_component[i] || "-";  // If index out of bounds, insert "-"
                        let oldSection10 = section10_amount[i] || "0";
                        let newSection10 = 0;  // Assuming new value is 0 for now
                        Section10Rows += `<tr><td>${Section10component}</td><td>${"₹" + oldSection10}</td><td>${"₹" + newSection10}</td></tr>`;
                    }


                    let Section80Rows = "";
                    for (let i = 0; i < section80_maxLength; i++) {
                        let Section80component = section80c_component[i] || "-";  // If index out of bounds, insert "-"
                        let oldSection80c = section80c_amount[i] || "0";
                        let newSection80c = 0;  // Assuming new value is 0 for now
                        Section80Rows += `<tr><td>${Section80component}</td><td>${"₹" + oldSection80c}</td><td>${"₹" + newSection80c}</td></tr>`;
                    }

                    let Section80DRows = "";
                    for (let i = 0; i < section80D_maxLength; i++) {
                        let Section80Dcomponent = section80d_component[i] || "-";  // If index out of bounds, insert "-"
                        let oldSection80D = section80d_amount[i] || "0";
                        let newSection80D = 0;  // Assuming new value is 0 for now
                        Section80DRows += `<tr><td>${Section80Dcomponent}</td><td>${"₹" + oldSection80D}</td><td>${"₹" + newSection80D}</td></tr>`;
                    }


                    let Section80DOtherRows = "";
                    for (let i = 0; i < section80DOther_maxLength; i++) {
                        let Section80DOthercomponent = section80d_other[i] || "-";  // If index out of bounds, insert "-"
                        let oldSection80DOther = section80d_other_amount[i] || "0";
                        let newSection80D_other = 0;  // Assuming new value is 0 for now
                        Section80DOtherRows += `<tr><td>${Section80DOthercomponent}</td><td>${"₹" + oldSection80DOther}</td><td>${"₹" + newSection80D_other}</td></tr>`;
                    }

                    let OtherRows = "";
                    for (let i = 0; i < other_maxLength; i++) {
                        let Othercomponent = other_component[i] || "-";  // If index out of bounds, insert "-"
                        let oldSectionOther = other_amount[i] || "0";
                        let newSectionOther = 0;  // Assuming new value is 0 for now
                        OtherRows += `<tr><td>${Othercomponent}</td><td>${"₹" + oldSectionOther}</td><td>${"₹" + newSectionOther}</td></tr>`;
                    }






                    let annual_old_taxable_income=(oldValue+old_future_amount+total_per_sum)-(total_section10_sum+old_std+pt_value+total_section80C_sum+total_section80d_sum+total_other_sum+nps_value+annual_hra_exemption)
                    let annual_new_taxable_income=(newValue+new_future_amount+total_per_sum)-(nps_value+new_std)

                    let tds_already_deducted=frm.doc.custom_tds_already_deducted_amount

                    // console.log(tds_already_deducted,"*****************************************")

                    // console.log(annual_old_taxable_income,"1111111")
                    // console.log(annual_new_taxable_income,"22222222")



                    function getPerComp1() {
                      return new Promise((resolve, reject) => {
                          frappe.call({
                              method: "cn_indian_payroll.cn_indian_payroll.overrides.tds_projection_calculation.slab_calculation",
                              args: {
                                  employee: frm.doc.employee,
                                  company: frm.doc.company,
                                  payroll_period: frm.doc.payroll_period,
                                  old_annual_slab: annual_old_taxable_income,
                                  new_annual_slab: annual_new_taxable_income
                              },
                              callback: function (response) {
                                  if (response.message) {
                                      let old_from_amount = response.message.from_amount || [];
                                      let old_to_amount = response.message.to_amount || [];
                                      let old_percentage_amount = response.message.percentage || [];
                                      let old_value_amount = response.message.total_value || [];
                                      let total_sum=response.message.total_sum
                                      let rebate=response.message.rebate
                                      let max_amount=response.message.max_amount
                                      let old_rebate_value=response.message.old_rebate_value


                                      let  old_surcharge_m=response.message.old_surcharge_m
                                      let old_education_cess=response.message.old_education_cess
                                      let new_from_amount = response.message.from_amount_new || [];
                                      let new_to_amount = response.message.to_amount_new || [];
                                      let new_percentage_amount = response.message.percentage_new || [];
                                      let new_value_amount = response.message.total_value_new || [];
                                      let total_sum_new=response.message.total_sum_new
                                      let newrebate=response.message.rebate_new
                                      let newmax_amount=response.message.max_amount_new
                                      let new_rebate_value=response.message.new_rebate_value
                                      let new_surcharge_m=response.message.new_surcharge_m
                                      let new_education_cess=response.message.new_education_cess


                                      let new_regime_marginal_relief_min_value=response.message.new_regime_marginal_relief_min_value
                                      let new_regime_marginal_relief_max_value=response.message.new_regime_marginal_relief_max_value
                                      let old_regime_marginal_relief_min_value=response.message.old_regime_marginal_relief_min_value
                                      let old_regime_marginal_relief_max_value=response.message.old_regime_marginal_relief_max_value





                                      let salary_slip_sum=Math.round(response.message.salary_slip_sum)






                                      resolve({
                                        old_from_amount,
                                         old_to_amount,
                                         old_percentage_amount,
                                         old_value_amount,
                                         new_from_amount ,
                                         new_to_amount,
                                         new_percentage_amount,
                                         new_value_amount,
                                         total_sum,
                                         total_sum_new,
                                         rebate,
                                         max_amount,
                                         newrebate,
                                         newmax_amount,
                                         old_rebate_value,
                                         new_rebate_value,
                                         old_surcharge_m,
                                          old_education_cess,
                                          new_surcharge_m,
                                          new_education_cess,
                                          salary_slip_sum,
                                          num_months,
                                          salary_slip_count,
                                          from_month,
                                          to_month,
                                          new_regime_marginal_relief_min_value,
                                          new_regime_marginal_relief_max_value,
                                          old_regime_marginal_relief_min_value,
                                          old_regime_marginal_relief_max_value,



                                        });
                                  } else {
                                      console.error("Error: No response received from Python method.");
                                      reject("No response received");
                                  }
                              }
                          });
                      });
                  }

                  async function processPerComp1() {
                    try {
                        let { old_from_amount, old_to_amount, old_percentage_amount, old_value_amount,new_from_amount ,
                          new_to_amount,
                          new_percentage_amount,
                          new_value_amount,total_sum,total_sum_new,
                          rebate,
                          max_amount,
                          newrebate,
                          newmax_amount,
                          old_rebate_value,
                          new_rebate_value,
                          old_surcharge_m,
                          old_education_cess,
                          new_surcharge_m,
                          new_education_cess,
                          salary_slip_sum,
                          num_months,
                          salary_slip_count,
                          from_month,
                          to_month,
                          new_regime_marginal_relief_min_value,
                          new_regime_marginal_relief_max_value,
                          old_regime_marginal_relief_min_value,
                          old_regime_marginal_relief_max_value,

                        } = await getPerComp1();

                        let OtherRows1 = "";
                        for (let i = 0; i < old_from_amount.length; i++) {
                            let fromcomponent = old_from_amount[i]|| 0;
                            let tocomponent = old_to_amount[i] || 0;
                            let percentage =old_percentage_amount[i] || 0;
                            let final_amount = old_value_amount[i] || 0;



                            OtherRows1 += `<tr><td>${fromcomponent}</td><td>${"₹" + tocomponent}</td><td>${"₹" + percentage}</td><td>${"₹" + final_amount}</td></tr>`;
                            // console.log(OtherRows1,"OtherRows1OtherRows1")

                          }

                        let OtherRows2 = "";
                        for (let i = 0; i < new_from_amount.length; i++) {
                            let newfromcomponent = new_from_amount[i]|| 0;
                            let newtocomponent = new_to_amount[i] || 0;
                            let newpercentage =new_percentage_amount[i] || 0;
                            let newfinal_amount = new_value_amount[i] || 0;



                            OtherRows2 += `<tr><td>${newfromcomponent}</td><td>${"₹" + newtocomponent}</td><td>${"₹" + newpercentage}</td><td>${"₹" + newfinal_amount}</td></tr>`;
                        }

                    const periodText = (from_month !== to_month)
                        ? `${from_month} - ${to_month}`
                        : from_month;
                    const table_html = `
                    <table class="table table-bordered">
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>Old Regime</th>
                                <th>New Regime</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Current Taxable Earnings(${periodText})</td>
                                <td>₹ ${oldValue}</td>
                                <td>₹ ${newValue}</td>
                            </tr>
                            <tr>
                                <td>Future Taxable Earnings</td>
                                <td>₹ ${old_future_amount}</td>
                                <td>₹ ${new_future_amount}</td>
                            </tr>
                            <tr>
                                <td>
                                    Total Perquisite
                                    <button class="btn btn-secondary btn-sm incomeTaxDropdown" style="margin-left: 10px;">
                                        <i class="fa fa-caret-down"></i>
                                    </button>
                                    <div class="incomeTaxDetails" style="display: none; margin-top: 10px;">
                                        <table class="table table-sm table-bordered">
                                            <thead>
                                                <tr>
                                                    <th>Perquisite Component</th>
                                                    <th>Old Regime</th>
                                                    <th>New Regime</th>
                                                </tr>
                                            </thead>
                                            <tbody>${perquisiteRows}</tbody>
                                        </table>
                                    </div>
                                </td>
                                <td>₹ ${total_per_sum}</td>
                                <td>₹ ${total_per_sum}</td>
                            </tr>



                            <tr>
                                <td>
                                    Accrued Components
                                    <button class="btn btn-secondary btn-sm incomeTaxDropdown" style="margin-left: 10px;">
                                        <i class="fa fa-caret-down"></i>
                                    </button>
                                    <div class="incomeTaxDetails" style="display: none; margin-top: 10px;">
                                        <table class="table table-sm table-bordered">
                                            <thead>
                                                <tr>
                                                    <th>Accrued Component </th>
                                                    <th>Accrued Amount</th>
                                                    <th>Future Amount</th>
                                                </tr>
                                            </thead>
                                            <tbody>${accrued_components}</tbody>
                                        </table>
                                    </div>
                                </td>
                                <td>₹0</td>
                                <td>₹0</td>
                            </tr>








                             <tr>
                                <td>Total Taxable Income</td>
                                <td>₹ ${oldValue+old_future_amount+total_per_sum}</td>
                                <td>₹ ${newValue+new_future_amount+total_per_sum}</td>
                            </tr>





                            <tr>
                                <td>
                                    Less : Allowances Exempted U/s 10
                                    <button class="btn btn-secondary btn-sm incomeTaxDropdown" style="margin-left: 10px;">
                                        <i class="fa fa-caret-down"></i>
                                    </button>
                                    <div class="incomeTaxDetails" style="display: none; margin-top: 10px;">
                                        <table class="table table-sm table-bordered">
                                            <thead>
                                                <tr>
                                                    <th>Title</th>
                                                    <th>Old Regime</th>
                                                    <th>New Regime</th>
                                                </tr>
                                            </thead>
                                            <tbody>${Section10Rows}</tbody>
                                        </table>
                                    </div>
                                </td>
                                <td>₹ ${total_section10_sum}</td>
                                <td>₹ 0</td>
                            </tr>

                            <tr>
                                  <td>Less: Allowances Exempted U/s 16
                                      <button class="btn btn-secondary btn-sm incomeTaxDropdown">
                                          <i class="fa fa-caret-down"></i>
                                      </button>
                                      <div class="incomeTaxDetails" style="display: none;">
                                          <table class="table table-sm table-bordered">
                                              <thead>
                                                  <tr>
                                                      <th>Option</th>
                                                      <th>Old Regime</th>
                                                      <th>New Regime</th>
                                                  </tr>
                                              </thead>
                                              <tbody>
                                                  <tr>
                                                      <td>Standard Deduction</td>
                                                      <td>₹ ${old_std}</td>
                                                      <td>₹ ${new_std}</td>
                                                  </tr>
                                                  <tr>
                                                      <td>Tax on Employment</td>
                                                      <td>₹ ${pt_value}</td>
                                                      <td>₹ 0</td>
                                                  </tr>


                                              </tbody>
                                          </table>
                                      </div>
                                  </td>
                                  <td>₹ ${old_std+pt_value}</td>
                                  <td>₹ ${new_std}</td>
                              </tr>


                              <tr>
                                <td>
                                    Less: Deduction under Sec 80C (Max Rs.1,50,000/-)
                                    <button class="btn btn-secondary btn-sm incomeTaxDropdown" style="margin-left: 10px;">
                                        <i class="fa fa-caret-down"></i>
                                    </button>
                                    <div class="incomeTaxDetails" style="display: none; margin-top: 10px;">
                                        <table class="table table-sm table-bordered">
                                            <thead>
                                                <tr>
                                                    <th>Title</th>
                                                    <th>Old Regime</th>
                                                    <th>New Regime</th>
                                                </tr>
                                            </thead>
                                            <tbody>${Section80Rows}</tbody>
                                        </table>
                                    </div>
                                </td>
                                <td>₹ ${total_section80C_sum}</td>
                                <td>₹ 0</td>
                            </tr>

                            <tr>
                                <td>
                                    Less: Deductions Under Chapter VI- A(80D,80DD,80E,80EE,80U)
                                    <button class="btn btn-secondary btn-sm incomeTaxDropdown" style="margin-left: 10px;">
                                        <i class="fa fa-caret-down"></i>
                                    </button>
                                    <div class="incomeTaxDetails" style="display: none; margin-top: 10px;">
                                        <table class="table table-sm table-bordered">
                                            <thead>
                                                <tr>
                                                    <th>Title</th>
                                                    <th>Old Regime</th>
                                                    <th>New Regime</th>
                                                </tr>
                                            </thead>
                                            <tbody>${Section80DRows}</tbody>
                                            <tr>
                                            <td colspan="3" style="height: 10px; background-color: #f9f9f9;"></td>
                                          </tr>

                                          <tbody>
                                            ${Section80DOtherRows}
                                          </tbody>
                                        </table>
                                    </div>


                                </td>
                                <td>₹ ${total_section80d_sum}</td>
                                <td>₹ 0</td>
                            </tr>

                            <tr>
                                <td>NPS</td>
                                <td>₹ ${nps_value}</td>
                                <td>₹ ${nps_value}</td>
                            </tr>


                            <tr>
                                <td>
                                   Other
                                    <button class="btn btn-secondary btn-sm incomeTaxDropdown" style="margin-left: 10px;">
                                        <i class="fa fa-caret-down"></i>
                                    </button>
                                    <div class="incomeTaxDetails" style="display: none; margin-top: 10px;">
                                        <table class="table table-sm table-bordered">
                                            <thead>
                                                <tr>
                                                    <th>Title</th>
                                                    <th>Old Regime</th>
                                                    <th>New Regime</th>
                                                </tr>
                                            </thead>
                                            <tbody>${OtherRows}</tbody>
                                        </table>
                                    </div>
                                </td>
                                <td>₹ ${total_other_sum}</td>
                                <td>₹ 0</td>
                            </tr>

                            <tr>
                                <td>HRA Exemption</td>
                                <td>₹ ${annual_hra_exemption}</td>
                                <td>₹ 0</td>
                            </tr>






                            <tr>
                                <td>Total Exemption/Deductions</td>
                                <td>₹ ${total_section10_sum+old_std+pt_value+total_section80C_sum+total_section80d_sum+total_other_sum+nps_value+annual_hra_exemption}</td>
                                <td>₹ ${nps_value+new_std}</td>
                            </tr>
                            <tr>
                                <td>Annual Taxable Income</td>
                                <td>₹ ${(oldValue+old_future_amount+total_per_sum)-(total_section10_sum+old_std+pt_value+total_section80C_sum+total_section80d_sum+total_other_sum+nps_value+annual_hra_exemption)}</td>
                                <td>₹ ${(newValue+new_future_amount+total_per_sum)-(nps_value+new_std)}</td>
                            </tr>



                            <tr>
                                <td>
                                    Tax Slab
                                    <button class="btn btn-secondary btn-sm incomeTaxDropdown" style="margin-left: 10px;">
                                        <i class="fa fa-caret-down"></i>
                                    </button>
                                    <div class="incomeTaxDetails" style="display: none; margin-top: 10px;">
                                        <table class="table table-sm table-bordered">
                                            <thead>
                                                <tr>
                                                    <th>From Amount</th>
                                                    <th>To Amount</th>
                                                    <th>Percentage</th>
                                                    <th>Amount</th>
                                                </tr>
                                            </thead>
                                            Old Regime Slab
                                            <tbody>${OtherRows1}</tbody>
                                        </table>

                                        <table class="table table-sm table-bordered">
                                            <thead>
                                                <tr>
                                                    <th>From Amount</th>
                                                    <th>To Amount</th>
                                                    <th>Percentage</th>
                                                    <th>Amount</th>
                                                </tr>
                                            </thead>
                                            New Regime Slab
                                            <tbody>${OtherRows2}</tbody>
                                        </table>


                                    </div>
                                </td>
                                <td>₹ ${total_sum}</td>
                                <td>₹ ${total_sum_new}</td>
                            </tr>




                            <tr>
                                <td>
                                   Rebate
                                    <button class="btn btn-secondary btn-sm incomeTaxDropdown" style="margin-left: 10px;">
                                        <i class="fa fa-caret-down"></i>
                                    </button>
                                    <div class="incomeTaxDetails" style="display: none; margin-top: 10px;">
                                        <table class="table table-sm table-bordered">
                                            <thead>
                                                <tr>
                                                    <th>Regime</th>
                                                    <th>Annual Taxable Lessthan</th>
                                                    <th>Max Amount</th>
                                                    <th>Marginal Relief</th>


                                                </tr>
                                            </thead>
                                            <tbody>

                                            <tr>
                                                    <th>Old Regime</th>
                                                    <th>₹ ${rebate}</th>
                                                    <th>₹ ${max_amount}</th>

                                                    <th>${old_regime_marginal_relief_min_value}-${old_regime_marginal_relief_max_value}</th>



                                            </tr>
                                            <tr>
                                                    <th>New Regime</th>
                                                    <th>₹ ${newrebate}</th>
                                                    <th>₹ ${newmax_amount}</th>
                                                    <th>${new_regime_marginal_relief_min_value}-${new_regime_marginal_relief_max_value}</th>


                                            </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                </td>
                                <td>₹ ${Math.round(old_rebate_value)}
                                         </td>
                                <td>₹ ${Math.round(new_rebate_value)}</td>
                            </tr>


                            <tr>
                                <td>Total Tax on Income</td>
                                <td>₹ ${Math.round(total_sum-old_rebate_value)}</td>
                                <td>₹ ${Math.round(total_sum_new-new_rebate_value)}</td>
                            </tr>

                            <tr>
                                <td>Surcharge</td>
                                <td>₹ ${Math.round(old_surcharge_m)}</td>
                                <td>₹ ${Math.round(new_surcharge_m)}</td>



                            </tr>

                            <tr>
                                <td>Education Cess</td>
                                <td>₹ ${Math.round(old_education_cess)}</td>
                                <td>₹ ${Math.round(new_education_cess)}</td>
                            </tr>




                            <tr>
                                <td>Tax Payable</td>
                                <td>₹ ${Math.round(old_education_cess+old_surcharge_m+(total_sum-old_rebate_value))}</td>
                                <td>₹ ${Math.round(new_education_cess+new_surcharge_m+(total_sum_new-new_rebate_value))}</td>
                            </tr>

                            <tr>
                                <td>TDS already deducted</td>
                                <td>₹ ${Math.round(tds_already_deducted)}</td>
                                <td>₹ ${Math.round(tds_already_deducted)}</td>

                            </tr>

                            <tr>
                                <td>Balance TDS payable</td>
                                <td>₹ ${Math.round((old_education_cess+old_surcharge_m+(total_sum-old_rebate_value))-tds_already_deducted)}</td>
                                <td>₹ ${Math.round((new_education_cess+new_surcharge_m+(total_sum_new-new_rebate_value))-tds_already_deducted)}</td>
                            </tr>






                            <tr>
                                <td>Tax Paid</td>
                                <td>₹ ${Math.round(salary_slip_sum)}</td>
                                <td>₹ ${Math.round(salary_slip_sum)}</td>
                            </tr>

                            <tr>
                            <td>Current Tax</td>
                            <td>
                              ₹ ${Math.round(
                                (old_education_cess + old_surcharge_m + (total_sum - old_rebate_value) - tds_already_deducted - salary_slip_sum) /
                                ((num_months - salary_slip_count)+1)
                              )}
                            </td>
                            <td>
                              ₹ ${Math.round(
                                (new_education_cess + new_surcharge_m + (total_sum_new - new_rebate_value) - tds_already_deducted - salary_slip_sum) /
                                ((num_months - salary_slip_count)+1)
                              )}
                            </td>
                          </tr>








                        </tbody>
                    </table>
                `;

                        // Set the value of the HTML field
                        frm.set_df_property('custom_employee_tax_projection', 'options', table_html);

                        // Add event listeners for dropdown buttons
                        setTimeout(() => {
                            document.querySelectorAll('.incomeTaxDropdown').forEach((button, index) => {
                                button.addEventListener('click', function () {
                                    const detailsDiv = document.querySelectorAll('.incomeTaxDetails')[index];
                                    detailsDiv.style.display = (detailsDiv.style.display === 'none') ? 'block' : 'none';
                                });
                            });
                        }, 100);

                    } catch (error) {
                        console.error("Error fetching per_comp1:", error);
                    }
                }

                // Call the function to fetch and process the data
                processPerComp1();
                }
            }
        });

    }
  }
