
import frappe
import json

@frappe.whitelist()
def get_salary_component(data=None, component=None, custom_field=None):
    try:
        data = json.loads(data)  
        custom_field = json.loads(custom_field) if custom_field else []  # Ensure custom_field is parsed as a list



        salary_component = data.get("salary_component")
        component_type = data.get("type")

        if component and custom_field and salary_component:
            existing_components = frappe.get_list(
                'Salary Component',
                filters={
                    "name": salary_component,
                    "disabled": 0,
                    "type": data.get("component_type"),
                },
                fields=['*']
            )

            if len(existing_components) > 0:
                get_each_doc = frappe.get_doc("Salary Component", existing_components[0].name)

                get_each_doc.depends_on_payment_days = data.get("depends_on_payment_days")
                get_each_doc.is_tax_applicable = data.get("is_tax_applicable")
                get_each_doc.do_not_include_in_total = data.get("do_not_include_in_total")
                get_each_doc.remove_if_zero_valued = data.get("remove_if_zero_valued")
                get_each_doc.custom_is_part_of_gross_pay = data.get("is_part_of_gross_pay")
                get_each_doc.disabled = data.get("disabled")
                get_each_doc.custom_is_part_of_ctc = data.get("is_part_of_ctc")
                get_each_doc.custom_perquisite = data.get("perquisite")
                get_each_doc.custom_is_accrual = data.get("is_accrual")
                get_each_doc.custom_is_reimbursement = data.get("reimbursement")
                get_each_doc.custom_is_part_of_appraisal = data.get("is_part_of_appraisal")
                get_each_doc.custom_tax_exemption_applicable_based_on_regime = data.get("tax_applicable_based_on_regime")
                get_each_doc.custom_regime = data.get("regime")
                get_each_doc.condition = data.get("condition")
                get_each_doc.formula = data.get("formula")

                get_each_doc.save()

                if data.get("is_arrear") == 1:

                    arrear_check = frappe.get_list('Salary Component',
                    filters={

                            
                                "name":data.get("salary_component") + "(Arrear)",

                            },
                        fields=['*']
                        )

                    if len(arrear_check)==0:
                        insert_doc = frappe.new_doc('Salary Component')
                        insert_doc.name = data.get("salary_component") + "(Arrear)"
                        insert_doc.salary_component = data.get("salary_component") + "(Arrear)"
                        insert_doc.salary_component_abbr = data.get("abbr") + "Arrear"
                        insert_doc.type = data.get("component_type")
                        insert_doc.is_tax_applicable = 1
                        insert_doc.depends_on_payment_days = 0
                        insert_doc.round_to_the_nearest_integer = 1
                        insert_doc.do_not_include_in_total = 0
                        insert_doc.custom_is_part_of_gross_pay = 1
                        insert_doc.custom_is_part_of_ctc = 0
                        insert_doc.custom_is_arrear = 1
                        insert_doc.custom_tax_exemption_applicable_based_on_regime = 1
                        insert_doc.custom_regime = "All"
                        insert_doc.custom_component = data.get("salary_component")
                        insert_doc.insert()



                for field in custom_field:

                    custom_field_check = frappe.get_list('Custom Field',
                    filters={
      
                        "fieldname":field.get('field_name'),
                        "dt":"Salary Structure Assignment",

                        
                        },
                        fields=['*']
                        )

                    if len(custom_field_check)==0:

                        custom_field = frappe.new_doc('Custom Field')
                        custom_field.dt = field.get('doctype')
                        custom_field.label = field.get('label')
                        custom_field.fieldname = field.get('field_name')
                        custom_field.insert_after = field.get('insert_after')
                        custom_field.fieldtype = field.get('field_type')
                        custom_field.allow_on_submit = 1
                        custom_field.depends_on = field.get('depends')
                        custom_field.insert()
                    
                    else:
                        frappe.msgprint("Custom Field Already Exists")



                get_library_item = frappe.get_doc('Salary Component Library Item',salary_component)
                get_library_item.component_added = 1
                get_library_item.save()
                frappe.msgprint("Salary Component Added")

            else:
                get_abbr_component = frappe.get_list('Salary Component',
                    filters={
                            
                        "disabled":0,
                            
                        "salary_component_abbr":data.get("abbr"),

                        
                        },
                        fields=['*']
                        )

                if len(get_abbr_component)>0:
                    frappe.msgprint("Another component uses same abbr,plz change the abbr")

                else:
                    get_each_doc = frappe.new_doc('Salary Component')
                    get_each_doc.name=data.get("salary_component")
                    get_each_doc.salary_component=data.get("salary_component")
                    get_each_doc.salary_component_abbr=data.get("abbr")
                    get_each_doc.type=data.get("component_type")

                    get_each_doc.depends_on_payment_days=data.get("depends_on_payment_days")
                    get_each_doc.is_tax_applicable=data.get("is_tax_applicable")
                    get_each_doc.do_not_include_in_total=data.get("do_not_include_in_total")
                    get_each_doc.remove_if_zero_valued=data.get("remove_if_zero_valued")
                    get_each_doc.custom_is_part_of_gross_pay=data.get("is_part_of_gross_pay")
                    get_each_doc.disabled=data.get("disabled")
                    get_each_doc.custom_is_part_of_ctc=data.get("is_part_of_ctc")
                    get_each_doc.custom_perquisite=data.get("perquisite")
                    get_each_doc.custom_is_accrual=data.get("is_accrual")
                    get_each_doc.custom_is_reimbursement=data.get("reimbursement")
                        
                    get_each_doc.custom_is_part_of_appraisal=data.get("is_part_of_appraisal")
                    get_each_doc.custom_tax_exemption_applicable_based_on_regime=data.get("tax_applicable_based_on_regime")
                    get_each_doc.custom_regime=data.get("regime")
                        
                    get_each_doc.insert()

                    if data.get("is_arrear") == 1:
                        insert_doc = frappe.new_doc('Salary Component')
                        insert_doc.name = data.get("salary_component") + "Arrear"
                        insert_doc.salary_component = data.get("salary_component") + "Arrear"
                        insert_doc.salary_component_abbr = data.get("abbr") + "Arrear"
                        insert_doc.type = data.get("component_type")
                        insert_doc.is_tax_applicable = 1
                        insert_doc.depends_on_payment_days = 0
                        insert_doc.round_to_the_nearest_integer = 1
                        insert_doc.do_not_include_in_total = 0
                        insert_doc.custom_is_part_of_gross_pay = 1
                        insert_doc.custom_is_part_of_ctc = 0
                        insert_doc.custom_is_arrear = 1
                        insert_doc.custom_tax_exemption_applicable_based_on_regime = 1
                        insert_doc.custom_regime = "All"
                        insert_doc.custom_component = data.get("salary_component")
                        insert_doc.insert()


                    for field in custom_field:

                        custom_field_check = frappe.get_list('Custom Field',
                        filters={
        
                            "fieldname":field.get('field_name'),
                            "dt":"Salary Structure Assignment",

                            
                            },
                            fields=['*']
                            )

                        if len(custom_field_check)==0:

                            custom_field = frappe.new_doc('Custom Field')
                            custom_field.dt = field.get('doctype')
                            custom_field.label = field.get('label')
                            custom_field.fieldname = field.get('field_name')
                            custom_field.insert_after = field.get('insert_after')
                            custom_field.fieldtype = field.get('field_type')
                            custom_field.allow_on_submit = 1
                            custom_field.depends_on = field.get('depends')
                            custom_field.insert()

                    get_library_item = frappe.get_doc('Salary Component Library Item',salary_component)
                    get_library_item.component_added = 1
                    get_library_item.save()
                    frappe.msgprint("Salary Component Added")

           
            

        elif component_type != "LTA Reimbursement" and not custom_field:
            get_each_doc = frappe.new_doc('Salary Component')
            get_each_doc.name=data.get("salary_component")
            get_each_doc.salary_component=data.get("salary_component")
            get_each_doc.salary_component_abbr=data.get("abbr")
            get_each_doc.type=data.get("component_type")

            get_each_doc.depends_on_payment_days=data.get("depends_on_payment_days")
            get_each_doc.is_tax_applicable=data.get("is_tax_applicable")
            get_each_doc.do_not_include_in_total=data.get("do_not_include_in_total")
            get_each_doc.remove_if_zero_valued=data.get("remove_if_zero_valued")
            get_each_doc.custom_is_part_of_gross_pay=data.get("is_part_of_gross_pay")
            get_each_doc.disabled=data.get("disabled")
            get_each_doc.custom_is_part_of_ctc=data.get("is_part_of_ctc")
            get_each_doc.custom_perquisite=data.get("perquisite")
            get_each_doc.custom_is_accrual=data.get("is_accrual")
            get_each_doc.custom_is_reimbursement=data.get("reimbursement")
                        
            get_each_doc.custom_is_part_of_appraisal=data.get("is_part_of_appraisal")
            get_each_doc.custom_tax_exemption_applicable_based_on_regime=data.get("tax_applicable_based_on_regime")
            get_each_doc.custom_regime=data.get("regime")

            get_each_doc.formula=data.get("formula")
            get_each_doc.condition=data.get("condition")
            get_each_doc.custom_sequence=data.get("sequence")
            
                        
            get_each_doc.insert()

            get_library_item = frappe.get_doc('Salary Component Library Item',salary_component)
            get_library_item.component_added = 1
            get_library_item.save()
            frappe.msgprint("Salary Component Added")

            
            

        elif component_type == "LTA Reimbursement" and not custom_field:
            salary_component = data.get("salary_component")
            
            # Insert LTA Reimbursement Component
            lta_reimbursement = frappe.new_doc("Salary Component")
            lta_reimbursement.name = salary_component
            lta_reimbursement.salary_component = salary_component
            lta_reimbursement.salary_component_abbr = data.get("abbr")
            lta_reimbursement.type = data.get("component_type")

            lta_reimbursement.depends_on_payment_days = data.get("depends_on_payment_days")
            lta_reimbursement.is_tax_applicable = data.get("is_tax_applicable")
            lta_reimbursement.do_not_include_in_total = data.get("do_not_include_in_total")
            lta_reimbursement.remove_if_zero_valued = data.get("remove_if_zero_valued")
            lta_reimbursement.custom_is_part_of_gross_pay = data.get("is_part_of_gross_pay")
            lta_reimbursement.disabled = data.get("disabled")
            lta_reimbursement.custom_is_part_of_ctc = data.get("is_part_of_ctc")
            lta_reimbursement.custom_perquisite = data.get("perquisite")
            lta_reimbursement.custom_is_accrual = data.get("is_accrual")
            lta_reimbursement.custom_is_reimbursement = data.get("reimbursement")

            lta_reimbursement.custom_is_part_of_appraisal = data.get("is_part_of_appraisal")
            lta_reimbursement.custom_tax_exemption_applicable_based_on_regime = data.get("tax_applicable_based_on_regime")
            lta_reimbursement.custom_regime = data.get("regime")

            lta_reimbursement.formula = data.get("formula")
            lta_reimbursement.condition = data.get("condition")
            lta_reimbursement.custom_sequence = data.get("sequence")
            lta_reimbursement.component_type = "LTA Reimbursement"
            lta_reimbursement.insert()

            # Insert LTA Taxable Component
            lta_taxable = frappe.new_doc("Salary Component")
            lta_taxable.name = "LTA Taxable"
            lta_taxable.salary_component = "LTA Taxable"
            lta_taxable.salary_component_abbr = "LTA_TAX"
            lta_taxable.type = data.get("component_type")

            lta_taxable.depends_on_payment_days = data.get("depends_on_payment_days")
            lta_taxable.is_tax_applicable = 1
            lta_taxable.do_not_include_in_total = data.get("do_not_include_in_total")
            lta_taxable.remove_if_zero_valued = data.get("remove_if_zero_valued")
            lta_taxable.custom_is_part_of_gross_pay = data.get("is_part_of_gross_pay")
            lta_taxable.disabled = data.get("disabled")
            lta_taxable.custom_is_part_of_ctc = data.get("is_part_of_ctc")
            lta_taxable.custom_perquisite = data.get("perquisite")
            lta_taxable.custom_is_accrual = data.get("is_accrual")
            lta_taxable.custom_is_reimbursement = 0

            lta_taxable.custom_is_part_of_appraisal = data.get("is_part_of_appraisal")
            lta_taxable.custom_tax_exemption_applicable_based_on_regime = data.get("tax_applicable_based_on_regime")
            lta_taxable.custom_regime = data.get("regime")

            lta_taxable.formula = data.get("formula")
            lta_taxable.condition = data.get("condition")
            lta_taxable.custom_sequence = data.get("sequence")
            lta_taxable.component_type = "LTA Taxable"
            lta_taxable.insert()

            # Insert LTA Non-Taxable Component
            lta_non_taxable = frappe.new_doc("Salary Component")
            lta_non_taxable.name = "LTA Non Taxable"
            lta_non_taxable.salary_component = "LTA Non Taxable"
            lta_non_taxable.salary_component_abbr = "LTA_NON_TAX"
            lta_non_taxable.type = data.get("component_type")

            lta_non_taxable.depends_on_payment_days = data.get("depends_on_payment_days")
            lta_non_taxable.is_tax_applicable = 0
            lta_non_taxable.do_not_include_in_total = data.get("do_not_include_in_total")
            lta_non_taxable.remove_if_zero_valued = data.get("remove_if_zero_valued")
            lta_non_taxable.custom_is_part_of_gross_pay = data.get("is_part_of_gross_pay")
            lta_non_taxable.disabled = data.get("disabled")
            lta_non_taxable.custom_is_part_of_ctc = data.get("is_part_of_ctc")
            lta_non_taxable.custom_perquisite = data.get("perquisite")
            lta_non_taxable.custom_is_accrual = data.get("is_accrual")
            lta_non_taxable.custom_is_reimbursement = 0

            lta_non_taxable.custom_is_part_of_appraisal = data.get("is_part_of_appraisal")
            lta_non_taxable.custom_tax_exemption_applicable_based_on_regime = data.get("tax_applicable_based_on_regime")
            lta_non_taxable.custom_regime = data.get("regime")

            lta_non_taxable.formula = data.get("formula")
            lta_non_taxable.condition = data.get("condition")
            lta_non_taxable.custom_sequence = data.get("sequence")
            lta_non_taxable.component_type = "LTA Non Taxable"
            lta_non_taxable.insert()

            # Update Salary Component Library Item
            if salary_component:
                get_library_item = frappe.get_doc("Salary Component Library Item", salary_component)
                get_library_item.component_added = 1
                get_library_item.save()

            frappe.msgprint("Salary Components Added Successfully!")


           
        






    except Exception as e:
        frappe.log_error(f"Error in get_salary_component: {e}")
        raise

