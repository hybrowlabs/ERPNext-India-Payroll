

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

    # -------- Existing Salary Slips -------- #
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

    # -------- Build FY Months List -------- #
    months = []
    current = fy_start
    while current <= fy_end:
        months.append(current.strftime("%B-%Y"))
        current = add_months(current, 1)

    # -------- Last Salary Slip Amounts -------- #
    last_amount_map = {}
    if slips:
        last_slip = slips[-1]
        last_details = frappe.get_all(
            "Salary Detail",
            filters={"parent": last_slip.name},
            fields=["salary_component", "amount"]
        )
        last_amount_map = {d.salary_component: d.amount for d in last_details}

    # -------- Preview Slip for FUTURE Months -------- #
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

    # -------- All components to evaluate -------- #
    component_names = list(set(list(last_amount_map.keys()) + list(preview_amount_map.keys())))

    components = frappe.get_all(
        "Salary Component",
        filters={"name": ["in", component_names]},
        fields=[
            "name", "type", "is_tax_applicable",
            "custom_is_reimbursement",
            "custom_is_offcycle_component",
            "do_not_include_in_total",
            "custom_sequence",
            "component_type"
        ],
        order_by="custom_sequence asc"
    )

    # Buckets
    earnings = []
    deductions = []
    reimbursements = []
    offcycle = []

    # Allowed deduction component types
    allowed_deduction_types = [
        "Provident Fund",
        "ESIC",
        "Professional Tax",
        "LWF",
        "Income Tax"
    ]

    # -------- Fill Month Values -------- #
    for comp in components:

        # taxable earnings only
        if comp.type == "Earning" and not comp.is_tax_applicable and not comp.custom_is_reimbursement and not comp.custom_is_offcycle_component:
            continue

        # filter deductions based ONLY on component_type
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

        data = {"name": comp.name, "values": values, "total": sum(values)}

        if comp.type == "Earning" and comp.custom_is_reimbursement:
            reimbursements.append(data)
        elif comp.type == "Earning" and comp.custom_is_offcycle_component:
            offcycle.append(data)
        elif comp.type == "Earning":
            earnings.append(data)
        elif comp.type == "Deduction":
            deductions.append(data)

    # -----------------------------------------------------------------------
    # SUMMARY ROWS
    # -----------------------------------------------------------------------

    # Gross Earnings
    gross_earn_values = [sum(x["values"][i] for x in earnings) for i in range(len(months))]
    earnings.append({
        "name": "Gross Earnings (A)",
        "values": gross_earn_values,
        "total": sum(gross_earn_values)
    })

    # Total Deductions
    deduction_values = [sum(x["values"][i] for x in deductions) for i in range(len(months))]
    deductions.append({
        "name": "Total Deductions (B)",
        "values": deduction_values,
        "total": sum(deduction_values)
    })

    # NET PAY
    net_pay_values = [
        gross_earn_values[i] - deduction_values[i] for i in range(len(months))
    ]

    net_pay = {
        "name": "Net Pay (A-B)",
        "values": net_pay_values,
        "total": sum(net_pay_values)
    }

    # Total Reimbursements
    reimbursement_values = [sum(x["values"][i] for x in reimbursements) for i in range(len(months))]
    reimbursements.append({
        "name": "Total Reimbursements",
        "values": reimbursement_values,
        "total": sum(reimbursement_values)
    })

    # Total Offcycle
    offcycle_values = [sum(x["values"][i] for x in offcycle) for i in range(len(months))]
    offcycle.append({
        "name": "Total Offcycle",
        "values": offcycle_values,
        "total": sum(offcycle_values)
    })

    # -----------------------------------------------------------------------

    return {
        "status": "success",
        "months": months,

        "earnings": earnings,
        "deductions": deductions,
        "net_pay": [net_pay],

        "reimbursements": reimbursements,
        "offcycle_earnings": offcycle,
    }
