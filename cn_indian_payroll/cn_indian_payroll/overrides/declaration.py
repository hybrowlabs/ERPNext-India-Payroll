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


#SWITCH REGIME IN DECLARATION FORM
@frappe.whitelist()
def choose_regime(doc_id, employee, payroll_period, company, regime):
    """
    This function selects the tax regime for an employee and updates tax-related fields
    based on the chosen regime in Employee Tax Exemption Declaration.
    """

    if not employee:
        frappe.throw("Employee is required")

    # Fetch selected tax regime from Income Tax Slab
    selected_regime = None
    income_tax_slab = frappe.get_list(
        "Income Tax Slab",
        filters={"company": company, "docstatus": 1, "disabled": 0, "custom_select_regime": regime},
        fields=["name"]
    )
    if income_tax_slab:
        selected_regime = income_tax_slab[0]["name"]

    # Initialize variables
    month_count = 0
    nps_amount, epf_amount, pt_amount = 0, 0, 0

    # Fetch Salary Structure Assignment
    ss_assignment = frappe.get_list(
        "Salary Structure Assignment",
        filters={"employee": employee, "docstatus": 1, "custom_payroll_period": payroll_period},
        fields=["name", "from_date", "salary_structure", "custom_payroll_period"],
        order_by="from_date desc"
    )

    if ss_assignment:
        first_assignment = ss_assignment[0]
        start_date = first_assignment["from_date"]
        first_assignment_id = first_assignment["name"]
        first_assignment_structure = first_assignment["salary_structure"]

        # Calculate month count based on payroll period
        if first_assignment["custom_payroll_period"]:
            payroll_period_doc = frappe.get_doc("Payroll Period", first_assignment["custom_payroll_period"])
            end_date = payroll_period_doc.end_date
            month_count = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1

        # Fetch Salary Slips
        salary_slips = frappe.get_list(
            "Salary Slip",
            filters={"employee": employee, "custom_payroll_period": first_assignment["custom_payroll_period"], "docstatus": ["in", [0, 1]]},
            fields=["name"],
            order_by="posting_date desc"
        )

        if not salary_slips:
            # Generate Salary Slip for preview
            new_salary_slip = make_salary_slip(
                source_name=first_assignment_structure,
                employee=employee,
                print_format="Salary Slip Standard for CTC",
                posting_date=start_date,
                for_preview=1
            )

            # Compute earnings and deductions
            for earning in new_salary_slip.earnings:
                component = frappe.get_doc("Salary Component", earning.salary_component)
                if component.component_type == "NPS":
                    nps_amount = month_count * earning.amount

            for deduction in new_salary_slip.deductions:
                ded_component = frappe.get_doc("Salary Component", deduction.salary_component)
                if ded_component.component_type == "EPF":
                    epf_amount = month_count * deduction.amount
                elif ded_component.component_type == "Professional Tax":
                    pt_amount = month_count * deduction.amount

        else:
            slip_count = len(salary_slips)

            # Accumulate amounts from existing salary slips
            for slip in salary_slips:
                salary_slip_doc = frappe.get_doc("Salary Slip", slip["name"])
                for earning in salary_slip_doc.earnings:
                    component = frappe.get_doc("Salary Component", earning.salary_component)
                    if component.component_type == "NPS":
                        nps_amount += earning.amount

                for deduction in salary_slip_doc.deductions:
                    ded_component = frappe.get_doc("Salary Component", deduction.salary_component)
                    if ded_component.component_type == "EPF":
                        epf_amount += deduction.amount
                    elif ded_component.component_type == "Professional Tax":
                        pt_amount += deduction.amount

            # Compute remaining months and add additional amount
            new_salary_slip = make_salary_slip(
                source_name=first_assignment_structure,
                employee=employee,
                print_format="Salary Slip Standard for CTC",
                posting_date=start_date,
                for_preview=1
            )

            for earning in new_salary_slip.earnings:
                component = frappe.get_doc("Salary Component", earning.salary_component)
                if component.component_type == "NPS":
                    nps_amount += (month_count - slip_count) * earning.amount

            for deduction in new_salary_slip.deductions:
                ded_component = frappe.get_doc("Salary Component", deduction.salary_component)
                if ded_component.component_type == "EPF":
                    epf_amount += (month_count - slip_count) * deduction.amount
                elif ded_component.component_type == "Professional Tax":
                    pt_amount += (month_count - slip_count) * deduction.amount

    # Update Employee Tax Exemption Declaration based on selected regime
    get_declaration = frappe.get_doc("Employee Tax Exemption Declaration", doc_id)

    if regime == "New Regime":
        form_data = {"nineNumber": nps_amount}

        get_declaration.custom_declaration_form_data = json.dumps(form_data)
        get_declaration.custom_income_tax = selected_regime
        get_declaration.monthly_house_rent = 0
        get_declaration.salary_structure_hra = 0
        get_declaration.custom_basic = 0
        get_declaration.custom_basic_as_per_salary_structure = 0
        get_declaration.annual_hra_exemption = 0
        get_declaration.monthly_hra_exemption = 0
        get_declaration.total_declared_amount = nps_amount
        get_declaration.total_exemption_amount = nps_amount
        get_declaration.save()

    elif regime == "Old Regime":
        form_data = {
            "nineNumber": round(nps_amount),
            "pfValue": min(round(epf_amount), 150000),
            "nineteenNumber": round(pt_amount)
        }

        get_declaration.custom_declaration_form_data = json.dumps(form_data)
        get_declaration.custom_income_tax = selected_regime
        get_declaration.total_exemption_amount = nps_amount + epf_amount + pt_amount
        get_declaration.save()

    # Update Salary Structure Assignment with selected tax regime
    frappe.db.set_value("Salary Structure Assignment", first_assignment_id, "income_tax_slab", selected_regime)

