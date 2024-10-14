import frappe

@frappe.whitelist()
def switch_regime(doc_id, employee, regime,company):
    ss_assignment = frappe.get_doc("Salary Structure Assignment", doc_id)


    get_tax_regime=frappe.get_list(
                'Income Tax Slab',
                filters={'custom_select_regime':regime,"company":company},
                fields=['*']
            )

    if len(get_tax_regime)>0:

        ss_assignment.income_tax_slab =get_tax_regime[0].name 

        

    
    
        if regime == "Old Regime":
            component_array = []
            amount = []
            max_amount = []
            
            # Uniform Allowance
            if ss_assignment.custom_is_uniform_allowance and ss_assignment.custom_uniform_allowance_value:
                uniform_component = frappe.get_list(
                    'Employee Tax Exemption Sub Category',
                    filters={'custom_component_type': "Uniform"},
                    fields=['*']
                )

                for i in uniform_component:
                    component_array.append(i.name)
                    amount.append(0)
                    max_amount.append(i.max_amount)

            # Employee Provident Fund (EPF)
            if ss_assignment.custom_is_epf:
                basic_amount = (ss_assignment.base * 0.35) / 12
                epf_amount = (basic_amount * 12) / 100
                epf_amount_year = epf_amount * 12

                epf_component = frappe.get_list(
                    'Employee Tax Exemption Sub Category',
                    filters={'custom_component_type': "EPF"},
                    fields=['*']
                )

                for i in epf_component:
                    component_array.append(i.name)
                    max_amount.append(i.max_amount)

                    if epf_amount_year > i.max_amount:
                        amount.append(i.max_amount)
                    else:
                        amount.append(epf_amount_year)

            # NPS (National Pension System)
            if ss_assignment.custom_is_nps:
                nps_amount = ((ss_assignment.base * 0.35) / 12)
                nps_amount_percentage = (nps_amount * ss_assignment.custom_nps_percentage) / 100
                nps_amount_year = nps_amount_percentage * 12

                nps_component = frappe.get_list(
                    'Employee Tax Exemption Sub Category',
                    filters={'custom_component_type': "NPS"},
                    fields=['*']
                )

                for i in nps_component:
                    component_array.append(i.name)
                    max_amount.append(nps_amount_year)
                    amount.append(nps_amount_year)

            # Professional Tax (PT)
            if ss_assignment.custom_state:
                pt_component = frappe.get_list(
                    'Employee Tax Exemption Sub Category',
                    filters={'custom_component_type': "Professional Tax"},
                    fields=['*']
                )

                for i in pt_component:
                    component_array.append(i.name)
                    max_amount.append(i.max_amount)
                    amount.append(2400)

            # Updating Employee Tax Exemption Declaration
            update_each_doc = frappe.get_list(
                'Employee Tax Exemption Declaration',
                filters={'employee': ss_assignment.employee, 'payroll_period': ss_assignment.custom_payroll_period, 'docstatus': ['in', [0, 1]]},
                fields=['*']
            )

            # Insert and submit the Employee Tax Exemption Declaration
            if len(update_each_doc)>0:
                for doc in update_each_doc:
                    doc1 = frappe.get_doc("Employee Tax Exemption Declaration", doc.name)
                    doc1.custom_income_tax=get_tax_regime[0].name
                    doc1.custom_posting_date = frappe.utils.nowdate()
                    doc1.declarations=[]
                    
                    for x in range(len(component_array)):
                        # Add child records
                        doc2_child1 = doc1.append("declarations", {})
                        doc2_child1.exemption_sub_category = component_array[x]
                        doc2_child1.amount = amount[x]
                        doc2_child1.max_amount = max_amount[x]
                    
                    # Save and submit the document
                    doc1.save()
                    doc1.submit()
                    
                    # Commit the changes to the database
                    frappe.db.commit()

        if regime == "New Regime":
            component_array = []
            amount = []
            max_amount = []
            if ss_assignment.custom_is_nps:
                nps_amount = ((ss_assignment.base * 0.35) / 12)
                nps_amount_percentage = (nps_amount * ss_assignment.custom_nps_percentage) / 100
                nps_amount_year = nps_amount_percentage * 12

                nps_component = frappe.get_list(
                    'Employee Tax Exemption Sub Category',
                    filters={'custom_component_type': "NPS"},
                    fields=['*']
                )

                for i in nps_component:
                    component_array.append(i.name)
                    max_amount.append(nps_amount_year)
                    amount.append(nps_amount_year)

            update_each_doc = frappe.get_list(
                'Employee Tax Exemption Declaration',
                filters={'employee': ss_assignment.employee, 'payroll_period': ss_assignment.custom_payroll_period, 'docstatus': ['in', [0, 1]]},
                fields=['name']
            )

            if len(update_each_doc)>0:
                for doc in update_each_doc:
                    doc1 = frappe.get_doc("Employee Tax Exemption Declaration", doc.name)
                    doc1.custom_income_tax=get_tax_regime[0].name
                    doc1.custom_posting_date = frappe.utils.nowdate()
                    doc1.declarations=[]
                    
                    for x in range(len(component_array)):
                        # Add child records
                        doc2_child1 = doc1.append("declarations", {})
                        doc2_child1.exemption_sub_category = component_array[x]
                        doc2_child1.amount = amount[x]
                        doc2_child1.max_amount = max_amount[x]
                    
                    # Save and submit the document
                    doc1.save()
                    doc1.submit()
                    
                    # Commit the changes to the database
                    frappe.db.commit()
    

            

        
        ss_assignment.save()

    

    else:
        frappe.msgprint("Create Income Tax Slab")