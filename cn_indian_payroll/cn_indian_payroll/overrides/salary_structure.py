import frappe
import json

@frappe.whitelist()
def get_ctc_breakup(doc):
    if isinstance(doc, str):
        doc = json.loads(doc)

    doc = frappe._dict(doc)

    response = frappe.get_doc({
        "doctype": "Salary Slip"
    })

    # Call salary slip generator
    slip = frappe.get_doc(
        frappe.get_attr("hrms.payroll.doctype.salary_structure.salary_structure.make_salary_slip")(
            source_name=doc.salary_structure,
            employee=doc.employee,
            print_format="Salary Slip Standard",            
            posting_date=doc.from_date,
            for_preview=1,
        )
    )

    earnings_data = []
    deductions_data = []
    reimbursements_data = []
    variable_include = []
    variable_exclude = []

    total_monthly = 0
    total_annual = 0
    fixed_gross = 0
    fixed_gross_annual = 0

    for v in slip.earnings:
        component = frappe.get_cached_doc("Salary Component", v.salary_component)

        if component.custom_is_part_of_ctc and component.custom_component_sub_type == "Fixed":
            monthly = round(v.amount)
            annual = monthly * 12

            earnings_data.append({
                "component": component.name,
                "monthly": monthly,
                "annual": annual
            })

            total_monthly += monthly
            total_annual += annual

            fixed_gross += monthly
            fixed_gross_annual += annual


    for v in slip.deductions:
        component = frappe.get_cached_doc("Salary Component", v.salary_component)

        if component.custom_is_part_of_ctc and component.custom_component_sub_type == "Fixed":
            monthly = round(v.amount)
            annual = monthly * 12

            deductions_data.append({
                "component": component.name,
                "monthly": monthly,
                "annual": annual
            })

            total_monthly += monthly
            total_annual += annual


    for r in doc.get("custom_employee_reimbursements", []):
        component = frappe.get_cached_doc("Salary Component", r.get("reimbursements"))

        monthly = round(r.get("monthly_total_amount", 0))
        annual = monthly * 12

        if component.custom_include_ctc_total:
            reimbursements_data.append({
                "component": r.get("reimbursements"),
                "monthly": monthly,
                "annual": annual
            })

            total_monthly += monthly
            total_annual += annual

        else:
            earnings_data.append({
                "component": r.get("reimbursements"),
                "monthly": monthly,
                "annual": annual
            })

            fixed_gross += monthly
            fixed_gross_annual += annual



    for v in doc.get("custom_variable_pay_components", []):
        amount = round(v.get("amount", 0))

        if v.get("part_of_ctc"):
            variable_include.append({
                "component": v.get("variable_name"),
                "amount": amount
            })
            total_annual += amount
        else:
            variable_exclude.append({
                "component": v.get("variable_name"),
                "amount": amount
            })

    return {
        "earnings": earnings_data,
        "deductions": deductions_data,
        "reimbursements": reimbursements_data,
        "variable_include": variable_include,
        "variable_exclude": variable_exclude,
        "total_monthly": total_monthly,
        "total_annual": total_annual,
        "fixed_gross": fixed_gross,
        "fixed_gross_annual": fixed_gross_annual
    }