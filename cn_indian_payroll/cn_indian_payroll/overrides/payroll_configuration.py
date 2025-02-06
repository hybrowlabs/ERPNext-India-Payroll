# import frappe
# import json

# @frappe.whitelist()


# def get_salary_component(data,component,custom_field):


#     try:
#         data = json.loads(data)  

        
#         salary_component = data.get("salary_component")

#         if len(component)>0 and len(custom_field)>0 and salary_component:

#             for field in custom_field:
#                 frappe.msgprint(f"Doctype: {field.get('doctype')}")

            # for ji in custom_field:
            #     frappe.msgprint(str(ji.doctype))
            

                # get_salary_component = frappe.get_list('Salary Component',
                # filters={
                #     "name":salary_component,
                #     "disabled":0,
                #     "type":component_type

                  
                # },
                # fields=['*']
                # )
                # if len(get_salary_component)>0:
                    # get_each_doc=frappe.get_doc("Salary Component",get_salary_component[0].name)

                    # get_each_doc.depends_on_payment_days=data.get("depends_on_payment_days")
                    # get_each_doc.is_tax_applicable=data.get("is_tax_applicable")
                    # get_each_doc.do_not_include_in_total=data.get("do_not_include_in_total")
                    # get_each_doc.remove_if_zero_valued=data.get("remove_if_zero_valued")
                    # get_each_doc.custom_is_part_of_gross_pay=data.get("is_part_of_gross_pay")
                    # get_each_doc.disabled=data.get("disabled")
                    # get_each_doc.custom_is_part_of_ctc=data.get("is_part_of_ctc")
                    # get_each_doc.custom_perquisite=data.get("perquisite")
                    # get_each_doc.custom_is_accrual=data.get("is_accrual")
                    # get_each_doc.custom_is_reimbursement=data.get("reimbursement")
                    
                    # get_each_doc.custom_is_part_of_appraisal=data.get("is_part_of_appraisal")
                    # get_each_doc.custom_tax_exemption_applicable_based_on_regime=data.get("tax_applicable_based_on_regime")
                    # get_each_doc.custom_regime=data.get("regime")
                    # get_each_doc.condition=data.get("condition")
                    # get_each_doc.formula=data.get("formula")

                    # get_each_doc.save()

                    # if data.get("is_arrear")==1:

                    #     insert_doc = frappe.new_doc('Salary Component')
                    #     insert_doc.name = data.get("salary_component")+("Arrear")
                    #     insert_doc.salary_component = data.get("salary_component")+("Arrear")
                    #     insert_doc.salary_component_abbr=data.get("abbr")+"Arrear"
                    #     insert_doc.type=data.get("component_type")
                    #     insert_doc.is_tax_applicable=1
                    #     insert_doc.depends_on_payment_days=0
                    #     insert_doc.round_to_the_nearest_integer=1
                    #     insert_doc.do_not_include_in_total=0
                    #     insert_doc.custom_is_part_of_gross_pay=1
                    #     insert_doc.custom_is_part_of_ctc=0
                    #     insert_doc.custom_is_arrear=1
                    #     insert_doc.custom_tax_exemption_applicable_based_on_regime=1
                    #     insert_doc.custom_regime="All"
                    #     insert_doc.custom_component=data.get("salary_component")
                    #     insert_doc.insert()

                    
                    

                    # if custom_field:
                    #     frappe.msgprint(str(custom_field))
                        # for field in custom_field:
                        #     frappe.msgprint(str(field.))
                    # # Creating custom field in "Salary Structure Assignment"
                    # fieldname = salary_component.lower().replace(" ", "_")  

                    # custom_field_1 = frappe.new_doc('Custom Field')
                    # custom_field_1.dt = "Salary Structure Assignment"
                    # custom_field_1.label = get_salary_component[0]['name']
                    # custom_field_1.fieldname = fieldname
                    # custom_field_1.insert_after = "custom_tab_3"
                    # custom_field_1.fieldtype = "Check"
                    # custom_field_1.allow_on_submit = 1
                    # custom_field_1.insert()

                    # # Creating second custom field for storing value
                    # custom_field_2 = frappe.new_doc('Custom Field')
                    # custom_field_2.dt = "Salary Structure Assignment"
                    # custom_field_2.label = f"{get_salary_component[0]['name']} Value"
                    # custom_field_2.fieldname = f"{fieldname}_value"
                    # custom_field_2.insert_after = fieldname
                    # custom_field_2.fieldtype = "Float"
                    # custom_field_2.allow_on_submit = 1
                    # custom_field_2.depends_on = f"eval:doc.{fieldname}==1"
                    # custom_field_2.insert()


                    # update_doc=frappe.get_doc("Salary Component Library Item",get_salary_component[0].name)
                    # update_doc.component_added=1
                    # update_doc.save()



                    


                # else:


                #     get_abbr_component = frappe.get_list('Salary Component',
                #     filters={
                        
                #         "disabled":0,
                        
                #         "salary_component_abbr":data.get("abbr")

                    
                #     },
                #     fields=['*']
                #     )

                #     if len(get_abbr_component)>0:
                #         frappe.msgprint("Another component uses same abbr,change abbr")

                #     else:

                #         get_each_doc = frappe.new_doc('Salary Component')
                #         get_each_doc.name=data.get("salary_component")
                #         get_each_doc.salary_component=data.get("salary_component")

                #         get_each_doc.salary_component_abbr=data.get("abbr")
                #         get_each_doc.type=data.get("component_type")

                #         get_each_doc.depends_on_payment_days=data.get("depends_on_payment_days")
                #         get_each_doc.is_tax_applicable=data.get("is_tax_applicable")
                #         get_each_doc.do_not_include_in_total=data.get("do_not_include_in_total")
                #         get_each_doc.remove_if_zero_valued=data.get("remove_if_zero_valued")
                #         get_each_doc.custom_is_part_of_gross_pay=data.get("is_part_of_gross_pay")
                #         get_each_doc.disabled=data.get("disabled")
                #         get_each_doc.custom_is_part_of_ctc=data.get("is_part_of_ctc")
                #         get_each_doc.custom_perquisite=data.get("perquisite")
                #         get_each_doc.custom_is_accrual=data.get("is_accrual")
                #         get_each_doc.custom_is_reimbursement=data.get("reimbursement")
                        
                #         get_each_doc.custom_is_part_of_appraisal=data.get("is_part_of_appraisal")
                #         get_each_doc.custom_tax_exemption_applicable_based_on_regime=data.get("tax_applicable_based_on_regime")
                #         get_each_doc.custom_regime=data.get("regime")
                        
                #         get_each_doc.insert()


                #         if data.get("is_arrear")==1:

                #             insert_doc = frappe.new_doc('Salary Component')
                #             insert_doc.name = data.get("salary_component")+("Arrear")
                #             insert_doc.salary_component = data.get("salary_component")+("Arrear")
                #             insert_doc.salary_component_abbr=data.get("abbr")+"Arrear"
                #             insert_doc.type=data.get("component_type")
                #             insert_doc.is_tax_applicable=1
                #             insert_doc.depends_on_payment_days=0
                #             insert_doc.round_to_the_nearest_integer=1
                #             insert_doc.do_not_include_in_total=0
                #             insert_doc.custom_is_part_of_gross_pay=1
                #             insert_doc.custom_is_part_of_ctc=0
                #             insert_doc.custom_is_arrear=1
                #             insert_doc.custom_tax_exemption_applicable_based_on_regime=1
                #             insert_doc.custom_regime="All"
                #             insert_doc.custom_component=data.get("salary_component")
                #             insert_doc.insert()

                #         fieldname = salary_component.lower().replace(" ", "_")

                #         # Create first Custom Field (Check field)
                #         custom_field_3 = frappe.new_doc('Custom Field')
                #         custom_field_3.dt = "Salary Structure Assignment"
                #         custom_field_3.label = salary_component
                #         custom_field_3.fieldname = fieldname
                #         custom_field_3.insert_after = "custom_tab_3"
                #         custom_field_3.fieldtype = "Check"
                #         custom_field_3.allow_on_submit = 1
                #         custom_field_3.insert()

                #         frappe.db.commit()

                #         custom_field_4 = frappe.new_doc('Custom Field')
                #         custom_field_4.dt = "Salary Structure Assignment"
                #         custom_field_4.label = f"{salary_component} Value"
                #         custom_field_4.fieldname = f"{fieldname}_value"
                #         custom_field_4.insert_after = fieldname
                #         custom_field_4.fieldtype = "Float"
                #         custom_field_4.allow_on_submit = 1
                #         custom_field_4.depends_on = f"eval:doc.{fieldname}==1" 
                #         custom_field_4.insert()

                #         frappe.db.commit() 


                #         update_doc=frappe.get_doc("Salary Component Library Item",data.get("salary_component"))
                #         update_doc.component_added=1
                #         update_doc.save()

                #         return{"message":"Added"}


                        


                       



                    


                                
                                

								




                

            



            





        





        # salary_component = data.get("salary_component")  
        # frappe.msgprint(f"Salary Component: {salary_component}")  
        # return {"message": f"Received salary component: {salary_component}"}
    # except Exception as e:
    #     frappe.log_error(f"Error in get_salary_component: {str(e)}")
    #     return {"error": str(e)}




import frappe
import json

@frappe.whitelist()
def get_salary_component(data, component, custom_field):

    frappe.msgprint(str(custom_field))
    # try:
    #     data = json.loads(data)  
    #     custom_field = json.loads(custom_field)  # Ensure custom_field is parsed as a list

    #     salary_component = data.get("salary_component")

    #     if len(component) > 0 and len(custom_field) > 0 and salary_component:
    #         for field in custom_field:
    #             # frappe.msgprint(str(field.get('doctype')))

    #             custom_field = frappe.new_doc('Custom Field')
    #             custom_field.dt = field.get('doctype')
    #             custom_field.label = field.get('label')
    #             custom_field.fieldname = field.get('field_name')
    #             custom_field.insert_after = field.get('insert_after')
    #             custom_field.fieldtype = field.get('field_type')
    #             custom_field.allow_on_submit = 1
    #             custom_field.allow_on_submit = 1
    #             custom_field.insert()








    # except Exception as e:
    #     frappe.msgprint(f"Error: {str(e)}")

