

import frappe
from frappe.utils import getdate, add_months, flt
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip



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

        row = {"name": comp.name, "values": values, "total": sum(values)}

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

    # ---------------- OFF CYCLE ---------------- #
    offcycle_values = [sum(x["values"][i] for x in offcycle) for i in range(len(months))]

    offcycle.append({
        "name": "Total Offcycle (D)",
        "values": offcycle_values,
        "total": sum(offcycle_values)
    })

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
        "name": "Off Cycle TDSDeduction (E)",
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
        "extra_payment_grand_total": extra_payment_grand_total,
        "total_perquisite_total": total_perquisite_total
    }




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



@frappe.whitelist()
def get_employee_declaration_investments(employee=None,company=None,payroll_period=None):
    if not employee:
        return {"status": "failed", "message": "Employee is required"}


    declaration_form=frappe.db.get_list("Employee Tax Exemption Declaration")
    filter={"company":company,"employee":employee,"payroll_period":payroll_period},
    fileds=["*"],

    if not declaration_form:
        return {"status": "failed", "message": "No declaration form is created for the payroll period"}

    get_each_doc=frappe.get_doc("Employee Tax Exemption Declaration",declaration_form[0].name)
