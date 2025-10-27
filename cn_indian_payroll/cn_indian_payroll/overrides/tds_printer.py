import frappe
from frappe.utils import getdate, add_months, flt

@frappe.whitelist()
def get_annual_statement_pdf(employee, payroll_period, end_date, month, tax_regime,id,income_tax_slab):


    end_date = getdate(end_date)

    period = frappe.db.get_value(
        "Payroll Period",
        payroll_period,
        ["start_date", "end_date"],
        as_dict=True
    )
    if not period:
        return {"html": "<p>Invalid Payroll Period.</p>"}

    fy_start = getdate(period.start_date)
    fy_end = getdate(period.end_date)

    slips = frappe.get_all(
        "Salary Slip",
        filters={
            "employee": employee,
            "end_date": ("<=", end_date),
            "docstatus": ["in", [1, 0]]
        },
        fields=["name", "start_date", "end_date", "employee"],
        order_by="start_date asc"
    )
    if not slips:
        return {"html": "<p>No salary slips found for given period.</p>"}


    months = []
    month_slip_map = {}
    month_date_map = {}

    current = fy_start
    while current <= fy_end:
        month_label = current.strftime("%B-%Y")
        months.append(month_label)
        month_date_map[month_label] = current

        for s in slips:
            if getdate(s.start_date).month == current.month and getdate(s.start_date).year == current.year:
                month_slip_map[month_label] = s.name
                tds_already_deducted=s.custom_additional_tds_deducted_amount

        current = add_months(current, 1)

    component_names = frappe.get_all(
        "Salary Detail",
        filters={"parent": ["in", [s.name for s in slips]]},
        distinct=True,
        pluck="salary_component"
    )

    components = frappe.get_all(
        "Salary Component",
        fields=[
            "name",
            "custom_sequence",
            "custom_component_sub_type",
            "component_type",  # Earning / Deduction
            "variable_based_on_taxable_salary",
            "type",
            "is_tax_applicable",
            "custom_tax_exemption_applicable_based_on_regime",
            "custom_is_reimbursement",
            "custom_is_offcycle_component"

        ],
        filters={"name": ["in", component_names]},
        order_by="custom_sequence asc"
    )

    last_slip = slips[-1]
    employee_doc = frappe.get_doc("Employee", last_slip.employee)

    last_slip_components = frappe.get_all(
        "Salary Detail",
        filters={"parent": last_slip.name},
        fields=["salary_component", "amount", "custom_actual_amount"]
    )
    last_slip_map = {
        d.salary_component: flt(d.custom_actual_amount or d.amount, 0)
        for d in last_slip_components
    }

    earnings = []
    deductions = []
    reimbursements=[]
    offcycle_earnings=[]
    tds_amounts=[]

    for m in months:
        slip_name = month_slip_map.get(m)
        if slip_name:
            slip_doc = frappe.get_doc("Salary Slip", slip_name)
            tds_amounts.append(flt(slip_doc.custom_additional_tds_deducted_amount or 0))
        else:
            tds_amounts.append(0)




    for comp in components:
        values = []
        for m in months:
            slip_name = month_slip_map.get(m)

            if slip_name:
                amount = frappe.db.get_value(
                    "Salary Detail",
                    {"parent": slip_name, "salary_component": comp.name},
                    "amount"
                ) or 0



            else:
                if month_date_map[m] > end_date:
                    if comp.custom_component_sub_type == "Fixed" or comp.type == "Deduction":
                        amount = round(last_slip_map.get(comp.name, 0))
                    else:
                        amount = 0


                else:
                    amount = 0

            values.append(amount)

        if comp.type == "Earning" and comp.is_tax_applicable and comp.custom_tax_exemption_applicable_based_on_regime and not comp.custom_is_offcycle_component and not comp.custom_is_reimbursement:
            earnings.append({
                "name": comp.name,
                "values": [flt(v, 0) for v in values],
                "total": flt(sum(values), 0),
                "sub_type": comp.custom_component_sub_type,
                "component_type": comp.component_type,
                "type": comp.type
            })

        if comp.type == "Earning" and comp.is_tax_applicable and comp.custom_tax_exemption_applicable_based_on_regime and comp.custom_is_offcycle_component and not comp.custom_is_reimbursement:
            offcycle_earnings.append({
                "name": comp.name,
                "values": [flt(v, 0) for v in values],
                "total": flt(sum(values), 0),
                "sub_type": comp.custom_component_sub_type,
                "component_type": comp.component_type,
                "type": comp.type
            })

        if comp.type == "Earning" and comp.is_tax_applicable and comp.custom_tax_exemption_applicable_based_on_regime and comp.custom_is_reimbursement:
            reimbursements.append({
                "name": comp.name,
                "values": [flt(v, 0) for v in values],
                "total": flt(sum(values), 0),
                "sub_type": comp.custom_component_sub_type,
                "component_type": comp.component_type,
                "type": comp.type
            })


        if comp.type == "Deduction" and (comp.component_type in ["Professional Tax","Provident Fund"] or comp.variable_based_on_taxable_salary):
            deductions.append({
                "name": comp.name,
                "values": [flt(v, 0) for v in values],
                "total": flt(sum(values), 0),
                "sub_type": comp.custom_component_sub_type,
                "component_type": comp.component_type,
                "type": comp.type,

            })


    monthly_totals = []
    for i in range(len(months)):
        monthly_earnings = sum(row["values"][i] for row in earnings)
        monthly_deductions = sum(row["values"][i] for row in deductions)
        monthly_totals.append(monthly_earnings - monthly_deductions)


    grand_total = flt(sum(monthly_totals), 0)

    total_earnings_sum = sum(row["total"] for row in earnings)
    total_deduction_sum = sum(row["total"] for row in deductions)
    total_reimbursement_sum = sum(row["total"] for row in reimbursements)
    total_offcycle_earning_sum = sum(row["total"] for row in offcycle_earnings)

    tds_amounts_sum = sum(tds_amounts)

    offcycle_net_pay = []

    offcycle_net_pay = []

    if offcycle_earnings:
        earning_values = offcycle_earnings[0].get("values", [])
        for i, earning in enumerate(earning_values):
            tds = tds_amounts[i] if i < len(tds_amounts) else 0
            offcycle_net_pay.append(earning - tds)

    tds_net_sum = sum(offcycle_net_pay)

    salary_slip_doc = frappe.get_doc("Salary Slip", id)

    sub_category = frappe.get_list(
        "Employee Tax Exemption Sub Category",
        filters={"custom_component_type": "LTA Reimbursement"},
        fields=["name"],
        limit=1
    )

    lta_component = None
    if sub_category:
        lta_component = sub_category[0]["name"]

    lta_array = []
    hra_received=0
    basic_as_per_salary_structure_10=0
    hra_exemption=0
    hra_percentage=0

    total_declaration=0
    net_taxable_income=0
    total_declaration_amount=0
    standard_amount=0

    declaration=[]
    if employee and payroll_period and end_date and month and tax_regime and income_tax_slab:
        tax_exemption = frappe.get_list(
            "Tax Declaration History",
            filters={
                "employee": employee,
                "posting_date": ["<=", end_date],
                "payroll_period": payroll_period,
                "tax_regime": tax_regime
            },
            fields=["name", "posting_date"],
            order_by="modified desc, posting_date desc",
            limit=1
        )

        if tax_exemption:
            section = frappe.get_doc("Tax Declaration History", tax_exemption[0]["name"])

            for i in section.declaration_details:
                if i.exemption_sub_category == lta_component:
                    lta_array.append({
                        "component": i.exemption_sub_category,
                        "amount": i.maximum_exempted_amount
                    })


                else:
                    eligible_amount = min(i.maximum_exempted_amount, i.declared_amount or 0)

                    declaration.append({
                        "component": i.exemption_sub_category,
                        "eligible_amount": eligible_amount,
                        "declared_amount": i.declared_amount or 0,
                    })



            hra_received=section.hra_as_per_salary_structure if section.hra_as_per_salary_structure  else 0
            basic_as_per_salary_structure_10=section.basic_as_per_salary_structure_10 if section.basic_as_per_salary_structure_10 else 0
            hra_exemption=section.annual_hra_exemption if section.annual_hra_exemption else 0
            if len(section.hra_breakup)>0:
                hra_percentage=section.hra_breakup[0].earned_basic
            else:
                hra_percentage=0

            standard_tax_amount=frappe.get_doc("Income Tax Slab",income_tax_slab)
            standard_amount=standard_tax_amount.standard_tax_exemption_amount

            total_declaration=section.total_exemption_amount





    lta_sum = sum(item["amount"] for item in lta_array)

    total_declaration_amount=round(total_declaration-lta_sum-hra_exemption)

    final_gross=(total_reimbursement_sum+total_earnings_sum+total_offcycle_earning_sum)

    final_after_hra_exemption=(final_gross-lta_sum-hra_exemption)

    net_taxable_income=round(final_gross-lta_sum-hra_exemption-standard_amount-total_declaration_amount)

    rebate=0
    total_tax_on_income=0
    surcharge=0
    education_cess=0
    total_income_taxable_amount=0
    taxable_amount=0
    tax_on_total_income=0
    custom_month_count=0
    tds=0


    if id:
        slip=frappe.get_doc("Salary Slip",id)
        rebate=slip.custom_rebate_under_section_87a
        total_tax_on_income=slip.custom_total_tax_on_income
        surcharge=slip.custom_surcharge
        education_cess=slip.custom_education_cess
        total_income_taxable_amount=slip.custom_total_income_with_taxable_component
        taxable_amount=slip.custom_taxable_amount
        tax_on_total_income=slip.custom_tax_on_total_income

        custom_month_count=slip.custom_month_count

        tds=slip.current_month_income_tax



    context = {
        "doc": salary_slip_doc,
        "employee": employee,
        "payroll_period": payroll_period,
        "months": months,
        "earnings": earnings,
        "total_earnings_sum":total_earnings_sum,

        "deductions": deductions,
        "total_deduction_sum":total_deduction_sum,

        "reimbursements":reimbursements,
        "total_reimbursement_sum":total_reimbursement_sum,

        "offcycle_earnings":offcycle_earnings,
        "total_offcycle_earning_sum":total_offcycle_earning_sum,

        "tds_amounts":tds_amounts,
        "tds_amounts_sum":tds_amounts_sum,


        "offcycle_net_pay":offcycle_net_pay,
        "tds_net_sum":tds_net_sum,


        "monthly_totals": monthly_totals,
        "grand_total": grand_total,
        "month": month,
        "date_of_joinee": employee_doc.date_of_joining,
        "pan": employee_doc.pan_number,
        "employee_name": employee_doc.employee_name,
        "esic": employee_doc.custom_esic_number,
        "pf": employee_doc.provident_fund_account,
        "tax_regime": tax_regime,
        "department": employee_doc.department,
        "designation": employee_doc.designation,
        "branch": employee_doc.branch,
        "tds_already_deducted":tds_already_deducted,
        "final_gross":final_gross,

        "lta_array":lta_array,
        "lta_sum":lta_sum,

        "hra_received":hra_received,
        "basic_as_per_salary_structure_10":basic_as_per_salary_structure_10,
        "hra_exemption":hra_exemption,
        "hra_percentage":hra_percentage,
        "final_after_hra_exemption":final_after_hra_exemption,
        "standard_amount":standard_amount,

        "declaration":declaration,

        "total_declaration":total_declaration_amount,
        "net_taxable_income":net_taxable_income,





        "rebate":rebate,
        "total_tax_on_income":total_tax_on_income,
        "surcharge":surcharge,
        "education_cess":education_cess,
        "total_income_taxable_amount":total_income_taxable_amount,
        "taxable_amount":taxable_amount,
        "tax_on_total_income":tax_on_total_income,

        "custom_month_count":custom_month_count,
        "tds":tds


    }

    html = frappe.render_template("cn_indian_payroll/templates/includes/annual_statement.html", context)
    return {"html": html}




# @frappe.whitelist(allow_guest=True)
# def get_payslip_tds_pdf_html(id):
#     slip = frappe.get_doc("Salary Slip", id)
#     context = {"doc": slip}
#     html = frappe.render_template(
#         "cn_indian_payroll/templates/includes/annual_statement.html", context
#     )
#     frappe.local.response["content_type"] = "text/html"
#     frappe.local.response["response"] = html




@frappe.whitelist(allow_guest=True)
def get_payslip_tds_pdf_html(id):
    from cn_indian_payroll.cn_indian_payroll.overrides.tds_printer import get_annual_statement_pdf

    slip = frappe.get_doc("Salary Slip", id)
    employee = slip.employee
    payroll_period = slip.payroll_period
    end_date = slip.end_date
    month = slip.custom_month or slip.month
    tax_regime = slip.custom_tax_regime
    income_tax_slab = slip.custom_income_tax_slab

    # Call the existing function to generate context
    result = get_annual_statement_pdf(employee, payroll_period, end_date, month, tax_regime, id, income_tax_slab)

    html = result.get("html")

    frappe.local.response["content_type"] = "text/html"
    frappe.local.response["response"] = html




# @frappe.whitelist()
# def get_payslip_pdf_json(id):
#     slip = frappe.get_doc("Salary Slip", id)
#     context = {"doc": slip}
#     html = frappe.render_template("cn_indian_payroll/templates/includes/regular_payslip.html", context)
#     return {"html": html}


@frappe.whitelist(allow_guest=True)
def get_payslip_pdf_html(id):
    slip = frappe.get_doc("Salary Slip", id)
    context = {"doc": slip}
    html = frappe.render_template(
        "cn_indian_payroll/templates/includes/regular_payslip.html", context
    )
    frappe.local.response["content_type"] = "text/html"
    frappe.local.response["response"] = html















@frappe.whitelist()
def get_payslip_pdf(id):
    # Fetch Salary Slip by name (id)
    try:
        slip = frappe.get_doc("Salary Slip", id)

    except frappe.DoesNotExistError:
        return {"html": "<p>No salary slip found.</p>"}

    context = {
        "doc": slip
    }



    html = frappe.render_template(
        "cn_indian_payroll/templates/includes/regular_payslip.html",
        context
    )
    return {"html": html}


@frappe.whitelist()
def get_benefit_payslip_pdf(id):
    try:
        slip = frappe.get_doc("Salary Slip", id)

        find = False

        if slip.earnings:
            for earning in slip.earnings:
                get_component = frappe.get_doc("Salary Component", earning.salary_component)
                if get_component.custom_is_reimbursement:
                    find = True
                    break

    except frappe.DoesNotExistError:
        return {"html": "<p>No salary slip found.</p>"}

    context = {"doc": slip}

    if find:
        html = frappe.render_template(
            "cn_indian_payroll/templates/includes/benefit_payslip.html",
            context
        )
        return {"html": html}
    else:
        return {
            "html": """
                <div style="
                    padding: 12px;
                    margin: 10px 0;
                    border: 1px solid #f5c2c7;
                    background-color: #f8d7da;
                    color: #842029;
                    border-radius: 6px;
                    font-size: 14px;
                    font-family: Arial, sans-serif;
                ">
                    ⚠️ No Reimbursement component found in salary slip.
                </div>
            """
        }




@frappe.whitelist(allow_guest=True)
def get_benefit_payslip_pdf_html(id):
    slip = frappe.get_doc("Salary Slip", id)

    # Check if any earning component is a reimbursement
    find = False
    if slip.earnings:
        for earning in slip.earnings:
            component = frappe.get_cached_doc("Salary Component", earning.salary_component)
            if component.custom_is_reimbursement:
                find = True
                break

    context = {"doc": slip}

    if find:
        # Render Benefit Payslip
        html = frappe.render_template(
            "cn_indian_payroll/templates/includes/benefit_payslip.html",
            context
        )
    else:
        # Render Warning Message inside HTML
        html = """
            <div style="
                padding: 12px;
                margin: 10px 0;
                border: 1px solid #f5c2c7;
                background-color: #f8d7da;
                color: #842029;
                border-radius: 6px;
                font-size: 14px;
                font-family: Arial, sans-serif;
            ">
                ⚠️ No Reimbursement component found in this salary slip.
            </div>
        """

    # Set HTTP Response
    frappe.local.response["content_type"] = "text/html"
    frappe.local.response["response"] = html












@frappe.whitelist()
def get_offcycle_payslip_pdf(id):
    try:
        slip = frappe.get_doc("Salary Slip", id)

        find = False

        if slip.earnings:
            for earning in slip.earnings:
                get_component = frappe.get_doc("Salary Component", earning.salary_component)
                if get_component.custom_is_part_of_gross_pay==0 and get_component.do_not_include_in_total==1 and get_component.custom_component_sub_type=="Variable":
                    find = True
                    break

    except frappe.DoesNotExistError:
        return {"html": "<p>No salary slip found.</p>"}

    context = {"doc": slip}

    if find:
        html = frappe.render_template(
            "cn_indian_payroll/templates/includes/off_cycle_payslip.html",
            context
        )
        return {"html": html}
    else:
        return {
            "html": """
                <div style="
                    padding: 12px;
                    margin: 10px 0;
                    border: 1px solid #f5c2c7;
                    background-color: #f8d7da;
                    color: #842029;
                    border-radius: 6px;
                    font-size: 14px;
                    font-family: Arial, sans-serif;
                ">
                    ⚠️ No Offcycle component found in salary slip.
                </div>
            """
        }




@frappe.whitelist(allow_guest=True)
def get_offcycle_payslip_pdf_html(id):
    try:
        slip = frappe.get_doc("Salary Slip", id)

        # Flag to check Offcycle eligibility
        find = False
        if slip.earnings:
            for earning in slip.earnings:
                component = frappe.get_cached_doc("Salary Component", earning.salary_component)
                if (
                    getattr(component, "custom_is_part_of_gross_pay", 0) == 0
                    and getattr(component, "do_not_include_in_total", 0) == 1
                    and getattr(component, "custom_component_sub_type", "") == "Variable"
                ):
                    find = True
                    break

    except frappe.DoesNotExistError:
        html = "<p>No salary slip found.</p>"
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "get_offcycle_payslip_pdf_html Error")
        html = f"<p style='color:red;'>Error: {str(e)}</p>"
    else:
        context = {"doc": slip}

        if find:
            html = frappe.render_template(
                "cn_indian_payroll/templates/includes/off_cycle_payslip.html",
                context
            )
        else:
            html = """
                <div style="
                    padding: 12px;
                    margin: 10px 0;
                    border: 1px solid #f5c2c7;
                    background-color: #f8d7da;
                    color: #842029;
                    border-radius: 6px;
                    font-size: 14px;
                    font-family: Arial, sans-serif;
                ">
                    ⚠️ No Offcycle component found in this salary slip.
                </div>
            """

    # Final Frappe HTTP Response
    frappe.local.response["content_type"] = "text/html"
    frappe.local.response["response"] = html
