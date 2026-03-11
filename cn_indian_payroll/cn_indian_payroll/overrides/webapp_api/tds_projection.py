

import frappe
from frappe.utils import getdate, add_months, flt
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip
from frappe.utils.pdf import get_pdf
from datetime import datetime
from frappe import _
import json
from dateutil.relativedelta import relativedelta
from frappe.utils import flt
from frappe.utils import cint
from frappe.utils import cstr
from frappe.utils import getdate
from hrms.payroll.doctype.salary_slip.salary_slip import eval_tax_slab_condition


# http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.tds_projection.get_annual_statement?employee=37004&company=PW&payroll_period=25-26

@frappe.whitelist()
def get_annual_statement(employee=None, payroll_period=None,company=None):

    target_employee = frappe.request.headers.get("X-Target-Employee-Id")
    if target_employee:
        employee = target_employee

    employee_list=frappe.get_doc("Employee",employee)
    employee_code=employee_list.name
    employee_name=employee_list.employee_name
    employee_department=employee_list.department
    employee_designation=employee_list.designation
    employment_type=employee_list.employment_type
    date_of_joinee=employee_list.date_of_joining

    pan=employee_list.pan_number
    # tax_regime=employee_list
    office_location=employee_list.branch
    pf=employee_list.provident_fund_account
    esic=employee_list.custom_esic_number

    # -------- Payroll Period -------- #
    period = frappe.db.get_value(
        "Payroll Period",
        payroll_period,
        ["start_date", "end_date"],
        as_dict=True
    )

    if not period:
        return {"status": "failed", "message": "Invalid Payroll Period"}

    fy_start = getdate(period.start_date)
    fy_end = getdate(period.end_date)

    # -------- Salary Slips -------- #
    slips = frappe.db.get_all(
        "Salary Slip",
        filters={
            "employee": employee,
            "custom_payroll_period": payroll_period,
            "docstatus": ["in", [0, 1]],
            "company": company,
        },
        fields=["name", "start_date"],
        order_by="start_date asc"
    )


    has_salary_slips = len(slips)




    slip_by_month = {}
    for s in slips:
        month = getdate(s.start_date).strftime("%B-%Y")
        slip_by_month[month] = s.name

    # -------- FY Months -------- #
    months = []

    doj = getdate(employee_list.date_of_joining)

    # Start month logic corrected
    if doj < fy_start:
        current = fy_start
    else:
        current = doj

    while current <= fy_end:
        months.append(current.strftime("%B-%Y"))
        current = add_months(current, 1)

    # -------- Last Salary Slip -------- #
    last_amount_map = {}
    if slips:
        last_slip = slips[-1]
        last_details = frappe.db.get_all(
            "Salary Detail",
            filters={"parent": last_slip.name},
            fields=["salary_component", "amount"]
        )
        last_amount_map = {d.salary_component: d.amount for d in last_details}

    # -------- Preview Slip (Future Months) -------- #
    ssa = frappe.get_list(
        "Salary Structure Assignment",
        filters={"employee": employee, "docstatus": 1,"company":company},
        fields=["name", "salary_structure", "from_date"],
        order_by="from_date desc",
        limit=1
    )



    preview_amount_map = {}
    if ssa:

        new_slip = make_salary_slip(
            source_name=ssa[0].salary_structure,
            employee=employee,
            posting_date=ssa[0].from_date,
            for_preview=1,
        )
        for e in new_slip.earnings:
            preview_amount_map[e.salary_component] = flt(e.amount)
        for d in new_slip.deductions:
            preview_amount_map[d.salary_component] = flt(d.amount)

    component_names = list(set(
        list(last_amount_map.keys()) + list(preview_amount_map.keys())
    ))






    components = frappe.db.get_all(
        "Salary Component",
        filters={"name": ["in", component_names]},
        fields=[
            "name", "type", "is_tax_applicable",
            "custom_is_reimbursement",
            "custom_is_offcycle_component",
            "custom_is_extra_payment",
            "custom_perquisite",
            "do_not_include_in_total",
            "custom_sequence",
            "component_type"
        ],
        order_by="custom_sequence asc"
    )



    earnings, deductions, reimbursements, offcycle = [], [], [], []

    allowed_deduction_types = [
        "Provident Fund", "ESIC", "Professional Tax", "LWF", "Income Tax"
    ]

   


    for comp in components:

        # Skip non-taxable normal earnings
        if comp.type == "Earning" and not comp.is_tax_applicable \
        and not comp.custom_is_reimbursement \
        and not comp.custom_is_offcycle_component:
            continue


        # Filter only allowed deductions
        if comp.type == "Deduction" and comp.component_type not in allowed_deduction_types:
            continue

        values = []

        for m in months:

            if m in slip_by_month:
                # Month has an actual salary slip
                amount = frappe.db.get_value(
                    "Salary Detail",
                    {
                        "parent": slip_by_month[m],
                        "salary_component": comp.name
                    },
                    "amount"
                ) or 0

            else:
                
                if comp.custom_is_offcycle_component or comp.custom_is_reimbursement:
                    amount = 0

                else:
                    # Normal earnings/deductions can use preview values
                    amount = preview_amount_map.get(comp.name, 0)

            values.append(flt(amount))


        rounded_values = [round(flt(v), 0) for v in values]

        row = {
            "name": comp.name,
            "values": rounded_values,
            "total": sum(rounded_values)
        }


        # -------- Proper Routing -------- #
        if comp.type == "Earning" and comp.custom_is_reimbursement:
            reimbursements.append(row)

        elif comp.type == "Earning" and comp.custom_is_offcycle_component:
            offcycle.append(row)

        elif comp.type == "Earning" and not comp.custom_perquisite:
            earnings.append(row)

        elif comp.type == "Deduction":
            deductions.append(row)

    # ------------------------------------------------------------------
    # EXTRA PAYMENT & PERQUISITE TOTAL
    # ------------------------------------------------------------------
    extra_payment_grand_total = 0
    total_perquisite_total = 0

    for row in earnings:
        comp = frappe.db.get_value(
            "Salary Component",
            row["name"],
            ["custom_is_extra_payment", "custom_perquisite"],
            as_dict=True
        )

        if comp:
            if comp.custom_is_extra_payment:
                extra_payment_grand_total += flt(row["total"])
            if comp.custom_perquisite:
                total_perquisite_total += flt(row["total"])

    # ------------------------------------------------------------------
    # SUMMARY CALCULATIONS
    # ------------------------------------------------------------------
    gross_earn_values = [sum(x["values"][i] for x in earnings) for i in range(len(months))]
    total_gross_earning=sum(gross_earn_values)
    earnings.append({
        "name": "Gross Earnings (A)",
        "values": gross_earn_values,
        "total": sum(gross_earn_values)
    })

    deduction_values = [sum(x["values"][i] for x in deductions) for i in range(len(months))]
    deductions.append({
        "name": "Total Deductions (B)",
        "values": deduction_values,
        "total": sum(deduction_values)
    })

    net_pay_values = [
        gross_earn_values[i] - deduction_values[i]
        for i in range(len(months))
    ]

    net_pay = {
        "name": "Net Pay (A-B)",
        "values": net_pay_values,
        "total": sum(net_pay_values)
    }

    reimbursement_values = [sum(x["values"][i] for x in reimbursements) for i in range(len(months))]
    reimbursements.append({
        "name": "Total Reimbursements (C)",
        "values": reimbursement_values,
        "total": sum(reimbursement_values)
    })


    reimbursements_total=sum(reimbursement_values)

    # ---------------- OFF CYCLE ---------------- #
    # offcycle_values = [sum(x["values"][i] for x in offcycle) for i in range(len(months))]

    # ---------------- OFF CYCLE ---------------- #

    offcycle_values = []

    for m in months:

        total = 0

        if m in slip_by_month:

            details = frappe.db.get_all(
                "Salary Detail",
                filters={
                    "parent": slip_by_month[m],
                    "parentfield": "earnings"
                },
                fields=["salary_component", "amount"]
            )

            for d in details:

                comp = frappe.db.get_value(
                    "Salary Component",
                    d.salary_component,
                    ["custom_is_offcycle_component"],
                    as_dict=True
                )

                if comp and comp.custom_is_offcycle_component:
                    total += flt(d.amount)

        offcycle_values.append(round(total, 0))



    offcycle.append({
        "name": "Total Offcycle (D)",
        "values": offcycle_values,
        "total": sum(offcycle_values)
    })

    total_off_cycle_payment=sum(offcycle_values)





    # ---- Off Cycle TDS (E) ---- #
    offcycle_tds_values = []
    for m in months:
        if m in slip_by_month:
            tds = frappe.db.get_value(
                "Salary Slip",
                slip_by_month[m],
                "custom_additional_tds_deducted_amount"
            ) or 0
        else:
            tds = 0
        offcycle_tds_values.append(flt(tds))

    offcycle.append({
        "name": "Off Cycle TDS Deduction (E)",
        "values": offcycle_tds_values,
        "total": sum(offcycle_tds_values)
    })

    # ---- Off Cycle Net Pay (D-E) ---- #
    offcycle_net_values = [
        offcycle_values[i] - offcycle_tds_values[i]
        for i in range(len(months))
    ]

    offcycle.append({
        "name": "Off Cycle Net Pay(D-E)",
        "values": offcycle_net_values,
        "total": sum(offcycle_net_values)
    })

    # ---- Non-Taxable Off Cycle (F) ---- #
    offcycle_nontax_values = []
    for m in months:
        # return months
        total = 0
        if m in slip_by_month:

            details = frappe.db.get_all(
                "Salary Detail",
                filters={"parent": slip_by_month[m], "parentfield": "earnings"},
                fields=["salary_component", "amount"]
            )

            for d in details:
                comp = frappe.db.get_value(
                    "Salary Component",
                    d.salary_component,
                    ["is_tax_applicable", "custom_is_offcycle_component"],
                    as_dict=True
                )


                if comp and not comp.is_tax_applicable and comp.custom_is_offcycle_component:
                    total += flt(d.amount)
        offcycle_nontax_values.append(total)



    perquisite_values = []
    for m in months:
        # return months
        perquisite_total = 0
        if m in slip_by_month:

            details = frappe.db.get_all(
                "Salary Detail",
                filters={"parent": slip_by_month[m], "parentfield": "earnings"},
                fields=["salary_component", "amount"]
            )

            for d in details:
                comp = frappe.db.get_value(
                    "Salary Component",
                    d.salary_component,
                    ["is_tax_applicable", "custom_perquisite"],
                    as_dict=True
                )


                if comp and comp.is_tax_applicable and comp.custom_perquisite:
                    perquisite_total += flt(d.amount)
        perquisite_values.append(perquisite_total)



    offcycle.append({
        "name": "Total Off Cycle Payments Non Taxable (F)",
        "values": offcycle_nontax_values,
        "total": sum(offcycle_nontax_values)
    })

    grand_total_values = []
    total_grand_total_payable=[]

    for i in range(len(months)):
        total_pay = (
            (gross_earn_values[i] - deduction_values[i] + reimbursement_values[i]) +
            (offcycle_values[i] - offcycle_tds_values[i] + offcycle_nontax_values[i])
        )
        grand_total_values.append(total_pay)

        total_grand_total_payable.append(gross_earn_values[i]+offcycle_values[i])

    offcycle.append({
        "name": "Grand Total Pay ((A-B)+C + (D-E)+F)",
        "values": grand_total_values,
        "total": sum(grand_total_values)
    })

    offcycle.append({
        "name": "Total Perquisites (G)",
        "values": perquisite_values,
        "total": sum(perquisite_values)
    })





    offcycle.append({
        "name": "Total Gross Salary (A+D+G)",
        "values": total_grand_total_payable,
        "total": sum(total_grand_total_payable)
    })

 

    return {
        "status": "success",
        "employee_code": employee_code,
        "employee_name": employee_name,
        "employee_department": employee_department,
        "employee_designation": employee_designation,
        "employment_type": employment_type,
        "date_of_joining": date_of_joinee,
        "pan": pan,
        "office_location": office_location,
        "pf": pf,
        "esic":esic,
        "months": months,
        "earnings": earnings,
        "deductions": deductions,
        "net_pay": [net_pay],
        "reimbursements": reimbursements,
        "offcycle_earnings": offcycle,
        "extra_payment_grand_total": round(extra_payment_grand_total) if extra_payment_grand_total else 0,
        "total_perquisite_total": round(total_perquisite_total) if total_perquisite_total else 0,
        "total_gross_earning":round(total_gross_earning) if total_gross_earning else 0,
        "total_off_cycle_payment":round(total_off_cycle_payment) if total_off_cycle_payment else 0,
        "reimbursements_total":round(reimbursements_total) if reimbursements_total else 0,

    }







# http://127.0.0.1:8002/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.tds_projection.tds_declaration_form?employee=PW0220&company=Pen Pencil&payroll_period=25-26&go_head_with_new_regime=0

@frappe.whitelist()
def tds_declaration_form(employee=None, company=None, payroll_period=None, go_head_with_new_regime=None):

    # ------------------ Validation ------------------
    if not employee or not company or not payroll_period:
        return {
            "status": "failed",
            "message": "Employee, Company and Payroll Period are required"
        }

    target_employee = frappe.request.headers.get("X-Target-Employee-Id")
    if target_employee:
        employee = target_employee


    payroll_setting=frappe.get_doc("Payroll Settings")
    if payroll_setting.custom_tax_calculation_based_on=="Use IT Declaration Values in Payroll Processing":
        month_count=0
        declaration = frappe.get_all(
            "Employee Tax Exemption Declaration",
            filters={
                "employee": employee,
                "company": company,
                "payroll_period": payroll_period
            },
            fields=["name"],
            limit=1
        )

        if not declaration:
            return {
                "status": "failed",
                "message": "No declaration form created for this payroll period"
            }

        declaration_doc = frappe.get_doc(
            "Employee Tax Exemption Declaration",
            declaration[0].name
        )

        declaration_id = declaration_doc.name
        current_tax_regime = declaration_doc.custom_tax_regime

        hra_exemption=[]


        if declaration_doc.custom_tax_regime=="Old Regime":

            monthly_hra=declaration_doc.monthly_house_rent if declaration_doc.monthly_house_rent else 0
            rented_in_metro_city=declaration_doc.rented_in_metro_city if declaration_doc.rented_in_metro_city else 0
            annual_hra_exemption=declaration_doc.annual_hra_exemption if declaration_doc.annual_hra_exemption else 0
            monthly_hra_exemption=declaration_doc.monthly_hra_exemption if declaration_doc.monthly_hra_exemption else 0


            hra_exemption.append({
                "monthly_hra": declaration_doc.monthly_house_rent or 0,
                "rented_in_metro_city": declaration_doc.rented_in_metro_city or 0,
                "annual_hra_exemption": declaration_doc.annual_hra_exemption or 0,
                "monthly_hra_exemption": declaration_doc.monthly_hra_exemption or 0,
                "start_date": declaration_doc.custom_start_date or "",
                "end_date": declaration_doc.custom_end_date or "",
                "pan": declaration_doc.custom_pan or "",
                "address_line1": declaration_doc.custom_address_title1 or "",
                "address_line2": declaration_doc.custom_address_title2 or "",
                "attach_reqd": 0,
                "attach_proof": "",
                "approval_needed":"No",
                "attach_link": "",
                "custom_name": declaration_doc.custom_name or "",
                "custom_proof_status": "",
                "custom_note": ""



            })




        # ------------------ DB → UI Flag ------------------
        current_flag = 1 if current_tax_regime == "New Regime" else 0

        # ------------------ Existing Declaration Map ------------------
        existing_declaration = []
        for d in declaration_doc.declarations:
            
            existing_declaration.append({
                "exemption_category": d.exemption_category,
                "exemption_sub_category": d.exemption_sub_category,
                "amount": d.amount,
                "max_amount": d.max_amount,
                "custom_attach": d.custom_attach,
                "custom_proof_status": d.custom_status if d.custom_status in ["Approved","Rejected","Pending"] else "",
                "custom_note": d.custom_note
            })

        existing_map = {
            d["exemption_sub_category"]: d for d in existing_declaration
        }

        # ------------------ Initial Load (No Toggle) ------------------
        if go_head_with_new_regime is None:
            return {
                "status": "success",
                "declaration_id": declaration_id,
                "current_tax_regime": current_tax_regime,
                "go_head_with_new_regime": current_flag
            }

        go_head_with_new_regime = int(go_head_with_new_regime)


        if go_head_with_new_regime == current_flag:


            if current_tax_regime == "Old Regime":

                NON_EDITABLE_COMPONENTS = [
                    "Professional Tax",
                    "Provident Fund",
                    "NPS"
                ]

                # ------------------ Fetch Section Category sequence ------------------
                section_sequence_map = {
                    d.name: d.sequence_number
                    for d in frappe.get_all(
                        "Section Category",
                        fields=["name", "sequence_number"]
                    )
                }

                # ------------------ Fetch Exemption Category meta ------------------
                category_meta_map = {
                    d.name: {
                        "custom_select_type": d.custom_select_type,
                        "max_amount": d.max_amount,
                        "custom_80d_variable": d.custom_80d_variable
                    }
                    for d in frappe.get_all(
                        "Employee Tax Exemption Category",
                        fields=["name", "custom_select_type", "max_amount","custom_80d_variable"]
                    )
                }

                # ------------------ Fetch Sub Categories ------------------
                records = frappe.get_all(
                    "Employee Tax Exemption Sub Category",
                    filters={
                        "is_active": 1,
                        "custom_component_type": ["!=", "LTA Reimbursement"]
                    },
                    fields=[
                        "exemption_category",
                        "name",
                        "max_amount",
                        "custom_component_type",
                        "custom_description",
                        "custom_sequence",
                        "custom_section_property",
                        "custom_approval_needed"
                    ],
                    order_by="custom_sequence asc"
                )

                # ------------------ Group by Category ------------------
                category_grouped = {}

                for row in records:
                    category = row.exemption_category
                    category_meta = category_meta_map.get(category, {})

                    if category not in category_grouped:
                        category_grouped[category] = {
                            "category_name": category,
                            "custom_select_type": category_meta.get("custom_select_type"),
                            "custom_80d_variable": category_meta.get("custom_80d_variable"),
                            "category_max_amount": category_meta.get("max_amount"),
                            "custom_section_property": row.custom_section_property,
                            
                            "items": []
                        }

                    declaration_row = existing_map.get(row.name)
                    editable = 0 if row.custom_component_type in NON_EDITABLE_COMPONENTS else 1

                    category_grouped[category]["items"].append({
                        "exemption_sub_category": row.name,
                        "component_type": row.custom_component_type,
                        "description": row.custom_description,
                        "editable": editable,
                        "amount": round(declaration_row["amount"]) if declaration_row else 0,
                        "max_amount": round(
                            declaration_row["max_amount"]
                            if declaration_row and declaration_row.get("max_amount") is not None
                            else row.max_amount
                        ),
                        "attach_reqd": 0,
                        "attach_proof": "",
                        "approval_needed": row.custom_approval_needed,
                        "attach_link": declaration_row["custom_attach"] if declaration_row else "",
                        "custom_proof_status": declaration_row["custom_proof_status"] if declaration_row else "",
                        "custom_note": declaration_row["custom_note"] if declaration_row else "",
                    })

                # ------------------ Group by Section Property (FIXED PART) ------------------
                section_grouped = {}

                for category_data in category_grouped.values():
                    section = category_data.get("custom_section_property")
                    if not section:
                        continue

                    if section not in section_grouped:
                        section_grouped[section] = {
                            "custom_section_property": section,
                            "sequence_number": section_sequence_map.get(section, 999),
                            "exemption_category": []
                        }

                    category_name = category_data["category_name"]
                    meta = category_meta_map.get(category_name, {})

                    section_grouped[section]["exemption_category"].append({
                        "category_name": category_name,
                        "custom_select_type": meta.get("custom_select_type"),
                        "max_amount": meta.get("max_amount"),
                        "custom_80d_variable": meta.get("custom_80d_variable"),
                        "items": category_data["items"]
                    })

                # ------------------ Sort Sections ------------------
                final_categories = sorted(
                    section_grouped.values(),
                    key=lambda x: x["sequence_number"]
                )

                # ------------------ LTA Reimbursement Logic (unchanged) ------------------
                records = frappe.get_all(
                    "Employee Tax Exemption Sub Category",
                    filters={"is_active": 1, "custom_component_type": "LTA Reimbursement"},
                    fields=[
                        "exemption_category",
                        "name",
                        "max_amount",
                        "custom_component_type",
                        "custom_description",
                        "custom_sequence",
                        "custom_section_property",
                        "custom_approval_needed"
                    ],
                    order_by="custom_sequence asc"
                )

                grouped = {}

                for row in records:
                    category = row.exemption_category
                    if category not in grouped:
                        grouped[category] = []

                    declaration_row = existing_map.get(row.name)
                    editable = 0 if row.custom_component_type in NON_EDITABLE_COMPONENTS else 1

                    grouped[category].append({
                        "exemption_sub_category": row.name,
                        "component_type": row.custom_component_type,
                        "description": row.custom_description,
                        "editable": editable,
                        "amount": round(declaration_row["amount"]) if declaration_row else 0,
                        "max_amount": round(
                            declaration_row["max_amount"]
                            if declaration_row and declaration_row.get("max_amount") is not None
                            else row.max_amount
                        ),
                        "attach_reqd": 0,
                        "attach_proof": "",
                        "approval_needed":row.custom_approval_needed,
                        "attach_link": declaration_row["custom_attach"] if declaration_row else "",
                        "custom_proof_status": declaration_row["custom_proof_status"] if declaration_row else "",

                        "custom_note": declaration_row["custom_note"] if declaration_row else "",

                    })

                final_list = []
                for category, items in grouped.items():
                    final_list.append({
                        "category_name": category,
                        "items": items
                    })

                hra_exemption.append({"items": final_list})

                return {
                    "status": "success",
                    "declaration_id": declaration_id,
                    "doctype":"Employee Tax Exemption Declaration",
                    "proof_id":"",
                    "current_tax_regime": current_tax_regime,
                    "go_head_with_new_regime": current_flag,
                    "hra_exemption": hra_exemption,
                    "categories": final_categories
                }


            elif current_tax_regime == "New Regime":

                # ------------------ Fetch Section Category sequence ------------------
                section_sequence_map = {
                    d.name: d.sequence_number
                    for d in frappe.get_all(
                        "Section Category",
                        fields=["name", "sequence_number"]
                    )
                }

                # ------------------ Fetch Exemption Category meta ------------------
                category_meta_map = {
                    d.name: {
                        "custom_select_type": d.custom_select_type,
                        "max_amount": d.max_amount
                    }
                    for d in frappe.get_all(
                        "Employee Tax Exemption Category",
                        fields=["name", "custom_select_type", "max_amount"]
                    )
                }

                # ------------------ Fetch NPS Sub Categories ------------------
                records = frappe.get_all(
                    "Employee Tax Exemption Sub Category",
                    filters={
                        "is_active": 1,
                        "custom_component_type": "NPS"
                    },
                    fields=[
                        "exemption_category",
                        "name",
                        "max_amount",
                        "custom_component_type",
                        "custom_description",
                        "custom_sequence",
                        "custom_section_property"
                    ],
                    order_by="custom_sequence asc"
                )

                # ------------------ Group by Category ------------------
                category_grouped = {}

                for row in records:
                    category = row.exemption_category
                    category_meta = category_meta_map.get(category, {})

                    if category not in category_grouped:
                        category_grouped[category] = {
                            "category_name": category,
                            "custom_select_type": category_meta.get("custom_select_type"),
                            "category_max_amount": category_meta.get("max_amount"),
                            "custom_section_property": row.custom_section_property,
                            "items": []
                        }

                    declaration_row = existing_map.get(row.name)

                    category_grouped[category]["items"].append({
                        "exemption_sub_category": row.name,
                        "component_type": row.custom_component_type,
                        "description": row.custom_description,
                        "editable": 0,  # NPS is always non-editable
                        "amount": round(declaration_row["amount"]) if declaration_row else 0,
                        "max_amount": round(
                            declaration_row["max_amount"]
                            if declaration_row and declaration_row.get("max_amount") is not None
                            else row.max_amount
                        ),
                        "attach_reqd": 0,
                        "attach_proof": "",
                        "custom_proof_status": "",
                        "custom_note": "",
                    })

                # ------------------ Group by Section Property ------------------
                section_grouped = {}

                for category_data in category_grouped.values():
                    section = category_data.get("custom_section_property")
                    if not section:
                        continue

                    if section not in section_grouped:
                        section_grouped[section] = {
                            "custom_section_property": section,
                            "sequence_number": section_sequence_map.get(section, 999),
                            "exemption_category": []
                        }

                    category_name = category_data["category_name"]
                    meta = category_meta_map.get(category_name, {})

                    section_grouped[section]["exemption_category"].append({
                        "category_name": category_name,
                        "custom_select_type": meta.get("custom_select_type"),
                        "max_amount": meta.get("max_amount"),
                        "items": category_data["items"]
                    })

                # ------------------ Sort Sections by sequence ------------------
                final_categories = sorted(
                    section_grouped.values(),
                    key=lambda x: x["sequence_number"]
                )

                return {
                    "status": "success",
                    "declaration_id": declaration_id,
                    "doctype":"Employee Tax Exemption Declaration",
                    "proof_id":"",
                    "current_tax_regime": current_tax_regime,
                    "go_head_with_new_regime": current_flag,
                    "categories": final_categories
                }









            # ------------------ Old → New ------------------
        if go_head_with_new_regime == 1 and current_flag == 0:

            nps_amount_ctc = 0
            num_months = 0
            choosed_tax_regime = None

            # ---------------- Latest Tax Slab (NEW REGIME) ----------------
            latest_tax_slab = frappe.get_list(
                "Income Tax Slab",
                filters={
                    "company": company,
                    "docstatus": 1,
                    "disabled": 0,
                    "custom_select_regime": "New Regime",
                },
                fields=["name", "custom_select_regime", "standard_tax_exemption_amount"],
                order_by="effective_from DESC",
                limit=1,
            )

            latest_tax_slab_name = None
            if latest_tax_slab:
                latest_tax_slab_name = latest_tax_slab[0].name
                choosed_tax_regime = "New Regime"

            # ---------------- Salary Structure Assignment ----------------
            salary_structure_assignments = frappe.get_list(
                "Salary Structure Assignment",
                filters={
                    "employee": employee,
                    "docstatus": 1,
                    "custom_payroll_period": payroll_period,
                    "company": company,
                },
                fields=["*"],
                order_by="from_date desc",
                limit=1
            )

            if not salary_structure_assignments:
                return {
                    "status": "success",
                    "message": "No salary structure assignment found",
                    "categories": []
                }

            assignment = salary_structure_assignments[0]

            employee_doc = frappe.get_doc("Employee", employee)
            payroll_period_doc = frappe.get_doc("Payroll Period", payroll_period)

            # ---------------- Date Calculations ----------------
            start_candidates = [
                assignment.from_date,
                payroll_period_doc.start_date,
                employee_doc.date_of_joining,
            ]

            start = max(getdate(d) for d in start_candidates if d)
            end = getdate(payroll_period_doc.end_date)

            num_months = (end.year - start.year) * 12 + (end.month - start.month) + 1

            # ---------------- Salary Slips ----------------
            salary_slips = frappe.get_list(
                "Salary Slip",
                filters={
                    "employee": employee,
                    "custom_payroll_period": payroll_period,
                    "docstatus": ["in", [0, 1]],
                    "company": company,
                },
                fields=["name", "custom_month_count"],
                order_by="end_date desc",
            )

            # ---------------- CASE 1: No Salary Slips ----------------
            if not salary_slips:

                salary_slip_preview = make_salary_slip(
                    source_name=assignment.salary_structure,
                    employee=employee,
                    posting_date=assignment.from_date,
                    for_preview=1,
                )

                if salary_slip_preview:
                    for earning in salary_slip_preview.earnings:
                        component = frappe.get_doc("Salary Component", earning.salary_component)

                        if (
                            component.is_tax_applicable
                            and component.custom_tax_exemption_applicable_based_on_regime
                            and component.custom_regime == "All"
                            and component.custom_component_sub_type == "Fixed"
                            and component.component_type == "NPS"
                        ):
                            nps_amount_ctc += earning.amount * num_months

            # ---------------- CASE 2: Salary Slips Exist ----------------
            else:
                month_count = salary_slips[0].custom_month_count or 0

                for slip in salary_slips:
                    slip_doc = frappe.get_doc("Salary Slip", slip.name)

                    for earning in slip_doc.earnings:
                        component = frappe.get_doc("Salary Component", earning.salary_component)

                        if (
                            component.is_tax_applicable
                            and component.custom_tax_exemption_applicable_based_on_regime
                            and component.custom_regime == "All"
                            and component.component_type == "NPS"
                        ):
                            nps_amount_ctc += earning.amount

                # Preview remaining months
                salary_slip_preview = make_salary_slip(
                    source_name=assignment.salary_structure,
                    employee=employee,
                    posting_date=assignment.from_date,
                    for_preview=1,
                )

                if salary_slip_preview:
                    for earning in salary_slip_preview.earnings:
                        component = frappe.get_doc("Salary Component", earning.salary_component)

                        if (
                            component.is_tax_applicable
                            and component.custom_tax_exemption_applicable_based_on_regime
                            and component.custom_regime == "All"
                            and component.custom_component_sub_type == "Fixed"
                            and component.component_type == "NPS"
                        ):
                            nps_amount_ctc += earning.amount * month_count




            section_sequence_map = {
                d.name: d.sequence_number
                for d in frappe.get_all(
                    "Section Category",
                    fields=["name", "sequence_number"]
                )
            }

            # ------------------ Fetch Exemption Category meta ------------------
            category_meta_map = {
                d.name: {
                    "custom_select_type": d.custom_select_type,
                    "max_amount": d.max_amount
                }
                for d in frappe.get_all(
                    "Employee Tax Exemption Category",
                    fields=["name", "custom_select_type", "max_amount"]
                )
            }

            # ------------------ Fetch NPS Sub Categories ------------------
            records = frappe.get_all(
                "Employee Tax Exemption Sub Category",
                filters={
                    "is_active": 1,
                    "custom_component_type": "NPS"
                },
                fields=[
                    "exemption_category",
                    "name",
                    "max_amount",
                    "custom_component_type",
                    "custom_description",
                    "custom_sequence",
                    "custom_section_property"
                ],
                order_by="custom_sequence asc"
            )

            # ------------------ Group by Category ------------------
            category_grouped = {}

            for row in records:
                category = row.exemption_category
                category_meta = category_meta_map.get(category, {})

                if category not in category_grouped:
                    category_grouped[category] = {
                        "category_name": category,
                        "custom_select_type": category_meta.get("custom_select_type"),
                        "category_max_amount": category_meta.get("max_amount"),
                        "custom_section_property": row.custom_section_property,
                        "items": []
                    }

                declaration_row = existing_map.get(row.name)

                category_grouped[category]["items"].append({
                    "exemption_sub_category": row.name,
                    "component_type": row.custom_component_type,
                    "description": row.custom_description,
                    "editable": 0,  # NPS is always non-editable
                    "amount": round(declaration_row["amount"]) if declaration_row else 0,
                    "max_amount": round(
                        declaration_row["max_amount"]
                        if declaration_row and declaration_row.get("max_amount") is not None
                        else row.max_amount
                    ),
                    "attach_reqd": 0,
                    "attach_proof": "",
                    "custom_proof_status": "",
                    "custom_note": "",
                })

            # ------------------ Group by Section Property ------------------
            section_grouped = {}

            for category_data in category_grouped.values():
                section = category_data.get("custom_section_property")
                if not section:
                    continue

                if section not in section_grouped:
                    section_grouped[section] = {
                        "custom_section_property": section,
                        "sequence_number": section_sequence_map.get(section, 999),
                        "exemption_category": []
                    }

                category_name = category_data["category_name"]
                meta = category_meta_map.get(category_name, {})

                section_grouped[section]["exemption_category"].append({
                    "category_name": category_name,
                    "custom_select_type": meta.get("custom_select_type"),
                    "max_amount": meta.get("max_amount"),
                    "items": category_data["items"]
                })

            # ------------------ Sort Sections by sequence ------------------
            final_categories = sorted(
                section_grouped.values(),
                key=lambda x: x["sequence_number"]
            )


            return {
                "status": "success",
                "doctype":"Employee Tax Exemption Declaration",
                "proof_id":"",
                "declaration_id": declaration_id,
                "current_tax_regime": current_tax_regime,
                "go_head_with_new_regime": current_flag,
                "categories": final_categories
            }





        # ------------------ New  to OLD------------------

        if go_head_with_new_regime == 0 and current_flag == 1:

            nps_amount_ctc = 0
            pf_amount_ctc = 0
            pt_amount_ctc = 0
            lta_amount_ctc = 0




            hra_exemption.append({
                "monthly_hra": None,
                "rented_in_metro_city": None,
                "annual_hra_exemption": None,
                "monthly_hra_exemption": None,
                "start_date": None,
                "end_date": None,
                "pan": None,
                "address_line1": None,
                "address_line2": None,
                "attach_reqd": 0,
                "attach_proof": "",
                "custom_name": None
            })


            assignment = frappe.get_list(
                "Salary Structure Assignment",
                filters={
                    "employee": employee,
                    "company": company,
                    "custom_payroll_period": payroll_period,
                    "docstatus": 1,
                },
                fields=["salary_structure", "from_date"],
                order_by="from_date desc",
                limit=1,
            )

            if not assignment:
                return {
                    "status": "success",
                    "message": "No salary structure assignment found",
                    "categories": [],
                }

            assignment = assignment[0]

            employee_doc = frappe.get_doc("Employee", employee)
            payroll_doc = frappe.get_doc("Payroll Period", payroll_period)


            start = max(
                getdate(d)
                for d in [
                    assignment.from_date,
                    payroll_doc.start_date,
                    employee_doc.date_of_joining,
                ]
                if d
            )
            end = getdate(payroll_doc.end_date)
            total_months = (end.year - start.year) * 12 + (end.month - start.month) + 1


            salary_slips = frappe.get_list(
                "Salary Slip",
                filters={
                    "employee": employee,
                    "company": company,
                    "custom_payroll_period": payroll_period,
                    "docstatus": ["in", [0, 1]],
                },
                fields=["name", "custom_month_count"],
                order_by="end_date desc",
            )


            if not salary_slips:

                preview = make_salary_slip(
                    source_name=assignment.salary_structure,
                    employee=employee,
                    posting_date=assignment.from_date,
                    for_preview=1,
                )

                for row in preview.earnings:
                    component = frappe.get_doc("Salary Component", row.salary_component)

                    if (
                        component.custom_tax_exemption_applicable_based_on_regime
                        and component.custom_regime == "All"
                        and component.custom_component_sub_type == "Fixed"
                    ):
                        if component.component_type == "NPS":
                            nps_amount_ctc += row.amount * total_months
                        elif component.component_type == "LTA Reimbursement":
                            lta_amount_ctc += row.amount * total_months

                for row in preview.deductions:
                    component = frappe.get_doc("Salary Component", row.salary_component)

                    if component.component_type == "Provident Fund":
                        pf_amount_ctc += row.amount * total_months
                    elif component.component_type == "Professional Tax":
                        pt_amount_ctc += row.amount * total_months


            else:
                processed_months = salary_slips[0].custom_month_count or 0

                for slip in salary_slips:
                    slip_doc = frappe.get_doc("Salary Slip", slip.name)

                    for row in slip_doc.earnings:
                        component = frappe.get_doc("Salary Component", row.salary_component)

                        if (
                            component.custom_tax_exemption_applicable_based_on_regime
                            and component.custom_regime == "All"
                        ):
                            if component.component_type == "NPS":
                                nps_amount_ctc += row.amount
                            elif component.component_type == "LTA Reimbursement":
                                lta_amount_ctc += row.amount

                    for row in slip_doc.deductions:
                        component = frappe.get_doc("Salary Component", row.salary_component)


                        if component.component_type == "Provident Fund":
                            pf_amount_ctc += row.amount
                        elif component.component_type == "Professional Tax":
                            pt_amount_ctc += row.amount


                # ---- Remaining months preview (THIS WAS MISSING) ----
                if processed_months > 0:
                    preview = make_salary_slip(
                        source_name=assignment.salary_structure,
                        employee=employee,
                        posting_date=assignment.from_date,
                        for_preview=1,
                    )


                    for row in preview.earnings:
                        component = frappe.get_doc("Salary Component", row.salary_component)

                        if (
                            component.custom_tax_exemption_applicable_based_on_regime
                            and component.custom_regime == "All"
                            and component.custom_component_sub_type == "Fixed"
                        ):
                            if component.component_type == "NPS":
                                nps_amount_ctc += row.amount * processed_months
                            elif component.component_type == "LTA Reimbursement":
                                lta_amount_ctc += row.amount * processed_months

                    for row in preview.deductions:
                        component = frappe.get_doc("Salary Component", row.salary_component)

                        if component.custom_component_sub_type == "Fixed":
                            if component.component_type == "Provident Fund":
                                pf_amount_ctc += row.amount * processed_months
                            elif component.component_type == "Professional Tax":
                                pt_amount_ctc += row.amount * processed_months




            SYSTEM_COMPONENT_MAP = {
                "NPS": round(nps_amount_ctc, 2),
                "Provident Fund": round(pf_amount_ctc, 2),
                "Professional Tax": round(pt_amount_ctc, 2),
            }

            NON_EDITABLE_COMPONENTS = set(SYSTEM_COMPONENT_MAP.keys())

            # ------------------ Fetch Section Category sequence ------------------
            section_sequence_map = {
                d.name: d.sequence_number
                for d in frappe.get_all(
                    "Section Category",
                    fields=["name", "sequence_number"]
                )
            }

            # ------------------ Fetch Exemption Category meta ------------------
            category_meta_map = {
                d.name: {
                    "custom_select_type": d.custom_select_type,
                    "max_amount": d.max_amount,
                    "custom_80d_variable": d.custom_80d_variable
                }
                for d in frappe.get_all(
                    "Employee Tax Exemption Category",
                    fields=["name", "custom_select_type", "max_amount","custom_80d_variable"]
                )
            }

            # ------------------ Fetch Sub Categories (NON-LTA) ------------------
            records = frappe.get_all(
                "Employee Tax Exemption Sub Category",
                filters={
                    "is_active": 1,
                    "custom_component_type": ["!=", "LTA Reimbursement"]
                },
                fields=[
                    "exemption_category",
                    "name",
                    "max_amount",
                    "custom_component_type",
                    "custom_description",
                    "custom_sequence",
                    "custom_section_property",
                    "custom_approval_needed"
                ],
                order_by="custom_sequence asc"
            )

            # ------------------ Group by Category ------------------
            category_grouped = {}

            for row in records:
                category = row.exemption_category
                category_meta = category_meta_map.get(category, {})

                if category not in category_grouped:
                    category_grouped[category] = {
                        "category_name": category,
                        "custom_select_type": category_meta.get("custom_select_type"),
                        "custom_80d_variable": category_meta.get("custom_80d_variable"),
                        "category_max_amount": category_meta.get("max_amount"),
                        "custom_section_property": row.custom_section_property,
                        "items": []
                    }

                declaration_row = existing_map.get(row.name)

                # ------------------ SYSTEM vs USER logic ------------------
                if row.custom_component_type in SYSTEM_COMPONENT_MAP:
                    amount = SYSTEM_COMPONENT_MAP[row.custom_component_type]
                    max_amount = amount
                    editable = 0
                else:
                    amount = declaration_row["amount"] if declaration_row else 0
                    max_amount = (
                        declaration_row.get("max_amount")
                        if declaration_row and declaration_row.get("max_amount") is not None
                        else row.max_amount
                    )
                    editable = 1

                category_grouped[category]["items"].append({
                    "exemption_sub_category": row.name,
                    "component_type": row.custom_component_type,
                    "description": row.custom_description,
                    "editable": editable,
                    "amount": round(amount),
                    "max_amount": round(max_amount),
                    "attach_reqd": 0,
                    "attach_proof": "",
                    "approval_needed":row.custom_approval_needed,
                    "attach_link": declaration_row["custom_attach"] if declaration_row else "",
                    "custom_proof_status": "",
                    "custom_note": "",
                })

            # ------------------ Group by Section Property ------------------
            section_grouped = {}

            for category_data in category_grouped.values():
                section = category_data.get("custom_section_property")
                if not section:
                    continue

                if section not in section_grouped:
                    section_grouped[section] = {
                        "custom_section_property": section,
                        "sequence_number": section_sequence_map.get(section, 999),
                        "exemption_category": []
                    }

                category_name = category_data["category_name"]
                meta = category_meta_map.get(category_name, {})

                section_grouped[section]["exemption_category"].append({
                    "category_name": category_name,
                    "custom_select_type": meta.get("custom_select_type"),
                    "custom_80d_variable": meta.get("custom_80d_variable"),
                    "max_amount": meta.get("max_amount"),
                    "items": category_data["items"]
                })

            # ------------------ Sort Sections ------------------
            final_categories = sorted(
                section_grouped.values(),
                key=lambda x: x["sequence_number"]
            )

            # ------------------ LTA Reimbursement (UNCHANGED) ------------------
            records = frappe.get_all(
                "Employee Tax Exemption Sub Category",
                filters={"is_active": 1, "custom_component_type": "LTA Reimbursement"},
                fields=[
                    "exemption_category",
                    "name",
                    "max_amount",
                    "custom_component_type",
                    "custom_description",
                    "custom_sequence",
                    "custom_section_property",
                    "custom_approval_needed"
                ],
                order_by="custom_sequence asc"
            )

            grouped = {}

            for row in records:
                category = row.exemption_category
                if category not in grouped:
                    grouped[category] = []

                declaration_row = existing_map.get(row.name)

                grouped[category].append({
                    "exemption_sub_category": row.name,
                    "component_type": row.custom_component_type,
                    "description": row.custom_description,
                    "editable": 1,
                    "amount": round(declaration_row["amount"]) if declaration_row else 0,
                    "max_amount": round(
                        declaration_row["max_amount"]
                        if declaration_row and declaration_row.get("max_amount") is not None
                        else row.max_amount
                    ),
                    "attach_reqd": 0,
                    "attach_proof": "",
                    "approval_needed":row.custom_approval_needed,
                    "attach_link": declaration_row["custom_attach"] if declaration_row else "",
                    "custom_proof_status": "",
                    "custom_note": "",
                })

            hra_exemption.append({
                "items": [
                    {
                        "category_name": category,
                        "items": items
                    }
                    for category, items in grouped.items()
                ]
            })

            return {
                "status": "success",
                "declaration_id": declaration_id,
                "proof_id":"",
                "doctype":"Employee Tax Exemption Declaration",
                "current_tax_regime": "Old Regime",
                "go_head_with_new_regime": 0,
                "message": "User switched from New Regime to Old Regime",
                "categories": final_categories,
                "hra_exemption": hra_exemption,
            }





    elif payroll_setting.custom_tax_calculation_based_on=="Use POI Approved Values in Payroll Processing":
        month_count=0

        declaration = frappe.get_all(
            "Employee Tax Exemption Declaration",
            filters={
                "employee": employee,
                "company": company,
                "payroll_period": payroll_period
            },
            fields=["name"],
            limit=1
        )

        if not declaration:
            return {
                "status": "failed",
                "message": "No declaration form created for this payroll period"
            }

        declaration_doc = frappe.get_doc(
            "Employee Tax Exemption Declaration",
            declaration[0].name
        )

        declaration_id = declaration_doc.name

        proof_submission = frappe.get_all(
            "Employee Tax Exemption Proof Submission",
            filters={
                "employee": employee,
                "company": company,
                "payroll_period": payroll_period,
                "docstatus": ["in", [0, 1]]
            },
            fields=["name"],
            limit=1
        )
        if proof_submission:

            proof_doc = frappe.get_doc(
                "Employee Tax Exemption Proof Submission",
                proof_submission[0].name
            )

            proof_id = proof_doc.name

            current_tax_regime = proof_doc.custom_tax_regime

            hra_exemption=[]


            if proof_doc.custom_tax_regime=="Old Regime":

                monthly_hra=proof_doc.house_rent_payment_amount if proof_doc.house_rent_payment_amount else 0
                rented_in_metro_city=proof_doc.rented_in_metro_city if proof_doc.rented_in_metro_city else 0
                annual_hra_exemption=proof_doc.custom_annual_eligible_amount if proof_doc.custom_annual_eligible_amount else 0
                monthly_hra_exemption=proof_doc.monthly_hra_exemption if proof_doc.monthly_hra_exemption else 0


                hra_exemption.append({
                    "monthly_hra": proof_doc.house_rent_payment_amount or 0,
                    "rented_in_metro_city": proof_doc.rented_in_metro_city or 0,
                    "annual_hra_exemption": proof_doc.custom_annual_eligible_amount or 0,
                    "monthly_hra_exemption": proof_doc.monthly_hra_exemption or 0,
                    "start_date": proof_doc.rented_from_date or "",
                    "end_date": proof_doc.rented_to_date or "",
                    "pan": proof_doc.custom_pan or "",
                    "address_line1": proof_doc.custom_address_title1 or "",
                    "address_line2": proof_doc.custom_address_title2 or "",
                    "attach_proof": proof_doc.custom_hra_proof_attach or "",
                    "attach_reqd": 1,
                    "custom_name": proof_doc.custom_name or "",
                    "custom_proof_status": proof_doc.custom_hra_approval_status or "",
                    "custom_note": proof_doc.custom_note or "",
                    
                })




            # ------------------ DB → UI Flag ------------------
            current_flag = 1 if current_tax_regime == "New Regime" else 0

            # ------------------ Existing Declaration Map ------------------
            existing_declaration = []
            for d in proof_doc.tax_exemption_proofs:
                existing_declaration.append({
                    "exemption_category": d.exemption_category,
                    "exemption_sub_category": d.exemption_sub_category,
                    "amount": d.amount,
                    "max_amount": d.max_amount,
                    "attach_proof": d.attach_proof,
                    "custom_proof_status": d.custom_proof_status,
                    "custom_note": d.custom_note
                })

            existing_map = {
                d["exemption_sub_category"]: d for d in existing_declaration
            }


            if go_head_with_new_regime is None:
                return {
                    "status": "success",
                    "declaration_id": declaration_id,
                    "current_tax_regime": current_tax_regime,
                    "go_head_with_new_regime": current_flag
                }

            # ------------------ Initial Load (No Toggle) ------------------
            go_head_with_new_regime = int(go_head_with_new_regime)


            if go_head_with_new_regime == current_flag:


                if current_tax_regime == "Old Regime":


                    NON_EDITABLE_COMPONENTS = [
                        "Professional Tax",
                        "Provident Fund",
                        "NPS"
                    ]

                    # ------------------ Fetch Section Category sequence ------------------
                    section_sequence_map = {
                        d.name: d.sequence_number
                        for d in frappe.get_all(
                            "Section Category",
                            fields=["name", "sequence_number"]
                        )
                    }

                    # ------------------ Fetch Exemption Category meta ------------------
                    category_meta_map = {
                        d.name: {
                            "custom_select_type": d.custom_select_type,
                            "max_amount": d.max_amount,
                            "custom_80d_variable": d.custom_80d_variable
                        }
                        for d in frappe.get_all(
                            "Employee Tax Exemption Category",
                            fields=["name", "custom_select_type", "max_amount","custom_80d_variable"]
                        )
                    }

                    # ------------------ Fetch Sub Categories ------------------
                    records = frappe.get_all(
                        "Employee Tax Exemption Sub Category",
                        filters={
                            "is_active": 1,
                            "custom_component_type": ["!=", "LTA Reimbursement"]
                        },
                        fields=[
                            "exemption_category",
                            "name",
                            "max_amount",
                            "custom_component_type",
                            "custom_description",
                            "custom_sequence",
                            "custom_section_property"
                        ],
                        order_by="custom_sequence asc"
                    )

                    # ------------------ Group by Category ------------------
                    category_grouped = {}

                    for row in records:
                        category = row.exemption_category
                        category_meta = category_meta_map.get(category, {})

                        if category not in category_grouped:
                            category_grouped[category] = {
                                "category_name": category,
                                "custom_select_type": category_meta.get("custom_select_type"),
                                "custom_80d_variable": category_meta.get("custom_80d_variable"),
                                "category_max_amount": category_meta.get("max_amount"),
                                "custom_section_property": row.custom_section_property,
                                "items": []
                            }

                        declaration_row = existing_map.get(row.name)
                        editable = 0 if row.custom_component_type in NON_EDITABLE_COMPONENTS else 1



                        item = {
                            "exemption_sub_category": row.name,
                            "component_type": row.custom_component_type,
                            "description": row.custom_description,
                            "editable": editable,
                            "amount": round(declaration_row["amount"]) if declaration_row else 0,
                            "max_amount": round(
                                declaration_row["max_amount"]
                                if declaration_row and declaration_row.get("max_amount") is not None
                                else row.max_amount
                            ),
                            "attach_reqd": 0,
                            "attach_proof": "",
                            "custom_proof_status": declaration_row.get("custom_proof_status") if declaration_row else "",
                            "custom_note": declaration_row.get("custom_note") if declaration_row else "",
                        }


                        if row.custom_component_type not in NON_EDITABLE_COMPONENTS:

                            item["attach_reqd"] = 1
                            item["attach_proof"] = (
                                declaration_row.get("attach_proof")
                                if declaration_row and declaration_row.get("attach_proof")
                                else ""
                            )


                        category_grouped[category]["items"].append(item)

                    # ------------------ Group by Section Property (FIXED PART) ------------------
                    section_grouped = {}

                    for category_data in category_grouped.values():
                        section = category_data.get("custom_section_property")
                        if not section:
                            continue

                        if section not in section_grouped:
                            section_grouped[section] = {
                                "custom_section_property": section,
                                "sequence_number": section_sequence_map.get(section, 999),
                                "exemption_category": []
                            }

                        category_name = category_data["category_name"]
                        meta = category_meta_map.get(category_name, {})

                        section_grouped[section]["exemption_category"].append({
                            "category_name": category_name,
                            "custom_select_type": meta.get("custom_select_type"),
                            "custom_80d_variable": meta.get("custom_80d_variable"),
                            "max_amount": meta.get("max_amount"),
                            "items": category_data["items"]
                        })

                    # ------------------ Sort Sections ------------------
                    final_categories = sorted(
                        section_grouped.values(),
                        key=lambda x: x["sequence_number"]
                    )

                    # ------------------ LTA Reimbursement Logic (unchanged) ------------------
                    records = frappe.get_all(
                        "Employee Tax Exemption Sub Category",
                        filters={"is_active": 1, "custom_component_type": "LTA Reimbursement"},
                        fields=[
                            "exemption_category",
                            "name",
                            "max_amount",
                            "custom_component_type",
                            "custom_description",
                            "custom_sequence",
                            "custom_section_property"
                        ],
                        order_by="custom_sequence asc"
                    )

                    grouped = {}

                    for row in records:
                        category = row.exemption_category
                        if category not in grouped:
                            grouped[category] = []

                        declaration_row = existing_map.get(row.name)
                        editable = 0 if row.custom_component_type in NON_EDITABLE_COMPONENTS else 1

                        grouped[category].append({
                            "exemption_sub_category": row.name,
                            "component_type": row.custom_component_type,
                            "description": row.custom_description,
                            "editable": editable,
                            "amount": round(declaration_row["amount"]) if declaration_row else 0,
                            "max_amount": round(
                                declaration_row["max_amount"]
                                if declaration_row and declaration_row.get("max_amount") is not None
                                else row.max_amount
                            ),
                            "custom_proof_status": declaration_row.get("custom_proof_status") if declaration_row else "",
                            "custom_note": declaration_row.get("custom_note") if declaration_row else "",
                            "attach_reqd": 1,
                            "attach_proof": declaration_row.get("attach_proof")
                                if declaration_row and declaration_row.get("attach_proof")
                                else ""



                        })

                    final_list = []
                    for category, items in grouped.items():
                        final_list.append({
                            "category_name": category,
                            "items": items
                        })

                    hra_exemption.append({"items": final_list})

                    return {
                        "status": "success",
                        "note":"Proof Submission Found, Returning Old Regime Data",
                        "declaration_id": declaration_id,
                        "proof_id": proof_id,
                        "doctype":"Employee Tax Exemption Proof Submission",
                        "current_tax_regime": current_tax_regime,
                        "go_head_with_new_regime": current_flag,
                        "hra_exemption": hra_exemption,
                        "categories": final_categories,

                    }


                elif current_tax_regime == "New Regime":

                    # ------------------ Fetch Section Category sequence ------------------
                    section_sequence_map = {
                        d.name: d.sequence_number
                        for d in frappe.get_all(
                            "Section Category",
                            fields=["name", "sequence_number"]
                        )
                    }

                    # ------------------ Fetch Exemption Category meta ------------------
                    category_meta_map = {
                        d.name: {
                            "custom_select_type": d.custom_select_type,
                            "max_amount": d.max_amount
                        }
                        for d in frappe.get_all(
                            "Employee Tax Exemption Category",
                            fields=["name", "custom_select_type", "max_amount"]
                        )
                    }

                    # ------------------ Fetch NPS Sub Categories ------------------
                    records = frappe.get_all(
                        "Employee Tax Exemption Sub Category",
                        filters={
                            "is_active": 1,
                            "custom_component_type": "NPS"
                        },
                        fields=[
                            "exemption_category",
                            "name",
                            "max_amount",
                            "custom_component_type",
                            "custom_description",
                            "custom_sequence",
                            "custom_section_property"
                        ],
                        order_by="custom_sequence asc"
                    )

                    # ------------------ Group by Category ------------------
                    category_grouped = {}

                    for row in records:
                        category = row.exemption_category
                        category_meta = category_meta_map.get(category, {})

                        if category not in category_grouped:
                            category_grouped[category] = {
                                "category_name": category,
                                "custom_select_type": category_meta.get("custom_select_type"),
                                "category_max_amount": category_meta.get("max_amount"),
                                "custom_section_property": row.custom_section_property,
                                "items": []
                            }

                        declaration_row = existing_map.get(row.name)

                        category_grouped[category]["items"].append({
                            "exemption_sub_category": row.name,
                            "component_type": row.custom_component_type,
                            "description": row.custom_description,
                            "editable": 0,  # NPS is always non-editable
                            "amount": round(declaration_row["amount"]) if declaration_row else 0,
                            "max_amount": round(
                                declaration_row["max_amount"]
                                if declaration_row and declaration_row.get("max_amount") is not None
                                else row.max_amount
                            ),
                            "attach_reqd": 0,
                            "attach_proof": "" ,
                            "custom_proof_status": "",
                            "custom_note": "",
                        })

                    # ------------------ Group by Section Property ------------------
                    section_grouped = {}

                    for category_data in category_grouped.values():
                        section = category_data.get("custom_section_property")
                        if not section:
                            continue

                        if section not in section_grouped:
                            section_grouped[section] = {
                                "custom_section_property": section,
                                "sequence_number": section_sequence_map.get(section, 999),
                                "exemption_category": []
                            }

                        category_name = category_data["category_name"]
                        meta = category_meta_map.get(category_name, {})

                        section_grouped[section]["exemption_category"].append({
                            "category_name": category_name,
                            "custom_select_type": meta.get("custom_select_type"),
                            "max_amount": meta.get("max_amount"),
                            "items": category_data["items"]
                        })

                    # ------------------ Sort Sections by sequence ------------------
                    final_categories = sorted(
                        section_grouped.values(),
                        key=lambda x: x["sequence_number"]
                    )

                    return {
                        "status": "success",
                        "note":"Proof Submission Found, Returning New Regime Data",
                        "declaration_id": declaration_id,
                        "proof_id": proof_id,
                        "doctype":"Employee Tax Exemption Proof Submission",
                        "current_tax_regime": current_tax_regime,
                        "go_head_with_new_regime": current_flag,
                        "categories": final_categories
                    }


            if go_head_with_new_regime == 1 and current_flag == 0:

                nps_amount_ctc = 0
                num_months = 0
                choosed_tax_regime = None



                # ---------------- Latest Tax Slab (NEW REGIME) ----------------
                latest_tax_slab = frappe.get_list(
                    "Income Tax Slab",
                    filters={
                        "company": company,
                        "docstatus": 1,
                        "disabled": 0,
                        "custom_select_regime": "New Regime",
                    },
                    fields=["name", "custom_select_regime", "standard_tax_exemption_amount"],
                    order_by="effective_from DESC",
                    limit=1,
                )

                latest_tax_slab_name = None
                if latest_tax_slab:
                    latest_tax_slab_name = latest_tax_slab[0].name
                    choosed_tax_regime = "New Regime"

                # ---------------- Salary Structure Assignment ----------------
                salary_structure_assignments = frappe.get_list(
                    "Salary Structure Assignment",
                    filters={
                        "employee": employee,
                        "docstatus": 1,
                        "custom_payroll_period": payroll_period,
                        "company": company,
                    },
                    fields=["*"],
                    order_by="from_date desc",
                    limit=1
                )

                if not salary_structure_assignments:
                    return {
                        "status": "success",
                        "message": "No salary structure assignment found",
                        "categories": []
                    }

                assignment = salary_structure_assignments[0]

                employee_doc = frappe.get_doc("Employee", employee)
                payroll_period_doc = frappe.get_doc("Payroll Period", payroll_period)

                # ---------------- Date Calculations ----------------
                start_candidates = [
                    assignment.from_date,
                    payroll_period_doc.start_date,
                    employee_doc.date_of_joining,
                ]

                start = max(getdate(d) for d in start_candidates if d)
                end = getdate(payroll_period_doc.end_date)

                num_months = (end.year - start.year) * 12 + (end.month - start.month) + 1

                # ---------------- Salary Slips ----------------
                salary_slips = frappe.get_list(
                    "Salary Slip",
                    filters={
                        "employee": employee,
                        "custom_payroll_period": payroll_period,
                        "docstatus": ["in", [0, 1]],
                        "company": company,
                    },
                    fields=["name", "custom_month_count"],
                    order_by="end_date desc",
                )

                # ---------------- CASE 1: No Salary Slips ----------------
                if not salary_slips:

                    salary_slip_preview = make_salary_slip(
                        source_name=assignment.salary_structure,
                        employee=employee,
                        posting_date=assignment.from_date,
                        for_preview=1,
                    )

                    if salary_slip_preview:
                        for earning in salary_slip_preview.earnings:
                            component = frappe.get_doc("Salary Component", earning.salary_component)

                            if (
                                component.is_tax_applicable
                                and component.custom_tax_exemption_applicable_based_on_regime
                                and component.custom_regime == "All"
                                and component.custom_component_sub_type == "Fixed"
                                and component.component_type == "NPS"
                            ):
                                nps_amount_ctc += earning.amount * num_months

                # ---------------- CASE 2: Salary Slips Exist ----------------
                else:
                    month_count = salary_slips[0].custom_month_count or 0

                    for slip in salary_slips:
                        slip_doc = frappe.get_doc("Salary Slip", slip.name)

                        for earning in slip_doc.earnings:
                            component = frappe.get_doc("Salary Component", earning.salary_component)

                            if (
                                component.is_tax_applicable
                                and component.custom_tax_exemption_applicable_based_on_regime
                                and component.custom_regime == "All"
                                and component.component_type == "NPS"
                            ):
                                nps_amount_ctc += earning.amount

                    # Preview remaining months
                    salary_slip_preview = make_salary_slip(
                        source_name=assignment.salary_structure,
                        employee=employee,
                        posting_date=assignment.from_date,
                        for_preview=1,
                    )

                    if salary_slip_preview:
                        for earning in salary_slip_preview.earnings:
                            component = frappe.get_doc("Salary Component", earning.salary_component)

                            if (
                                component.is_tax_applicable
                                and component.custom_tax_exemption_applicable_based_on_regime
                                and component.custom_regime == "All"
                                and component.custom_component_sub_type == "Fixed"
                                and component.component_type == "NPS"
                            ):
                                nps_amount_ctc += earning.amount * month_count




                section_sequence_map = {
                    d.name: d.sequence_number
                    for d in frappe.get_all(
                        "Section Category",
                        fields=["name", "sequence_number"]
                    )
                }

                # ------------------ Fetch Exemption Category meta ------------------
                category_meta_map = {
                    d.name: {
                        "custom_select_type": d.custom_select_type,
                        "max_amount": d.max_amount
                    }
                    for d in frappe.get_all(
                        "Employee Tax Exemption Category",
                        fields=["name", "custom_select_type", "max_amount"]
                    )
                }

                # ------------------ Fetch NPS Sub Categories ------------------
                records = frappe.get_all(
                    "Employee Tax Exemption Sub Category",
                    filters={
                        "is_active": 1,
                        "custom_component_type": "NPS"
                    },
                    fields=[
                        "exemption_category",
                        "name",
                        "max_amount",
                        "custom_component_type",
                        "custom_description",
                        "custom_sequence",
                        "custom_section_property"
                    ],
                    order_by="custom_sequence asc"
                )

                # ------------------ Group by Category ------------------
                category_grouped = {}

                for row in records:
                    category = row.exemption_category
                    category_meta = category_meta_map.get(category, {})

                    if category not in category_grouped:
                        category_grouped[category] = {
                            "category_name": category,
                            "custom_select_type": category_meta.get("custom_select_type"),
                            "category_max_amount": category_meta.get("max_amount"),
                            "custom_section_property": row.custom_section_property,
                            "items": []
                        }

                    declaration_row = existing_map.get(row.name)

                    category_grouped[category]["items"].append({
                        "exemption_sub_category": row.name,
                        "component_type": row.custom_component_type,
                        "description": row.custom_description,
                        "editable": 0,  # NPS is always non-editable
                        "amount": round(declaration_row["amount"]) if declaration_row else 0,
                        "max_amount": round(
                            declaration_row["max_amount"]
                            if declaration_row and declaration_row.get("max_amount") is not None
                            else row.max_amount
                        ),
                        "attach_reqd": 0,
                        "attach_proof": "" ,
                        "custom_proof_status": "",
                        "custom_note": "",
                    })

                # ------------------ Group by Section Property ------------------
                section_grouped = {}

                for category_data in category_grouped.values():
                    section = category_data.get("custom_section_property")
                    if not section:
                        continue

                    if section not in section_grouped:
                        section_grouped[section] = {
                            "custom_section_property": section,
                            "sequence_number": section_sequence_map.get(section, 999),
                            "exemption_category": []
                        }

                    category_name = category_data["category_name"]
                    meta = category_meta_map.get(category_name, {})

                    section_grouped[section]["exemption_category"].append({
                        "category_name": category_name,
                        "custom_select_type": meta.get("custom_select_type"),
                        "max_amount": meta.get("max_amount"),
                        "items": category_data["items"]
                    })

                # ------------------ Sort Sections by sequence ------------------
                final_categories = sorted(
                    section_grouped.values(),
                    key=lambda x: x["sequence_number"]
                )


                return {
                    "status": "success",
                    "doctype":"Employee Tax Exemption Proof Submission",
                    "declaration_id": declaration_id,
                    "proof_id": proof_id,
                    "current_tax_regime": current_tax_regime,
                    "go_head_with_new_regime": current_flag,
                    "categories": final_categories
                }



            if go_head_with_new_regime == 0 and current_flag == 1:

                nps_amount_ctc = 0
                pf_amount_ctc = 0
                pt_amount_ctc = 0
                lta_amount_ctc = 0



                hra_exemption.append({
                    "monthly_hra": None,
                    "rented_in_metro_city": None,
                    "annual_hra_exemption": None,
                    "monthly_hra_exemption": None,
                    "start_date": None,
                    "end_date": None,
                    "pan": None,
                    "address_line1": None,
                    "address_line2": None,
                    "attach_reqd": 1,
                    "attach_proof": "" ,
                    "custom_name": "",
                    "custom_proof_status": "",
                    "custom_note": ""
                })


                assignment = frappe.get_list(
                    "Salary Structure Assignment",
                    filters={
                        "employee": employee,
                        "company": company,
                        "custom_payroll_period": payroll_period,
                        "docstatus": 1,
                    },
                    fields=["salary_structure", "from_date"],
                    order_by="from_date desc",
                    limit=1,
                )

                if not assignment:
                    return {
                        "status": "success",
                        "message": "No salary structure assignment found",
                        "categories": [],
                    }

                assignment = assignment[0]

                employee_doc = frappe.get_doc("Employee", employee)
                payroll_doc = frappe.get_doc("Payroll Period", payroll_period)


                start = max(
                    getdate(d)
                    for d in [
                        assignment.from_date,
                        payroll_doc.start_date,
                        employee_doc.date_of_joining,
                    ]
                    if d
                )
                end = getdate(payroll_doc.end_date)
                total_months = (end.year - start.year) * 12 + (end.month - start.month) + 1


                salary_slips = frappe.get_list(
                    "Salary Slip",
                    filters={
                        "employee": employee,
                        "company": company,
                        "custom_payroll_period": payroll_period,
                        "docstatus": ["in", [0, 1]],
                    },
                    fields=["name", "custom_month_count"],
                    order_by="end_date desc",
                )


                if not salary_slips:

                    preview = make_salary_slip(
                        source_name=assignment.salary_structure,
                        employee=employee,
                        posting_date=assignment.from_date,
                        for_preview=1,
                    )

                    for row in preview.earnings:
                        component = frappe.get_doc("Salary Component", row.salary_component)

                        if (
                            component.custom_tax_exemption_applicable_based_on_regime
                            and component.custom_regime == "All"
                            and component.custom_component_sub_type == "Fixed"
                        ):
                            if component.component_type == "NPS":
                                nps_amount_ctc += row.amount * total_months
                            elif component.component_type == "LTA Reimbursement":
                                lta_amount_ctc += row.amount * total_months

                    for row in preview.deductions:
                        component = frappe.get_doc("Salary Component", row.salary_component)

                        if component.component_type == "Provident Fund":
                            pf_amount_ctc += row.amount * total_months
                        elif component.component_type == "Professional Tax":
                            pt_amount_ctc += row.amount * total_months


                else:
                    processed_months = salary_slips[0].custom_month_count or 0

                    for slip in salary_slips:
                        slip_doc = frappe.get_doc("Salary Slip", slip.name)

                        for row in slip_doc.earnings:
                            component = frappe.get_doc("Salary Component", row.salary_component)

                            if (
                                component.custom_tax_exemption_applicable_based_on_regime
                                and component.custom_regime == "All"
                            ):
                                if component.component_type == "NPS":
                                    nps_amount_ctc += row.amount
                                elif component.component_type == "LTA Reimbursement":
                                    lta_amount_ctc += row.amount

                        for row in slip_doc.deductions:
                            component = frappe.get_doc("Salary Component", row.salary_component)


                            if component.component_type == "Provident Fund":
                                pf_amount_ctc += row.amount
                            elif component.component_type == "Professional Tax":
                                pt_amount_ctc += row.amount


                    # ---- Remaining months preview (THIS WAS MISSING) ----
                    if processed_months > 0:
                        preview = make_salary_slip(
                            source_name=assignment.salary_structure,
                            employee=employee,
                            posting_date=assignment.from_date,
                            for_preview=1,
                        )


                        for row in preview.earnings:
                            component = frappe.get_doc("Salary Component", row.salary_component)

                            if (
                                component.custom_tax_exemption_applicable_based_on_regime
                                and component.custom_regime == "All"
                                and component.custom_component_sub_type == "Fixed"
                            ):
                                if component.component_type == "NPS":
                                    nps_amount_ctc += row.amount * processed_months
                                elif component.component_type == "LTA Reimbursement":
                                    lta_amount_ctc += row.amount * processed_months

                        for row in preview.deductions:
                            component = frappe.get_doc("Salary Component", row.salary_component)

                            if component.custom_component_sub_type == "Fixed":
                                if component.component_type == "Provident Fund":
                                    pf_amount_ctc += row.amount * processed_months
                                elif component.component_type == "Professional Tax":
                                    pt_amount_ctc += row.amount * processed_months




                SYSTEM_COMPONENT_MAP = {
                    "NPS": round(nps_amount_ctc, 2),
                    "Provident Fund": round(pf_amount_ctc, 2),
                    "Professional Tax": round(pt_amount_ctc, 2),
                }

                NON_EDITABLE_COMPONENTS = set(SYSTEM_COMPONENT_MAP.keys())

                # ------------------ Fetch Section Category sequence ------------------
                section_sequence_map = {
                    d.name: d.sequence_number
                    for d in frappe.get_all(
                        "Section Category",
                        fields=["name", "sequence_number"]
                    )
                }

                # ------------------ Fetch Exemption Category meta ------------------
                category_meta_map = {
                    d.name: {
                        "custom_select_type": d.custom_select_type,
                        "max_amount": d.max_amount,
                        "custom_80d_variable": d.custom_80d_variable
                    }
                    for d in frappe.get_all(
                        "Employee Tax Exemption Category",
                        fields=["name", "custom_select_type", "max_amount", "custom_80d_variable"]
                    )
                }

                # ------------------ Fetch Sub Categories (NON-LTA) ------------------
                records = frappe.get_all(
                    "Employee Tax Exemption Sub Category",
                    filters={
                        "is_active": 1,
                        "custom_component_type": ["!=", "LTA Reimbursement"]
                    },
                    fields=[
                        "exemption_category",
                        "name",
                        "max_amount",
                        "custom_component_type",
                        "custom_description",
                        "custom_sequence",
                        "custom_section_property"
                    ],
                    order_by="custom_sequence asc"
                )

                # ------------------ Group by Category ------------------
                category_grouped = {}

                for row in records:
                    category = row.exemption_category
                    category_meta = category_meta_map.get(category, {})

                    if category not in category_grouped:
                        category_grouped[category] = {
                            "category_name": category,
                            "custom_select_type": category_meta.get("custom_select_type"),
                            "custom_80d_variable": category_meta.get("custom_80d_variable"),
                            "category_max_amount": category_meta.get("max_amount"),
                            "custom_section_property": row.custom_section_property,
                            "items": []
                        }

                    declaration_row = existing_map.get(row.name)

                    # ------------------ SYSTEM vs USER logic ------------------
                    if row.custom_component_type in SYSTEM_COMPONENT_MAP:
                        amount = SYSTEM_COMPONENT_MAP[row.custom_component_type]
                        max_amount = amount
                        editable = 0
                    else:
                        amount = declaration_row["amount"] if declaration_row else 0
                        max_amount = (
                            declaration_row.get("max_amount")
                            if declaration_row and declaration_row.get("max_amount") is not None
                            else row.max_amount
                        )
                        editable = 1

                  

                    item = {
                        "exemption_sub_category": row.name,
                        "component_type": row.custom_component_type,
                        "description": row.custom_description,
                        "editable": editable,
                        "amount": round(amount),
                        "max_amount": round(max_amount),
                        "attach_reqd": 0,
                        "attach_proof": "",
                        "custom_proof_status":"",
                        "custom_note": "",
                    }

                    
                    if row.custom_component_type not in NON_EDITABLE_COMPONENTS:
                        
                        item["attach_reqd"] = 1

                    category_grouped[category]["items"].append(item)



                # ------------------ Group by Section Property ------------------
                section_grouped = {}

                for category_data in category_grouped.values():
                    section = category_data.get("custom_section_property")
                    if not section:
                        continue

                    if section not in section_grouped:
                        section_grouped[section] = {
                            "custom_section_property": section,
                            "sequence_number": section_sequence_map.get(section, 999),
                            "exemption_category": []
                        }

                    category_name = category_data["category_name"]
                    meta = category_meta_map.get(category_name, {})

                    section_grouped[section]["exemption_category"].append({
                        "category_name": category_name,
                        "custom_select_type": meta.get("custom_select_type"),
                        "custom_80d_variable": meta.get("custom_80d_variable"),
                        "max_amount": meta.get("max_amount"),
                        "items": category_data["items"]
                    })

                # ------------------ Sort Sections ------------------
                final_categories = sorted(
                    section_grouped.values(),
                    key=lambda x: x["sequence_number"]
                )

                # ------------------ LTA Reimbursement (UNCHANGED) ------------------
                records = frappe.get_all(
                    "Employee Tax Exemption Sub Category",
                    filters={"is_active": 1, "custom_component_type": "LTA Reimbursement"},
                    fields=[
                        "exemption_category",
                        "name",
                        "max_amount",
                        "custom_component_type",
                        "custom_description",
                        "custom_sequence",
                        "custom_section_property"
                    ],
                    order_by="custom_sequence asc"
                )

                grouped = {}

                for row in records:
                    category = row.exemption_category
                    if category not in grouped:
                        grouped[category] = []

                    declaration_row = existing_map.get(row.name)

                    grouped[category].append({
                        "exemption_sub_category": row.name,
                        "component_type": row.custom_component_type,
                        "description": row.custom_description,
                        "editable": 1,
                        "amount": round(declaration_row["amount"]) if declaration_row else 0,
                        "max_amount": round(
                            declaration_row["max_amount"]
                            if declaration_row and declaration_row.get("max_amount") is not None
                            else row.max_amount
                        ),
                        "attach_reqd": 1,
                        "attach_proof": "",
                        "custom_proof_status": "",
                        "custom_note": "",
                    })

                hra_exemption.append({
                    "items": [
                        {
                            "category_name": category,
                            "items": items
                        }
                        for category, items in grouped.items()
                    ]
                })

                return {
                    "status": "success",
                    "declaration_id": declaration_id,
                    "doctype":"Employee Tax Exemption Proof Submission",
                    "proof_id": proof_id,
                    "current_tax_regime": "Old Regime",
                    "go_head_with_new_regime": 0,
                    "message": "User switched from New Regime to Old Regime",
                    "categories": final_categories,
                    "hra_exemption": hra_exemption,
                }



        else:
            current_tax_regime = declaration_doc.custom_tax_regime

            hra_exemption=[]


            if declaration_doc.custom_tax_regime=="Old Regime":

                monthly_hra=declaration_doc.monthly_house_rent if declaration_doc.monthly_house_rent else 0
                rented_in_metro_city=declaration_doc.rented_in_metro_city if declaration_doc.rented_in_metro_city else 0
                annual_hra_exemption=declaration_doc.annual_hra_exemption if declaration_doc.annual_hra_exemption else 0
                monthly_hra_exemption=declaration_doc.monthly_hra_exemption if declaration_doc.monthly_hra_exemption else 0


                hra_exemption.append({
                    "monthly_hra": declaration_doc.monthly_house_rent or 0,
                    "rented_in_metro_city": declaration_doc.rented_in_metro_city or 0,
                    "annual_hra_exemption": declaration_doc.annual_hra_exemption or 0,
                    "monthly_hra_exemption": declaration_doc.monthly_hra_exemption or 0,
                    "start_date": declaration_doc.custom_start_date or "",
                    "end_date": declaration_doc.custom_end_date or "",
                    "pan": declaration_doc.custom_pan or "",
                    "address_line1": declaration_doc.custom_address_title1 or "",
                    "address_line2": declaration_doc.custom_address_title2 or "",
                    "attach_reqd": 1,
                    "attach_proof": "" ,
                    "custom_name": declaration_doc.custom_name or "",
                    "custom_proof_status": "",
                    "custom_note": ""
                    
                })




            # ------------------ DB → UI Flag ------------------
            current_flag = 1 if current_tax_regime == "New Regime" else 0

            # ------------------ Existing Declaration Map ------------------
            existing_declaration = []
            for d in declaration_doc.declarations:
                
                existing_declaration.append({
                    "exemption_category": d.exemption_category,
                    "exemption_sub_category": d.exemption_sub_category,
                    "amount": d.amount,
                    "max_amount": d.max_amount,
                    "custom_proof_status": d.custom_status if d.custom_status in ["Approved","Rejected","Pending"] else "",
                    "custom_note": d.custom_note,
                })

            existing_map = {
                d["exemption_sub_category"]: d for d in existing_declaration
            }

            # ------------------ Initial Load (No Toggle) ------------------
            if go_head_with_new_regime is None:
                return {
                    "status": "success",
                    "declaration_id": declaration_id,
                    "current_tax_regime": current_tax_regime,
                    "go_head_with_new_regime": current_flag
                }

            go_head_with_new_regime = int(go_head_with_new_regime)


            if go_head_with_new_regime == current_flag:


                if current_tax_regime == "Old Regime":

                    NON_EDITABLE_COMPONENTS = [
                        "Professional Tax",
                        "Provident Fund",
                        "NPS"
                    ]

                    # ------------------ Fetch Section Category sequence ------------------
                    section_sequence_map = {
                        d.name: d.sequence_number
                        for d in frappe.get_all(
                            "Section Category",
                            fields=["name", "sequence_number"]
                        )
                    }

                    # ------------------ Fetch Exemption Category meta ------------------
                    category_meta_map = {
                        d.name: {
                            "custom_select_type": d.custom_select_type,
                            "max_amount": d.max_amount
                        }
                        for d in frappe.get_all(
                            "Employee Tax Exemption Category",
                            fields=["name", "custom_select_type", "max_amount"]
                        )
                    }

                    # ------------------ Fetch Sub Categories ------------------
                    records = frappe.get_all(
                        "Employee Tax Exemption Sub Category",
                        filters={
                            "is_active": 1,
                            "custom_component_type": ["!=", "LTA Reimbursement"]
                        },
                        fields=[
                            "exemption_category",
                            "name",
                            "max_amount",
                            "custom_component_type",
                            "custom_description",
                            "custom_sequence",
                            "custom_section_property"
                        ],
                        order_by="custom_sequence asc"
                    )

                    # ------------------ Group by Category ------------------
                    category_grouped = {}

                    for row in records:
                        category = row.exemption_category
                        category_meta = category_meta_map.get(category, {})

                        if category not in category_grouped:
                            category_grouped[category] = {
                                "category_name": category,
                                "custom_select_type": category_meta.get("custom_select_type"),
                                "category_max_amount": category_meta.get("max_amount"),
                                "custom_section_property": row.custom_section_property,
                                "items": []
                            }

                        declaration_row = existing_map.get(row.name)
                        editable = 0 if row.custom_component_type in NON_EDITABLE_COMPONENTS else 1


                        item = {
                            "exemption_sub_category": row.name,
                            "component_type": row.custom_component_type,
                            "description": row.custom_description,
                            "editable": editable,
                            "amount": round(declaration_row["amount"]) if declaration_row else 0,
                            "max_amount": round(
                                declaration_row["max_amount"]
                                if declaration_row and declaration_row.get("max_amount") is not None
                                else row.max_amount
                            ),
                            "attach_reqd": 0,
                            "attach_proof": "",
                            # "custom_proof_status": declaration_row.get("custom_proof_status") if declaration_row else ""
                        }

                        # ✅ Add attach_proof ONLY when allowed
                        if row.custom_component_type not in NON_EDITABLE_COMPONENTS:
                            item["attach_reqd"] = 1

                        category_grouped[category]["items"].append(item)

                    # ------------------ Group by Section Property (FIXED PART) ------------------
                    section_grouped = {}

                    for category_data in category_grouped.values():
                        section = category_data.get("custom_section_property")
                        if not section:
                            continue

                        if section not in section_grouped:
                            section_grouped[section] = {
                                "custom_section_property": section,
                                "sequence_number": section_sequence_map.get(section, 999),
                                "exemption_category": []
                            }

                        category_name = category_data["category_name"]
                        meta = category_meta_map.get(category_name, {})

                        section_grouped[section]["exemption_category"].append({
                            "category_name": category_name,
                            "custom_select_type": meta.get("custom_select_type"),
                            "max_amount": meta.get("max_amount"),
                            "items": category_data["items"]
                        })

                    # ------------------ Sort Sections ------------------
                    final_categories = sorted(
                        section_grouped.values(),
                        key=lambda x: x["sequence_number"]
                    )

                    # ------------------ LTA Reimbursement Logic (unchanged) ------------------
                    records = frappe.get_all(
                        "Employee Tax Exemption Sub Category",
                        filters={"is_active": 1, "custom_component_type": "LTA Reimbursement"},
                        fields=[
                            "exemption_category",
                            "name",
                            "max_amount",
                            "custom_component_type",
                            "custom_description",
                            "custom_sequence",
                            "custom_section_property"
                        ],
                        order_by="custom_sequence asc"
                    )

                    grouped = {}

                    for row in records:
                        category = row.exemption_category
                        if category not in grouped:
                            grouped[category] = []

                        declaration_row = existing_map.get(row.name)
                        editable = 0 if row.custom_component_type in NON_EDITABLE_COMPONENTS else 1

                        grouped[category].append({
                            "exemption_sub_category": row.name,
                            "component_type": row.custom_component_type,
                            "description": row.custom_description,
                            "editable": editable,
                            "amount": round(declaration_row["amount"]) if declaration_row else 0,
                            "max_amount": round(
                                declaration_row["max_amount"]
                                if declaration_row and declaration_row.get("max_amount") is not None
                                else row.max_amount
                            ),
                            "attach_reqd": 1,
                            "attach_proof": "" ,
                            # "custom_proof_status": declaration_row.get("custom_proof_status") if declaration_row else ""
                        })

                    final_list = []
                    for category, items in grouped.items():
                        final_list.append({
                            "category_name": category,
                            "items": items
                        })

                    hra_exemption.append({"items": final_list})

                    return {
                        "status": "success",
                        "note":"No Proof Submission Found, Returning Old Regime Data",
                        "declaration_id": declaration_id,
                        "proof_id": "",
                        "doctype":"Employee Tax Exemption Proof Submission",
                        "current_tax_regime": current_tax_regime,
                        "go_head_with_new_regime": current_flag,
                        "hra_exemption": hra_exemption,
                        "categories": final_categories
                    }


                elif current_tax_regime == "New Regime":

                    # ------------------ Fetch Section Category sequence ------------------
                    section_sequence_map = {
                        d.name: d.sequence_number
                        for d in frappe.get_all(
                            "Section Category",
                            fields=["name", "sequence_number"]
                        )
                    }

                    # ------------------ Fetch Exemption Category meta ------------------
                    category_meta_map = {
                        d.name: {
                            "custom_select_type": d.custom_select_type,
                            "max_amount": d.max_amount
                        }
                        for d in frappe.get_all(
                            "Employee Tax Exemption Category",
                            fields=["name", "custom_select_type", "max_amount"]
                        )
                    }

                    # ------------------ Fetch NPS Sub Categories ------------------
                    records = frappe.get_all(
                        "Employee Tax Exemption Sub Category",
                        filters={
                            "is_active": 1,
                            "custom_component_type": "NPS"
                        },
                        fields=[
                            "exemption_category",
                            "name",
                            "max_amount",
                            "custom_component_type",
                            "custom_description",
                            "custom_sequence",
                            "custom_section_property"
                        ],
                        order_by="custom_sequence asc"
                    )

                    # ------------------ Group by Category ------------------
                    category_grouped = {}

                    for row in records:
                        category = row.exemption_category
                        category_meta = category_meta_map.get(category, {})

                        if category not in category_grouped:
                            category_grouped[category] = {
                                "category_name": category,
                                "custom_select_type": category_meta.get("custom_select_type"),
                                "category_max_amount": category_meta.get("max_amount"),
                                "custom_section_property": row.custom_section_property,
                                "items": []
                            }

                        declaration_row = existing_map.get(row.name)

                        category_grouped[category]["items"].append({
                            "exemption_sub_category": row.name,
                            "component_type": row.custom_component_type,
                            "description": row.custom_description,
                            "editable": 0,  # NPS is always non-editable
                            "amount": round(declaration_row["amount"]) if declaration_row else 0,
                            "max_amount": round(
                                declaration_row["max_amount"]
                                if declaration_row and declaration_row.get("max_amount") is not None
                                else row.max_amount
                            ),
                            "attach_reqd": 0,
                            "attach_proof": "",
                            # "custom_proof_status": declaration_row.get("custom_proof_status") if declaration_row else ""
                        })

                    # ------------------ Group by Section Property ------------------
                    section_grouped = {}

                    for category_data in category_grouped.values():
                        section = category_data.get("custom_section_property")
                        if not section:
                            continue

                        if section not in section_grouped:
                            section_grouped[section] = {
                                "custom_section_property": section,
                                "sequence_number": section_sequence_map.get(section, 999),
                                "exemption_category": []
                            }

                        category_name = category_data["category_name"]
                        meta = category_meta_map.get(category_name, {})

                        section_grouped[section]["exemption_category"].append({
                            "category_name": category_name,
                            "custom_select_type": meta.get("custom_select_type"),
                            "max_amount": meta.get("max_amount"),
                            "items": category_data["items"]
                        })

                    # ------------------ Sort Sections by sequence ------------------
                    final_categories = sorted(
                        section_grouped.values(),
                        key=lambda x: x["sequence_number"]
                    )

                    return {
                        "status": "success",
                        "note":"No Proof Submission Found, Returning New Regime Data",
                        "declaration_id": declaration_id,
                        "proof_id": "",
                        "doctype":"Employee Tax Exemption Proof Submission",
                        "current_tax_regime": current_tax_regime,
                        "go_head_with_new_regime": current_flag,
                        "categories": final_categories
                    }


            if go_head_with_new_regime == 1 and current_flag == 0:

                nps_amount_ctc = 0
                num_months = 0
                choosed_tax_regime = None

                # ---------------- Latest Tax Slab (NEW REGIME) ----------------
                latest_tax_slab = frappe.get_list(
                    "Income Tax Slab",
                    filters={
                        "company": company,
                        "docstatus": 1,
                        "disabled": 0,
                        "custom_select_regime": "New Regime",
                    },
                    fields=["name", "custom_select_regime", "standard_tax_exemption_amount"],
                    order_by="effective_from DESC",
                    limit=1,
                )

                latest_tax_slab_name = None
                if latest_tax_slab:
                    latest_tax_slab_name = latest_tax_slab[0].name
                    choosed_tax_regime = "New Regime"

                # ---------------- Salary Structure Assignment ----------------
                salary_structure_assignments = frappe.get_list(
                    "Salary Structure Assignment",
                    filters={
                        "employee": employee,
                        "docstatus": 1,
                        "custom_payroll_period": payroll_period,
                        "company": company,
                    },
                    fields=["*"],
                    order_by="from_date desc",
                    limit=1
                )

                if not salary_structure_assignments:
                    return {
                        "status": "success",
                        "message": "No salary structure assignment found",
                        "categories": []
                    }

                assignment = salary_structure_assignments[0]

                employee_doc = frappe.get_doc("Employee", employee)
                payroll_period_doc = frappe.get_doc("Payroll Period", payroll_period)

                # ---------------- Date Calculations ----------------
                start_candidates = [
                    assignment.from_date,
                    payroll_period_doc.start_date,
                    employee_doc.date_of_joining,
                ]

                start = max(getdate(d) for d in start_candidates if d)
                end = getdate(payroll_period_doc.end_date)

                num_months = (end.year - start.year) * 12 + (end.month - start.month) + 1

                # ---------------- Salary Slips ----------------
                salary_slips = frappe.get_list(
                    "Salary Slip",
                    filters={
                        "employee": employee,
                        "custom_payroll_period": payroll_period,
                        "docstatus": ["in", [0, 1]],
                        "company": company,
                    },
                    fields=["name", "custom_month_count"],
                    order_by="end_date desc",
                )

                # ---------------- CASE 1: No Salary Slips ----------------
                if not salary_slips:

                    salary_slip_preview = make_salary_slip(
                        source_name=assignment.salary_structure,
                        employee=employee,
                        posting_date=assignment.from_date,
                        for_preview=1,
                    )

                    if salary_slip_preview:
                        for earning in salary_slip_preview.earnings:
                            component = frappe.get_doc("Salary Component", earning.salary_component)

                            if (
                                component.is_tax_applicable
                                and component.custom_tax_exemption_applicable_based_on_regime
                                and component.custom_regime == "All"
                                and component.custom_component_sub_type == "Fixed"
                                and component.component_type == "NPS"
                            ):
                                nps_amount_ctc += earning.amount * num_months

                # ---------------- CASE 2: Salary Slips Exist ----------------
                else:
                    month_count = salary_slips[0].custom_month_count or 0

                    for slip in salary_slips:
                        slip_doc = frappe.get_doc("Salary Slip", slip.name)

                        for earning in slip_doc.earnings:
                            component = frappe.get_doc("Salary Component", earning.salary_component)

                            if (
                                component.is_tax_applicable
                                and component.custom_tax_exemption_applicable_based_on_regime
                                and component.custom_regime == "All"
                                and component.component_type == "NPS"
                            ):
                                nps_amount_ctc += earning.amount

                    # Preview remaining months
                    salary_slip_preview = make_salary_slip(
                        source_name=assignment.salary_structure,
                        employee=employee,
                        posting_date=assignment.from_date,
                        for_preview=1,
                    )

                    if salary_slip_preview:
                        for earning in salary_slip_preview.earnings:
                            component = frappe.get_doc("Salary Component", earning.salary_component)

                            if (
                                component.is_tax_applicable
                                and component.custom_tax_exemption_applicable_based_on_regime
                                and component.custom_regime == "All"
                                and component.custom_component_sub_type == "Fixed"
                                and component.component_type == "NPS"
                            ):
                                nps_amount_ctc += earning.amount * month_count




                section_sequence_map = {
                    d.name: d.sequence_number
                    for d in frappe.get_all(
                        "Section Category",
                        fields=["name", "sequence_number"]
                    )
                }

                # ------------------ Fetch Exemption Category meta ------------------
                category_meta_map = {
                    d.name: {
                        "custom_select_type": d.custom_select_type,
                        "max_amount": d.max_amount
                    }
                    for d in frappe.get_all(
                        "Employee Tax Exemption Category",
                        fields=["name", "custom_select_type", "max_amount"]
                    )
                }

                # ------------------ Fetch NPS Sub Categories ------------------
                records = frappe.get_all(
                    "Employee Tax Exemption Sub Category",
                    filters={
                        "is_active": 1,
                        "custom_component_type": "NPS"
                    },
                    fields=[
                        "exemption_category",
                        "name",
                        "max_amount",
                        "custom_component_type",
                        "custom_description",
                        "custom_sequence",
                        "custom_section_property"
                    ],
                    order_by="custom_sequence asc"
                )

                # ------------------ Group by Category ------------------
                category_grouped = {}

                for row in records:
                    category = row.exemption_category
                    category_meta = category_meta_map.get(category, {})

                    if category not in category_grouped:
                        category_grouped[category] = {
                            "category_name": category,
                            "custom_select_type": category_meta.get("custom_select_type"),
                            "category_max_amount": category_meta.get("max_amount"),
                            "custom_section_property": row.custom_section_property,
                            "items": []
                        }

                    declaration_row = existing_map.get(row.name)

                    category_grouped[category]["items"].append({
                        "exemption_sub_category": row.name,
                        "component_type": row.custom_component_type,
                        "description": row.custom_description,
                        "editable": 0,  # NPS is always non-editable
                        "amount": round(declaration_row["amount"]) if declaration_row else 0,
                        "max_amount": round(
                            declaration_row["max_amount"]
                            if declaration_row and declaration_row.get("max_amount") is not None
                            else row.max_amount
                        ),
                        "attach_reqd": 0,
                        "attach_proof": "",
                        # "custom_proof_status": declaration_row.get("custom_proof_status") if declaration_row else ""
                    })

                # ------------------ Group by Section Property ------------------
                section_grouped = {}

                for category_data in category_grouped.values():
                    section = category_data.get("custom_section_property")
                    if not section:
                        continue

                    if section not in section_grouped:
                        section_grouped[section] = {
                            "custom_section_property": section,
                            "sequence_number": section_sequence_map.get(section, 999),
                            "exemption_category": []
                        }

                    category_name = category_data["category_name"]
                    meta = category_meta_map.get(category_name, {})

                    section_grouped[section]["exemption_category"].append({
                        "category_name": category_name,
                        "custom_select_type": meta.get("custom_select_type"),
                        "max_amount": meta.get("max_amount"),
                        "items": category_data["items"]
                    })

                # ------------------ Sort Sections by sequence ------------------
                final_categories = sorted(
                    section_grouped.values(),
                    key=lambda x: x["sequence_number"]
                )


                return {
                    "status": "success",
                    "doctype":"Employee Tax Exemption Proof Submission",
                    "declaration_id": declaration_id,
                    "proof_id": "",
                    "current_tax_regime": current_tax_regime,
                    "go_head_with_new_regime": current_flag,
                    "categories": final_categories
                }


            if go_head_with_new_regime == 0 and current_flag == 1:

                nps_amount_ctc = 0
                pf_amount_ctc = 0
                pt_amount_ctc = 0
                lta_amount_ctc = 0




                hra_exemption.append({
                    "monthly_hra": None,
                    "rented_in_metro_city": None,
                    "annual_hra_exemption": None,
                    "monthly_hra_exemption": None,
                    "start_date": None,
                    "end_date": None,
                    "pan": None,
                    "address_line1": None,
                    "address_line2": None,
                    "attach_proof": "",
                    "custom_name": "",
                })


                assignment = frappe.get_list(
                    "Salary Structure Assignment",
                    filters={
                        "employee": employee,
                        "company": company,
                        "custom_payroll_period": payroll_period,
                        "docstatus": 1,
                    },
                    fields=["salary_structure", "from_date"],
                    order_by="from_date desc",
                    limit=1,
                )

                if not assignment:
                    return {
                        "status": "success",
                        "message": "No salary structure assignment found",
                        "categories": [],
                    }

                assignment = assignment[0]

                employee_doc = frappe.get_doc("Employee", employee)
                payroll_doc = frappe.get_doc("Payroll Period", payroll_period)


                start = max(
                    getdate(d)
                    for d in [
                        assignment.from_date,
                        payroll_doc.start_date,
                        employee_doc.date_of_joining,
                    ]
                    if d
                )
                end = getdate(payroll_doc.end_date)
                total_months = (end.year - start.year) * 12 + (end.month - start.month) + 1


                salary_slips = frappe.get_list(
                    "Salary Slip",
                    filters={
                        "employee": employee,
                        "company": company,
                        "custom_payroll_period": payroll_period,
                        "docstatus": ["in", [0, 1]],
                    },
                    fields=["name", "custom_month_count"],
                    order_by="end_date desc",
                )


                if not salary_slips:

                    preview = make_salary_slip(
                        source_name=assignment.salary_structure,
                        employee=employee,
                        posting_date=assignment.from_date,
                        for_preview=1,
                    )

                    for row in preview.earnings:
                        component = frappe.get_doc("Salary Component", row.salary_component)

                        if (
                            component.custom_tax_exemption_applicable_based_on_regime
                            and component.custom_regime == "All"
                            and component.custom_component_sub_type == "Fixed"
                        ):
                            if component.component_type == "NPS":
                                nps_amount_ctc += row.amount * total_months
                            elif component.component_type == "LTA Reimbursement":
                                lta_amount_ctc += row.amount * total_months

                    for row in preview.deductions:
                        component = frappe.get_doc("Salary Component", row.salary_component)

                        if component.component_type == "Provident Fund":
                            pf_amount_ctc += row.amount * total_months
                        elif component.component_type == "Professional Tax":
                            pt_amount_ctc += row.amount * total_months


                else:
                    processed_months = salary_slips[0].custom_month_count or 0

                    for slip in salary_slips:
                        slip_doc = frappe.get_doc("Salary Slip", slip.name)

                        for row in slip_doc.earnings:
                            component = frappe.get_doc("Salary Component", row.salary_component)

                            if (
                                component.custom_tax_exemption_applicable_based_on_regime
                                and component.custom_regime == "All"
                            ):
                                if component.component_type == "NPS":
                                    nps_amount_ctc += row.amount
                                elif component.component_type == "LTA Reimbursement":
                                    lta_amount_ctc += row.amount

                        for row in slip_doc.deductions:
                            component = frappe.get_doc("Salary Component", row.salary_component)


                            if component.component_type == "Provident Fund":
                                pf_amount_ctc += row.amount
                            elif component.component_type == "Professional Tax":
                                pt_amount_ctc += row.amount


                    # ---- Remaining months preview (THIS WAS MISSING) ----
                    if processed_months > 0:
                        preview = make_salary_slip(
                            source_name=assignment.salary_structure,
                            employee=employee,
                            posting_date=assignment.from_date,
                            for_preview=1,
                        )


                        for row in preview.earnings:
                            component = frappe.get_doc("Salary Component", row.salary_component)

                            if (
                                component.custom_tax_exemption_applicable_based_on_regime
                                and component.custom_regime == "All"
                                and component.custom_component_sub_type == "Fixed"
                            ):
                                if component.component_type == "NPS":
                                    nps_amount_ctc += row.amount * processed_months
                                elif component.component_type == "LTA Reimbursement":
                                    lta_amount_ctc += row.amount * processed_months

                        for row in preview.deductions:
                            component = frappe.get_doc("Salary Component", row.salary_component)

                            if component.custom_component_sub_type == "Fixed":
                                if component.component_type == "Provident Fund":
                                    pf_amount_ctc += row.amount * processed_months
                                elif component.component_type == "Professional Tax":
                                    pt_amount_ctc += row.amount * processed_months




                SYSTEM_COMPONENT_MAP = {
                    "NPS": round(nps_amount_ctc, 2),
                    "Provident Fund": round(pf_amount_ctc, 2),
                    "Professional Tax": round(pt_amount_ctc, 2),
                }

                NON_EDITABLE_COMPONENTS = set(SYSTEM_COMPONENT_MAP.keys())

                # ------------------ Fetch Section Category sequence ------------------
                section_sequence_map = {
                    d.name: d.sequence_number
                    for d in frappe.get_all(
                        "Section Category",
                        fields=["name", "sequence_number"]
                    )
                }

                # ------------------ Fetch Exemption Category meta ------------------
                category_meta_map = {
                    d.name: {
                        "custom_select_type": d.custom_select_type,
                        "max_amount": d.max_amount,
                        "custom_80d_variable": d.custom_80d_variable
                    }
                    for d in frappe.get_all(
                        "Employee Tax Exemption Category",
                        fields=["name", "custom_select_type", "max_amount", "custom_80d_variable"]
                    )
                }

                # ------------------ Fetch Sub Categories (NON-LTA) ------------------
                records = frappe.get_all(
                    "Employee Tax Exemption Sub Category",
                    filters={
                        "is_active": 1,
                        "custom_component_type": ["!=", "LTA Reimbursement"]
                    },
                    fields=[
                        "exemption_category",
                        "name",
                        "max_amount",
                        "custom_component_type",
                        "custom_description",
                        "custom_sequence",
                        "custom_section_property"
                    ],
                    order_by="custom_sequence asc"
                )

                # ------------------ Group by Category ------------------
                category_grouped = {}

                for row in records:
                    category = row.exemption_category
                    category_meta = category_meta_map.get(category, {})

                    if category not in category_grouped:
                        category_grouped[category] = {
                            "category_name": category,
                            "custom_select_type": category_meta.get("custom_select_type"),
                            "custom_80d_variable": category_meta.get("custom_80d_variable"),
                            "category_max_amount": category_meta.get("max_amount"),
                            "custom_section_property": row.custom_section_property,
                            "items": []
                        }

                    declaration_row = existing_map.get(row.name)

                    # ------------------ SYSTEM vs USER logic ------------------
                    if row.custom_component_type in SYSTEM_COMPONENT_MAP:
                        amount = SYSTEM_COMPONENT_MAP[row.custom_component_type]
                        max_amount = amount
                        editable = 0
                    else:
                        amount = declaration_row["amount"] if declaration_row else 0
                        max_amount = (
                            declaration_row.get("max_amount")
                            if declaration_row and declaration_row.get("max_amount") is not None
                            else row.max_amount
                        )
                        editable = 1

                   
                    item = {
                        "exemption_sub_category": row.name,
                        "component_type": row.custom_component_type,
                        "description": row.custom_description,
                        "editable": editable,
                        "amount": round(amount),
                        "max_amount": round(max_amount),
                        "attach_reqd": 0,
                        "attach_proof": "",
                    }

                    # ✅ Attach proof ONLY for editable (non-system) components
                    if row.custom_component_type not in NON_EDITABLE_COMPONENTS:
                        item["attach_reqd"] = 1

                    category_grouped[category]["items"].append(item)

                # ------------------ Group by Section Property ------------------
                section_grouped = {}

                for category_data in category_grouped.values():
                    section = category_data.get("custom_section_property")
                    if not section:
                        continue

                    if section not in section_grouped:
                        section_grouped[section] = {
                            "custom_section_property": section,
                            "sequence_number": section_sequence_map.get(section, 999),
                            "exemption_category": []
                        }

                    category_name = category_data["category_name"]
                    meta = category_meta_map.get(category_name, {})

                    section_grouped[section]["exemption_category"].append({
                        "category_name": category_name,
                        "custom_select_type": meta.get("custom_select_type"),
                        "custom_80d_variable": meta.get("custom_80d_variable"),
                        "max_amount": meta.get("max_amount"),
                        "items": category_data["items"]
                    })

                # ------------------ Sort Sections ------------------
                final_categories = sorted(
                    section_grouped.values(),
                    key=lambda x: x["sequence_number"]
                )

                # ------------------ LTA Reimbursement (UNCHANGED) ------------------
                records = frappe.get_all(
                    "Employee Tax Exemption Sub Category",
                    filters={"is_active": 1, "custom_component_type": "LTA Reimbursement"},
                    fields=[
                        "exemption_category",
                        "name",
                        "max_amount",
                        "custom_component_type",
                        "custom_description",
                        "custom_sequence",
                        "custom_section_property"
                    ],
                    order_by="custom_sequence asc"
                )

                grouped = {}

                for row in records:
                    category = row.exemption_category
                    if category not in grouped:
                        grouped[category] = []

                    declaration_row = existing_map.get(row.name)

                    grouped[category].append({
                        "exemption_sub_category": row.name,
                        "component_type": row.custom_component_type,
                        "description": row.custom_description,
                        "editable": 1,
                        "amount": round(declaration_row["amount"]) if declaration_row else 0,
                        "max_amount": round(
                            declaration_row["max_amount"]
                            if declaration_row and declaration_row.get("max_amount") is not None
                            else row.max_amount
                        ),
                        "attach_reqd": 1,
                        "attach_proof": "",
                        # "custom_proof_status": declaration_row.get("custom_proof_status") if declaration_row else ""
                    })

                hra_exemption.append({
                    "items": [
                        {
                            "category_name": category,
                            "items": items
                        }
                        for category, items in grouped.items()
                    ]
                })

                return {
                    "status": "success",
                    "declaration_id": declaration_id,
                    "doctype":"Employee Tax Exemption Proof Submission",
                    "proof_id": "",
                    "current_tax_regime": "Old Regime",
                    "go_head_with_new_regime": 0,
                    "message": "User switched from New Regime to Old Regime",
                    "categories": final_categories,
                    "hra_exemption": hra_exemption,
                }






# http://127.0.0.1:8002/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.tds_projection.get_employee_declaration_investments?employee=PW0220&payroll_period=25-26&company=Pen%20Pencil
@frappe.whitelist()
def get_employee_declaration_investments(employee=None, company=None, payroll_period=None):

    # ------------------ Validation ------------------
    if not employee or not company:
        return {
            "status": "failed",
            "message": "Employee and Company are required"
        }

    target_employee = frappe.request.headers.get("X-Target-Employee-Id")
    if target_employee:
        employee = target_employee

    # ------------------ Get Declaration ------------------
    tax_slab_id=None
    net_taxable_income=0
    previous_tds_income= 0
    previous_tds_deducted_value= 0
    num_months=0
    

    payroll_setting=frappe.get_doc("Payroll Settings")
    if payroll_setting.custom_tax_calculation_based_on=="Use IT Declaration Values in Payroll Processing":

        declaration = frappe.get_all(
            "Employee Tax Exemption Declaration",
            filters={
                "employee": employee,
                "company": company,
                "payroll_period": payroll_period
            },
            fields=["name"],
            limit=1
        )

        if not declaration:
            return {
                "status": "failed",
                "message": "No declaration form created for this payroll period"
            }

        declaration_doc = frappe.get_doc(
            "Employee Tax Exemption Declaration",
            declaration[0].name
        )

        
        previous_tds_income=declaration_doc.custom_total_taxable_income or 0
        previous_tds_deducted_value=declaration_doc.custom_total_tds_deducted_value or 0
        current_tax_regime=declaration_doc.custom_tax_regime

        declaration_id=declaration[0].name
        tax_slab_id=declaration_doc.custom_income_tax

        advance_tax=declaration_doc.custom_tds_already_deducted_amount if declaration_doc.custom_tds_already_deducted_amount else 0



        # ------------------ 80C & LTA ------------------
        eighty_c = []
        lta_amount = 0
        eighty_d=[]
        other_investment=[]
        lta_declared_amount=0
        lta_exempted_amount=0
        home_loan_investment=[]
        home_loan_investment_sum=0

        declared_home_loan = 0
        qualified_home_loan = 0
        taxable_home_loan=0


        if declaration_doc.declarations:
            for d in declaration_doc.declarations:

                sub_category = frappe.get_doc(
                    "Employee Tax Exemption Sub Category",
                    d.exemption_sub_category
                )

                # LTA
                if sub_category.custom_component_type == "LTA Reimbursement":
                    lta_declared_amount = flt(d.amount or 0)
                    lta_exempted_amount = flt(d.max_amount or 0)
                    lta_amount = flt(d.max_amount or 0) if d.amount and d.max_amount and d.amount > d.max_amount else flt(d.amount or 0)


                category = frappe.get_doc(
                    "Employee Tax Exemption Category",
                    d.exemption_category
                )

                # Section 80C
                if category.custom_select_section == "80 C":
                    declared = flt(d.amount or 0)
                    qualified = flt(d.max_amount or 0)

                    eighty_c.append({
                        "component": d.exemption_sub_category,
                        "declared_amount": declared,
                        "qualified_amount": 0,
                        "deductible_amount": qualified if declared > qualified else declared
                    })


                if category.custom_select_section == "80 D":

                    declared_80d = flt(d.amount or 0)
                    qualified_80d = flt(d.max_amount or 0)

                    eighty_d.append({
                        "component": d.exemption_sub_category,
                        "declared_amount": declared_80d,
                        "qualified_amount": qualified_80d,
                        "deductible_amount": qualified_80d if declared_80d > qualified_80d else declared_80d
                    })

                if not category.custom_select_section and not sub_category.custom_component_type=="LTA Reimbursement" and not sub_category.custom_component_type=="Home Loan" and d.custom_status in ["Approved","Not Needed"]:

                    declared_other = flt(d.amount or 0)
                    qualified_other = flt(d.max_amount or 0)

                    deductible = (
                        declared_other
                        if qualified_other == 0
                        else min(declared_other, qualified_other)
                    )

                    other_investment.append({
                        "component": d.exemption_sub_category,
                        "declared_amount": declared_other,
                        "qualified_amount": qualified_other,
                        "deductible_amount": deductible
                    })

                    # other_investment.append({

                    #     "component": d.exemption_sub_category,
                    #     "declared_amount": declared_other,
                    #     "qualified_amount": qualified_other,
                    #     "deductible_amount": qualified_other if declared_other > qualified_other else declared_other
                    # })

                if sub_category.custom_component_type=="Home Loan":

                    declared_home_loan = flt(d.amount or 0)
                    qualified_home_loan = flt(d.max_amount or 0)
                    taxable_home_loan = declared_home_loan if declared_home_loan < qualified_home_loan else qualified_home_loan

                    home_loan_investment.append({

                        "component": d.exemption_sub_category,
                        "declared_amount": declared_home_loan,
                        "qualified_amount": qualified_home_loan,
                        "deductible_amount": qualified_home_loan if declared_home_loan > qualified_home_loan else declared_home_loan
                    })

        # ------------------ Annual Statement ------------------



        eighty_c_sum = min(
            sum(r["deductible_amount"] for r in eighty_c),
            150000
        )
        eighty_d_sum = sum(r["deductible_amount"] for r in eighty_d)
        other_investment_sum = sum(r["deductible_amount"] for r in other_investment)
        home_loan_investment_sum = sum(r["deductible_amount"] for r in home_loan_investment)

        annual_statement = get_annual_statement(employee, payroll_period,company)

        if annual_statement.get("status") != "success":
            return annual_statement

        extra_payment_grand_total = flt(annual_statement.get("extra_payment_grand_total", 0))
        total_perquisite_total = flt(annual_statement.get("total_perquisite_total", 0))
        total_gross_earning = flt(annual_statement.get("total_gross_earning", 0))+(previous_tds_income)
        total_off_cycle_payment = flt(annual_statement.get("total_off_cycle_payment", 0))
        reimbursements_total = flt(annual_statement.get("reimbursements_total", 0))
        total_perquisite_total=flt(annual_statement.get("total_perquisite_total", 0))

        total_gross_salary_current = round(
            total_gross_earning + total_off_cycle_payment + extra_payment_grand_total+total_perquisite_total, 2
        )

        hra_received_annual=declaration_doc.custom_hra_received_annual if declaration_doc.custom_hra_received_annual else 0
        rent_paid_of_basic=declaration_doc.custom_rent_paid__10_of_basic_annual if declaration_doc.custom_rent_paid__10_of_basic_annual else 0
        basic_percentage=declaration_doc.custom_50_of_basic_metro if declaration_doc.custom_50_of_basic_metro else 0

        hra_exemption=declaration_doc.annual_hra_exemption if declaration_doc.annual_hra_exemption else 0

        salary_after_section_10= round(
                    flt(total_gross_salary_current) - flt(lta_amount)-flt(hra_exemption), 2
                )

        income_tax_slab=frappe.get_doc("Income Tax Slab",declaration_doc.custom_income_tax)
        standard_deduction=income_tax_slab.standard_tax_exemption_amount if income_tax_slab.standard_tax_exemption_amount else 0

        gross_total_income=round(flt(salary_after_section_10) - flt(standard_deduction), 2)

        total_declaration_sum=round(eighty_c_sum + eighty_d_sum + other_investment_sum+home_loan_investment_sum)

        net_taxable_income=round(gross_total_income-total_declaration_sum,2)


    elif payroll_setting.custom_tax_calculation_based_on=="Use POI Approved Values in Payroll Processing":

        proof_submission = frappe.get_all(
            "Employee Tax Exemption Proof Submission",
            filters={
                "employee": employee,
                "company": company,
                "payroll_period": payroll_period
            },
            fields=["name"],
            limit=1
        )
        if not proof_submission:
            declaration = frappe.get_all(
                "Employee Tax Exemption Declaration",
                filters={
                    "employee": employee,
                    "company": company,
                    "payroll_period": payroll_period
                },
                fields=["name"],
                limit=1
            )

            if not declaration:
                return {
                    "status": "failed",
                    "message": "No declaration form created for this payroll period"
                }

            declaration_doc = frappe.get_doc(
                "Employee Tax Exemption Declaration",
                declaration[0].name
            )

            previous_tds_income=declaration_doc.custom_total_taxable_income or 0
            previous_tds_deducted_value=declaration_doc.custom_total_tds_deducted_value or 0

            current_tax_regime=declaration_doc.custom_tax_regime
            declaration_id=declaration[0].name
            tax_slab_id=declaration_doc.custom_income_tax

            advance_tax=declaration_doc.custom_tds_already_deducted_amount if declaration_doc.custom_tds_already_deducted_amount else 0



            # ------------------ 80C & LTA ------------------
            eighty_c = []
            lta_amount = 0
            eighty_d=[]
            other_investment=[]

            lta_declared_amount=0
            lta_exempted_amount=0
            home_loan_investment=[]
            home_loan_investment_sum=0

            declared_home_loan = 0
            qualified_home_loan = 0
            taxable_home_loan=0

            if declaration_doc.declarations:
                for d in declaration_doc.declarations:

                    sub_category = frappe.get_doc(
                        "Employee Tax Exemption Sub Category",
                        d.exemption_sub_category
                    )

                    # LTA
                    if sub_category.custom_component_type == "LTA Reimbursement":
                        lta_declared_amount = flt(d.amount or 0)
                        lta_exempted_amount = flt(d.max_amount or 0)
                        lta_amount = flt(d.max_amount or 0) if d.amount and d.max_amount and d.amount > d.max_amount else flt(d.amount or 0)

                    category = frappe.get_doc(
                        "Employee Tax Exemption Category",
                        d.exemption_category
                    )

                    # Section 80C
                    if category.custom_select_section == "80 C":
                        declared = flt(d.amount or 0)
                        qualified = flt(d.max_amount or 0)

                        eighty_c.append({
                            "component": d.exemption_sub_category,
                            "declared_amount": declared,
                            "qualified_amount": qualified,
                            "deductible_amount": qualified if declared > qualified else declared
                        })


                    if category.custom_select_section == "80 D":

                        declared_80d = flt(d.amount or 0)
                        qualified_80d = flt(d.max_amount or 0)

                        eighty_d.append({
                            "component": d.exemption_sub_category,
                            "declared_amount": declared_80d,
                            "qualified_amount": qualified_80d,
                            "deductible_amount": qualified_80d if declared_80d > qualified_80d else declared_80d
                        })

                    if not category.custom_select_section and not sub_category.custom_component_type=="LTA Reimbursement" and not sub_category.custom_component_type=="Home Loan":

                        declared_other = flt(d.amount or 0)
                        qualified_other = flt(d.max_amount or 0)

                        other_investment.append({

                            "component": d.exemption_sub_category,
                            "declared_amount": declared_other,
                            "qualified_amount": qualified_other,
                            "deductible_amount": qualified_other if declared_other > qualified_other else declared_other
                        })

                    if sub_category.custom_component_type=="Home Loan":

                        declared_home_loan = flt(d.amount or 0)
                        qualified_home_loan = flt(d.max_amount or 0)
                        taxable_home_loan = declared_home_loan if declared_home_loan < qualified_home_loan else qualified_home_loan

                        home_loan_investment.append({

                            "component": d.exemption_sub_category,
                            "declared_amount": declared_home_loan,
                            "qualified_amount": qualified_home_loan,
                            "deductible_amount": qualified_home_loan if declared_home_loan > qualified_home_loan else declared_home_loan
                        })

                    

            # ------------------ Annual Statement ------------------



            eighty_c_sum = min(
                sum(r["deductible_amount"] for r in eighty_c),
                150000
            )
            eighty_d_sum = sum(r["deductible_amount"] for r in eighty_d)
            other_investment_sum = sum(r["deductible_amount"] for r in other_investment)
            home_loan_investment_sum = sum(r["deductible_amount"] for r in home_loan_investment)

            annual_statement = get_annual_statement(employee, payroll_period,company)

            if annual_statement.get("status") != "success":
                return annual_statement

            extra_payment_grand_total = flt(annual_statement.get("extra_payment_grand_total", 0))
            total_perquisite_total = flt(annual_statement.get("total_perquisite_total", 0))
            total_gross_earning = flt(annual_statement.get("total_gross_earning", 0))
            total_off_cycle_payment = flt(annual_statement.get("total_off_cycle_payment", 0))
            reimbursements_total = flt(annual_statement.get("reimbursements_total", 0))
            total_perquisite_total=flt(annual_statement.get("total_perquisite_total", 0))

            total_gross_salary_current = round(
                total_gross_earning + total_off_cycle_payment + extra_payment_grand_total+total_perquisite_total, 2
            )

            hra_received_annual=declaration_doc.custom_hra_received_annual if declaration_doc.custom_hra_received_annual else 0
            rent_paid_of_basic=declaration_doc.custom_rent_paid__10_of_basic_annual if declaration_doc.custom_rent_paid__10_of_basic_annual else 0
            basic_percentage=declaration_doc.custom_50_of_basic_metro if declaration_doc.custom_50_of_basic_metro else 0

            hra_exemption=declaration_doc.annual_hra_exemption if declaration_doc.annual_hra_exemption else 0

            salary_after_section_10= round(
                        flt(total_gross_salary_current) - flt(lta_amount)-flt(hra_exemption), 2
                    )

            income_tax_slab=frappe.get_doc("Income Tax Slab",declaration_doc.custom_income_tax)
            standard_deduction=income_tax_slab.standard_tax_exemption_amount if income_tax_slab.standard_tax_exemption_amount else 0

            gross_total_income=round(flt(salary_after_section_10) - flt(standard_deduction), 2)

            total_declaration_sum=round(eighty_c_sum + eighty_d_sum + other_investment_sum+home_loan_investment_sum, 2)

            net_taxable_income=round(gross_total_income-total_declaration_sum,2)


        else:

            proof_submission = frappe.get_all(
                "Employee Tax Exemption Proof Submission",
                filters={
                    "employee": employee,
                    "company": company,
                    "payroll_period": payroll_period
                },
                fields=["name"],
                limit=1
            )

            if not proof_submission:
                return {
                    "status": "failed",
                    "message": "No declaration form created for this payroll period"
                }

            proof_submission_doc = frappe.get_doc(
                "Employee Tax Exemption Proof Submission",
                proof_submission[0].name
            )

            current_tax_regime=proof_submission_doc.custom_tax_regime
            declaration_id=proof_submission_doc.name
            tax_slab_id=proof_submission_doc.custom_income_tax

            advance_tax=proof_submission_doc.custom_tds_already_deducted_amount if proof_submission_doc.custom_tds_already_deducted_amount else 0



            # ------------------ 80C & LTA ------------------
            eighty_c = []
            lta_amount = 0
            eighty_d=[]
            other_investment=[]

            lta_declared_amount=0
            lta_exempted_amount=0
            home_loan_investment=[]
            home_loan_investment_sum=0

            declared_home_loan = 0
            qualified_home_loan = 0
            taxable_home_loan=0



            if proof_submission_doc.tax_exemption_proofs:
                for d in proof_submission_doc.tax_exemption_proofs:

                    sub_category = frappe.get_doc(
                        "Employee Tax Exemption Sub Category",
                        d.exemption_sub_category
                    )

                    # LTA
                    if sub_category.custom_component_type == "LTA Reimbursement":
                        lta_declared_amount = flt(d.amount or 0)
                        lta_exempted_amount = flt(d.max_amount or 0)
                        lta_amount = flt(d.max_amount or 0) if d.amount and d.max_amount and d.amount > d.max_amount else flt(d.amount or 0)


                    category = frappe.get_doc(
                        "Employee Tax Exemption Category",
                        d.exemption_category
                    )

                    # Section 80C
                    if category.custom_select_section == "80 C":
                        declared = flt(d.amount or 0)
                        qualified = flt(d.max_amount or 0)

                        eighty_c.append({
                            "component": d.exemption_sub_category,
                            "declared_amount": declared,
                            "qualified_amount": qualified,
                            "deductible_amount": qualified if declared > qualified else declared
                        })


                    if category.custom_select_section == "80 D":

                        declared_80d = flt(d.amount or 0)
                        qualified_80d = flt(d.max_amount or 0)

                        eighty_d.append({
                            "component": d.exemption_sub_category,
                            "declared_amount": declared_80d,
                            "qualified_amount": qualified_80d,
                            "deductible_amount": qualified_80d if declared_80d > qualified_80d else declared_80d
                        })

                    if not category.custom_select_section and not sub_category.custom_component_type=="LTA Reimbursement" and not sub_category.custom_component_type=="Home Loan":

                        declared_other = flt(d.amount or 0)
                        qualified_other = flt(d.max_amount or 0)

                        other_investment.append({

                            "component": d.exemption_sub_category,
                            "declared_amount": declared_other,
                            "qualified_amount": qualified_other,
                            "deductible_amount": qualified_other if declared_other > qualified_other else declared_other
                        })

                    if sub_category.custom_component_type=="Home Loan":

                        declared_home_loan = flt(d.amount or 0)
                        qualified_home_loan = flt(d.max_amount or 0)
                        taxable_home_loan = declared_home_loan if declared_home_loan < qualified_home_loan else qualified_home_loan

                        home_loan_investment.append({

                            "component": d.exemption_sub_category,
                            "declared_amount": declared_home_loan,
                            "qualified_amount": qualified_home_loan,
                            "deductible_amount": qualified_home_loan if declared_home_loan > qualified_home_loan else declared_home_loan
                        })

            # ------------------ Annual Statement ------------------



            eighty_c_sum = min(
                sum(r["deductible_amount"] for r in eighty_c),
                150000
            )
            eighty_d_sum = sum(r["deductible_amount"] for r in eighty_d)
            other_investment_sum = sum(r["deductible_amount"] for r in other_investment)
            home_loan_investment_sum = sum(r["deductible_amount"] for r in home_loan_investment)

            annual_statement = get_annual_statement(employee, payroll_period,company)

            if annual_statement.get("status") != "success":
                return annual_statement

            extra_payment_grand_total = flt(annual_statement.get("extra_payment_grand_total", 0))
            total_perquisite_total = flt(annual_statement.get("total_perquisite_total", 0))
            total_gross_earning = flt(annual_statement.get("total_gross_earning", 0))
            total_off_cycle_payment = flt(annual_statement.get("total_off_cycle_payment", 0))
            reimbursements_total = flt(annual_statement.get("reimbursements_total", 0))
            total_perquisite_total=flt(annual_statement.get("total_perquisite_total", 0))

            total_gross_salary_current = round(
                total_gross_earning + total_off_cycle_payment + extra_payment_grand_total+total_perquisite_total, 2
            )

            hra_received_annual=proof_submission_doc.custom_hra_received_annual if proof_submission_doc.custom_hra_received_annual else 0
            rent_paid_of_basic=proof_submission_doc.custom_rent_paid__10_of_basic_annual if proof_submission_doc.custom_rent_paid__10_of_basic_annual else 0
            basic_percentage=proof_submission_doc.custom_50_of_basic_metro if proof_submission_doc.custom_50_of_basic_metro else 0

            hra_exemption=proof_submission_doc.custom_annual_eligible_amount if proof_submission_doc.custom_annual_eligible_amount else 0
            salary_after_section_10= round(
                        flt(total_gross_salary_current) - flt(lta_amount)-flt(hra_exemption), 2
                    )

            income_tax_slab=frappe.get_doc("Income Tax Slab",proof_submission_doc.custom_income_tax)
            standard_deduction=income_tax_slab.standard_tax_exemption_amount if income_tax_slab.standard_tax_exemption_amount else 0

            gross_total_income=round(flt(salary_after_section_10) - flt(standard_deduction), 2)

            total_declaration_sum=round(eighty_c_sum + eighty_d_sum + other_investment_sum+home_loan_investment_sum, 2)

            net_taxable_income=round(gross_total_income-total_declaration_sum,2)







    eval_globals = frappe._dict()
    eval_locals = frappe._dict()

    rebate=0
    tax_slab_doc = frappe.get_doc("Income Tax Slab", tax_slab_id)



    slab_result = calculate_tax_by_tax_slab(
        net_taxable_income,
        tax_slab_id,
        eval_globals,
        eval_locals,
    )

    income_tax_on_net_taxable_income = round((slab_result.get("base_tax") or 0), 0)
    surcharge = round((slab_result.get("surcharge") or 0), 0)
    education_cess = round((slab_result.get("education_cess_amount") or 0), 0)
    total_tax_payable = round((slab_result.get("total_tax_payable") or 0), 0)
    marginal_relief = round((slab_result.get("marginal_relief") or 0), 0)
        
        

    # if tax_slab_doc.custom_taxable_income_is_less_than>=income_tax_on_net_taxable_income:
    #     rebate=income_tax_on_net_taxable_income
    # else:
    #     rebate=0

    if net_taxable_income <= (tax_slab_doc.custom_taxable_income_is_less_than or 0):
    
        rebate = min(
            income_tax_on_net_taxable_income,
            tax_slab_doc.custom_maximum_amount or 0
        )
    else:
        rebate = 0

    tds_sum = 0
    salary_slips = frappe.db.get_all(
        "Salary Slip",
        filters={
            "employee": employee,
            "custom_payroll_period": payroll_period,
            "company": company,
            "docstatus": ["in", [0, 1]]
        },
        fields=["current_month_income_tax","custom_month_count"],
        order_by="end_date desc",
    )

    if salary_slips:
        num_months = salary_slips[0].custom_month_count or 0
        for slip in salary_slips:
            tds_sum += slip.get("current_month_income_tax") or 0
    else:   
        salary_assignment = frappe.get_list(
                "Salary Structure Assignment",
                filters={
                    "employee": employee,
                    "docstatus": 1,
                    "custom_payroll_period":payroll_period,
                    "company":company,
                },
                fields=["*"],
                order_by="from_date asc",
                limit=1,
            )

        if not salary_assignment:
            frappe.throw("No active Salary Structure Assignment found.")

        assignment = frappe.get_doc(
            "Salary Structure Assignment", salary_assignment[0].name
        )

        employee = frappe.get_doc("Employee", assignment.employee)
        payroll_period = frappe.get_doc("Payroll Period", assignment.custom_payroll_period)

        
        effective_start_date = getdate(assignment.from_date)
        payroll_start_date = getdate(payroll_period.start_date)
        payroll_end_date = getdate(payroll_period.end_date)
        date_of_joining = getdate(employee.date_of_joining)

        tds_from_previous_employer = assignment.taxable_earnings_till_date or 0
        already_paid_previous_employer=assignment.tax_deducted_till_date or 0


        start_date = max(
            filter(None, [effective_start_date, payroll_start_date, date_of_joining])
        )


        num_months = (
            (payroll_end_date.year - start_date.year) * 12
            + (payroll_end_date.month - start_date.month)
            + 1
        )

    remaining_tax=(total_tax_payable-previous_tds_deducted_value-advance_tax-tds_sum)or 0



    # ------------------ Response ------------------
    return {
    "status": "success",
    "current_tax_regime":current_tax_regime,
    "declaration_id":declaration_id,
    "net_taxable_income":net_taxable_income,
    "tax_slab_id":tax_slab_id,
    "income_tax_on_net_taxable_income": round((slab_result.get("base_tax") or 0), 0),
    "surcharge": round((slab_result.get("surcharge") or 0), 0),
    "education_cess" :round((slab_result.get("education_cess_amount") or 0), 0),
    "total_tax_payable" : round((slab_result.get("total_tax_payable") or 0), 0),
    "marginal_relief" :round((slab_result.get("marginal_relief") or 0), 0),

    

    "summary": [
        {
            "key": "gross_salary",
            "name": "Gross Salary",
            "amount": round(flt(total_gross_earning), 2),
            "col1":"",
            "col2":"",
            "col3":"",
            "col4":round(flt(total_gross_earning), 2),
            "declared_amount":"",
            "exemption_amount":"",
            "taxable_amount":round(flt(total_gross_earning), 2),

        },
        {
            "key": "previous_tds_income",
            "name": "Previous TDS Income",
            "amount": round(flt(previous_tds_income), 2),
            "col1":"",
            "col2":"",
            "col3":"",
            "col4":round(flt(previous_tds_income), 2),
            "declared_amount":"",
            "exemption_amount":"",
            "taxable_amount":round(flt(previous_tds_income), 2),

        },
        
        {
            "key": "total_extra_payment",
            "name": "Total Extra Payment",
            "amount": round(flt(extra_payment_grand_total), 2),
            "col1":round(flt(extra_payment_grand_total), 2),
            "col2":"",
            "col3":"",
            "col4":"",
            "declared_amount":round(flt(extra_payment_grand_total), 2),
            "exemption_amount":"",
            "taxable_amount":"",
        },
        {
            "key": "total_off_cycle_extra_payment",
            "name": "Total Offcycle Extra Payments",
            "amount": round(flt(total_off_cycle_payment), 2),
            "col1":round(flt(total_off_cycle_payment), 2),
            "col2":"",
            "col3":"",
            "col4":"",
            "declared_amount":round(flt(total_off_cycle_payment), 2),
            "exemption_amount":"",
            "taxable_amount":"",
        },
        {
            "key": "total_perquisite_total",
            "name": "Total Perquisite Total",
            "amount": round(flt(total_perquisite_total), 2),
            "col1":round(flt(total_perquisite_total), 2),
            "col2":"",
            "col3":"",
            "col4":"",
            "declared_amount":round(flt(total_perquisite_total), 2),
            "exemption_amount":"",
            "taxable_amount":"",
        },


        {
            "key": "total_gross_salary_current",
            "name": "Total Gross Salary (Current Employer)",
            "col1":"",
            "col2":"",
            "col3":"",
            "col4":"",
            "declared_amount":"",
            "exemption_amount":"",
            "taxable_amount":round(flt(total_gross_salary_current), 2),

        },

        {
            "key": "total_gross_salary",
            "name": "Total Gross Salary",
            "amount": round(flt(total_gross_salary_current), 2),
            "col1":"",
            "col2":"",
            "col3":"",
            "col4":round(flt(total_gross_salary_current), 2),
            "declared_amount":"",
            "exemption_amount":"",
            "taxable_amount":round(flt(total_gross_salary_current), 2),
        },



        {
            "key": "less_ctc_reimbursements",
            "name": "Less CTC Reimbursements",
            "col1":"",
            "col2":"",
            "col3":"",
            "col4":"",
            "declared_amount":"",
            "exemption_amount":"",
            "taxable_amount":"",

        },
        {
            "key": "lta_component",
            "name": "LTA",
            "amount": round(flt(lta_amount), 2),
            "col1":round(flt(lta_amount), 2),
            "col2":"",
            "col3":"",
            "col4":"",
            "declared_amount":lta_declared_amount,
            "exemption_amount":round(flt(lta_amount), 2),
            "taxable_amount":"",
        },
        {
            "key": "total_reimbursements",
            "name": "Total Reimbursements",
            "amount": round(flt(lta_amount), 2),
            "col1":"",
            "col2":round(flt(lta_amount), 2),
            "col3":"",
            "col4":"",
            "declared_amount":"",
            "exemption_amount":round(flt(lta_amount), 2),
            "taxable_amount":"",
        },
        {
            "key": "total_income_after_deduction_and_reimbursements",
            "name": "Gross Income after Deduction and Reimbursements",
            "amount": round(
                flt(total_gross_salary_current) - flt(lta_amount), 2
            ),
            "col1":"",
            "col2":"",
            "col3":"",
            "col4":round(
                flt(total_gross_salary_current) - flt(lta_amount), 2
            ),
            "declared_amount":"",
            "exemption_amount":"",
            "taxable_amount":round(
                flt(total_gross_salary_current) - flt(lta_amount), 2
            ),
        },
        {
            "key": "less_exemption_under_section_10",
            "name": "Less exemption under Section 10",
            "col1":"",
            "col2":"",
            "col3":"",
            "col4":"",
            "declared_amount":"",
            "exemption_amount":"",
            "taxable_amount":"",

        },
        {
            "key": "hra_calculation",
            "name": "HRA Calculation",
            "col1":"",
            "col2":"",
            "col3":"",
            "col4":"",
            "declared_amount":"",
            "exemption_amount":"",
            "taxable_amount":"",

        },
        {
            "key": "basic_and_dearness_allowance",
            "name": "Basic + Dearness Allowance (40% or 50%)",
            "amount": basic_percentage,
            "col1":basic_percentage,
            "col2":"",
            "col3":"",
            "col4":"",
            "declared_amount":basic_percentage,
            "exemption_amount":"",
            "taxable_amount":"",

        },
        {
            "key": "rent_paid",
            "name": "Rent Paid - 10% of Basic + Dearness Allowance",
            "amount": rent_paid_of_basic,
            "col1":rent_paid_of_basic,
            "col2":"",
            "col3":"",
            "col4":"",
            "declared_amount":rent_paid_of_basic,
            "exemption_amount":"",
            "taxable_amount":"",

        },
        {
            "key": "hra_received",
            "name": "H.R.A received",
            "amount": hra_received_annual,
            "col1":hra_received_annual,
            "col2":"",
            "col3":"",
            "col4":"",
            "declared_amount":hra_received_annual,
            "exemption_amount":"",
            "taxable_amount":"",

        },
        {
            "key": "hra_exemption",
            "name": "HRA Exemption",
            "amount": hra_exemption,
            "col1":hra_exemption,
            "col2":"",
            "col3":"",
            "col4":"",
            "declared_amount":hra_exemption,
            "exemption_amount":"",
            "taxable_amount":"",

        },
        {
            "key": "total_section_10_exemptions",
            "name": "Total Section 10 Exemptions",
            "amount": hra_exemption,
            "col1":"",
            "col2":hra_exemption,
            "col3":"",
            "col4":"",
            "declared_amount":"",
            "exemption_amount":hra_exemption,
            "taxable_amount":"",

        },
        {
            "key": "salary_after_section_10",
            "name": "Total amount of Salary received after Section 10",
            "amount": salary_after_section_10,
            "col1":"",
            "col2":"",
            "col3":"",
            "col4":salary_after_section_10,
            "declared_amount":"",
            "exemption_amount":"",
            "taxable_amount":salary_after_section_10,

        },
        {
            "key": "less_deduction_under_section_16",
            "name": "Less: Deductions under section 16",
            "col1":"",
            "col2":"",
            "col3":"",
            "col4":"",
            "declared_amount":"",
            "exemption_amount":"",
            "taxable_amount":"",

        },
        {
            "key": "standard_deduction_section_16",
            "name": "Standard deduction under section 16(ia)",
            "amount": standard_deduction,
            "col1":standard_deduction,
            "col2":"",
            "col3":"",
            "col4":"",
            "declared_amount":standard_deduction,
            "exemption_amount":"",
            "taxable_amount":"",
        },
        {
            "key": "total_deduction_section_16",
            "name": "Total amount of deductions under section 16",
            "amount": standard_deduction,
            "col1":"",
            "col2":standard_deduction,
            "col3":"",
            "col4":"",
            "declared_amount":"",
            "exemption_amount":standard_deduction,
            "taxable_amount":"",
        },
        {
            "key": "income_chargeable_salary",
            "name": "Income chargeable under the head Salaries",
            "amount": round(
                flt(salary_after_section_10) - flt(standard_deduction), 2
            ),
            "col1":"",
            "col2":"",
            "col3":"",
            "col4":round(
                flt(salary_after_section_10) - flt(standard_deduction), 2
            ),
            "declared_amount":"",
            "exemption_amount":"",
            "taxable_amount":round(
                flt(salary_after_section_10) - flt(standard_deduction), 2
            ),
        },
        {
            "key": "income_loss_house_property",
            "name": "A. Income/Loss from house property",
            "col1":"",
            "col2":"",
            "col3":"",
            "col4":"",
            "declared_amount":"",
            "exemption_amount":"",
            "taxable_amount":"",

        },


        {
            "key": "home_loan_interest_paid",
            "name": "Home Loan Interest Paid for Self-occupied Property",
            "col1":"",
            "col2":"",
            "col3":"",
            "col4":"",
            "declared_amount":declared_home_loan,
            "exemption_amount":taxable_home_loan,
            "taxable_amount":"",

        },



        {
            "key": "total_income_loss_house_property",
            "name": "Total for Income/Loss from house property",
            "amount": 0,
            "col1":"",
            "col2":"",
            "col3":"",
            "col4":"",
            "declared_amount":"",
            "exemption_amount":taxable_home_loan,
            "taxable_amount":"",
        },
        {
            "key": "other_sources",
            "name": "B. Other Sources",
            "col1":"",
            "col2":"",
            "col3":"",
            "col4":"",
            "declared_amount":"",
            "exemption_amount":"",
            "taxable_amount":"",

        },
        {
            "key": "total_other_sources",
            "name": "Total from Other Sources",
            "amount": 0,
            "col1":"",
            "col2":"",
            "col3":"",
            "col4":"",
            "declared_amount":"",
            "exemption_amount":"",
            "taxable_amount":"",
        },
        {
            "key": "gross_total_income",
            "name": "Gross Total Income",
            "amount": round(
                flt(salary_after_section_10) - flt(standard_deduction), 2
            ),
            "col1":"",
            "col2":"",
            "col3":"",
            "col4":round(
                flt(salary_after_section_10) - flt(standard_deduction), 2
            ),
            "declared_amount":"",
            "exemption_amount":"",
            "taxable_amount":"",
        }
    ],

    "chapter_via": [
        {
            "key": "total_chapter_via",
            "name": "Total Chapter-VIA",
            "headers": ["Declared Value", "Qualified Value", "Deductible Value"]
        },
        {
            "key": "section_80C",
            "name": "Section 80C, 80CCC, 80CCD",
            "components": eighty_c
        },

        {
            "key": "total_section_80C",
            "name": "Total Section 80C,80CCC,80CCD",
            "amount": eighty_c_sum
        },

        {
            "key": "section_80D",
            "name": "Section 80D",
            "components": eighty_d
        },
        {
            "key": "total_section_80D",
            "name": "Total Section 80D",
            "amount": eighty_d_sum
        },

        {
            "key": "other_investment",
            "name": "Other Investment",
            "components": other_investment
        },
        {
            "key": "total_other_investment",
            "name": "Total Other Investment",

            "amount": other_investment_sum
        },

        {
            "key": "total_chapter_via_total",
            "name": "Total Chapter-VIA Total",

            "amount": round(
                eighty_c_sum + eighty_d_sum + other_investment_sum, 2
            )
        },


    ],

    "net_taxable_breakup":
    [
        {
            "key": "net_taxable_income",
            "name":"Net Taxable Income",
            "amount":net_taxable_income
        },
        {
            "key": "net_taxable_income_rounded_to_next_10",

            "name":"Net Taxable Income (Rounded to Next 10)",
            "amount":net_taxable_income
        },

        {
            "key": "income_tax_on_net_taxable_income",
            "name":"Income Tax on Net Taxable Income (Before Rebate U/s 87A)",
            "amount":income_tax_on_net_taxable_income
        },

        {
            "key": "rebate",
            "name":"Rebate (U/s 87A)",
            "amount":rebate
        },

        {
            "key": "income_tax_after_rebate",
            "name":"Income Tax After Rebate (u/s 87A)/Marginal Relief under New Tax Regime",
            "amount":0
        },
        {
            "key": "surcharge",
            "name":"Raw Surcharge",
            "amount":surcharge
        },
        {
            "key": "marginal_relief",
            "name":"Marginal Relief",
            "amount":marginal_relief
        },
        {
            "key": "cess_fee",
            "name":"Add Edn Cess + Health Cess @ 4%",
            "amount":education_cess
        },
        {
            "key": "net_tax_payable",
            "name":"Net Tax Payable (A)",
            "amount":total_tax_payable
        },
        {
            "key": "previous_employer_tds",
            "name":"Previous Employer TDS (B)",
            "amount":previous_tds_deducted_value
        },
        {
            "key": "advance_tax",
            "name":"Outside Tax / Advance Tax (C)",
            "amount":advance_tax
        },
        {
            "key": "tax_deducted_till_date_by_current_employer",
            "name":"Tax Deducted till Date by Current Employer (D)",
            "amount":tds_sum
        },
        {
            "key": "remaining_tax",
            "name":"Remaining Tax (A - B - C - D)",
            "amount":remaining_tax
        },

        {
            "key": "remaining_months",
            "name":"Remaining Months",
            "amount":num_months
        },
        {
            "key": "monthly_tds",
            "name":"Monthly TDS",
            "amount":remaining_tax/num_months
        },

    ]


}



def calculate_tax_by_tax_slab(annual_taxable_earning,tax_slab,eval_globals=None,eval_locals=None):
    eval_globals = eval_globals or {}
    eval_locals = eval_locals or {}


    if isinstance(tax_slab, str):
        tax_slab = frappe.get_doc("Income Tax Slab", tax_slab)

    eval_locals.update({
        "annual_taxable_earning": annual_taxable_earning,
        "annual_taxable_amount": annual_taxable_earning, 
    })


    base_tax = 0
    rebate = 0
    surcharge = 0
    charge_percent = 0
    education_cess_amount = 0
    total_tax_payable = 0
    excess_income=0
    marginal_relief=0


    for slab in tax_slab.slabs:
        cond = cstr(slab.condition).strip()
        if cond and not eval_tax_slab_condition(cond, eval_globals, eval_locals):
            continue

        from_amt = slab.from_amount
        to_amt = slab.to_amount or annual_taxable_earning
        rate = slab.percent_deduction * 0.01


        if annual_taxable_earning > from_amt:

            taxable_range = min(annual_taxable_earning, to_amt) - from_amt
            base_tax += taxable_range * rate


    if (
        tax_slab.custom_marginal_relief_applicable
        and tax_slab.custom_minmum_value
        and tax_slab.custom_maximun_value
    ):
        if (
            tax_slab.custom_minmum_value
            < annual_taxable_earning
            < tax_slab.custom_maximun_value
        ):
            excess_income = annual_taxable_earning - tax_slab.custom_minmum_value
            marginal_relief = base_tax-(annual_taxable_earning- tax_slab.custom_minmum_value)
            if base_tax > excess_income:
                base_tax = excess_income


    
   

    for d in tax_slab.other_taxes_and_charges:
        if d.custom_is_education_cess == 0:
            min_value = flt(d.min_taxable_income) or 0
            max_value = flt(d.max_taxable_income) or None

            if annual_taxable_earning >= min_value and (
                not max_value or annual_taxable_earning < max_value
            ):
                charge_percent = flt(d.percent)
                surcharge = (base_tax * charge_percent) / 100.0

    for d in tax_slab.other_taxes_and_charges:
        if d.custom_is_education_cess == 1:
            total_tax_before_cess = base_tax + surcharge

            education_cess_amount = (total_tax_before_cess * flt(d.percent)) / 100.0

    total_tax_payable = round(education_cess_amount + surcharge + base_tax)


    return {
        "base_tax": round(base_tax, 2),
        "education_cess_amount": round(education_cess_amount, 2),
        "surcharge": round(surcharge, 2),
        "total_tax_payable":round(total_tax_payable,2),
        "marginal_relief":round(marginal_relief,2),
    }



#http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.tds_projection.update_declaration_form?declaration_id=HR-TAX-DEC-2025-00009
#BODY------------------
# {
#   "declaration_id": "HR-TAX-DEC-2025-00009",
#   "data": {
#   "monthly_house_rent": 20000,
#   "rented_in_metro_city":1,
#   "start_date": "2025-01-01,
#   "end_date": "2025-12-31,
#   "pan":"12223",
#   "address_title1":"test",
#   "address_title2":"test,

#   "company":"PW",
#   "payroll_period":"25-26",
#   "employee":"37001",
#   "go_head_with_new_regime":0,
#     "declarations": [
#       {
#         "exemption_category": "EXEMPT U/S 80C, 80CCC & 80 CCD",
#         "exemption_sub_category": "VPF Contribution",
#         "amount": 50000,
#         "max_amount": 50000
#       },
#       {
#         "exemption_category": "EXEMPT U/S 80C, 80CCC & 80 CCD",
#         "exemption_sub_category": "ULIP Premium",
#         "amount": 25000,
#         "max_amount": 25000
#       }
#     ]
#   }
# }




@frappe.whitelist()
def update_declaration_form(declaration_id=None,data=None,doctype=None,proof_id=None,employee=None,company=None,payroll_period=None):

    # ------------------ Resolve data payload safely ------------------
    if not data:
        data = frappe.form_dict.get("data")

    if isinstance(data, str):
        data = frappe.parse_json(data)



    if doctype == "Employee Tax Exemption Declaration" and declaration_id:

        declaration = frappe.get_doc(
            "Employee Tax Exemption Declaration",
            declaration_id
        )

        company = declaration.company
        employee = declaration.employee
        payroll_period = declaration.payroll_period

        # -------- HRA fields --------
        declaration.monthly_house_rent = data.get("monthly_house_rent")
        declaration.rented_in_metro_city = data.get("rented_in_metro_city")
        declaration.custom_start_date = data.get("start_date")
        declaration.custom_end_date = data.get("end_date")
        declaration.custom_pan = data.get("pan")
        declaration.custom_address_title1 = data.get("address_title1")
        declaration.custom_address_title2 = data.get("address_title2")
        declaration.custom_name=data.get("custom_name")
        declaration.custom_hra_proof_attach = data.get("attach_proof")

        # -------- Regime --------
        go_head_with_new_regime = data.get("go_head_with_new_regime", 0)
        selected_regime = "New Regime" if go_head_with_new_regime == 1 else "Old Regime"

        income_tax_slab = frappe.get_list(
            "Income Tax Slab",
            filters={
                "disabled": 0,
                "company": company,
                "custom_select_regime": selected_regime,
                "docstatus": 1,
            },
            fields=["name", "custom_select_regime"],
            order_by="effective_from desc",
            limit=1,
        )

        if not income_tax_slab:
            frappe.throw(f"No active Income Tax Slab found for {selected_regime}")

        declaration.custom_income_tax = income_tax_slab[0].name
        declaration.custom_tax_regime = income_tax_slab[0].custom_select_regime

        # -------- Child table --------
        declaration.set("declarations", [])

        for row in data.get("declarations", []):
            declaration.append("declarations", {
                "exemption_category": row.get("exemption_category"),
                "exemption_sub_category": row.get("exemption_sub_category"),
                "amount": row.get("amount"),
                "max_amount": row.get("max_amount"),
                "custom_attach":row.get("attach_proof"),
            })

        declaration.save(ignore_permissions=True)

        # -------- Update Salary Structure Assignment --------
        latest_assignment = frappe.get_list(
            "Salary Structure Assignment",
            filters={
                "employee": employee,
                "company": company,
                "custom_payroll_period": payroll_period,
                "docstatus": 1,
            },
            fields=["name"],
            order_by="from_date desc",
            limit=1,
        )

        if latest_assignment:
            assignment_doc = frappe.get_doc(
                "Salary Structure Assignment",
                latest_assignment[0].name
            )
            assignment_doc.income_tax_slab = income_tax_slab[0].name
            assignment_doc.custom_tax_regime = selected_regime
            assignment_doc.save(ignore_permissions=True)

        frappe.db.commit()

        return {
            "status": "success",
            "message": "Declaration updated successfully",
            "tax_regime": selected_regime,
            "income_tax_slab": income_tax_slab[0].name,
        }


    elif doctype == "Employee Tax Exemption Proof Submission" and declaration_id and not proof_id:


        declaration = frappe.get_doc(
            "Employee Tax Exemption Declaration",
            declaration_id
        )

        company = declaration.company
        employee = declaration.employee
        payroll_period = declaration.payroll_period

        # -------- Regime --------
        go_head_with_new_regime = data.get("go_head_with_new_regime", 0)
        selected_regime = "New Regime" if go_head_with_new_regime == 1 else "Old Regime"

        # -------- Income Tax Slab --------
        income_tax_slab = frappe.get_list(
            "Income Tax Slab",
            filters={
                "disabled": 0,
                "company": company,
                "custom_select_regime": selected_regime,
                "docstatus": 1,
            },
            fields=["name"],
            order_by="effective_from desc",
            limit=1,
        )

        if not income_tax_slab:
            frappe.throw(f"No active Income Tax Slab found for {selected_regime}")

        # -------- Create Proof Submission --------
        proof_doc = frappe.new_doc("Employee Tax Exemption Proof Submission")
        proof_doc.custom_declaration_id = declaration_id
        proof_doc.company = company
        proof_doc.employee = employee
        proof_doc.payroll_period = payroll_period
        proof_doc.custom_income_tax = income_tax_slab[0].name
        proof_doc.custom_tax_regime = selected_regime
        proof_doc.submission_date = frappe.utils.nowdate()

        # -------- HRA fields --------
        proof_doc.house_rent_payment_amount = data.get("monthly_house_rent")
        proof_doc.rented_in_metro_city = data.get("rented_in_metro_city")
        proof_doc.rented_from_date = data.get("start_date")
        proof_doc.rented_to_date = data.get("end_date")
        proof_doc.custom_pan = data.get("pan")
        proof_doc.custom_address_title1 = data.get("address_title1")
        proof_doc.custom_address_title2 = data.get("address_title2")
        proof_doc.custom_hra_proof_attach = data.get("attach_proof")
        proof_doc.custom_name=data.get("custom_name")

        # -------- Child table --------
        proof_doc.set("tax_exemption_proofs", [])

        for row in data.get("declarations", []):
            proof_doc.append("tax_exemption_proofs", {
                "exemption_category": row.get("exemption_category"),
                "exemption_sub_category": row.get("exemption_sub_category"),
                "amount": row.get("amount"),
                "max_amount": row.get("max_amount"),
                "attach_proof": row.get("attach_proof"),
                "custom_note": row.get("custom_note"),
            })


        proof_doc.insert()
        # proof_doc.submit()
        frappe.db.commit()

        return {
            "status": "success",
            "message": "Proof Submission created successfully",
            "proof_id": proof_doc.name,
        }


    elif doctype == "Employee Tax Exemption Proof Submission" and declaration_id and proof_id:

        # ------------------ Parse & Validate data ------------------
        if not data:
            frappe.throw("Data payload is required")

        if isinstance(data, str):
            data = frappe.parse_json(data)


        company = company
        employee = employee
        payroll_period = payroll_period

        # ------------------ Tax Regime ------------------
        go_head_with_new_regime = data.get("go_head_with_new_regime", 0)
        selected_regime = "New Regime" if go_head_with_new_regime == 1 else "Old Regime"

        # ------------------ Income Tax Slab ------------------
        income_tax_slab = frappe.get_list(
            "Income Tax Slab",
            filters={
                "disabled": 0,
                "company": company,
                "custom_select_regime": selected_regime,
                "docstatus": 1,
            },
            fields=["name"],
            order_by="effective_from desc",
            limit=1,
        )

        if not income_tax_slab:
            frappe.throw(f"No active Income Tax Slab found for {selected_regime}")


        proof_doc = frappe.get_doc(
            "Employee Tax Exemption Proof Submission",
            proof_id
        )


        proof_doc.custom_income_tax = income_tax_slab[0].name
        proof_doc.custom_tax_regime = selected_regime

        # ------------------ HRA Fields ------------------
        proof_doc.house_rent_payment_amount = data.get("monthly_house_rent")
        proof_doc.rented_in_metro_city = data.get("rented_in_metro_city")
        proof_doc.rented_from_date = data.get("start_date")
        proof_doc.rented_to_date = data.get("end_date")
        proof_doc.custom_pan = data.get("pan")
        proof_doc.custom_address_title1 = data.get("address_title1")
        proof_doc.custom_address_title2 = data.get("address_title2")
        proof_doc.custom_hra_proof_attach = data.get("attach_proof")
        proof_doc.custom_name=data.get("custom_name")

        # ------------------ Child Table ------------------
        proof_doc.set("tax_exemption_proofs", [])

        for row in data.get("declarations", []):
            proof_doc.append("tax_exemption_proofs", {
                "exemption_category": row.get("exemption_category"),
                "exemption_sub_category": row.get("exemption_sub_category"),
                "amount": row.get("amount"),
                "max_amount": row.get("max_amount"),
                "attach_proof": row.get("attach_proof"),
                "custom_note": row.get("custom_note"),
            })

        # ------------------ Save ------------------

        proof_doc.save()
        message = "Proof Submission updated successfully"

        frappe.db.commit()


        return {
            "status": "success",
            "message": message,
            "proof_id": proof_doc.name,
        }













# http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.tds_projection.calculate_tds_projection?declaration_id=HR-TAX-DEC-2025-00009
@frappe.whitelist()
def calculate_tds_projection(declaration_id):

    current_taxable_earnings_old_regime = 0
    current_taxable_earnings_new_regime = 0
    future_taxable_earnings_old_regime = 0
    future_taxable_earnings_new_regime = 0
    loan_perquisite_component=None
    loan_perquisite_amount=0
    pt_amount=0
    pf_amount=0
    nps_amount=0

    old_regime_standard_value = 0
    new_regime_standard_value = 0

    hra_exemptions = 0

    eighty_c_maximum_limit = 0

    old_regime_annual_taxable_income=0
    new_regime_annual_taxable_income=0

    month_count=0
    num_months=0

    total_new_regime_deductions = 0
    total_old_regime_deductions = 0

    new_tax_slab=None
    old_tax_slab=None

    tds_income_from_previous_employer=0
    tds_deducted_from_previuos_employer=0
    total_tax_already_paid=0



    declaration = frappe.get_doc(
        "Employee Tax Exemption Declaration",
        declaration_id
    )

    advance_tax_deducted=declaration.custom_tds_already_deducted_amount if declaration.custom_tds_already_deducted_amount else 0
    tds_income_from_previous_employer=declaration.custom_total_taxable_income
    tds_deducted_from_previuos_employer=declaration.custom_total_tds_deducted_value

    company = declaration.company
    employee = declaration.employee
    payroll_period = declaration.payroll_period

    custom_income_tax = declaration.custom_income_tax
    custom_tax_regime = declaration.custom_tax_regime


    



    if employee:

        latest_salary_structure = frappe.get_list(
            "Salary Structure Assignment",
            filters={
                "employee": employee,
                "docstatus": 1,
                "custom_payroll_period": payroll_period,
            },
            fields=["*"],
            order_by="from_date desc",
        )

        if latest_salary_structure:
            assignment = latest_salary_structure[0]
            employee_doc=frappe.get_doc("Employee", assignment.employee)
            get_payroll_period = frappe.get_doc("Payroll Period", assignment.custom_payroll_period)

            effective_start_date = assignment.from_date
            payroll_end_date = get_payroll_period.end_date
            payroll_start_date = get_payroll_period.start_date
            doj = employee_doc.date_of_joining

            start_candidates = [d for d in [effective_start_date, payroll_start_date, doj] if d]
            start = max(datetime.strptime(str(d), "%Y-%m-%d").date() if isinstance(d, str) else d for d in start_candidates)
            end = datetime.strptime(str(payroll_end_date), "%Y-%m-%d").date() if isinstance(payroll_end_date, str) else payroll_end_date

            num_months = (end.year - start.year) * 12 + (end.month - start.month) + 1



            loan_repayments = frappe.get_list(
                "Loan Repayment Schedule",
                filters={
                    "custom_employee": employee,
                    "status": "Active",
                    "docstatus": 1,
                },
                fields=["*"],
            )

            if loan_repayments:
                loan_perquisite_component="Loan Perquisite"
                for repayment in loan_repayments:
                    get_each_perquisite = frappe.get_doc(
                        "Loan Repayment Schedule", repayment.name
                    )
                    if len(get_each_perquisite.custom_loan_perquisite) > 0:
                        for date in get_each_perquisite.custom_loan_perquisite:
                            payment_date = frappe.utils.getdate(
                                date.payment_date
                            )
                            if payroll_start_date <= payment_date <= payroll_end_date:
                                loan_perquisite_amount += date.perquisite_amount

            else:
                loan_perquisite_component="Loan Perquisite"
                loan_perquisite_amount=0

        get_exemption_category = frappe.get_list(
            "Employee Tax Exemption Category",
            filters={
                "custom_select_section": "80 C",

                "is_active": 1,
            },
            fields=["*"],
        )
        if get_exemption_category:
            eighty_c_maximum_limit = get_exemption_category[0].max_amount



        if custom_tax_regime == "Old Regime" and declaration.monthly_house_rent:
            hra_exemptions = declaration.annual_hra_exemption


        latest_tax_slab_old_regime = frappe.get_list(
            "Income Tax Slab",
            filters={
                "company": company,
                "docstatus": 1,
                "disabled": 0,
                "custom_select_regime": "Old Regime",
            },
            fields=["name", "custom_select_regime", "standard_tax_exemption_amount"],
            order_by="effective_from DESC",
            limit=1,
        )

        if latest_tax_slab_old_regime:
            old_regime_standard_value = latest_tax_slab_old_regime[0].standard_tax_exemption_amount
            old_tax_slab=latest_tax_slab_old_regime[0].name

        latest_tax_slab_new_regime = frappe.get_list(
            "Income Tax Slab",
            filters={
                "company":company,
                "docstatus": 1,
                "disabled": 0,
                "custom_select_regime": "New Regime",
            },
            fields=["name", "custom_select_regime", "standard_tax_exemption_amount"],
            order_by="effective_from DESC",
            limit=1,
        )

        if latest_tax_slab_new_regime:
            new_regime_standard_value = latest_tax_slab_new_regime[0].standard_tax_exemption_amount
            new_tax_slab=latest_tax_slab_new_regime[0].name


        # return employee,payroll_period

        get_all_salary_slip = frappe.get_list(
            "Salary Slip",
            filters={
                "employee": employee,
                "custom_payroll_period": payroll_period,
                "docstatus": ["in", [0,1]],
            },
            fields=["*"],
            order_by="end_date desc",
        )
        if not get_all_salary_slip:

            salary_slip_preview = make_salary_slip(
                source_name=assignment.salary_structure,
                employee=employee,
                print_format="Salary Slip Standard",
                posting_date=assignment.from_date,
                for_preview=1,
                )
            if salary_slip_preview:
                for earning in salary_slip_preview.earnings:
                    earning_component_data = frappe.get_doc(
                        "Salary Component", earning.salary_component
                    )

                    if (
                        earning_component_data.is_tax_applicable == 1
                        and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                        and earning_component_data.custom_regime == "All"
                        and earning_component_data.custom_component_sub_type== "Fixed"

                    ):

                        future_taxable_earnings_old_regime += earning.amount * (
                            num_months
                        )
                        future_taxable_earnings_new_regime += earning.amount * (
                            num_months
                        )


                    if (
                            earning_component_data.is_tax_applicable == 1
                            and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                            and earning_component_data.custom_regime == "Old Regime"
                            and earning_component_data.custom_component_sub_type== "Fixed"

                        ):
                            future_taxable_earnings_old_regime += earning.amount * (
                            num_months
                        )


                    if (
                            earning_component_data.is_tax_applicable == 1
                            and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                            and earning_component_data.custom_regime == "New Regime"
                            and earning_component_data.custom_component_sub_type== "Fixed"

                        ):

                            future_taxable_earnings_new_regime += earning.amount * (
                                num_months
                            )

                    if (
                            earning_component_data.is_tax_applicable == 1
                            and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                            and earning_component_data.custom_regime == "All"
                            and earning_component_data.custom_component_sub_type== "Fixed"
                            and earning_component_data.component_type =="NPS"


                        ):
                        nps_amount+=earning.amount*(num_months)


                for deduction in salary_slip_preview.deductions:
                    deduction_component_data = frappe.get_doc(
                        "Salary Component", deduction.salary_component
                    )
                    if (
                            deduction_component_data.component_type =="Professional Tax"
                            and deduction_component_data.custom_component_sub_type== "Fixed"

                        ):
                        pt_amount+=deduction.amount*(num_months)

                    if (
                            deduction_component_data.component_type =="Provident Fund"
                            and deduction_component_data.custom_component_sub_type== "Fixed"

                        ):

                        pf_amount+=deduction.amount*(num_months)


        else:

            for slip in get_all_salary_slip:
                total_tax_already_paid += slip.get("current_month_income_tax") or 0

            month_count=get_all_salary_slip[0].custom_month_count
            for slip in get_all_salary_slip:
                get_each_sslip= frappe.get_doc("Salary Slip", slip.name)
                for earning in get_each_sslip.earnings:
                    earning_component_data = frappe.get_doc(
                        "Salary Component", earning.salary_component
                    )

                    if (
                        earning_component_data.is_tax_applicable == 1
                        and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                        and earning_component_data.custom_regime == "All"


                    ):
                        current_taxable_earnings_old_regime += earning.amount
                        current_taxable_earnings_new_regime += earning.amount




                    if (
                            earning_component_data.is_tax_applicable == 1
                            and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                            and earning_component_data.custom_regime == "Old Regime"


                        ):
                            current_taxable_earnings_old_regime += earning.amount



                    if (
                            earning_component_data.is_tax_applicable == 1
                            and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                            and earning_component_data.custom_regime == "New Regime"


                        ):

                            current_taxable_earnings_new_regime += earning.amount



                    if (
                            earning_component_data.is_tax_applicable == 1
                            and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                            and earning_component_data.custom_regime == "All"

                            and earning_component_data.component_type =="NPS"


                        ):
                        nps_amount+=earning.amount

                for deduction in get_each_sslip.deductions:
                    deduction_component_data = frappe.get_doc(
                        "Salary Component", deduction.salary_component
                    )
                    if (
                            deduction_component_data.component_type =="Professional Tax"


                        ):
                        pt_amount+=deduction.amount

                    if (
                            deduction_component_data.component_type =="Provident Fund"


                        ):

                        pf_amount+=deduction.amount

            salary_slip_preview = make_salary_slip(
                source_name=assignment.salary_structure,
                employee=employee,
                print_format="Salary Slip Standard",
                posting_date=assignment.from_date,
                for_preview=1,
                )
            if salary_slip_preview:
                for earning in salary_slip_preview.earnings:
                    earning_component_data = frappe.get_doc(
                        "Salary Component", earning.salary_component
                    )

                    if (
                        earning_component_data.is_tax_applicable == 1
                        and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                        and earning_component_data.custom_regime == "All"
                        and earning_component_data.custom_component_sub_type== "Fixed"

                    ):

                        future_taxable_earnings_old_regime += earning.amount * (
                            month_count
                        )
                        future_taxable_earnings_new_regime += earning.amount * (
                            month_count
                        )


                    if (
                            earning_component_data.is_tax_applicable == 1
                            and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                            and earning_component_data.custom_regime == "Old Regime"
                            and earning_component_data.custom_component_sub_type== "Fixed"

                        ):
                            future_taxable_earnings_old_regime += earning.amount * (
                            month_count
                        )


                    if (
                            earning_component_data.is_tax_applicable == 1
                            and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                            and earning_component_data.custom_regime == "New Regime"
                            and earning_component_data.custom_component_sub_type== "Fixed"

                        ):

                            future_taxable_earnings_new_regime += earning.amount * (
                                month_count
                            )

                    if (
                            earning_component_data.is_tax_applicable == 1
                            and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                            and earning_component_data.custom_regime == "All"
                            and earning_component_data.custom_component_sub_type== "Fixed"
                            and earning_component_data.component_type =="NPS"


                        ):
                        nps_amount+=earning.amount*(month_count)


                for deduction in salary_slip_preview.deductions:
                    deduction_component_data = frappe.get_doc(
                        "Salary Component", deduction.salary_component
                    )
                    if (
                            deduction_component_data.component_type =="Professional Tax"
                            and deduction_component_data.custom_component_sub_type== "Fixed"

                        ):
                        pt_amount+=deduction.amount*(month_count)

                    if (
                            deduction_component_data.component_type =="Provident Fund"
                            and deduction_component_data.custom_component_sub_type== "Fixed"

                        ):

                        pf_amount+=deduction.amount*(month_count)


        pf_max_amount=min(eighty_c_maximum_limit, pf_amount)



        if custom_tax_regime == "Old Regime" :
            total_new_regime_deductions = nps_amount
            total_old_regime_deductions = (declaration.total_exemption_amount)-(pt_amount)
        if custom_tax_regime == "New Regime" :
            total_new_regime_deductions = declaration.total_exemption_amount
            total_old_regime_deductions = pf_max_amount + pt_amount + nps_amount





        old_regime_annual_taxable_income =(
            round(current_taxable_earnings_old_regime + future_taxable_earnings_old_regime + loan_perquisite_amount+tds_income_from_previous_employer)
            - round(pt_amount)
            - old_regime_standard_value
            - round(total_old_regime_deductions)

        )

        new_regime_annual_taxable_income =(
            round(current_taxable_earnings_new_regime + future_taxable_earnings_new_regime + loan_perquisite_amount+tds_income_from_previous_employer)
            - new_regime_standard_value
            - round(total_new_regime_deductions)

        )

# 



        eval_globals = frappe._dict()
        eval_locals = frappe._dict()


        old_tax_slab_doc = frappe.get_doc("Income Tax Slab", old_tax_slab)

        old_slab_result = calculate_tax_by_tax_slab(
            old_regime_annual_taxable_income,
            old_tax_slab_doc,
            eval_globals,
            eval_locals,
        )



        new_tax_slab_doc = frappe.get_doc("Income Tax Slab", new_tax_slab)

        new_slab_result = calculate_tax_by_tax_slab(
            new_regime_annual_taxable_income,
            new_tax_slab_doc,
            eval_globals,
            eval_locals,
        )

        # safe_month_count = month_count if month_count else num_months
        safe_month_count = month_count if month_count else num_months or 1

        balance_tax_payable_old_regime = (
            round(old_slab_result.get("total_tax_payable"))
            - tds_deducted_from_previuos_employer
            - advance_tax_deducted
            - total_tax_already_paid
        )

        balance_tax_payable_new_regime = (
            round(new_slab_result.get("total_tax_payable"))
            - tds_deducted_from_previuos_employer
            - advance_tax_deducted
            - total_tax_already_paid
        )

        return {
                


                "num_months": num_months if num_months else 0,
                "month_count": month_count if month_count else num_months,
                "tds_income_from_previous_employer":round(tds_income_from_previous_employer),
                "tds_deducted_from_previuos_employer":round(tds_deducted_from_previuos_employer),
                
                "current_taxable_earnings_old_regime":round(current_taxable_earnings_old_regime),
                "current_taxable_earnings_new_regime":round(current_taxable_earnings_new_regime),
                "future_taxable_earnings_new_regime":round(future_taxable_earnings_new_regime),
                "future_taxable_earnings_old_regime":round(future_taxable_earnings_old_regime),
                "loan_perquisite_component":loan_perquisite_component,
                "loan_perquisite_amount":round(loan_perquisite_amount),
                "total_taxable_earnings_old_regime": round(current_taxable_earnings_old_regime + future_taxable_earnings_old_regime + loan_perquisite_amount+tds_income_from_previous_employer),
                "total_taxable_earnings_new_regime": round(current_taxable_earnings_new_regime + future_taxable_earnings_new_regime + loan_perquisite_amount+tds_income_from_previous_employer),
                "pt_amount":round(pt_amount),

                "old_regime_standard_value": old_regime_standard_value,
                "new_regime_standard_value": new_regime_standard_value,

                "old_regime_total":old_regime_standard_value+pt_amount,
                "new_regime_total":new_regime_standard_value,

                "hra_exemptions": hra_exemptions,

                "total_old_regime_deductions": round(total_old_regime_deductions),
                "total_new_regime_deductions": round(total_new_regime_deductions),

                "old_regime_annual_taxable_income": round(old_regime_annual_taxable_income),
                "new_regime_annual_taxable_income": round(new_regime_annual_taxable_income),
                "advance_tax":advance_tax_deducted,


                "old_regime_total_tax_on_income":round(old_slab_result.get("base_tax")),
                "old_regime_surcharge": round(old_slab_result.get("surcharge")),
                "old_regime_education_cess": round(old_slab_result.get("education_cess_amount")),
                "old_regime_total_tax_payable":round(old_slab_result.get("total_tax_payable")),
                "old_marginal_relief":round(old_slab_result.get("marginal_relief")),

                "tds_deducted_from_previuos_employer":tds_deducted_from_previuos_employer,


                "new_regime_total_tax_on_income":round(new_slab_result.get("base_tax")),
                "new_regime_surcharge": round(new_slab_result.get("surcharge")),
                "new_regime_education_cess": round(new_slab_result.get("education_cess_amount")),
                "new_regime_total_tax_payable":round(new_slab_result.get("total_tax_payable")),
                "new_marginal_relief":round(new_slab_result.get("marginal_relief")),
                "total_tax_already_paid":round(total_tax_already_paid),

                "balance_tax_payable_old_regime":round(balance_tax_payable_old_regime),
                "balance_tax_payable_new_regime":round(balance_tax_payable_new_regime),


                "balance_month":safe_month_count,
                "old_regime_current_tax": (
                    round(balance_tax_payable_old_regime / safe_month_count)
                    if safe_month_count else 0
                ),

                "new_regime_current_tax": (
                    round(balance_tax_payable_new_regime / safe_month_count)
                    if safe_month_count else 0
                ),               


                }
















# http://127.0.0.1:8002/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.tds_projection.download_tds_poi_projection_pdf?proof_id=HR-TAX-PRF-2026-00001

@frappe.whitelist()
def calculate_tds_projection_poi(proof_id):


    current_taxable_earnings_old_regime = 0
    current_taxable_earnings_new_regime = 0
    future_taxable_earnings_old_regime = 0
    future_taxable_earnings_new_regime = 0
    loan_perquisite_component=None
    loan_perquisite_amount=0
    pt_amount=0
    pf_amount=0
    nps_amount=0

    old_regime_standard_value = 0
    new_regime_standard_value = 0

    hra_exemptions = 0

    eighty_c_maximum_limit = 0

    old_regime_annual_taxable_income=0
    new_regime_annual_taxable_income=0

    month_count=0
    num_months=0

    total_new_regime_deductions = 0
    total_old_regime_deductions = 0
    tds_income_from_previous_employer=0
    tds_deducted_from_previuos_employer=0
    total_tax_already_paid=0


    declaration = frappe.get_doc(
        "Employee Tax Exemption Proof Submission",
        proof_id
    )

    advance_tax_deducted=declaration.custom_tds_already_deducted_amount if declaration.custom_tds_already_deducted_amount else 0
    tds_income_from_previous_employer=declaration.custom_tds_from_previous_employer
    tds_deducted_from_previuos_employer=declaration.custom_tds_deducted_from_previous_employer

    company = declaration.company
    employee = declaration.employee
    payroll_period = declaration.payroll_period

    custom_income_tax = declaration.custom_income_tax
    custom_tax_regime = declaration.custom_tax_regime


    
    if employee:

        latest_salary_structure = frappe.get_list(
            "Salary Structure Assignment",
            filters={
                "employee": employee,
                "docstatus": 1,
                "custom_payroll_period": payroll_period,
            },
            fields=["*"],
            order_by="from_date desc",
        )

        if latest_salary_structure:
            assignment = latest_salary_structure[0]
            employee_doc=frappe.get_doc("Employee", assignment.employee)
            get_payroll_period = frappe.get_doc("Payroll Period", assignment.custom_payroll_period)

            effective_start_date = assignment.from_date
            payroll_end_date = get_payroll_period.end_date
            payroll_start_date = get_payroll_period.start_date
            doj = employee_doc.date_of_joining

            start_candidates = [d for d in [effective_start_date, payroll_start_date, doj] if d]
            start = max(datetime.strptime(str(d), "%Y-%m-%d").date() if isinstance(d, str) else d for d in start_candidates)
            end = datetime.strptime(str(payroll_end_date), "%Y-%m-%d").date() if isinstance(payroll_end_date, str) else payroll_end_date

            num_months = (end.year - start.year) * 12 + (end.month - start.month) + 1



            loan_repayments = frappe.get_list(
                "Loan Repayment Schedule",
                filters={
                    "custom_employee": employee,
                    "status": "Active",
                    "docstatus": 1,
                },
                fields=["*"],
            )

            if loan_repayments:
                loan_perquisite_component="Loan Perquisite"
                for repayment in loan_repayments:
                    get_each_perquisite = frappe.get_doc(
                        "Loan Repayment Schedule", repayment.name
                    )
                    if len(get_each_perquisite.custom_loan_perquisite) > 0:
                        for date in get_each_perquisite.custom_loan_perquisite:
                            payment_date = frappe.utils.getdate(
                                date.payment_date
                            )
                            if payroll_start_date <= payment_date <= payroll_end_date:
                                loan_perquisite_amount += date.perquisite_amount

            else:
                loan_perquisite_component="Loan Perquisite"
                loan_perquisite_amount=0

        get_exemption_category = frappe.get_list(
            "Employee Tax Exemption Category",
            filters={
                "custom_select_section": "80 C",

                "is_active": 1,
            },
            fields=["*"],
        )
        if get_exemption_category:
            eighty_c_maximum_limit = get_exemption_category[0].max_amount



        if custom_tax_regime == "Old Regime" and declaration.house_rent_payment_amount:
            hra_exemptions = declaration.custom_annual_hra_exemption


        latest_tax_slab_old_regime = frappe.get_list(
            "Income Tax Slab",
            filters={
                "company": company,
                "docstatus": 1,
                "disabled": 0,
                "custom_select_regime": "Old Regime",
            },
            fields=["name", "custom_select_regime", "standard_tax_exemption_amount"],
            order_by="effective_from DESC",
            limit=1,
        )

        if latest_tax_slab_old_regime:
            old_regime_standard_value = latest_tax_slab_old_regime[0].standard_tax_exemption_amount
            old_tax_slab=latest_tax_slab_old_regime[0].name

        latest_tax_slab_new_regime = frappe.get_list(
            "Income Tax Slab",
            filters={
                "company":company,
                "docstatus": 1,
                "disabled": 0,
                "custom_select_regime": "New Regime",
            },
            fields=["name", "custom_select_regime", "standard_tax_exemption_amount"],
            order_by="effective_from DESC",
            limit=1,
        )

        if latest_tax_slab_new_regime:
            new_regime_standard_value = latest_tax_slab_new_regime[0].standard_tax_exemption_amount
            new_tax_slab=latest_tax_slab_old_regime[0].name


        # return employee,payroll_period

        get_all_salary_slip = frappe.get_list(
            "Salary Slip",
            filters={
                "employee": employee,
                "custom_payroll_period": payroll_period,
                "docstatus": ["in", [0,1]],
            },
            fields=["*"],
            order_by="end_date desc",
        )
        if not get_all_salary_slip:

            salary_slip_preview = make_salary_slip(
                source_name=assignment.salary_structure,
                employee=employee,
                print_format="Salary Slip Standard",
                posting_date=assignment.from_date,
                for_preview=1,
                )
            if salary_slip_preview:
                for earning in salary_slip_preview.earnings:
                    earning_component_data = frappe.get_doc(
                        "Salary Component", earning.salary_component
                    )

                    if (
                        earning_component_data.is_tax_applicable == 1
                        and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                        and earning_component_data.custom_regime == "All"
                        and earning_component_data.custom_component_sub_type== "Fixed"

                    ):

                        future_taxable_earnings_old_regime += earning.amount * (
                            num_months
                        )
                        future_taxable_earnings_new_regime += earning.amount * (
                            num_months
                        )


                    if (
                            earning_component_data.is_tax_applicable == 1
                            and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                            and earning_component_data.custom_regime == "Old Regime"
                            and earning_component_data.custom_component_sub_type== "Fixed"

                        ):
                            future_taxable_earnings_old_regime += earning.amount * (
                            num_months
                        )


                    if (
                            earning_component_data.is_tax_applicable == 1
                            and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                            and earning_component_data.custom_regime == "New Regime"
                            and earning_component_data.custom_component_sub_type== "Fixed"

                        ):

                            future_taxable_earnings_new_regime += earning.amount * (
                                num_months
                            )

                    if (
                            earning_component_data.is_tax_applicable == 1
                            and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                            and earning_component_data.custom_regime == "All"
                            and earning_component_data.custom_component_sub_type== "Fixed"
                            and earning_component_data.component_type =="NPS"


                        ):
                        nps_amount+=earning.amount*(num_months)


                for deduction in salary_slip_preview.deductions:
                    deduction_component_data = frappe.get_doc(
                        "Salary Component", deduction.salary_component
                    )
                    if (
                            deduction_component_data.component_type =="Professional Tax"
                            and deduction_component_data.custom_component_sub_type== "Fixed"

                        ):
                        pt_amount+=deduction.amount*(num_months)

                    if (
                            deduction_component_data.component_type =="Provident Fund"
                            and deduction_component_data.custom_component_sub_type== "Fixed"

                        ):

                        pf_amount+=deduction.amount*(num_months)


        else:
            total_tax_already_paid += slip.get("current_month_income_tax") or 0
            month_count=get_all_salary_slip[0].custom_month_count
            for slip in get_all_salary_slip:
                get_each_sslip= frappe.get_doc("Salary Slip", slip.name)
                for earning in get_each_sslip.earnings:
                    earning_component_data = frappe.get_doc(
                        "Salary Component", earning.salary_component
                    )

                    if (
                        earning_component_data.is_tax_applicable == 1
                        and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                        and earning_component_data.custom_regime == "All"


                    ):
                        current_taxable_earnings_old_regime += earning.amount
                        current_taxable_earnings_new_regime += earning.amount




                    if (
                            earning_component_data.is_tax_applicable == 1
                            and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                            and earning_component_data.custom_regime == "Old Regime"


                        ):
                            current_taxable_earnings_old_regime += earning.amount



                    if (
                            earning_component_data.is_tax_applicable == 1
                            and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                            and earning_component_data.custom_regime == "New Regime"


                        ):

                            current_taxable_earnings_new_regime += earning.amount



                    if (
                            earning_component_data.is_tax_applicable == 1
                            and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                            and earning_component_data.custom_regime == "All"

                            and earning_component_data.component_type =="NPS"


                        ):
                        nps_amount+=earning.amount

                for deduction in get_each_sslip.deductions:
                    deduction_component_data = frappe.get_doc(
                        "Salary Component", deduction.salary_component
                    )
                    if (
                            deduction_component_data.component_type =="Professional Tax"


                        ):
                        pt_amount+=deduction.amount

                    if (
                            deduction_component_data.component_type =="Provident Fund"


                        ):

                        pf_amount+=deduction.amount

            salary_slip_preview = make_salary_slip(
                source_name=assignment.salary_structure,
                employee=employee,
                print_format="Salary Slip Standard",
                posting_date=assignment.from_date,
                for_preview=1,
                )
            if salary_slip_preview:
                for earning in salary_slip_preview.earnings:
                    earning_component_data = frappe.get_doc(
                        "Salary Component", earning.salary_component
                    )

                    if (
                        earning_component_data.is_tax_applicable == 1
                        and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                        and earning_component_data.custom_regime == "All"
                        and earning_component_data.custom_component_sub_type== "Fixed"

                    ):

                        future_taxable_earnings_old_regime += earning.amount * (
                            month_count
                        )
                        future_taxable_earnings_new_regime += earning.amount * (
                            month_count
                        )


                    if (
                            earning_component_data.is_tax_applicable == 1
                            and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                            and earning_component_data.custom_regime == "Old Regime"
                            and earning_component_data.custom_component_sub_type== "Fixed"

                        ):
                            future_taxable_earnings_old_regime += earning.amount * (
                            month_count
                        )


                    if (
                            earning_component_data.is_tax_applicable == 1
                            and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                            and earning_component_data.custom_regime == "New Regime"
                            and earning_component_data.custom_component_sub_type== "Fixed"

                        ):

                            future_taxable_earnings_new_regime += earning.amount * (
                                month_count
                            )

                    if (
                            earning_component_data.is_tax_applicable == 1
                            and earning_component_data.custom_tax_exemption_applicable_based_on_regime== 1
                            and earning_component_data.custom_regime == "All"
                            and earning_component_data.custom_component_sub_type== "Fixed"
                            and earning_component_data.component_type =="NPS"


                        ):
                        nps_amount+=earning.amount*(month_count)


                for deduction in salary_slip_preview.deductions:
                    deduction_component_data = frappe.get_doc(
                        "Salary Component", deduction.salary_component
                    )
                    if (
                            deduction_component_data.component_type =="Professional Tax"
                            and deduction_component_data.custom_component_sub_type== "Fixed"

                        ):
                        pt_amount+=deduction.amount*(month_count)

                    if (
                            deduction_component_data.component_type =="Provident Fund"
                            and deduction_component_data.custom_component_sub_type== "Fixed"

                        ):

                        pf_amount+=deduction.amount*(month_count)


        pf_max_amount=min(eighty_c_maximum_limit, pf_amount)



        if custom_tax_regime == "Old Regime" :
            total_new_regime_deductions = nps_amount
            total_old_regime_deductions = (declaration.exemption_amount)-(pt_amount)
        if custom_tax_regime == "New Regime" :
            total_new_regime_deductions = declaration.exemption_amount
            total_old_regime_deductions = pf_max_amount + pt_amount + nps_amount



        old_regime_annual_taxable_income =(
            round(current_taxable_earnings_old_regime + future_taxable_earnings_old_regime + loan_perquisite_amount+tds_income_from_previous_employer)
            - round(pt_amount)
            - old_regime_standard_value
            - round(total_old_regime_deductions)

        )

        new_regime_annual_taxable_income =(
            round(current_taxable_earnings_new_regime + future_taxable_earnings_new_regime + loan_perquisite_amount+tds_income_from_previous_employer)
            - new_regime_standard_value
            - round(total_new_regime_deductions)

        )



       

        eval_globals = frappe._dict()
        eval_locals = frappe._dict()


        old_tax_slab_doc = frappe.get_doc("Income Tax Slab", old_tax_slab)

        old_slab_result = calculate_tax_by_tax_slab(
            old_regime_annual_taxable_income,
            old_tax_slab_doc,
            eval_globals,
            eval_locals,
        )



        new_tax_slab_doc = frappe.get_doc("Income Tax Slab", new_tax_slab)

        new_slab_result = calculate_tax_by_tax_slab(
            new_regime_annual_taxable_income,
            new_tax_slab_doc,
            eval_globals,
            eval_locals,
        )

        # safe_month_count = month_count if month_count else num_months
        safe_month_count = month_count if month_count else num_months or 1

        balance_tax_payable_old_regime = (
            round(old_slab_result.get("total_tax_payable"))
            - tds_deducted_from_previuos_employer
            - advance_tax_deducted
            - total_tax_already_paid
        )

        balance_tax_payable_new_regime = (
            round(new_slab_result.get("total_tax_payable"))
            - tds_deducted_from_previuos_employer
            - advance_tax_deducted
            - total_tax_already_paid
        )


        return {
                "num_months": num_months if num_months else 0,
                "month_count": month_count if month_count else num_months,
                "current_taxable_earnings_old_regime":round(current_taxable_earnings_old_regime),
                "current_taxable_earnings_new_regime":round(current_taxable_earnings_new_regime),
                "future_taxable_earnings_new_regime":round(future_taxable_earnings_new_regime),
                "future_taxable_earnings_old_regime":round(future_taxable_earnings_old_regime),
                "loan_perquisite_component":loan_perquisite_component,
                "loan_perquisite_amount":round(loan_perquisite_amount),
                "total_taxable_earnings_old_regime": round(current_taxable_earnings_old_regime + future_taxable_earnings_old_regime + loan_perquisite_amount),
                "total_taxable_earnings_new_regime": round(current_taxable_earnings_new_regime + future_taxable_earnings_new_regime + loan_perquisite_amount),
                "pt_amount":round(pt_amount),

                "old_regime_standard_value": old_regime_standard_value,
                "new_regime_standard_value": new_regime_standard_value,

                "old_regime_total":old_regime_standard_value+pt_amount,
                "new_regime_total":new_regime_standard_value,

                "hra_exemptions": hra_exemptions,

                "total_old_regime_deductions": round(total_old_regime_deductions),
                "total_new_regime_deductions": round(total_new_regime_deductions),

                "old_regime_annual_taxable_income": round(old_regime_annual_taxable_income),
                "new_regime_annual_taxable_income": round(new_regime_annual_taxable_income),
                "advance_tax":advance_tax_deducted,



                "old_regime_total_tax_on_income":round(old_slab_result.get("base_tax")),
                "old_regime_surcharge": round(old_slab_result.get("surcharge")),
                "old_regime_education_cess": round(old_slab_result.get("education_cess_amount")),
                "old_regime_total_tax_payable":round(old_slab_result.get("total_tax_payable")),
                "old_marginal_relief":round(old_slab_result.get("marginal_relief")),

                "tds_deducted_from_previuos_employer":tds_deducted_from_previuos_employer,


                "new_regime_total_tax_on_income":round(new_slab_result.get("base_tax")),
                "new_regime_surcharge": round(new_slab_result.get("surcharge")),
                "new_regime_education_cess": round(new_slab_result.get("education_cess_amount")),
                "new_regime_total_tax_payable":round(new_slab_result.get("total_tax_payable")),
                "new_marginal_relief":round(new_slab_result.get("marginal_relief")),
                "total_tax_already_paid":round(total_tax_already_paid),

                "balance_tax_payable_old_regime":round(balance_tax_payable_old_regime),
                "balance_tax_payable_new_regime":round(balance_tax_payable_new_regime),


                "balance_month":safe_month_count,
                "old_regime_current_tax": (
                    round(balance_tax_payable_old_regime / safe_month_count)
                    if safe_month_count else 0
                ),

                "new_regime_current_tax": (
                    round(balance_tax_payable_new_regime / safe_month_count)
                    if safe_month_count else 0
                ),               

                


                }








@frappe.whitelist()
def slab_calculation(
    employee, company, payroll_period, old_annual_slab, new_annual_slab
):
    old_annual_slab = float(old_annual_slab)
    new_annual_slab = float(new_annual_slab)

    latest_tax_slab = frappe.get_list(
        "Income Tax Slab",
        filters={
            "company": company,
            "docstatus": 1,
            "disabled": 0,
            "custom_select_regime": "Old Regime",
        },
        fields=["*"],
        order_by="effective_from DESC",
        limit=1,
    )

    if latest_tax_slab:
        for slab in latest_tax_slab:
            income_doc = frappe.get_doc("Income Tax Slab", slab.name)

            total_value = []
            from_amount = []
            to_amount = []
            percentage = []
            difference = []
            total_array = []

            total_sum = 0
            old_rebate_value = 0
            old_surcharge_m = 0
            old_education_cess = 0

            old_regime_marginal_relief_min_value = 0
            old_regime_marginal_relief_max_value = 0


            old_rebate = income_doc.custom_taxable_income_is_less_than
            old_max_amount = income_doc.custom_maximum_amount

            if (
                income_doc.custom_marginal_relief_applicable
                and income_doc.custom_minmum_value
                and income_doc.custom_maximun_value
            ):
                old_regime_marginal_relief_min_value = income_doc.custom_minmum_value
                old_regime_marginal_relief_max_value = income_doc.custom_maximun_value

            if old_annual_slab > old_rebate:
                # Store all slab details in a structured list
                for i in income_doc.slabs:
                    total_array.append(
                        {
                            "from": i.from_amount,
                            "to": i.to_amount,
                            "percent": i.percent_deduction,
                        }
                    )

                # Iterate through the slabs to calculate tax
                for slab in total_array:
                    if slab["to"] == 0.0:  # Upper limit not defined
                        if round(old_annual_slab) >= slab["from"]:
                            taxable_amount = round(old_annual_slab) - slab["from"]

                            tax_percent = slab["percent"]
                            tax_amount = round((taxable_amount * tax_percent) / 100)

                            remaining_slabs = [
                                s for s in total_array if s["from"] < slab["from"]
                            ]
                            for rem_slab in remaining_slabs:
                                from_amount.append(rem_slab["from"])
                                to_amount.append(rem_slab["to"])
                                percentage.append(rem_slab["percent"])
                                difference.append(rem_slab["to"] - rem_slab["from"])
                                total_value.append(
                                    round(
                                        (rem_slab["to"] - rem_slab["from"])
                                        * rem_slab["percent"]
                                        / 100
                                    )
                                )

                            from_amount.append(slab["from"])
                            to_amount.append(slab["to"])
                            percentage.append(tax_percent)
                            difference.append(taxable_amount)
                            total_value.append(tax_amount)

                    else:  # Standard slab range
                        if slab["from"] <= round(old_annual_slab) <= slab["to"]:
                            taxable_amount = round(old_annual_slab) - slab["from"]
                            tax_percent = slab["percent"]
                            tax_amount = round((taxable_amount * tax_percent) / 100)

                            # Process lower slabs
                            remaining_slabs = [
                                s for s in total_array if s["from"] < slab["from"]
                            ]
                            for rem_slab in remaining_slabs:
                                from_amount.append(rem_slab["from"])
                                to_amount.append(rem_slab["to"])
                                percentage.append(rem_slab["percent"])
                                difference.append(rem_slab["to"] - rem_slab["from"])
                                total_value.append(
                                    round(
                                        (rem_slab["to"] - rem_slab["from"])
                                        * rem_slab["percent"]
                                        / 100
                                    )
                                )

                            from_amount.append(slab["from"])
                            to_amount.append(slab["to"])
                            percentage.append(tax_percent)
                            difference.append(taxable_amount)
                            total_value.append(tax_amount)

                total_sum = sum(total_value)

                final_value = 0
                if (
                    income_doc.custom_marginal_relief_applicable
                    and income_doc.custom_minmum_value
                    and income_doc.custom_maximun_value
                ):
                    if (
                        income_doc.custom_minmum_value
                        < old_annual_slab
                        < income_doc.custom_maximun_value
                    ):
                        old_rebate_value = total_sum - (
                            old_annual_slab - income_doc.custom_minmum_value
                        )
                        final_value = total_sum - old_rebate_value

                        old_education_cess = final_value * 4 / 100

                    else:
                        if old_annual_slab < old_rebate:
                            old_rebate_value = total_sum

                        else:
                            old_rebate_value = 0

                        if old_annual_slab > 5000000:
                            old_surcharge_m = round((total_sum * 10) / 100)
                            old_education_cess = round(
                                (old_surcharge_m + total_sum) * 4 / 100
                            )

                        else:
                            old_surcharge_m = 0
                            old_education_cess = round((0 + total_sum) * 4 / 100)
                else:
                    if old_annual_slab < old_rebate:
                        old_rebate_value = total_sum

                    else:
                        old_rebate_value = 0

                    if old_annual_slab > 5000000:
                        old_surcharge_m = round((total_sum * 10) / 100)
                        old_education_cess = round(
                            (old_surcharge_m + total_sum) * 4 / 100
                        )

                    else:
                        old_surcharge_m = 0
                        old_education_cess = round((0 + total_sum) * 4 / 100)
            else:
                old_rebate_value = 0
                old_surcharge_m = 0
                old_education_cess = 0

    latest_tax_slab_new = frappe.get_list(
        "Income Tax Slab",
        filters={
            "company": company,
            "docstatus": 1,
            "disabled": 0,
            "custom_select_regime": "New Regime",
        },
        fields=["name", "custom_select_regime", "standard_tax_exemption_amount"],
        order_by="effective_from DESC",
        limit=1,
    )

    if latest_tax_slab_new:
        for slab_new in latest_tax_slab_new:
            income_doc_new = frappe.get_doc("Income Tax Slab", slab_new.name)

            # Initialize Lists
            total_value_new = []
            from_amount_new = []
            to_amount_new = []
            percentage_new = []
            difference_new = []
            total_array_new = []

            total_sum_new = 0  # Initialize early to avoid UnboundLocalError
            new_rebate_value = 0
            new_surcharge_m = 0
            new_education_cess = 0

            new_regime_marginal_relief_min_value = 0
            new_regime_marginal_relief_max_value = 0

            # Retrieve Exemption & Maximum Values
            new_rebate = income_doc_new.custom_taxable_income_is_less_than
            new_max_amount = income_doc_new.custom_maximum_amount

            if (
                income_doc_new.custom_marginal_relief_applicable
                and income_doc_new.custom_minmum_value
                and income_doc_new.custom_maximun_value
            ):
                new_regime_marginal_relief_min_value = (
                    income_doc_new.custom_minmum_value
                )
                new_regime_marginal_relief_max_value = (
                    income_doc_new.custom_maximun_value
                )

            if new_annual_slab > new_rebate:
                # Store all slab details in a structured list
                for i in income_doc_new.slabs:
                    total_array_new.append(
                        {
                            "from": i.from_amount,
                            "to": i.to_amount,
                            "percent": i.percent_deduction,
                        }
                    )

                for slab_new in total_array_new:
                    if slab_new["to"] == 0.0:  # Upper limit not defined
                        if round(new_annual_slab) >= slab_new["from"]:
                            taxable_amount_new = (
                                round(new_annual_slab) - slab_new["from"]
                            )
                            tax_percent_new = slab_new["percent"]
                            tax_amount_new = round(
                                (taxable_amount_new * tax_percent_new) / 100
                            )

                            remaining_slabs_new = [
                                s
                                for s in total_array_new
                                if s["from"] < slab_new["from"]
                            ]
                            for rem_slab in remaining_slabs_new:
                                from_amount_new.append(rem_slab["from"])
                                to_amount_new.append(rem_slab["to"])
                                percentage_new.append(rem_slab["percent"])
                                difference_new.append(rem_slab["to"] - rem_slab["from"])
                                total_value_new.append(
                                    round(
                                        (rem_slab["to"] - rem_slab["from"])
                                        * rem_slab["percent"]
                                        / 100
                                    )
                                )

                            from_amount_new.append(slab_new["from"])
                            to_amount_new.append(slab_new["to"])
                            percentage_new.append(tax_percent_new)
                            difference_new.append(taxable_amount_new)
                            total_value_new.append(tax_amount_new)

                    else:  # Standard slab range
                        if slab_new["from"] <= round(new_annual_slab) <= slab_new["to"]:
                            taxable_amount_new = (
                                round(new_annual_slab) - slab_new["from"]
                            )
                            tax_percent_new = slab_new["percent"]
                            tax_amount_new = round(
                                (taxable_amount_new * tax_percent_new) / 100
                            )

                            # Process lower slabs
                            remaining_slabs = [
                                s
                                for s in total_array_new
                                if s["from"] < slab_new["from"]
                            ]
                            for rem_slab in remaining_slabs:
                                from_amount_new.append(rem_slab["from"])
                                to_amount_new.append(rem_slab["to"])
                                percentage_new.append(rem_slab["percent"])
                                difference_new.append(rem_slab["to"] - rem_slab["from"])
                                total_value_new.append(
                                    round(
                                        (rem_slab["to"] - rem_slab["from"])
                                        * rem_slab["percent"]
                                        / 100
                                    )
                                )

                            from_amount_new.append(slab_new["from"])
                            to_amount_new.append(slab_new["to"])
                            percentage_new.append(tax_percent_new)
                            difference_new.append(taxable_amount_new)
                            total_value_new.append(tax_amount_new)

                total_sum_new = sum(total_value_new)

                if (
                    income_doc_new.custom_marginal_relief_applicable
                    and income_doc_new.custom_minmum_value
                    and income_doc_new.custom_maximun_value
                ):
                    if (
                        income_doc_new.custom_minmum_value
                        < new_annual_slab
                        < income_doc_new.custom_maximun_value
                    ):
                        new_rebate_value = total_sum_new - (
                            new_annual_slab - income_doc_new.custom_minmum_value
                        )
                        final_value = total_sum_new - new_rebate_value

                        new_education_cess = final_value * 4 / 100

                    else:
                        if new_annual_slab < new_rebate:
                            new_rebate_value = total_sum_new

                        else:
                            new_rebate_value = 0

                        if new_annual_slab > 5000000:
                            new_surcharge_m = round((total_sum_new * 10) / 100)
                            new_education_cess = round(
                                (new_surcharge_m + total_sum_new) * 4 / 100
                            )

                        else:
                            new_surcharge_m = 0
                            new_education_cess = round((0 + total_sum_new) * 4 / 100)

                else:
                    if new_annual_slab < new_rebate:
                        new_rebate_value = total_sum_new

                    else:
                        new_rebate_value = 0

                    if new_annual_slab > 5000000:
                        new_surcharge_m = round((total_sum_new * 10) / 100)
                        new_education_cess = round(
                            (new_surcharge_m + total_sum_new) * 4 / 100
                        )

                    else:
                        new_surcharge_m = 0
                        new_education_cess = round((0 + total_sum_new) * 4 / 100)

    tax_already_paid = 0

    get_all_salary_slip = frappe.get_list(
        "Salary Slip",
        filters={
            "employee": employee,
            "docstatus": ["in", [1]],
            "custom_payroll_period": payroll_period,
        },
        fields=["current_month_income_tax"],
    )


    tax_already_paid = round(sum(slip.current_month_income_tax for slip in get_all_salary_slip))

    return {
        "from_amount": from_amount,
        "to_amount": to_amount,
        "percentage": percentage,
        "total_value": total_value,
        "total_sum": total_sum,
        "rebate": old_rebate,
        "max_amount": old_max_amount,
        "old_rebate_value": old_rebate_value,
        "old_surcharge_m": old_surcharge_m,
        "old_education_cess": old_education_cess,
        "from_amount_new": from_amount_new,
        "to_amount_new": to_amount_new,
        "percentage_new": percentage_new,
        "total_value_new": total_value_new,
        "total_sum_new": total_sum_new,
        "rebate_new": new_rebate,
        "max_amount_new": new_max_amount,
        "new_regime_marginal_relief_min_value": new_regime_marginal_relief_min_value,
        "new_regime_marginal_relief_max_value": new_regime_marginal_relief_max_value,
        "old_regime_marginal_relief_min_value": old_regime_marginal_relief_min_value,
        "old_regime_marginal_relief_max_value": old_regime_marginal_relief_max_value,
        "new_rebate_value": new_rebate_value,
        "new_surcharge_m": new_surcharge_m,
        "new_education_cess": new_education_cess,
        "tax_already_paid": tax_already_paid,


    }



@frappe.whitelist()
def download_tds_projection_pdf(declaration_id):

    
    data = calculate_tds_projection(declaration_id)

    if not data:
        frappe.throw("No TDS projection data found")

    
    html = frappe.render_template(
        "cn_indian_payroll/templates/includes/tds_projection_print.html",
        data
    )

    
    pdf = get_pdf(html)

    
    frappe.local.response.filename = "TDS_Projection.pdf"
    frappe.local.response.filecontent = pdf
    frappe.local.response.type = "download"



@frappe.whitelist()
def download_tds_poi_projection_pdf(proof_id):

    
    data = calculate_tds_projection_poi(proof_id)

    if not data:
        frappe.throw("No TDS projection data found")

   
    html = frappe.render_template(
        "cn_indian_payroll/templates/includes/tds_projection_poi_print.html",
        data
    )

    
    pdf = get_pdf(html)


    frappe.local.response.filename = "TDS_Projection.pdf"
    frappe.local.response.filecontent = pdf
    frappe.local.response.type = "download"







#http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.tds_projection.get_tds_projection_print_html?declaration_id=HR-TAX-DEC-2025-00009

@frappe.whitelist(allow_guest=True)
def get_tds_projection_print_html(declaration_id):

    context = calculate_tds_projection(declaration_id)

    if not context:
        frappe.throw("No TDS projection data found")

    html = frappe.render_template(
        "cn_indian_payroll/templates/includes/tds_projection_print.html",
        context
    )

    frappe.local.response["content_type"] = "text/html"
    frappe.local.response["response"] = html




#http://127.0.0.1:8002/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.tds_projection.get_tds_projection_poi_print_html?proof_id=HR-TAX-PRF-2026-00010

@frappe.whitelist(allow_guest=True)
def get_tds_projection_poi_print_html(proof_id):

    context = calculate_tds_projection_poi(proof_id)

    if not context:
        frappe.throw("No TDS projection data found")

    html = frappe.render_template(
        "cn_indian_payroll/templates/includes/tds_projection_poi_print.html",
        context
    )

    frappe.local.response["content_type"] = "text/html"
    frappe.local.response["response"] = html


# http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.tds_projection.print_declaration_preview?employee=37001&payroll_period=25-26&company=PW

@frappe.whitelist()
def print_declaration_preview(employee, payroll_period, company):


    target_employee = frappe.request.headers.get("X-Target-Employee-Id")
    if target_employee:
        employee = target_employee

    salary_projection = get_annual_statement(
        employee=employee,
        payroll_period=payroll_period,
        company=company
    )


    existing_declaration = get_employee_declaration_investments(
        employee=employee,
        company=company,
        payroll_period=payroll_period
    )

    result = {
        "salary_projection": salary_projection,
        "existing_declaration": existing_declaration
    }

    return result




@frappe.whitelist()
def print_declaration_pdf(employee, payroll_period, company):

    target_employee = frappe.request.headers.get("X-Target-Employee-Id")
    if target_employee:
        employee = target_employee

    salary_projection = get_annual_statement(
        employee=employee,
        payroll_period=payroll_period,
        company=company
    )

    existing_declaration = get_employee_declaration_investments(
        employee=employee,
        company=company,
        payroll_period=payroll_period
    )

    salary_data = salary_projection.get("message", salary_projection)

    context = {
        "employee_code": salary_data.get("employee_code"),
        "employee_name": salary_data.get("employee_name"),
        "employee_department": salary_data.get("employee_department"),
        "employee_designation": salary_data.get("employee_designation"),
        "employment_type": salary_data.get("employment_type"),
        "date_of_joining": salary_data.get("date_of_joining"),
        "pan": salary_data.get("pan"),
        "office_location": salary_data.get("office_location"),
        "pf": salary_data.get("pf"),
        "esic": salary_data.get("esic"),

        "salary_projection": salary_data,
        "existing_declaration": existing_declaration.get("message", existing_declaration),
    }

    html = frappe.render_template(
        "cn_indian_payroll/templates/includes/annual_statement1.html",
        context
    )

    # ✅ THIS IS THE FIX
    return {
        "html": html
    }



#http://127.0.0.1:8002/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.tds_projection.get_form12b_pdf?doctype=Employee%20Tax%20Exemption%20Declaration&docname=HR-TAX-DEC-2026-00001
@frappe.whitelist(allow_guest=True)
def get_form12b_pdf(doctype, docname):

    try:
        if not doctype or not docname:
            return {
                "html": "<p>Missing parameters.</p>"
            }

        # Allowed doctypes
        allowed_doctypes = [
            "Employee Tax Exemption Declaration",
            "Employee Tax Exemption Proof Submission"
        ]

        if doctype not in allowed_doctypes:
            return {
                "html": "<p>Invalid Doctype.</p>"
            }

        # Get document
        doc = frappe.get_doc(doctype, docname)

        # Choose template based on doctype
        if doctype == "Employee Tax Exemption Declaration":
            template = "cn_indian_payroll/templates/includes/form12b_declaration.html"

        elif doctype == "Employee Tax Exemption Proof Submission":
            template = "cn_indian_payroll/templates/includes/form12b_proof.html"

        # Render template
        context = {
            "doc": doc
        }

        html = frappe.render_template(template, context)

        return {
            "html": html
        }

    except frappe.DoesNotExistError:
        return {
            "html": "<p>Document not found.</p>"
        }

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Form12B Print Error"
        )

        return {
            "html": "<p>Error while generating print.</p>"
        }

    

# http://127.0.0.1:8002/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.tds_projection.get_approved_poi_category?proof_id=HR-TAX-PRF-2026-00003

@frappe.whitelist()
def get_approved_poi_category(proof_id):

    proofs = frappe.get_list(
        "POI Approved Category",
        filters={"proof_id": proof_id},
        fields=["*"]
    )

    # If no records
    if not proofs:
        return []

    result = []

    for proof in proofs:

        # If category is HRA
        if proof.get("category") == "HRA":

            result.append({
                "category": "HRA",
                "annual_hra_exemption": proof.get("custom_annual_eligible_amount"),
                "monthly_hra_exemption": proof.get("monthly_hra_exemption"),
                "payroll_period": proof.get("payroll_period"),
                "date": proof.get("submission_date"),
                "proof_id": proof_id,
                "hra_attach": proof.get("custom_hra_proof_attach"),
                "hra_paid": proof.get("house_rent_payment_amount"),
                "holder_name": proof.get("custom_name"),
                "pan": proof.get("custom_pan"),
                "address_line1": proof.get("custom_address_title1"),
                "employee": proof.get("employee"),
                "employee_name": proof.get("employee_name"),
                "status": proof.get("status"),
                "doc_name": proof.get("name"),
            })

        else:

            result.append({
                "category": proof.get("exemption_category"),
                "exemption_sub_category": proof.get("exemption_sub_category"),
                "declared_amount": proof.get("declared_amount"),
                "max_amount": proof.get("max_amount"),
                "proof_id": proof_id,
                "status": proof.get("status"),
                "employee": proof.get("employee"),
                "employee_name": proof.get("employee_name"),
                "attach": proof.get("attach"),
                "doc_name": proof.get("name"),
            })

    return result



    




# @frappe.whitelist()
# def approved_poi_components(proof_id=None, sub_category=None, status=None, note=None,amount=None):

#     # Validate required fields
#     if not proof_id or not sub_category or not status:
#         frappe.throw("proof_id, sub_category, and status are required")

#     # Get matching records
#     approved_proofs = frappe.get_all(
#         "POI Approved Category",
#         filters={"proof_id": proof_id},
#         fields=["name", "exemption_sub_category"]
#     )

#     updated = False

#     for row in approved_proofs:
#         if row.exemption_sub_category == sub_category:
#             doc = frappe.get_doc("POI Approved Category", row.name)

#             if doc.declared_amount!=amount:
#                 doc.status = "Pending"
#                 doc.command = note
#                 if amount:
#                     doc.declared_amount = amount
            

#             doc.save(ignore_permissions=True)

#             updated = True

#     if updated:
#         frappe.db.commit()

#     return {
#         "message": "Status updated successfully",
#         "proof_id": proof_id,
#         "sub_category": sub_category,
#         # "amount": amount,
#         "status": status,
#         "amount":doc.declared_amount
#     }




#http://127.0.0.1:8002/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.tds_projection.approved_poi_components?proof_id=HR-TAX-PRF-2026-00010&sub_category=LIC-%20Life%20Insurance%20Premium%20Directly%20Paid%20By%20Employee&status=Rejected&note=shiniln&amount=5200221

@frappe.whitelist()
def approved_poi_components(proof_id=None, sub_category=None, status=None, note=None, amount=None):

    if not proof_id or not sub_category or not status:
        frappe.throw("proof_id, sub_category, and status are required")

    approved_proofs = frappe.get_all(
        "POI Approved Category",
        filters={
            "proof_id": proof_id,
            "exemption_sub_category": sub_category
        },
        fields=["name"]
    )

    updated = False
    final_amount = None

    for row in approved_proofs:
        doc = frappe.get_doc("POI Approved Category", row.name)

        current_amount = float(doc.declared_amount or 0)
        new_amount = float(amount or 0)

        if current_amount != new_amount:
            doc.status = "Pending"
            doc.declared_amount = new_amount

        else:
            doc.status = status  

        doc.command = note
        doc.save(ignore_permissions=True)

        final_amount = doc.declared_amount
        updated = True

    if updated:
        frappe.db.commit()

    return {
        "message": "Status updated successfully",
        "proof_id": proof_id,
        "sub_category": sub_category,
        "status": status,
        "amount": final_amount

    }
