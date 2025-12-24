

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





#http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.tds_projection.tds_declaration_form?employee=37001&company=PW&payroll_period=25-26&go_head_with_new_regime=0

@frappe.whitelist()
def tds_declaration_form(employee=None, company=None, payroll_period=None, go_head_with_new_regime=None):

    # ------------------ Validation ------------------
    if not employee or not company or not payroll_period:
        return {
            "status": "failed",
            "message": "Employee, Company and Payroll Period are required"
        }

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

    # ------------------ DB → UI Flag ------------------
    current_flag = 1 if current_tax_regime == "New Regime" else 0

    # ------------------ Existing Declaration Map ------------------
    existing_declaration = []
    for d in declaration_doc.declarations:
        existing_declaration.append({
            "exemption_category": d.exemption_category,
            "exemption_sub_category": d.exemption_sub_category,
            "amount": d.amount,
            "max_amount": d.max_amount
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

    # ------------------ No Regime Change ------------------
    if go_head_with_new_regime == current_flag:
        if current_tax_regime=="Old Regime":


            NON_EDITABLE_COMPONENTS = [
                "LTA Reimbursement",
                "Professional Tax",
                "Provident Fund",
                "NPS"
            ]

            records = frappe.get_all(
                "Employee Tax Exemption Sub Category",
                filters={"is_active": 1},
                fields=[
                    "exemption_category",
                    "name",
                    "max_amount",
                    "custom_component_type",
                    "custom_description",
                    "custom_sequence"
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
                    "amount": declaration_row["amount"] if declaration_row else 0,
                    "max_amount": (
                        declaration_row["max_amount"]
                        if declaration_row and declaration_row.get("max_amount") is not None
                        else row.max_amount
                    )
                })

            final_list = []
            for category, items in grouped.items():
                final_list.append({
                    "category_name": category,
                    "items": items
                })

            return {
                "status": "success",
                "declaration_id": declaration_id,
                "current_tax_regime": current_tax_regime,
                "go_head_with_new_regime": current_flag,
                "categories": final_list,

            }
        elif current_tax_regime == "New Regime":

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
                    "custom_description"
                ]
            )

            nps_items = []

            for row in records:
                declaration_row = existing_map.get(row.name)

                nps_items.append({
                    "exemption_sub_category": row.name,
                    "component_type": row.custom_component_type,
                    "description": row.custom_description,
                    "editable": 0,
                    "amount": declaration_row["amount"] if declaration_row else 0,
                    "max_amount": (
                        declaration_row["max_amount"]
                        if declaration_row and declaration_row.get("max_amount") is not None
                        else row.max_amount
                    )
                })

            return {
                "status": "success",
                "declaration_id": declaration_id,
                "current_tax_regime": current_tax_regime,
                "go_head_with_new_regime": current_flag,
                "categories": [
                    {
                        "category_name": "NPS",
                        "items": nps_items
                    }
                ]
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



        # ---------------- NPS SUB CATEGORY ----------------
        records = frappe.get_all(
            "Employee Tax Exemption Sub Category",
            filters={
                "is_active": 1,
                "custom_component_type": "NPS",
            },
            fields=[
                "exemption_category",
                "name",
                "max_amount",
                "custom_component_type",
                "custom_description",
            ],
        )

        nps_items = []

        for row in records:
            nps_items.append({
                "exemption_sub_category": row.name,
                "component_type": row.custom_component_type,
                "description": row.custom_description,
                "editable": 0,
                "amount": round(nps_amount_ctc),
                "max_amount": round(nps_amount_ctc),
            })

        return {
            "status": "success",

            "month_count":month_count,

            "choosed_tax_regime": choosed_tax_regime,
            "latest_tax_slab_new_regime": latest_tax_slab_name,
            "declaration_id": declaration_id,
            "current_tax_regime": current_tax_regime,
            "go_head_with_new_regime": 1,
            "message": "User switched from Old Regime to New Regime",
            "categories": [
                {
                    "category_name": "NPS",
                    "items": nps_items,
                }
            ],
        }







    if go_head_with_new_regime == 0 and current_flag == 1:

        nps_amount_ctc = 0
        pf_amount_ctc = 0
        pt_amount_ctc = 0
        lta_amount_ctc = 0


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
            "LTA Reimbursement": round(lta_amount_ctc, 2),
        }

        NON_EDITABLE_COMPONENTS = set(SYSTEM_COMPONENT_MAP.keys())

        records = frappe.get_all(
            "Employee Tax Exemption Sub Category",
            filters={"is_active": 1},
            fields=[
                "exemption_category",
                "name",
                "max_amount",
                "custom_component_type",
                "custom_description",
                "custom_sequence",
            ],
            order_by="custom_sequence asc",
        )

        grouped = {}

        for row in records:
            grouped.setdefault(row.exemption_category, [])

            declaration_row = existing_map.get(row.name)

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

            grouped[row.exemption_category].append({
                "exemption_sub_category": row.name,
                "component_type": row.custom_component_type,
                "description": row.custom_description,
                "editable": editable,
                "amount": round(amount),
                "max_amount": round(max_amount),
            })

        final_categories = [
            {"category_name": cat, "items": items}
            for cat, items in grouped.items()
        ]


        return {
            "status": "success",
            "declaration_id": declaration_id,
            "current_tax_regime": "Old Regime",
            "go_head_with_new_regime": 0,
            "message": "User switched from New Regime to Old Regime",
            "categories": final_categories,
        }








# @frappe.whitelist()
# def tds_declaration_form():





#     records = frappe.get_all(
#         "Employee Tax Exemption Sub Category",
#         filters={"is_active": 1},
#         fields=[
#             "exemption_category",
#             "max_amount",
#             "name",
#             "is_active",
#             "custom_component_type",

#             "custom_description"
#         ],
#         order_by="custom_sequence asc"
#     )

#     grouped = {}

#     # Group by exemption_category
#     for row in records:
#         category = row.get("exemption_category")
#         if category not in grouped:
#             grouped[category] = []
#         grouped[category].append(row)

#     # Convert to required format (list of dicts)
#     final_list = []

#     for category, items in grouped.items():
#         final_list.append({
#             "category_name": category,
#             "items": items
#         })

#     return final_list


#http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.tds_projection.get_annual_statement?employee=37001&payroll_period=25-26

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

    current_tax_regime=declaration_doc.custom_tax_regime
    declaration_id=declaration[0].name


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
    "current_tax_regime":current_tax_regime,
    "declaration_id":declaration_id,

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




#http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.tds_projection.get_existing_declaration_form?employee=37001&payroll_period=25-26&company=PW

# @frappe.whitelist()
# def get_existing_declaration_form(employee=None, company=None, payroll_period=None):

#     # ---------------- Validation ----------------
#     if not employee or not company or not payroll_period:
#         return {
#             "status": "failed",
#             "message": "Employee, Company, and Payroll Period are required"
#         }

#     existing_component_part_of_ctc = []

#     # ---------------- Fetch Declaration ----------------
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

#     current_tax_regime = declaration_doc.custom_tax_regime
#     declaration_id = declaration_doc.name

#     # ---------------- Components Part of CTC ----------------
#     VALID_COMPONENT_TYPES = {
#         "LTA Reimbursement",
#         "Provident Fund",
#         "Professional Tax"
#         "NPS"
#     }

#     if declaration_doc.declarations:
#         for d in declaration_doc.declarations:

#             if not d.exemption_sub_category:
#                 continue

#             sub_category = frappe.get_cached_doc(
#                 "Employee Tax Exemption Sub Category",
#                 d.exemption_sub_category
#             )

#             if sub_category.custom_component_type in VALID_COMPONENT_TYPES:
#                 existing_component_part_of_ctc.append({
#                     "component": d.exemption_sub_category,
#                     "component_type": sub_category.custom_component_type,
#                     "declared_amount": flt(d.amount or 0)
#                 })

#     # ---------------- Response ----------------
#     return {
#         "status": "success",
#         "current_tax_regime": current_tax_regime,
#         "declaration_id": declaration_id,
#         "existing_component_part_of_ctc": existing_component_part_of_ctc
#     }



# @frappe.whitelist()
# def update_declaration_form(declaration_id, data):
#     import frappe

#     if isinstance(data, str):
#         data = frappe.parse_json(data)

#     declaration = frappe.get_doc(
#         "Employee Tax Exemption Declaration",
#         declaration_id
#     )

#     # Update parent field
#     declaration.monthly_house_rent = data.get("monthly_house_rent")

#     if data.get("go_head_with_new_regime")==1:
#         income_tax_slab=frappe.get_list("Income Tax Slab",filters={"disabled":0,"company":company,"custom_select_regime":"New Regime"},fields=["name","custom_select_regime"])
#         order_by effective_from desc,
#     if data.get("go_head_with_new_regime")==0:
#         income_tax_slab=frappe.get_list("Income Tax Slab",filters={"disabled":0,"company":company,"custom_select_regime":"Old Regime"},fields=["name","custom_select_regime"])
#         order_by effective_from desc,

#     declaration.custom_income_tax=income_tax_slab[0].name
#     declaration.custom_tax_regime=income_tax_slab[0].custom_select_regime


#     # Reset child table
#     declaration.set("declarations", [])

#     for row in data.get("declarations", []):
#         declaration.append("declarations", {
#             "exemption_category": row.get("exemption_category"),
#             "exemption_sub_category": row.get("exemption_sub_category"),
#             "amount": row.get("amount"),
#             "max_amount": row.get("max_amount")
#         })

#     declaration.save(ignore_permissions=True)
#     frappe.db.commit()

#     return {
#         "status": "success",
#         "message": "Declaration updated successfully"
#     }
