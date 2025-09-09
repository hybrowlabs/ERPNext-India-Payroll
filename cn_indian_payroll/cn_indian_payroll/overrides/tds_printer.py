



# import frappe
# from frappe.utils import getdate, add_months, flt

# @frappe.whitelist()
# def get_annual_statement_pdf(employee, payroll_period, end_date, month,tax_regime):
#     end_date = getdate(end_date)

#     # Fetch payroll period (get its start and end date)
#     period = frappe.db.get_value(
#         "Payroll Period",
#         payroll_period,
#         ["start_date", "end_date"],
#         as_dict=True
#     )
#     if not period:
#         return {"html": "<p>Invalid Payroll Period.</p>"}

#     fy_start = getdate(period.start_date)
#     fy_end = getdate(period.end_date)

#     # 1. Get Salary Slips till given end_date
#     slips = frappe.get_all(
#         "Salary Slip",
#         filters={
#             "employee": employee,
#             "end_date": ("<=", end_date),
#             "docstatus": ["in", [1, 0]]
#         },
#         fields=["name", "start_date", "end_date","employee"],
#         order_by="start_date asc"
#     )
#     if not slips:
#         return {"html": "<p>No salary slips found for given period.</p>"}

#     # Build months list from payroll_period start_date to end_date
#     months = []
#     month_slip_map = {}
#     current = fy_start
#     while current <= fy_end:
#         month_label = current.strftime("%B-%Y")
#         months.append(month_label)

#         # map slip if available
#         for s in slips:
#             if getdate(s.start_date).month == current.month and getdate(s.start_date).year == current.year:
#                 month_slip_map[month_label] = s.name

#         current = add_months(current, 1)

#     # 2. Get all components that appeared in actual slips
#     component_names = frappe.get_all(
#         "Salary Detail",
#         filters={"parent": ["in", [s.name for s in slips]]},
#         distinct=True,
#         pluck="salary_component"
#     )

#     # Fetch their custom sequence and type (Fixed/Variable)
#     components = frappe.get_all(
#         "Salary Component",
#         fields=["name", "custom_sequence", "custom_component_sub_type"],
#         filters={
#             "name": ["in", component_names],
#             "is_tax_applicable": 1,
#             "custom_tax_exemption_applicable_based_on_regime": 1,
#             "custom_regime": ["in", ["All", "Old Regime", "New Regime"]],
#         },
#         order_by="custom_sequence asc"
#     )

#     # frappe.msgprint(str(components))

#     for deduction in component_names:
#         deduction_component=frappe.get_doc("Salary Component",deduction)

#         if deduction_component.component_type=="Provident Fund":
#             pf_amount+=

#         if  deduction_component.component_type=="Professional Tax":
#             pt_amount+=


#         if  deduction_component.variable_based_on_taxable_salary==1:
#             income_tax_amount+=


#     # 3. Get the last available slip (for projection)
#     last_slip = slips[-1]
#     employee_doc=frappe.get_doc("Employee",last_slip.employee)
#     date_of_joinee=employee_doc.date_of_joining
#     pan=employee_doc.pan_number
#     employee_name=employee_doc.employee_name
#     esic=employee_doc.custom_esic_number
#     pf=employee_doc.provident_fund_account
#     branch=employee_doc.branch
#     designation=employee_doc.designation
#     department=employee_doc.department


#     last_slip_components = frappe.get_all(
#         "Salary Detail",
#         filters={"parent": last_slip.name},
#         fields=["salary_component", "amount", "custom_actual_amount"]
#     )
#     # Prefer custom_actual_amount for future projection
#     last_slip_map = {
#         d.salary_component: flt(d.custom_actual_amount or d.amount, 0)
#         for d in last_slip_components
#     }

#     # 4. Prepare particulars matrix
#     particulars = []
#     for comp in components:
#         values = []
#         for m in months:
#             slip_name = month_slip_map.get(m)
#             if slip_name:
#                 # actual slip value
#                 amount = frappe.db.get_value(
#                     "Salary Detail",
#                     {"parent": slip_name, "salary_component": comp.name},
#                     "amount"
#                 ) or 0
#                 amount = flt(amount, 0)
#             else:
#                 # future month
#                 if comp.custom_component_sub_type == "Fixed":
#                     # use custom_actual_amount (rounded)
#                     amount = round(last_slip_map.get(comp.name, 0))
#                 else:  # Variable
#                     amount = 0
#             values.append(amount)

#         particulars.append({
#             "name": comp.name,
#             "values": [flt(v, 0) for v in values],
#             "total": flt(sum(values), 0),
#             "sub_type": comp.custom_component_sub_type
#         })


#     # 5. Monthly totals
#     monthly_totals = [flt(sum(row["values"][i] for row in particulars), 0) for i in range(len(months))]



#     # 6. Grand total
#     grand_total = flt(sum(monthly_totals), 0)

#     # 7. Context for template
#     context = {
#         "employee": employee,
#         "payroll_period": payroll_period,
#         "months": months,
#         "particulars": particulars,
#         "monthly_totals": monthly_totals,
#         "grand_total": grand_total,
#         "month": month,
#         "date_of_joinee":date_of_joinee,
#         "pan":pan,
#         "employee_name":employee_name,
#         "esic":esic,
#         "pf":pf,
#         "tax_regime":tax_regime,
#         "department":department,
#         "designation":designation,
#         "branch":branch
#         }

#     html = frappe.render_template("cn_indian_payroll/templates/includes/annual_statement.html", context)
#     return {"html": html}


import frappe
from frappe.utils import getdate, add_months, flt

@frappe.whitelist()
def get_annual_statement_pdf(employee, payroll_period, end_date, month, tax_regime):
    end_date = getdate(end_date)

    # Fetch payroll period (get its start and end date)
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

    # 1. Get Salary Slips till given end_date
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

    # Build months list from payroll_period start_date to end_date
    months = []
    month_slip_map = {}
    current = fy_start
    while current <= fy_end:
        month_label = current.strftime("%B-%Y")
        months.append(month_label)

        # map slip if available
        for s in slips:
            if getdate(s.start_date).month == current.month and getdate(s.start_date).year == current.year:
                month_slip_map[month_label] = s.name

        current = add_months(current, 1)

    # 2. Get all components that appeared in actual slips (earnings + deductions)
    component_names = frappe.get_all(
        "Salary Detail",
        filters={"parent": ["in", [s.name for s in slips]]},
        distinct=True,
        pluck="salary_component"
    )

    # Fetch component details
    components = frappe.get_all(
        "Salary Component",
        fields=[
            "name",
            "custom_sequence",
            "custom_component_sub_type",
            "component_type",  # Earning / Deduction
            "variable_based_on_taxable_salary"
        ],
        filters={"name": ["in", component_names]},
        order_by="custom_sequence asc"
    )

    # 3. Get the last available slip (for projection)
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

    # 4. Prepare particulars matrix (earnings + deductions)
    particulars = []
    for comp in components:
        values = []
        for m in months:
            slip_name = month_slip_map.get(m)
            if slip_name:
                # actual slip value
                amount = frappe.db.get_value(
                    "Salary Detail",
                    {"parent": slip_name, "salary_component": comp.name},
                    "amount"
                ) or 0
                amount = flt(amount, 0)
            else:
                # future month projection
                if comp.custom_component_sub_type == "Fixed" or comp.component_type == "Deduction":
                    amount = round(last_slip_map.get(comp.name, 0))
                else:
                    amount = 0
            values.append(amount)

        particulars.append({
            "name": comp.name,
            "values": [flt(v, 0) for v in values],
            "total": flt(sum(values), 0),
            "sub_type": comp.custom_component_sub_type,
            "component_type": comp.component_type
        })

    # 5. Monthly totals (earnings - deductions)
    monthly_totals = []
    for i in range(len(months)):
        earnings = sum(row["values"][i] for row in particulars if row["component_type"] == "Earning")
        deductions = sum(row["values"][i] for row in particulars if row["component_type"] == "Deduction")
        monthly_totals.append(earnings - deductions)

    # 6. Grand total (net salary for year)
    grand_total = flt(sum(monthly_totals), 0)

    # 7. Context for template
    context = {
        "employee": employee,
        "payroll_period": payroll_period,
        "months": months,
        "particulars": particulars,
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
        "branch": employee_doc.branch
    }

    html = frappe.render_template("cn_indian_payroll/templates/includes/annual_statement.html", context)
    return {"html": html}




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

    # frappe.msgprint(str(context))

    html = frappe.render_template(
        "cn_indian_payroll/templates/includes/regular_payslip.html",
        context
    )
    return {"html": html}


@frappe.whitelist()
def get_benefit_payslip_pdf(id):
    # Fetch Salary Slip by name (id)
    try:
        slip = frappe.get_doc("Salary Slip", id)

    except frappe.DoesNotExistError:
        return {"html": "<p>No salary slip found.</p>"}

    context = {
        "doc": slip
    }

    # frappe.msgprint(str(context))

    html = frappe.render_template(
        "cn_indian_payroll/templates/includes/benefit_payslip.html",
        context
    )
    return {"html": html}

@frappe.whitelist()
def get_offcycle_payslip_pdf(id):
    # Fetch Salary Slip by name (id)
    try:
        slip = frappe.get_doc("Salary Slip", id)

    except frappe.DoesNotExistError:
        return {"html": "<p>No salary slip found.</p>"}

    context = {
        "doc": slip
    }

    # frappe.msgprint(str(context))

    html = frappe.render_template(
        "cn_indian_payroll/templates/includes/off_cycle_payslip.html",
        context
    )
    return {"html": html}
