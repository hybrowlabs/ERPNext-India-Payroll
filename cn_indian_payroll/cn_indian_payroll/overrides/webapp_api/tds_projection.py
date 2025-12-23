

import frappe
from frappe.utils import getdate, add_months, flt
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip






# @frappe.whitelist()
# def get_annual_statement(employee, payroll_period):

#     # -------- Payroll Period -------- #
#     period = frappe.db.get_value(
#         "Payroll Period",
#         payroll_period,
#         ["start_date", "end_date"],
#         as_dict=True
#     )

#     if not period:
#         return {"status": "failed", "message": "Invalid Payroll Period"}

#     fy_start = getdate(period.start_date)
#     fy_end = getdate(period.end_date)

#     # -------- Existing Salary Slips -------- #
#     slips = frappe.get_all(
#         "Salary Slip",
#         filters={
#             "employee": employee,
#             "custom_payroll_period": payroll_period,
#             "docstatus": ["in", [0, 1]]
#         },
#         fields=["name", "start_date"],
#         order_by="start_date asc"
#     )

#     slip_by_month = {}
#     for s in slips:
#         month = getdate(s.start_date).strftime("%B-%Y")
#         slip_by_month[month] = s.name

#     # -------- Build FY Months List -------- #
#     months = []
#     current = fy_start
#     while current <= fy_end:
#         months.append(current.strftime("%B-%Y"))
#         current = add_months(current, 1)

#     # -------- Last Salary Slip Amounts -------- #
#     last_amount_map = {}
#     if slips:
#         last_slip = slips[-1]
#         last_details = frappe.get_all(
#             "Salary Detail",
#             filters={"parent": last_slip.name},
#             fields=["salary_component", "amount"]
#         )
#         last_amount_map = {d.salary_component: d.amount for d in last_details}





#     # -------- Preview Slip for FUTURE Months -------- #
#     ssa = frappe.get_list(
#         "Salary Structure Assignment",
#         filters={"employee": employee, "docstatus": 1},
#         fields=["*"],
#         order_by="from_date desc",
#         limit=1
#     )

#     preview_amount_map = {}
#     if ssa:
#         new_slip = make_salary_slip(
#             source_name=ssa[0].salary_structure,
#             employee=employee,
#             posting_date=ssa[0].from_date,
#             for_preview=1,
#         )
#         for e in new_slip.earnings:
#             preview_amount_map[e.salary_component] = flt(e.amount)
#         for d in new_slip.deductions:
#             preview_amount_map[d.salary_component] = flt(d.amount)

#     # -------- All components to evaluate -------- #
#     component_names = list(set(list(last_amount_map.keys()) + list(preview_amount_map.keys())))




#     components = frappe.get_all(
#         "Salary Component",
#         filters={"name": ["in", component_names]},
#         fields=[
#             "name", "type", "is_tax_applicable",
#             "custom_is_reimbursement",
#             "custom_is_offcycle_component",
#             "do_not_include_in_total",
#             "custom_sequence",
#             "component_type"
#         ],
#         order_by="custom_sequence asc"
#     )

#     # Buckets
#     earnings = []
#     deductions = []
#     reimbursements = []
#     offcycle = []

#     # Allowed deduction component types
#     allowed_deduction_types = [
#         "Provident Fund",
#         "ESIC",
#         "Professional Tax",
#         "LWF",
#         "Income Tax"
#     ]

#     # -------- Fill Month Values -------- #
#     for comp in components:

#         # taxable earnings only
#         if comp.type == "Earning" and not comp.is_tax_applicable and not comp.custom_is_reimbursement and not comp.custom_is_offcycle_component:
#             continue

#         # filter deductions based ONLY on component_type
#         if comp.type == "Deduction" and comp.component_type not in allowed_deduction_types:
#             continue

#         values = []
#         for m in months:
#             if m in slip_by_month:
#                 amount = frappe.db.get_value(
#                     "Salary Detail",
#                     {"parent": slip_by_month[m], "salary_component": comp.name},
#                     "amount"
#                 ) or 0
#             else:
#                 amount = preview_amount_map.get(comp.name, 0)

#             values.append(flt(amount))



#         data = {"name": comp.name, "values": values, "total": sum(values)}

#         if comp.type == "Earning" and comp.custom_is_reimbursement:
#             reimbursements.append(data)
#         elif comp.type == "Earning" and comp.custom_is_offcycle_component:
#             offcycle.append(data)
#         elif comp.type == "Earning":
#             earnings.append(data)
#         elif comp.type == "Deduction":
#             deductions.append(data)

#     # -----------------------------------------------------------------------
#     # SUMMARY ROWS
#     # -----------------------------------------------------------------------
#     # return offcycle

#     extra_payment_grand_total = 0
#     total_perquisite_total = 0


#     for row in earnings:
#         comp_name = row.get("name")

#         # Check only extra payment components
#         if frappe.db.get_value(
#             "Salary Component",
#             comp_name,
#             "custom_is_extra_payment"
#         ):


#             extra_payment_grand_total += flt(row["total"])

#         if frappe.db.get_value(
#             "Salary Component",
#             comp_name,
#             "custom_perquisite"
#         ):
#             total_perquisite_total+= flt(row["total"])








#     # Gross Earnings
#     gross_earn_values = [sum(x["values"][i] for x in earnings) for i in range(len(months))]
#     earnings.append({
#         "name": "Gross Earnings (A)",
#         "values": gross_earn_values,
#         "total": sum(gross_earn_values)
#     })

#     # Total Deductions
#     deduction_values = [sum(x["values"][i] for x in deductions) for i in range(len(months))]
#     deductions.append({
#         "name": "Total Deductions (B)",
#         "values": deduction_values,
#         "total": sum(deduction_values)
#     })

#     # NET PAY
#     net_pay_values = [
#         gross_earn_values[i] - deduction_values[i] for i in range(len(months))
#     ]

#     net_pay = {
#         "name": "Net Pay (A-B)",
#         "values": net_pay_values,
#         "total": sum(net_pay_values)
#     }

#     # Total Reimbursements
#     reimbursement_values = [sum(x["values"][i] for x in reimbursements) for i in range(len(months))]
#     reimbursements.append({
#         "name": "Total Reimbursements (C)",
#         "values": reimbursement_values,
#         "total": sum(reimbursement_values)
#     })

#     # Total Offcycle
#     offcycle_values = [sum(x["values"][i] for x in offcycle) for i in range(len(months))]
#     offcycle.append({
#         "name": "Total Offcycle (D)",
#         "values": offcycle_values,
#         "total": sum(offcycle_values)
#     })

#     offcycle.append({
#         "name": "Off Cycle TDSDeduction (E)",
#         "values": 0,
#         "total": 0
#     })

#     offcycle.append({
#         "name": "Off Cycle Net Pay(D-E)",
#         "values": 0,
#         "total": 0
#     })

#     offcycle.append({
#         "name": "Total Off Cycle Payments Non Taxable (F)",
#         "values": 0,
#         "total": 0
#     })


#     offcycle.append({
#         "name": "Total Offcycle Pay((D-E)+F)",
#         "values": 0,
#         "total": 0
#     })

#     offcycle.append({
#         "name": "Grand Total Pay(Total Pay((A-B)+C)+Total Offcycle Pay(D-E)+F))",
#         "values": 0,
#         "total": 0
#     })








#     # -----------------------------------------------------------------------

#     return {
#         "status": "success",
#         "months": months,

#         "earnings": earnings,
#         "deductions": deductions,
#         "net_pay": [net_pay],

#         "reimbursements": reimbursements,
#         "offcycle_earnings": offcycle,
#         "extra_payment_grand_total": extra_payment_grand_total,
#         "total_perquisite_total": total_perquisite_total
#     }




@frappe.whitelist()
def get_annual_statement(employee, payroll_period):

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
    slips = frappe.get_all(
        "Salary Slip",
        filters={
            "employee": employee,
            "custom_payroll_period": payroll_period,
            "docstatus": ["in", [0, 1]]
        },
        fields=["name", "start_date"],
        order_by="start_date asc"
    )

    slip_by_month = {}
    for s in slips:
        month = getdate(s.start_date).strftime("%B-%Y")
        slip_by_month[month] = s.name

    # -------- FY Months -------- #
    months = []
    current = fy_start
    while current <= fy_end:
        months.append(current.strftime("%B-%Y"))
        current = add_months(current, 1)

    # -------- Last Salary Slip -------- #
    last_amount_map = {}
    if slips:
        last_slip = slips[-1]
        last_details = frappe.get_all(
            "Salary Detail",
            filters={"parent": last_slip.name},
            fields=["salary_component", "amount"]
        )
        last_amount_map = {d.salary_component: d.amount for d in last_details}

    # -------- Preview Slip (Future Months) -------- #
    ssa = frappe.get_list(
        "Salary Structure Assignment",
        filters={"employee": employee, "docstatus": 1},
        fields=["*"],
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

    components = frappe.get_all(
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

    # -------- Component Month Values -------- #
    for comp in components:

        if comp.type == "Earning" and not comp.is_tax_applicable \
           and not comp.custom_is_reimbursement \
           and not comp.custom_is_offcycle_component:
            continue

        if comp.type == "Deduction" and comp.component_type not in allowed_deduction_types:
            continue

        values = []
        for m in months:
            if m in slip_by_month:
                amount = frappe.db.get_value(
                    "Salary Detail",
                    {"parent": slip_by_month[m], "salary_component": comp.name},
                    "amount"
                ) or 0
            else:
                amount = preview_amount_map.get(comp.name, 0)

            values.append(flt(amount))

        rounded_values = [round(flt(v), 0) for v in values]

        row = {
            "name": comp.name,
            "values": rounded_values,
            "total": sum(rounded_values)
        }


        # row = {"name": comp.name, "values": values, "total": sum(values)}

        if comp.type == "Earning" and comp.custom_is_reimbursement and comp.is_tax_applicable:
            reimbursements.append(row)
        elif comp.type == "Earning" and comp.custom_is_offcycle_component:
            offcycle.append(row)
        elif comp.type == "Earning":
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
    offcycle_values = [sum(x["values"][i] for x in offcycle) for i in range(len(months))]



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

            details = frappe.get_all(
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

            details = frappe.get_all(
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



    # ------------------------------------------------------------------

    return {
        "status": "success",
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
        "reimbursements_total":round(reimbursements_total) if reimbursements_total else 0

    }





#http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.tds_projection.tds_declaration_form

@frappe.whitelist()
def tds_declaration_form():
    records = frappe.get_all(
        "Employee Tax Exemption Sub Category",
        filters={"is_active": 1},
        fields=[
            "exemption_category",
            "max_amount",
            "name",
            "is_active",
            "custom_component_type",

            "custom_description"
        ],
        order_by="custom_sequence asc"
    )

    grouped = {}

    # Group by exemption_category
    for row in records:
        category = row.get("exemption_category")
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(row)

    # Convert to required format (list of dicts)
    final_list = []

    for category, items in grouped.items():
        final_list.append({
            "category_name": category,
            "items": items
        })

    return final_list




#http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.tds_projection.get_employee_declaration_investments?employee=37001&company=PW&payroll_period=25-26
# @frappe.whitelist()
# def get_employee_declaration_investments(employee=None, company=None, payroll_period=None):

#     if not employee or not payroll_period or not company:
#         return {
#             "status": "failed",
#             "message": "Employee and Payroll Period are required"
#         }


#     declaration = frappe.get_all(
#         "Employee Tax Exemption Declaration",
#         filters={
#             "employee": employee,
#             "company": company,
#             "payroll_period": payroll_period
#         },
#         fields=["name"],
#         limit=1
#     )

#     if not declaration:
#         return {
#             "status": "failed",
#             "message": "No declaration form created for this payroll period"
#         }

#     declaration_doc = frappe.get_doc(
#         "Employee Tax Exemption Declaration",
#         declaration[0].name
#     )

#     eighty_c = []
#     lta_amount = 0

#     if declaration_doc.declarations:
#         for d in declaration_doc.declarations:

#             sub_category = frappe.get_doc(
#                 "Employee Tax Exemption Sub Category",
#                 d.exemption_sub_category
#             )

#             # LTA
#             if sub_category.custom_component_type == "LTA Reimbursement":
#                 lta_amount = flt(d.max_amount or 0)

#             category = frappe.get_doc(
#                 "Employee Tax Exemption Category",
#                 d.exemption_category
#             )

#             # Section 80C
#             if category.custom_select_section == "80 C":
#                 eighty_c.append({
#                     "component": d.exemption_sub_category,
#                     "declared_amount": flt(d.amount or 0),
#                     "qualified_amount": flt(d.max_amount or 0),
#                     "deductible_amount": flt(d.max_amount or 0)
#                 })


#     annual_statement = get_annual_statement(employee, payroll_period)

#     if annual_statement.get("status") != "success":
#         return annual_statement

#     extra_payment_grand_total = annual_statement.get("extra_payment_grand_total", 0)
#     total_perquisite_total = annual_statement.get("total_perquisite_total", 0)

#     total_gross_earning=annual_statement.get("total_gross_earning",0)

#     total_off_cycle_payment=annual_statement.get("total_off_cycle_payment",0)

#     reimbursements_total=annual_statement.get("reimbursements_total",0)


#     total_gross_salary_current=round(total_off_cycle_payment+total_gross_earning+extra_payment_grand_total)







#     return {
#         "status": "success",
#         "summary": {
#             "gross_salary": {
#                 "name": "Gross Salary",
#                 "amount": round(flt(total_gross_earning), 2)
#             },
#             "total_extra_payment": {
#                 "name": "Total Extra Payment",
#                 "amount": round(flt(extra_payment_grand_total), 2)
#             },

#             "total_off_cycle_extra_payment": {
#                 "name": "Total Offcycle Extra Payments",
#                 "amount": round(flt(total_off_cycle_payment), 2)
#             },

#             "total_gross_salary_current": {
#                 "name": "Total Gross Salary (Current Employer)",
#                 "amount": round(flt(total_gross_salary_current), 2)
#             },
#             "less_ctc_reimbursements": {
#                 "name": "Less CTC Reimbursements",

#             },

#             "lta_component": {
#                 "name": "LTA",
#                 "amount":lta_amount

#             },

#             "total_reimbursements": {
#                 "name": "Total Reimbursements",
#                 "amount":lta_amount

#             },

#             "total_income_after_deduction_and_reimbursements": {
#                 "name": "Gross Income after Deduction and Reimbursements",
#                 "amount":round(total_gross_salary_current-lta_amount)

#             },

#             "less_exemption_under_section_10": {
#                 "name": "Less exemption under Section 10",


#             },
#             "hra_calculation": {
#                 "name": "HRA Calculation",


#             },

#             "basic_and_dearness_allowance": {
#                 "name": "Basic + Dearness Allowance (40% or 50%)",
#                 "amount":0


#             },
#             "rent_paid": {
#                 "name": "Rent Paid - 10% of Basic + Dearness Allowance",
#                 "amount":0


#             },
#             "hra_received": {
#                 "name": "H.R.A received",
#                 "amount":0


#             },
#             "hra_exemption": {
#                 "name": "HRA Exemption",
#                 "amount":0


#             },
#             "total_section_10_exemptions": {
#                 "name": "Total Section 10 Exemptions",
#                 "amount":0
#             },
#             "total_amount_of_salary_received_after_section_10": {
#                 "name": "Total amount of Salary received after Section 10",
#                 "amount":0
#             },


#             "less_deduction_under_section_16": {
#                 "name": "Less: Deductions under section 16",
#                 "amount":0
#             },
#             "standard_deduction_under_section_16": {
#                 "name": "Standard deduction under section 16(ia)",
#                 "amount":0
#             },
#             "total_amount_of_deductions_under_section_16": {
#                 "name": "Total amount of deductions under section 16",

#             },
#             "income_chargeable_under_section_16": {
#                 "name": "Income chargeable under the head Salaries",
#                 "amount":0
#             },

#             "income_loss_from_house_property":  {
#                 "name": "A. Income/Loss from house property",
#                 "amount":0
#             },


#             "total_for_income_loss_from_house_property" :{
#                 "name": "Total for Income/Loss from house property",

#             },

#             "other_sources":  {
#                 "name": "B. Other Sources",
#                 "amount":0
#             },
#             "total_for_other_sources":  {
#                 "name": "Total from Other Sources",
#                 "amount":0
#             },

#             "gross_total_income":  {
#                 "name": "Gross Total Income",
#                 "amount":0
#             },

#             "total_chapter_via":  {
#                 "name": "Total Chapter-VIA",
#                 "category_1":"Declared value",
#                 "category_2":"Qualified Value",
#                 "category_3":"Deductible Value",

#             },
#             "section_80C_80CCC_80CCD":  {
#                 "name": "Section 80C,80CCC,80CCD",

#             },
#             "eighty_c_components": eighty_c









#         }
#     }

@frappe.whitelist()
def get_employee_declaration_investments(employee=None, company=None, payroll_period=None):

    # ------------------ Validation ------------------
    if not employee or not company:
        return {
            "status": "failed",
            "message": "Employee and Company are required"
        }

    # ------------------ Get Declaration ------------------
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

    # ------------------ 80C & LTA ------------------
    eighty_c = []
    lta_amount = 0
    eighty_d=[]
    other_investment=[]

    if declaration_doc.declarations:
        for d in declaration_doc.declarations:

            sub_category = frappe.get_doc(
                "Employee Tax Exemption Sub Category",
                d.exemption_sub_category
            )

            # LTA
            if sub_category.custom_component_type == "LTA Reimbursement":
                lta_amount = flt(d.max_amount or 0)

            category = frappe.get_doc(
                "Employee Tax Exemption Category",
                d.exemption_category
            )

            # Section 80C
            if category.custom_select_section == "80 C":
                eighty_c.append({
                    "component": d.exemption_sub_category,
                    "declared_amount": flt(d.amount or 0),
                    "qualified_amount": flt(d.max_amount or 0),
                    "deductible_amount": flt(d.max_amount or 0)
                })


            if category.custom_select_section == "80 D":
                eighty_d.append({
                    "component": d.exemption_sub_category,
                    "declared_amount": flt(d.amount or 0),
                    "qualified_amount": flt(d.max_amount or 0),
                    "deductible_amount": flt(d.max_amount or 0)
                })

            if not category.custom_select_section and not sub_category.custom_component_type=="LTA Reimbursement":

                other_investment.append({

                    "component": d.exemption_sub_category,
                    "declared_amount": flt(d.amount or 0),
                    "qualified_amount": flt(d.max_amount or 0),
                    "deductible_amount": flt(d.max_amount or 0)
                })

    # ------------------ Annual Statement ------------------



    eighty_c_sum = min(
        sum(r["deductible_amount"] for r in eighty_c),
        150000
    )
    eighty_d_sum = sum(r["deductible_amount"] for r in eighty_d)
    other_investment_sum = sum(r["deductible_amount"] for r in other_investment)

    annual_statement = get_annual_statement(employee, payroll_period)

    if annual_statement.get("status") != "success":
        return annual_statement

    extra_payment_grand_total = flt(annual_statement.get("extra_payment_grand_total", 0))
    total_perquisite_total = flt(annual_statement.get("total_perquisite_total", 0))
    total_gross_earning = flt(annual_statement.get("total_gross_earning", 0))
    total_off_cycle_payment = flt(annual_statement.get("total_off_cycle_payment", 0))
    reimbursements_total = flt(annual_statement.get("reimbursements_total", 0))

    total_gross_salary_current = round(
        total_gross_earning + total_off_cycle_payment + extra_payment_grand_total, 2
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

    total_declaration_sum=round(eighty_c_sum + eighty_d_sum + other_investment_sum)

    net_taxable_income=round(gross_total_income-total_declaration_sum,2)









    # ------------------ Response ------------------
    return {
    "status": "success",

    "summary": [
        {
            "key": "gross_salary",
            "name": "Gross Salary",
            "amount": round(flt(total_gross_earning), 2)
        },
        {
            "key": "total_extra_payment",
            "name": "Total Extra Payment",
            "amount": round(flt(extra_payment_grand_total), 2)
        },
        {
            "key": "total_off_cycle_extra_payment",
            "name": "Total Offcycle Extra Payments",
            "amount": round(flt(total_off_cycle_payment), 2)
        },
        {
            "key": "total_gross_salary_current",
            "name": "Total Gross Salary (Current Employer)",

        },

        {
            "key": "total_gross_salary",
            "name": "Total Gross Salary",
            "amount": round(flt(total_gross_salary_current), 2)
        },



        {
            "key": "less_ctc_reimbursements",
            "name": "Less CTC Reimbursements",

        },
        {
            "key": "lta_component",
            "name": "LTA",
            "amount": round(flt(lta_amount), 2)
        },
        {
            "key": "total_reimbursements",
            "name": "Total Reimbursements",
            "amount": round(flt(lta_amount), 2)
        },
        {
            "key": "total_income_after_deduction_and_reimbursements",
            "name": "Gross Income after Deduction and Reimbursements",
            "amount": round(
                flt(total_gross_salary_current) - flt(lta_amount), 2
            )
        },
        {
            "key": "less_exemption_under_section_10",
            "name": "Less exemption under Section 10",

        },
        {
            "key": "hra_calculation",
            "name": "HRA Calculation",

        },
        {
            "key": "basic_and_dearness_allowance",
            "name": "Basic + Dearness Allowance (40% or 50%)",
            "amount": basic_percentage
        },
        {
            "key": "rent_paid",
            "name": "Rent Paid - 10% of Basic + Dearness Allowance",
            "amount": rent_paid_of_basic
        },
        {
            "key": "hra_received",
            "name": "H.R.A received",
            "amount": hra_received_annual
        },
        {
            "key": "hra_exemption",
            "name": "HRA Exemption",
            "amount": hra_exemption
        },
        {
            "key": "total_section_10_exemptions",
            "name": "Total Section 10 Exemptions",
            "amount": hra_exemption
        },
        {
            "key": "salary_after_section_10",
            "name": "Total amount of Salary received after Section 10",
            "amount": salary_after_section_10
        },
        {
            "key": "less_deduction_under_section_16",
            "name": "Less: Deductions under section 16",

        },
        {
            "key": "standard_deduction_section_16",
            "name": "Standard deduction under section 16(ia)",
            "amount": standard_deduction
        },
        {
            "key": "total_deduction_section_16",
            "name": "Total amount of deductions under section 16",
            "amount": standard_deduction
        },
        {
            "key": "income_chargeable_salary",
            "name": "Income chargeable under the head Salaries",
            "amount": round(
                flt(salary_after_section_10) - flt(standard_deduction), 2
            )
        },
        {
            "key": "income_loss_house_property",
            "name": "A. Income/Loss from house property",

        },
        {
            "key": "total_income_loss_house_property",
            "name": "Total for Income/Loss from house property",
            "amount": 0
        },
        {
            "key": "other_sources",
            "name": "B. Other Sources",

        },
        {
            "key": "total_other_sources",
            "name": "Total from Other Sources",
            "amount": 0
        },
        {
            "key": "gross_total_income",
            "name": "Gross Total Income",
            "amount": round(
                flt(salary_after_section_10) - flt(standard_deduction), 2
            )
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
            "amount":0
        },

        {
            "key": "rebate",
            "name":"Rebate (U/s 87A)",
            "amount":0
        },

        {
            "key": "income_tax_after_rebate",
            "name":"Income Tax After Rebate (u/s 87A)/Marginal Relief under New Tax Regime",
            "amount":0
        },
        {
            "key": "surcharge",
            "name":"Raw Surcharge",
            "amount":0
        },
        {
            "key": "marginal_relief",
            "name":"Marginal Relief",
            "amount":0
        },
        {
            "key": "cess_fee",
            "name":"Add Edn Cess + Health Cess @ 4%",
            "amount":0
        },
        {
            "key": "net_tax_payable",
            "name":"Net Tax Payable (A)",
            "amount":0
        },
        {
            "key": "previous_employer_tds",
            "name":"Previous Employer TDS (B)",
            "amount":0
        },
        {
            "key": "advance_tax",
            "name":"Outside Tax / Advance Tax (C)",
            "amount":0
        },
        {
            "key": "tax_deducted_till_date_by_current_employer",
            "name":"Tax Deducted till Date by Current Employer (D)",
            "amount":0
        },
        {
            "key": "remaining_tax",
            "name":"Remaining Tax (A - B - C - D)",
            "amount":0
        },

        {
            "key": "remaining_months",
            "name":"Remaining Months",
            "amount":0
        },
        {
            "key": "monthly_tds",
            "name":"Monthly TDS",
            "amount":0
        },

    ]


}
