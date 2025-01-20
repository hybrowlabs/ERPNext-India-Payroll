import frappe

def validate(self, method):
    # Call the function to insert or update custom fields
    insert_custom_fields(self)
    salary_component(self)

def insert_custom_fields(self):
    # Check if there are any salary structure assignments
    if len(self.salary_structure_assignment) > 0:
        for assignment in self.salary_structure_assignment:
            # Fetch existing custom field based on the field name and doctype
            custom_field = frappe.db.get_list(
                'Custom Field',
                filters={
                    'dt': 'Salary Structure Assignment',
                    'fieldname': assignment.field_name,
                },
                fields=['name']
            )

            if not custom_field:  # If no custom field exists, create a new one
                doc = frappe.get_doc({
                    'doctype': 'Custom Field',
                    'insert_after': assignment.label,  
                    'dt': 'Salary Structure Assignment',
                    'label': assignment.label,  
                    'fieldname': assignment.field_name,  
                    'fieldtype': assignment.field_type,  
                    'insert_after': "custom_tab_3",
                    'hidden ':assignment.hidden,
                    'allow_on_submit':assignment.allow_on_submit,
                    'depends_on':assignment.depends_on,
                    'options':assignment.options
                })
                doc.insert()
                frappe.db.commit()  

            else:  
                custom_field_doc = frappe.get_doc("Custom Field", custom_field[0].name)
                if custom_field_doc.label != assignment.label:
                    custom_field_doc.label = assignment.label

                # if custom_field.hidden!=assignment.hidden:
                #     custom_field.hidden=assignment.hidden

                # if custom_field.allow_on_submit!=assignment.allow_on_submit:
                #     custom_field.allow_on_submit=assignment.allow_on_submit

                    




                custom_field_doc.save()
                frappe.db.commit()  




def salary_component(self):
    if len(self.salary_component_configuration)>0:
        for component in self.salary_component_configuration:
            get_component = frappe.db.get_list(
                'Salary Component',
                filters={

                    'name':component.salary_component,
                    
                },
                fields=['*']
            )

            if len(get_component)==0:  
                
                doc1 = frappe.get_doc({
                    'doctype': 'Salary Component',
                    'salary_component': component.salary_component,  
                    'salary_component_abbr': component.abbr,
                    'type': component.component_type, 
                    'name':component.salary_component, 
                    'condition':component.condition,
                    'formula':component.formula ,
                    'depends_on_payment_days':component.depends_on_payment_days,
                    'custom_perquisite' :component.perquisite,
                    'custom_is_part_of_appraisal':component.is_part_of_appraisal,
                    'is_tax_applicable':component.is_tax_applicable,
                    'custom_is_part_of_gross_pay':component.is_part_of_gross_pay,
                    'custom_is_accrual':component.is_accrual,
                    'round_to_the_nearest_integer':component.round_to_the_nearest_integer,
                    
                    'custom_is_reimbursement':component.is_reimbursement,
                    'custom_tax_exemption_applicable_based_on_regime':component.tax_applicable_based_on_regime,
                    'regime':component.regime,
                    'do_not_include_in_total':component.do_not_include_in_total,
                    'custom_is_part_of_ctc':component.is_part_of_ctc,
                    'custom_is_arrear':component.is_arrear,
                    'custom_component':component.component,
                    

                    
                })
                doc1.insert()
                frappe.db.commit()  

            else:  
                custom_component = frappe.get_doc("salary Component", get_component[0].name)
                
                # custom_component.type = component.component_type,

                

                    




            #     custom_field_doc.save()
            #     frappe.db.commit()
