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
        payroll_period_end_date=get_payroll_period.end_date
        payroll_period_start_date=get_payroll_period.start_date

        salary_structure=None
        effective_from=None
        latest_structure_assignment=None
        latest_salary_structure = frappe.get_list('Salary Structure Assignment',
                        filters={'employee':employee,'docstatus':1,'custom_payroll_period':payroll_period},
                        fields=["*"],
                        order_by='from_date desc',
                        limit=1
                    )

        if len(latest_salary_structure)>0:
            salary_structure=latest_salary_structure[0].salary_structure
            latest_structure_assignment=latest_salary_structure[0].name
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
                        order_by='end_date desc'
                    )
            new_regime_month_count=get_all_salary_slip[0].custom_month_count if get_all_salary_slip else 0

            if len(get_all_salary_slip) == 0:
                new_salary_slip = make_salary_slip(
                    source_name=salary_structure,
                    employee=employee,
                    print_format='Salary Slip Standard',
                    posting_date=latest_salary_structure[0].from_date,
                    for_preview=1,
                    )

                for new_earning in new_salary_slip.earnings:
                    nps_component = frappe.get_doc("Salary Component", new_earning.salary_component)
                    if nps_component.component_type=="NPS" and nps_component.custom_component_sub_type=="Fixed":
                        start_date=effective_from
                        end_date=payroll_period_end_date
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
                            sub = get_sub_category[0]
                            get_declaration.append("declarations", {
                                "exemption_sub_category": sub.name,
                                "exemption_category": sub.exemption_category,
                                "max_amount": sub.max_amount,
                                "amount": total_nps
                            })

                            json_data = [
                                        {
                                            "id": sub.name,
                                            "sub_category": sub.name,
                                            "exemption_category": sub.exemption_category,
                                            "max_amount": sub.max_amount,
                                            "amount": total_nps,
                                            "value": total_nps
                                        }
                                    ]

                        get_declaration.custom_declaration_form_data = json.dumps(json_data)
                        get_declaration.custom_income_tax = selected_regime
                        get_declaration.save()

                        get_assignment_doc=frappe.get_doc("Salary Structure Assignment",latest_structure_assignment)
                        get_assignment_doc.income_tax_slab=selected_regime
                        get_assignment_doc.custom_tax_regime=regime
                        get_assignment_doc.save()

            else:
                previous_nps_amount=future_nps_amount=0
                for slip in get_all_salary_slip:
                    get_each_salary_slip=frappe.get_doc("Salary Slip",slip.name)
                    for each_slip_doc in get_each_salary_slip.earnings:
                        nps_component=frappe.get_doc("Salary Component",each_slip_doc.salary_component)
                        if nps_component.component_type=="NPS":
                            previous_nps_amount+=each_slip_doc.amount

                new_salary_slip = make_salary_slip(
                    source_name=salary_structure,
                    employee=employee,
                    print_format='Salary Slip Standard',
                    posting_date=latest_salary_structure[0].from_date,
                    for_preview=1,
                    )

                for new_earning in new_salary_slip.earnings:
                    nps_component = frappe.get_doc("Salary Component", new_earning.salary_component)
                    if nps_component.component_type=="NPS" and nps_component.custom_component_sub_type=="Fixed":
                        future_nps_amount+=new_earning.amount*new_regime_month_count

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
                    sub = get_sub_category[0]
                    get_declaration.append("declarations", {
                        "exemption_sub_category": sub.name,
                        "exemption_category": sub.exemption_category,
                        "max_amount": sub.max_amount,
                        "amount": (previous_nps_amount + future_nps_amount)
                    })

                    json_data = [
                                {
                                    "id": sub.name,
                                    "sub_category": sub.name,
                                    "exemption_category": sub.exemption_category,
                                    "max_amount": sub.max_amount,
                                    "amount": (previous_nps_amount + future_nps_amount),
                                    "value": (previous_nps_amount + future_nps_amount)
                                }
                            ]

                get_declaration.custom_declaration_form_data = json.dumps(json_data)
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

                get_assignment_doc = frappe.get_doc("Salary Structure Assignment", latest_structure_assignment)
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
                        order_by='end_date desc'
                    )


            old_regime_month_count=get_all_salary_slip[0].custom_month_count if get_all_salary_slip else 0

            if len(get_all_salary_slip) == 0:
                new_salary_slip = make_salary_slip(
                    source_name=salary_structure,
                    employee=employee,
                    print_format='Salary Slip Standard',
                    posting_date=latest_salary_structure[0].from_date,
                    for_preview=1,
                    )
                nps_component = 0
                epf_amount = 0
                pt_amount = 0

                for new_earning in new_salary_slip.earnings:
                    component = frappe.get_doc("Salary Component", new_earning.salary_component)
                    if component.component_type == "NPS" and component.custom_component_sub_type=="Fixed":
                        nps_component += new_earning.amount

                for deduction in new_salary_slip.deductions:
                    component = frappe.get_doc("Salary Component", deduction.salary_component)
                    if component.component_type == "Provident Fund" and component.custom_component_sub_type=="Fixed":
                        epf_amount += deduction.amount
                    if component.component_type == "Professional Tax" and component.custom_component_sub_type=="Fixed":
                        pt_amount += deduction.amount

                start_date=effective_from
                end_date=payroll_period_end_date

                if isinstance(start_date, str):
                    start = datetime.strptime(start_date, "%Y-%m-%d").date()
                else:
                    start = start_date

                if isinstance(end_date, str):
                    end = datetime.strptime(end_date, "%Y-%m-%d").date()
                else:
                    end = end_date

                num_months = (end.year - start.year) * 12 + (end.month - start.month)+1

                total_nps_sum=round(num_months*nps_component)
                total_epf_sum = min(round(num_months * epf_amount), 150000)
                total_pt_sum = round(round(num_months * pt_amount))


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
                        "sub_category": sub_category["name"],
                        "exemption_category": sub_category["exemption_category"],
                        "max_amount": sub_category["max_amount"],
                        "amount": total_nps_sum
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
                        "sub_category": sub_category["name"],
                        "exemption_category": sub_category["exemption_category"],
                        "max_amount": sub_category["max_amount"],
                        "amount": total_epf_sum
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
                        "sub_category": sub_category["name"],
                        "exemption_category": sub_category["exemption_category"],
                        "max_amount": sub_category["max_amount"],
                        "amount": total_pt_sum
                    })

                json_data = []

                for sub in sub_category_list:
                    get_declaration.append("declarations", {
                        "exemption_sub_category": sub["sub_category"],
                        "exemption_category": sub["exemption_category"],
                        "max_amount": sub["max_amount"],
                        "amount": sub["amount"]
                    })

                    json_data.append({
                        "id": sub["sub_category"],
                        "sub_category": sub["sub_category"],
                        "exemption_category": sub["exemption_category"],
                        "max_amount": sub["max_amount"],
                        "amount": sub["amount"],
                        "value": sub["amount"]
                    })

                get_declaration.custom_declaration_form_data = json.dumps(json_data)
                get_declaration.custom_income_tax = selected_regime
                get_declaration.save()

                get_assignment_doc = frappe.get_doc("Salary Structure Assignment", latest_structure_assignment)
                get_assignment_doc.income_tax_slab = selected_regime
                get_assignment_doc.custom_tax_regime=regime
                get_assignment_doc.save()



            else:
                current_nps_amount = future_nps_amount = 0
                current_epf_amount = future_epf_amount = 0
                current_pt_amount = future_pt_amount = 0

                for slip in get_all_salary_slip:
                    get_each_salary_slip = frappe.get_doc("Salary Slip", slip.name)

                    for earning in get_each_salary_slip.earnings:
                        get_earning_component = frappe.get_doc("Salary Component", earning.salary_component)
                        if get_earning_component.component_type == "NPS":
                            current_nps_amount+=earning.amount

                    for deduction in get_each_salary_slip.deductions:
                        get_deduction_component = frappe.get_doc("Salary Component", deduction.salary_component)
                        if get_deduction_component.component_type == "Provident Fund":
                            current_epf_amount+=deduction.amount
                        if get_deduction_component.component_type == "Professional Tax":
                            current_pt_amount+=deduction.amount



                new_salary_slip = make_salary_slip(
                    source_name=salary_structure,
                    employee=employee,
                    print_format='Salary Slip Standard',
                    posting_date=latest_salary_structure[0].from_date,
                    for_preview=1,
                )

                for new_earning in new_salary_slip.earnings:
                    new_earning_component = frappe.get_doc("Salary Component", new_earning.salary_component)
                    if new_earning_component.component_type == "NPS" and new_earning_component.custom_component_sub_type=="Fixed":
                        future_nps_amount+=new_earning.amount*old_regime_month_count

                for old_deduction in new_salary_slip.deductions:
                    new_deduction_component = frappe.get_doc("Salary Component", old_deduction.salary_component)
                    if new_deduction_component.component_type == "Provident Fund" and new_deduction_component.custom_component_sub_type=="Fixed":
                        future_epf_amount += old_deduction.amount*old_regime_month_count

                    if new_deduction_component.component_type == "Professional Tax" and new_deduction_component.custom_component_sub_type=="Fixed":
                        future_pt_amount+= old_deduction.amount*old_regime_month_count


                nps_amount_sum = (current_nps_amount + future_nps_amount) if (current_nps_amount or future_nps_amount) else 0
                epf_amount_sum = min(current_epf_amount + future_epf_amount, 150000) if (current_epf_amount or future_epf_amount) else 0
                pt_amount_sum = (current_pt_amount + future_pt_amount) if (current_pt_amount or future_pt_amount) else 0

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
                        "sub_category": sub_category["name"],
                        "exemption_category": sub_category["exemption_category"],
                        "max_amount": sub_category["max_amount"],
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
                        "sub_category": sub_category["name"],
                        "exemption_category": sub_category["exemption_category"],
                        "max_amount": sub_category["max_amount"],
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
                        "sub_category": sub_category["name"],
                        "exemption_category": sub_category["exemption_category"],
                        "max_amount": sub_category["max_amount"],
                        "amount": pt_amount_sum
                    })

                json_data = []

                for sub in sub_category_list:
                    get_declaration.append("declarations", {
                        "exemption_sub_category": sub["sub_category"],
                        "exemption_category": sub["exemption_category"],
                        "max_amount": sub["max_amount"],
                        "amount": sub["amount"]
                    })

                    json_data.append({
                        "id": sub["sub_category"],
                        "sub_category": sub["sub_category"],
                        "exemption_category": sub["exemption_category"],
                        "max_amount": sub["max_amount"],
                        "amount": sub["amount"],
                        "value": sub["amount"]
                    })

                get_declaration.custom_declaration_form_data = json.dumps(json_data)

                get_declaration.custom_income_tax = selected_regime
                get_declaration.save()

                get_assignment_doc = frappe.get_doc("Salary Structure Assignment", latest_structure_assignment)
                get_assignment_doc.income_tax_slab = selected_regime
                get_assignment_doc.custom_tax_regime=regime
                get_assignment_doc.save()
