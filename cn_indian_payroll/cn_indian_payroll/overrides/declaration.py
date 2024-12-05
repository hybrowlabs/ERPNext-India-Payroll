import frappe

from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip

from datetime import datetime, timedelta
from datetime import date

from frappe.utils import getdate
import json


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
                new_salary_slip = make_salary_slip(
                        source_name=ss_assignment.salary_structure,
                        employee=ss_assignment.employee,
                        print_format='Salary Slip Standard for CTC',  
                        posting_date=ss_assignment.from_date  
                    )
                for new_earning in new_salary_slip.deductions:
                        epf_component = frappe.get_doc("Salary Component", new_earning.salary_component)
                        if epf_component.component_type == "EPF":

                            epf_amount_year=new_earning.amount*12

                            epf_component_subcategory = frappe.get_list('Employee Tax Exemption Sub Category',
                                    filters={'custom_component_type':"EPF"},
                                    fields=['*'],
                                
                                )
                            if len(epf_component_subcategory)>0:
                                for i in epf_component_subcategory:
                                    
                                    component_array.append(i.name)
                                    
                                    max_amount.append(i.max_amount)

                                    if epf_amount_year>i.max_amount:
                                        amount.append(i.max_amount)
                                    else:
                                        amount.append(epf_amount_year)
                

            # NPS (National Pension System)
            if ss_assignment.custom_is_nps:
                new_salary_slip = make_salary_slip(
                        source_name=ss_assignment.salary_structure,
                        employee=ss_assignment.employee,
                        print_format='Salary Slip Standard for CTC',  
                        posting_date=ss_assignment.from_date  
                    )
                for new_earning in new_salary_slip.earnings:
                        nps_component = frappe.get_doc("Salary Component", new_earning.salary_component)
                        if nps_component.component_type == "NPS":

                            nps_amount_year=new_earning.amount*12


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
                new_salary_slip = make_salary_slip(
                        source_name=ss_assignment.salary_structure,
                        employee=ss_assignment.employee,
                        print_format='Salary Slip Standard for CTC',  
                        posting_date=ss_assignment.from_date  
                    )
                for new_earning in new_salary_slip.earnings:
                        nps_component = frappe.get_doc("Salary Component", new_earning.salary_component)
                        if nps_component.component_type == "NPS":

                            nps_amount_year=new_earning.amount*12

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
                    doc1.monthly_house_rent=0
                    doc1.salary_structure_hra=0
                    doc1.annual_hra_exemption=0
                    doc1.monthly_hra_exemption=0
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


@frappe.whitelist()

def choose_regime(doc_id, employee,payroll_period,company,regime):

    if employee:
        selected_regime = None
        get_income_tax = frappe.get_list('Income Tax Slab',
                        filters={'company':company,'docstatus':1,"disabled":0,"custom_select_regime":regime},
                        fields=["*"],
                        
                    )
        if len(get_income_tax)>0:
            selected_regime=get_income_tax[0].name

        get_payroll_period=frappe.get_doc("Payroll Period",payroll_period)
        payroll_end_date=get_payroll_period.end_date
        payroll_period_start_date=get_payroll_period.start_date

        salary_structure=None
        effective_from=None
        salary_slip_count=0
        latest_structure=None
        latest_salary_structure = frappe.get_list('Salary Structure Assignment',
                        filters={'employee':employee,'docstatus':1},
                        fields=["*"],
                        order_by='from_date desc',
                        limit=1
                    )

        if len(latest_salary_structure)>0:
            salary_structure=latest_salary_structure[0].salary_structure
            latest_structure=latest_salary_structure[0].name
            if latest_salary_structure[0].from_date<=payroll_period_start_date:
                effective_from=payroll_period_start_date
                
            else:
                effective_from=latest_salary_structure[0].from_date


        



        if regime=="New Regime":

            get_all_salary_slip = frappe.get_list(
                        'Salary Slip',
                        filters={
                            'employee': employee,
                            'custom_payroll_period': payroll_period,
                            'docstatus': ['in', [0, 1]]
                        },
                        fields=['*'],
                        order_by='posting_date desc'
                    )

            if len(get_all_salary_slip) == 0:
                
                new_salary_slip = make_salary_slip(
                    source_name=salary_structure,
                    employee=employee,
                    print_format='Salary Slip Standard for CTC',
                    # posting_date=latest_salary_structure[0].from_date
                    )

                   

                for new_earning in new_salary_slip.earnings:
                        nps_component = frappe.get_doc("Salary Component", new_earning.salary_component)
                        if nps_component.component_type=="NPS":

                            start_date=effective_from
                            end_date=payroll_end_date


                            if isinstance(start_date, str):
                                start = datetime.strptime(start_date, "%Y-%m-%d").date()
                            else:
                                start = start_date  

                            if isinstance(end_date, str):
                                end = datetime.strptime(end_date, "%Y-%m-%d").date()
                            else:
                                end = end_date  

                            num_months = (end.year - start.year) * 12 + (end.month - start.month)+1

                            
                            total_nps=round(num_months*new_earning.amount)


                            get_declaration = frappe.get_doc("Employee Tax Exemption Declaration", doc_id)

                            form_data = {'nineNumber': total_nps}
                            get_declaration.custom_declaration_form_data = json.dumps(form_data)

                            get_declaration.custom_income_tax = selected_regime

                            get_declaration.save()

                            get_assignment_doc=frappe.get_doc("Salary Structure Assignment",latest_structure)
                            get_assignment_doc.income_tax_slab=selected_regime
                            get_assignment_doc.save()
                           
            else:
                salary_slip_count=len(get_all_salary_slip)
                nps_amount=[]
                for j in get_all_salary_slip:
                    get_each_salary_slip=frappe.get_doc("Salary Slip",j.name)
                    for k in get_each_salary_slip.earnings:
                        get_nps_component=frappe.get_doc("Salary Component",k.salary_component)
                        if get_nps_component.component_type=="NPS":
                            nps_amount.append(k.amount)

                new_salary_slip = make_salary_slip(
                    source_name=salary_structure,
                    employee=employee,
                    print_format='Salary Slip Standard for CTC',
                    # posting_date=latest_salary_structure[0].from_date
                    )

                   

                for new_earning in new_salary_slip.earnings:
                    nps_component = frappe.get_doc("Salary Component", new_earning.salary_component)
                    if nps_component.component_type=="NPS":

                        nps_amount.append((12-salary_slip_count)*new_earning.amount)

                nps_amount_sum=sum(nps_amount)

                get_declaration = frappe.get_doc("Employee Tax Exemption Declaration", doc_id)

                form_data = {'nineNumber': nps_amount_sum}

                get_declaration.custom_declaration_form_data = json.dumps(form_data)

                get_declaration.custom_income_tax = selected_regime

                get_declaration.save()

                get_assignment_doc=frappe.get_doc("Salary Structure Assignment",latest_structure)
                get_assignment_doc.income_tax_slab=selected_regime
                get_assignment_doc.save()
                



















                # frappe.msgprint(str(nps_amount))
                # frappe.msgprint(str(12-salary_slip_count))

                # nps_amount.append((12-salary_slip_count)*)


















    # get_doc=frappe.get_doc("Employee Tax Exemption Declaration",doc_id)

    # # frappe.msgprint(str(get_doc.custom_income_tax))

    # get_doc.custom_income_tax="New Regime"

    # get_doc.save()

