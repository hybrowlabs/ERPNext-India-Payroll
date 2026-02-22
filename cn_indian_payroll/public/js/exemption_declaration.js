

frappe.ui.form.on('Employee Tax Exemption Declaration', {
    refresh(frm) {
        frm.trigger("change_tax_regime");
        frm.trigger("display_declaration_form");
        frm.trigger("tds_projection_html");
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
                limit_page_length: 9999
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

                        const stored_value = stored_row ? stored_row.value || stored_row.amount || '' : '';

                        let is_readonly = false;
                        if (frm.doc.custom_tax_regime === "New Regime") {
                            is_readonly = true;
                        } else if (frm.doc.custom_tax_regime === "Old Regime") {
                            is_readonly = ["NPS", "Provident Fund", "Professional Tax"].includes(row.custom_component_type);
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

                    const html = `
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
                                    <th>Total Exemption Eligible Amount</th>
                                    <td><b>${Math.round(frm.doc.total_exemption_amount || 0)}</b></td>
                                </tr>
                            </thead>
                        </table>

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

                                   

                                    if (value > 0) {
                                        formData.push({
                                            id: id,
                                            sub_category: id,
                                            exemption_category: exemption_category,
                                            max_amount: max,
                                            amount: value,
                                            value: value
                                        });

                                        const d = frm.add_child("declarations");
                                        d.exemption_sub_category = id;
                                        d.exemption_category = exemption_category;
                                        d.max_amount = max;
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

                        //     let oldSlabRows = "";
                        //         for (let i = 0; i < data.old_regime_from_amounts.length; i++) {
                        //             oldSlabRows += `
                        //                 <tr>
                        //                     <td style="padding: 6px;">₹ ${data.old_regime_from_amounts[i]}</td>
                        //                     <td style="padding: 6px; text-align: right;">₹ ${data.old_regime_to_amounts[i]}</td>
                        //                     <td style="padding: 6px; text-align: right;">${data.old_regime_percentages[i]}%</td>
                        //                     <td style="padding: 6px; text-align: right;">₹ ${data.old_regime_tax_per_slab[i]}</td>
                        //                 </tr>
                        //             `;
                        //         }

                        //         // Build HTML rows for New Regime Slab
                        //         let newSlabRows = "";
                        //         for (let i = 0; i < data.new_regime_from_amounts.length; i++) {
                        //             newSlabRows += `
                        //                 <tr>
                        //                     <td style="padding: 6px;">₹ ${data.new_regime_from_amounts[i]}</td>
                        //                     <td style="padding: 6px; text-align: right;">₹ ${data.new_regime_to_amounts[i]}</td>
                        //                     <td style="padding: 6px; text-align: right;">${data.new_regime_percentages[i]}%</td>
                        //                     <td style="padding: 6px; text-align: right;">₹ ${data.new_regime_tax_per_slab[i]}</td>
                        //                 </tr>
                        //             `;
                        //         }

                        //         let old_tax = (
                        //             (data.old_regime_education_cess + data.old_regime_surcharge +
                        //             (data.old_regime_total_tax - data.old_regime_rebate_amount)) -
                        //             data.total_tax_already_paid
                        //         );

                        //         let new_tax = (
                        //             (data.new_regime_education_cess+data.new_regime_surcharge+
                        //             (data.new_regime_total_tax-data.new_regime_rebate_amount)) -
                        //             data.total_tax_already_paid
                        //         );

                        //         let old_tax_balance = (
                        //             (
                        //                 data.old_regime_education_cess +
                        //                 data.old_regime_surcharge +
                        //                 (data.old_regime_total_tax - data.old_regime_rebate_amount)
                        //             ) - data.advance_tax
                        //         ) - data.total_tax_already_paid;


                        //         let new_tax_balance = (
                        //             (
                        //                 data.new_regime_education_cess +
                        //                 data.new_regime_surcharge +
                        //                 (data.new_regime_total_tax - data.new_regime_rebate_amount)
                        //             ) - data.advance_tax
                        //         ) - data.total_tax_already_paid;


                        //         let monthBase = data.month_count === 0 ? data.num_months : data.month_count+1;

                        //         let currentTax_old_regime = old_tax / monthBase;
                        //         let currentTax_new_regime = new_tax / monthBase;

                        //         let currentTax_old_regime_tax = (old_tax_balance / monthBase) || 0;
                        //         let currentTax_new_regime_tax = (new_tax_balance / monthBase) || 0;



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
                                                <td style="padding: 10px; border: 1px solid #ddd;">TDS From Previous Employer</td>
                                                <td><div style="text-align: right"> ₹ ${data.tds_from_previous_employer}</div></td>
                                                <td><div style="text-align: right"> ₹ ${data.tds_from_previous_employer}</div></td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 10px; border: 1px solid #ddd;">Taxable Earnings (Current)</td>
                                                <td><div style="text-align: right"> ₹ ${data.current_taxable_earnings_old_regime}</div></td>
                                                <td><div style="text-align: right"> ₹ ${data.current_taxable_earnings_new_regime}</div></td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 10px; border: 1px solid #ddd;">Taxable Earnings (Future)</td>
                                                <td><div style="text-align: right"> ₹${data.future_taxable_earnings_old_regime}</div></td>
                                                <td><div style="text-align: right"> ₹ ${data.future_taxable_earnings_new_regime}</div></td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 10px; border: 1px solid #ddd;">Loan Perquisite</td>
                                                <td><div style="text-align: right"> ₹ </div></td>
                                                <td><div style="text-align: right"> ₹ </div></td>
                                            </tr>
                                            <tr style="font-weight: bold; background-color: #e9ecef;">
                                                <td>Total Taxable Earnings (Current+Future+Loan)</td>
                                                <td><div style="text-align: right"> ₹ </div></td>
                                                <td><div style="text-align: right"> ₹ </div></td>
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
        }






});
