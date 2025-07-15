import frappe

from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip

from datetime import datetime, timedelta
from datetime import date

from frappe.utils import getdate
import json

@frappe.whitelist()
def choose_regime(doc_id, employee,payroll_period,company,regime):
    if employee:
        selected_regime = None
        get_income_tax = frappe.get_list('Income Tax Slab',
                        filters={'company':company,'docstatus':1,"disabled":0,"custom_select_regime":regime},
                        fields=["*"],
                        order_by="effective_from desc",

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
                    posting_date=latest_salary_structure[0].from_date,
                    for_preview=1,
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


                        get_declaration.declarations = []

                        get_sub_category = frappe.get_list(
                            "Employee Tax Exemption Sub Category",
                            filters={
                                "is_active": 1,
                                "custom_component_type": "NPS"
                            },
                            fields=["name", "exemption_category", "max_amount"],
                            limit_page_length=1
                        )

                        if get_sub_category:
                            get_declaration.append("declarations", {
                                "exemption_sub_category": get_sub_category[0].name,
                                "exemption_category": get_sub_category[0].exemption_category,
                                "max_amount": get_sub_category[0].max_amount,
                                "amount": nps_amount_sum
                            })

                        form_data = {'nineNumber': total_nps}
                        get_declaration.custom_declaration_form_data = json.dumps(form_data)
                        get_declaration.custom_income_tax = selected_regime
                        get_declaration.save()
                        get_assignment_doc=frappe.get_doc("Salary Structure Assignment",latest_structure)
                        get_assignment_doc.income_tax_slab=selected_regime
                        get_assignment_doc.custom_tax_regime=regime
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
                    posting_date=latest_salary_structure[0].from_date,
                    for_preview=1,
                    )

                for new_earning in new_salary_slip.earnings:
                    nps_component = frappe.get_doc("Salary Component", new_earning.salary_component)
                    if nps_component.component_type=="NPS":
                        nps_amount.append((12-salary_slip_count)*new_earning.amount)
                nps_amount_sum=sum(nps_amount)
                get_declaration = frappe.get_doc("Employee Tax Exemption Declaration", doc_id)
                get_declaration.declarations = []
                get_sub_category = frappe.get_list(
                    "Employee Tax Exemption Sub Category",
                    filters={
                        "is_active": 1,
                        "custom_component_type": "NPS"
                    },
                    fields=["name", "exemption_category", "max_amount"],
                    limit_page_length=1
                )

                if get_sub_category:
                    get_declaration.append("declarations", {
                        "exemption_sub_category": get_sub_category[0].name,
                        "exemption_category": get_sub_category[0].exemption_category,
                        "max_amount": get_sub_category[0].max_amount,
                        "amount": nps_amount_sum
                    })

                form_data = {'nineNumber': nps_amount_sum}
                get_declaration.custom_declaration_form_data = json.dumps(form_data)
                get_declaration.custom_income_tax = selected_regime
                if get_declaration.monthly_house_rent:
                    get_declaration.get_declaration=None
                    get_declaration.salary_structure_hra=None
                    get_declaration.custom_basic=None
                    get_declaration.custom_basic_as_per_salary_structure=None
                    get_declaration.annual_hra_exemption=None
                    get_declaration.monthly_hra_exemption=None
                    get_declaration.custom_hra_breakup=[]
                get_declaration.save()
                get_assignment_doc = frappe.get_doc("Salary Structure Assignment", latest_structure)
                get_assignment_doc.income_tax_slab = selected_regime
                get_assignment_doc.custom_tax_regime=regime
                get_assignment_doc.save()





        if regime=="Old Regime":
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
                    posting_date=latest_salary_structure[0].from_date,
                    for_preview=1,
                    )


                nps_component = 0
                epf_amount = 0
                pt_amount = 0

                # Loop through earnings
                for new_earning in new_salary_slip.earnings:
                    component = frappe.get_doc("Salary Component", new_earning.salary_component)
                    if component.component_type == "NPS":
                        nps_component += new_earning.amount  # Add the earning amount

                # Loop through deductions
                for deduction in new_salary_slip.deductions:
                    component = frappe.get_doc("Salary Component", deduction.salary_component)
                    if component.component_type == "Provident Fund":
                        epf_amount += deduction.amount  # Add the deduction amount
                    if component.component_type == "Professional Tax":
                        pt_amount += deduction.amount  # Add the deduction amount


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


                total_nps=round(num_months*nps_component)
                total_epf = min(round(num_months * epf_amount), 150000)
                total_pt = min(round(num_months * pt_amount))




                get_declaration = frappe.get_doc("Employee Tax Exemption Declaration", doc_id)

                form_data = {
                    'nineNumber': round(total_nps),
                    'pfValue': round(total_epf),
                    'nineteenNumber': total_pt
                }

                get_declaration.custom_declaration_form_data = json.dumps(form_data)

                get_declaration.custom_income_tax = selected_regime

                get_declaration.save()

                get_assignment_doc = frappe.get_doc("Salary Structure Assignment", latest_structure)
                get_assignment_doc.income_tax_slab = selected_regime
                get_assignment_doc.custom_tax_regime=regime
                get_assignment_doc.save()



            else:
                salary_slip_count = len(get_all_salary_slip)
                nps_amount = []
                epf_amount = []
                pt_amount = []

                for slip in get_all_salary_slip:
                    get_each_salary_slip = frappe.get_doc("Salary Slip", slip.name)

                    for earning in get_each_salary_slip.earnings:
                        get_earning_component = frappe.get_doc("Salary Component", earning.salary_component)
                        if get_earning_component.component_type == "NPS":
                            nps_amount.append(earning.amount)

                    for deduction in get_each_salary_slip.deductions:
                        get_deduction_component = frappe.get_doc("Salary Component", deduction.salary_component)
                        if get_deduction_component.component_type == "Provident Fund":
                            epf_amount.append(deduction.amount)
                        if get_deduction_component.component_type == "Professional Tax":
                            pt_amount.append(deduction.amount)

                new_salary_slip = make_salary_slip(
                    source_name=salary_structure,
                    employee=employee,
                    print_format='Salary Slip Standard for CTC',
                    posting_date=latest_salary_structure[0].from_date,
                    for_preview=1,
                )

                for new_earning in new_salary_slip.earnings:
                    new_earning_component = frappe.get_doc("Salary Component", new_earning.salary_component)
                    if new_earning_component.component_type == "NPS":
                        nps_amount.append((12 - salary_slip_count) * new_earning.amount)

                for old_deduction in new_salary_slip.deductions:
                    new_deduction_component = frappe.get_doc("Salary Component", old_deduction.salary_component)
                    if new_deduction_component.component_type == "Provident Fund":
                        calculated_epf = (12 - salary_slip_count) * old_deduction.amount
                        epf_amount.append(calculated_epf)
                    if new_deduction_component.component_type == "Professional Tax":
                        calculated_pt = (12 - salary_slip_count) * old_deduction.amount
                        pt_amount.append(calculated_pt)

                nps_amount_sum = sum(nps_amount)
                epf_amount_sum = min(sum(epf_amount), 150000) if epf_amount else 0
                pt_amount_sum = sum(pt_amount)

                get_declaration = frappe.get_doc("Employee Tax Exemption Declaration", doc_id)
                get_declaration.declarations = []
                sub_category_list = []

                get_sub_category = frappe.get_list(
                    "Employee Tax Exemption Sub Category",
                    filters={
                        "is_active": 1,
                        "custom_component_type": "NPS"
                    },
                    fields=["name", "exemption_category", "max_amount"],
                    limit_page_length=1
                )

                if get_sub_category:
                    sub_category = get_sub_category[0]
                    sub_category_list.append({
                        "sub_category": sub_category.name,
                        "exemption_category": sub_category.exemption_category,
                        "max_amount": sub_category.max_amount,
                        "amount": nps_amount_sum
                    })



                get_sub_category = frappe.get_list(
                        "Employee Tax Exemption Sub Category",
                        filters={
                            "is_active": 1,
                            "custom_component_type": "Provident Fund"
                        },
                        fields=["name", "exemption_category", "max_amount"],
                        limit_page_length=1
                    )

                if get_sub_category:
                    sub_category = get_sub_category[0]
                    sub_category_list.append({
                        "sub_category": sub_category.name,
                        "exemption_category": sub_category.exemption_category,
                        "max_amount": sub_category.max_amount,
                        "amount": epf_amount_sum
                    })

                get_sub_category = frappe.get_list(
                        "Employee Tax Exemption Sub Category",
                        filters={
                            "is_active": 1,
                            "custom_component_type": "Professional Tax"
                        },
                        fields=["name", "exemption_category", "max_amount"],
                        limit_page_length=1
                    )

                if get_sub_category:
                    sub_category = get_sub_category[0]
                    sub_category_list.append({
                        "sub_category": sub_category.name,
                        "exemption_category": sub_category.exemption_category,
                        "max_amount": sub_category.max_amount,
                        "amount": pt_amount_sum
                    })



                form_data = {
                    'nineNumber': round(nps_amount_sum),
                    'pfValue': round(epf_amount_sum),
                    'nineteenNumber': round(pt_amount_sum)
                }

                for row in sub_category_list:
                    get_declaration.append("declarations", {
                        "exemption_sub_category": row["sub_category"],
                        "exemption_category": row["exemption_category"],
                        "max_amount": row["max_amount"],
                        "amount": row["amount"]
                    })

                get_declaration.custom_declaration_form_data = json.dumps(form_data)
                get_declaration.custom_income_tax = selected_regime
                get_declaration.save()

                get_assignment_doc = frappe.get_doc("Salary Structure Assignment", latest_structure)
                get_assignment_doc.income_tax_slab = selected_regime
                get_assignment_doc.save()
