

frappe.pages['tds-return-filing'].on_page_load = function (wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'TDS Return Challan',
        single_column: true
    });

    const html = frappe.render_template("employee_salary_table", {});
    $(page.body).html(html);

    initialize_tds_return_challan_logic(page);
};

function initialize_tds_return_challan_logic(page) {
    // --- Create link fields ---
    const company_field = frappe.ui.form.make_control({
        df: {
            fieldtype: 'Link',
            options: 'Company',
            label: 'Company',
            fieldname: 'company',
            reqd: 1
        },
        parent: $('#company_container'),
        render_input: true
    });

    const fiscal_field = frappe.ui.form.make_control({
        df: {
            fieldtype: 'Link',
            options: 'Fiscal Year',
            label: 'Financial Year',
            fieldname: 'fiscal_year',
            reqd: 1
        },
        parent: $('#fiscal_year_container'),
        render_input: true
    });

    const payroll_period_field = frappe.ui.form.make_control({
        df: {
            fieldtype: 'Link',
            options: 'Payroll Period',
            label: 'Payroll Period',
            fieldname: 'payroll_period',
            reqd: 1
        },
        parent: $('#payroll_period_container'),
        render_input: true
    });

    const branch_field = frappe.ui.form.make_control({
        df: {
            fieldtype: 'Link',
            options: 'Branch',
            label: 'Branch',
            fieldname: 'branch'
        },
        parent: $('#branch_container'),
        render_input: true
    });

    const company_address_field = frappe.ui.form.make_control({
        df: {
            fieldtype: 'Link',
            options: 'Address',
            label: 'Address',
            fieldname: 'company_address'
        },
        parent: $('#company_address'),
        render_input: true
    });

    // --- Auto-fill company-related fields ---
    company_field.df.onchange = () => {
        const company = company_field.get_value();
        if (!company) return;

        frappe.db.get_doc('Company', company).then(doc => {
            if (!doc) return;
            $('#tan_number').val(doc.custom_company_tan || '');
            $('#pan_number').val(doc.custom_company_pan || '');

            $('#deductor_name').val(doc.name || '');

            $('#ddo_code').val(doc.custom_ddo_code || '');
            $('#ddo_registration_number').val(doc.custom_ddo_registration_number || '');
            $('#pao_code').val(doc.custom_poa_code || '');
            $('#pao_registration_number').val(doc.custom_poa_registration_number || '');
        }).catch(() => frappe.msgprint('Error fetching company details.'));
    };
    company_field.refresh_input();


// --- Auto-fill address details when an address is selected ---
company_address_field.df.onchange = () => {
    const address_name = company_address_field.get_value();
    if (!address_name) return;

    frappe.db.get_doc('Address', address_name)
        .then(doc => {
            if (!doc) {
                frappe.msgprint("Address not found.");
                return;
            }

            console.log("📦 Address Details:", doc);

            // Fill address details
            $('#flat_no_responsible').val(doc.address_line1 || '');
            $('#road_street_responsible').val(doc.address_line2 || '');
            $('#town_city_responsible').val(doc.city || '');
            $('#state_responsible').val(doc.state || '');
            $('#pin_code_responsible').val(doc.pincode || '');
            $('#email_responsible').val(doc.email_id || doc.email || '');
            $('#mobile_responsible').val(doc.phone || doc.phone_no || '');


            $('#flat_no').val(doc.address_line1 || '');
            $('#road_name').val(doc.address_line2 || '');
            $('#city_district').val(doc.city || '');
            $('#state_name').val(doc.state || '');
            $('#pin_code').val(doc.pincode || '');
            $('#email').val(doc.email_id || doc.email || '');
            $('#telephone_number').val(doc.phone || doc.phone_no || '');

            // Optional: Display confirmation
            frappe.show_alert({
                message: __("Address details loaded successfully."),
                indicator: "green"
            });
        })
        .catch(err => {
            console.error("❌ Error fetching address:", err);
            frappe.msgprint("Error fetching address details.");
        });
};

// Refresh control input
company_address_field.refresh_input();


    // --- Tab switching ---
    $(page.body).on('click', '.tab-btn', function () {
        $('.tab-btn').removeClass('active');
        $('.tab-content').removeClass('active');
        $(this).addClass('active');
        $('#' + $(this).data('tab')).addClass('active');
    });

    // --- Data logging (for Save buttons) ---
    // --- Data logging (for Save buttons) ---
    $(page.body).on('click', '.submit-btn', function () {
        const tabId = $(this).closest('.tab-content').attr('id');
        const inputs = $(this).closest('.tab-content').find('input, select');
        const data = {};
        inputs.each(function () {
            const id = $(this).attr('id') || 'unnamed_field';
            data[id] = $(this).val();
        });
        console.log(`--- ${tabId} data ---`, data);
        // Removed unnecessary msgprint
    });


    // ✅ Moved this section AFTER all fields are initialized
    $("#get-details-btn").on("click", function () {
        const company = company_field.get_value();
        const fiscal_year = fiscal_field.get_value();
        const payroll_period = payroll_period_field.get_value();
        const quarter_ended = $("#quarter_ended").val();

        if (!company || !fiscal_year) {
            frappe.msgprint("Please select both Company and Fiscal Year.");
            return;
        }


        frappe.call({
            method: "cn_indian_payroll.cn_indian_payroll.overrides.tds_file.month_wise_tds_value",
            args: {
                company: company,
                fiscal_year: fiscal_year,
                quarter_ended: quarter_ended,
                payroll_period: payroll_period
            },
            freeze: true,
            freeze_message: "Fetching TDS details, please wait...",
            callback: function (r) {
                if (r.message && !r.message.error) {
                    const data = r.message.data || [];
                    console.log("✅ TDS Data:", data);

                    // -----------------------------
                    // 1️⃣ Populate Challan Table
                    // -----------------------------
                    const challanBody = document.querySelector("#challan-table tbody");
                    challanBody.innerHTML = "";

                    data.forEach((row, index) => {
                        const tr = document.createElement("tr");
                        tr.innerHTML = `
                            <td><input type="text" style="width:80px" value="${index + 1}"></td>
                            <td><input type="text" style="width:80px" value="${row.month || ''}"></td>
                            <td>
                                <select style="width:100px">
                                    <option value="">Select</option>
                                    <option value="Add">Add</option>
                                    <option value="Modify">Modify</option>
                                    <option value="Delete">Delete</option>
                                </select>
                            </td>
                            <td><input type="number" style="width:100px" value="${row.total_tds || 0}"></td>
                            <td><input type="number" style="width:100px" value="${row.total_education_cess || 0}"></td>
                            <td><input type="number" style="width:100px"></td>
                            <td><input type="number" style="width:120px"></td>
                            <td><input type="text" style="width:120px"></td>
                            <td><input type="text" style="width:160px"></td>
                            <td><input type="date"></td>
                            <td><input type="text" style="width:160px"></td>
                            <td><input type="number" style="width:100px"></td>
                            <td><input type="number" style="width:100px"></td>
                            <td><input type="number" style="width:100px"></td>
                            <td>
                                <select style="width:100px">
                                    <option value="">Select</option>
                                    <option value="92A">92A</option>
                                    <option value="92B">92B</option>
                                </select>
                            </td>
                            <td><input type="number" style="width:100px" value="${row.total_surcharge || 0}"></td>
                            <td><input type="number" style="width:100px"></td>
                            <td><input type="number" style="width:100px"></td>
                            <td><input type="number" style="width:130px"></td>
                            <td><input type="text" style="width:150px"></td>
                            <td><input type="date"></td>
                            <td><input type="text" style="width:150px"></td>
                            <td>
                                <select style="width:100px">
                                    <option value="">Select</option>
                                    <option value="No">No</option>
                                    <option value="Yes">Yes</option>
                                </select>
                            </td>
                            <td>
                                <select style="width:120px">
                                    <option value="">Select</option>
                                    <option value="100">100</option>
                                    <option value="200">200 - TDS payable by taxpayer</option>
                                    <option value="400">400 - TDS regular assessment</option>
                                </select>
                            </td>
                            <td><button class="remove-row">🗑</button></td>
                        `;
                        challanBody.appendChild(tr);
                    });

                    // -----------------------------
                    // 2️⃣ Populate Annexure Table (Employee-wise)
                    // -----------------------------
                    const annexureBody = document.querySelector("#annexure-table tbody");
                annexureBody.innerHTML = ""; // clear old rows

                // Loop over each month’s data
                data.forEach((monthRow, monthIndex) => {
                    const challanSerial = monthIndex + 1; // same serial for all employees of this month
                    const employees = monthRow.employees || [];

                    // Loop over employees of that month
                    employees.forEach((emp, empIndex) => {
                        const tr = document.createElement("tr");
                        tr.innerHTML = `
                            <td><input type="text" style="width:60px" value="${empIndex + 1}"></td>
                            <td><input type="text" style="width:140px" value="${challanSerial}"></td>
                            <td><input type="text" style="width:160px" value=""></td>
                            <td><input type="date" value=""></td>
                            <td>
                                <select>
                                    <option value="">Select</option>
                                    <option>92A</option>
                                    <option>92B</option>
                                    <option>92C</option>
                                    <option>94P</option>
                                </select>
                            </td>
                            <td><input type="number" style="width:120px" value="${emp.tds || ''}"></td>
                            <td><input type="number" style="width:120px" value=""></td>
                            <td><input type="text" style="width:180px" value="${emp.employee || ''}"></td>
                            <td><input type="text" style="width:150px" value="${emp.employee_pan || ''}"></td>
                            <td><input type="date" value=""></td>
                            <td><input type="number" style="width:120px" value="${emp.tds || ''}"></td>
                            <td><input type="number" style="width:120px" value="${emp.education_cess || ''}"></td>
                            <td><input type="number" style="width:130px" value=""></td>
                            <td><input type="number" style="width:130px" value=""></td>
                            <td>
                                <select>
                                    <option value="">Select</option>
                                    <option>Add</option>
                                    <option>Update</option>
                                    <option>PAN Update</option>
                                </select>
                            </td>
                            <td><input type="text" style="width:180px" value=""></td>
                            <td><input type="number" style="width:120px" value=""></td>
                            <td><input type="number" style="width:120px" value="${emp.total_amount || ''}"></td>
                            <td><input type="text" style="width:150px" value="${emp.employee_pan || ''}"></td>
                            <td><input type="text" style="width:180px" value="${emp.employee_name || ''}"></td>
                            <td><input type="number" style="width:130px" value=""></td>
                            <td><input type="number" style="width:130px" value="${emp.surcharge || ''}"></td>
                            <td><input type="number" style="width:130px" value="${emp.tds || ''}"></td>
                            <td><input type="number" style="width:130px" value=""></td>
                            <td><input type="date" value=""></td>
                            <td><input type="text" style="width:180px" value=""></td>
                            <td>
                                <select>
                                    <option value="">Select</option>
                                    <option>Zero Deduction</option>
                                    <option>Lower Deduction</option>
                                    <option>Higher Deduction</option>
                                </select>
                            </td>
                            <td><button class="remove-row">🗑</button></td>
                        `;
                        annexureBody.appendChild(tr);
                    });
                });

                frappe.msgprint({
                    title: "Success",
                    message: "✅ Annexure table populated successfully!",
                    indicator: "green"
                });
            } else {
                frappe.msgprint({
                    title: "Error",
                    message: "❌ Failed to fetch annexure data",
                    indicator: "red"
                });


                    frappe.msgprint({
                        title: "Success",
                        message: "✅ Both Challan and Annexure tables populated successfully!",
                        indicator: "green"
                    });
                }
            }
        });




    });


        // ✅ --- CSI FILE UPLOAD LOGIC (for "Other Services" tab) ---
        let selectedCSIFile = null;

        // When file is selected
        $(page.body).on("change", "#csi-upload", function (event) {
            const file = event.target.files[0];
            const fileNameSpan = document.getElementById("csi-file-name");

            if (file) {
                selectedCSIFile = file;
                fileNameSpan.textContent = file.name;
                console.log("CSI file selected:", file);
            } else {
                selectedCSIFile = null;
                fileNameSpan.textContent = "";
            }
        });



        // When "Save Services" button is clicked
        $(page.body).on("click", "#other-submit", function () {
            // 1️⃣ Validate CSI file
            if (!selectedCSIFile) {
                frappe.msgprint("Please attach a CSI file before saving.");
                return;
            }

            // 2️⃣ Collect all form field data
            const allFields = $(page.body).find("input, select, textarea");
            const fieldData = {};
            allFields.each(function () {
                const id = $(this).attr("id") || $(this).attr("name") || "unnamed_field";
                fieldData[id] = $(this).val();
            });

            // console.log("All Form Fields:11111111111111111", fieldData);

            // 3️⃣ Collect Challan Table Data
            const challanRows = [];
            $("#challan-table tbody tr").each(function () {
                const rowData = {};
                $(this).find("input, select").each(function (i, input) {
                    const header = $("#challan-table thead th").eq(i).text().trim() || `Col_${i + 1}`;
                    rowData[header] = $(input).val();
                });
                challanRows.push(rowData);
            });

            // console.log("Challan Table Data:", challanRows);

            // 4️⃣ Collect Annexure Table Data
            const annexureRows = [];
            $("#annexure-table tbody tr").each(function () {
                const rowData = {};
                $(this).find("input, select").each(function (i, input) {
                    const header = $("#annexure-table thead th").eq(i).text().trim() || `Col_${i + 1}`;
                    rowData[header] = $(input).val();
                });
                annexureRows.push(rowData);
            });

            // console.log("Annexure Table Data:", annexureRows);

            const company_value = company_field.get_value();
            const fiscal_year_value = fiscal_field.get_value();
            const payroll_period_value = payroll_period_field.get_value();
            const branch_value=branch_field.get_value();

            fieldData["company"] = company_value;
            fieldData["fiscal_year"] = fiscal_year_value;
            fieldData["payroll_period"] = payroll_period_value;
            fieldData["branch"] = branch_value;

            frappe.call({
                method: "cn_indian_payroll.cn_indian_payroll.overrides.tds_file.insert_tds_details",
                args: {
                    challan_data: challanRows,
                    annexure_data: annexureRows,
                    fieldData: fieldData,
                },
                freeze: true,
                freeze_message: "Saving TDS details...",
                callback: function (r) {
                    if (r.message) {
                        const tds_return_name = r.message.tds_return;

                        // frappe.msgprint({
                        //     title: "Success",
                        //     message: `✅ TDS Return <b>${tds_return_name}</b> created successfully.`,
                        //     indicator: "green",
                        // });


                        upload_csi_file(selectedCSIFile, tds_return_name);
                        create_txt_file(fieldData, tds_return_name);

                    }

                },

            });
        });

        function upload_csi_file(file, tds_return_name) {
            const reader = new FileReader();

            reader.onload = function (event) {
                const base64Data = event.target.result.split(",")[1];

                // console.log(file.name,"file.namefile.name")
                // console.log(base64Data,"base64Databas64Data")
                // console.log(tds_return_name,"tds_return_nametds_return_name")


                frappe.call({
                    method: "cn_indian_payroll.cn_indian_payroll.overrides.tds_file.upload_csi_file",
                    args: {
                        file_name: file.name,
                        file_data: base64Data,
                        attached_to_doctype: "TDS RETURN",
                        attached_to_name: tds_return_name,
                    },
                    freeze: true,
                    freeze_message: "Uploading CSI file...",
                    callback: function (r) {
                        if (r.message) {

                            console.log("CSI file upload response:", r.message);

                        }
                    },
                });
            };

            reader.readAsDataURL(file);
        }

        function create_txt_file(fieldData, tds_return_name) {
            frappe.call({
                method: "cn_indian_payroll.cn_indian_payroll.overrides.tds_file.create_txt_file",
                args: {
                    basic_data: fieldData,
                    attached_to_name: tds_return_name
                },
                freeze: true,
                freeze_message: "Creating .txt file...",
                callback: function (r) {
                    if (r.message) {
                        console.log("TXT file created:", r.message);
                    }
                },
            });
        }






}
