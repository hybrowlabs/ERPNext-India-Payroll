

import frappe
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip
from frappe import _



def process_components(components, ctc_component_names, comp_type):
    component_list = []
    total = 0

    for comp in components:
        if comp.salary_component in ctc_component_names:
            amount = round(comp.amount or 0)
            total += amount
            component_list.append({
                "component": comp.salary_component,
                "amount": amount,
                "annual_amount": amount * 12,
                "type": comp_type
            })

    return component_list, total

#http://127.0.0.1:8000/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.salary_structure_assignment.generate_salary_slip?employee=37001


@frappe.whitelist()
def generate_salary_slip(employee=None, payroll_period=None, company=None):
    try:

        if not employee:
            return {
                "status": "failed",
                "message": "Employee is mandatory"
            }


        filters = {
            "employee": employee,
            "docstatus": 1
        }

        if payroll_period:
            filters["custom_payroll_period"] = payroll_period

        if company:
            filters["company"] = company

        salary_structures = frappe.get_all(
            "Salary Structure Assignment",
            filters=filters,
            fields=["name", "salary_structure", "from_date","custom_fixed_gross_annual","custom_variable_pay"],
            order_by="from_date desc"
        )

        if not salary_structures:
            return {
                "status": "failed",
                "message": "No active Salary Structure Assignments found"
            }

        response_data = []


        for assignment in salary_structures:

            component_part_of_ctc = []
            monthly_ctc = 0
            annual_ctc = 0
            total_deduction = 0

            slip = make_salary_slip(
                source_name=assignment.salary_structure,
                employee=employee,
                posting_date=assignment.from_date,
                for_preview=1
            )

            component_names = list(
                {e.salary_component for e in slip.earnings if e.salary_component}.union(
                    {d.salary_component for d in slip.deductions if d.salary_component}
                )
            )

            ctc_component_names = set()
            if component_names:
                ctc_components = frappe.get_all(
                    "Salary Component",
                    filters={
                        "name": ["in", component_names],
                        "custom_is_part_of_ctc": 1
                    },
                    fields=["name"]
                )
                ctc_component_names = {c.name for c in ctc_components}

            earnings_ctc, earnings_total = process_components(
                slip.earnings, ctc_component_names, "Earning"
            )
            component_part_of_ctc.extend(earnings_ctc)
            monthly_ctc += round(earnings_total)
            annual_ctc += round(earnings_total) * 12

            deductions_ctc, deductions_total = process_components(
                slip.deductions, ctc_component_names, "Deduction"
            )
            component_part_of_ctc.extend(deductions_ctc)
            monthly_ctc += deductions_total
            annual_ctc += deductions_total * 12
            total_deduction += deductions_total * 12

            assignment_doc = frappe.get_doc(
                "Salary Structure Assignment", assignment.name
            )

            if hasattr(assignment_doc, "custom_employee_reimbursements"):
                for r in assignment_doc.custom_employee_reimbursements:
                    amount = round(r.monthly_total_amount or 0)
                    monthly_ctc += amount
                    annual_ctc += amount * 12
                    component_part_of_ctc.append({
                        "component": r.reimbursements,
                        "amount": amount,
                        "annual_amount": amount * 12,
                        "type": "Reimbursement"
                    })

            response_data.append({
                "assignment_name": assignment.name,
                "docstatus":1,
                "from_date": assignment.from_date,
                "salary_structure": assignment.salary_structure,
                "component_part_of_ctc": component_part_of_ctc,
                "monthly_ctc": round(monthly_ctc),
                "annual_ctc": round(annual_ctc),
                "gross_pay": round(slip.gross_pay or 0),
                "net_pay": round(slip.rounded_total or 0),
                "total_deduction": round(total_deduction),
                "fixed_gross_annual":round(assignment.custom_fixed_gross_annual),
                "fixed_gross_monthly":round(assignment.custom_fixed_gross_annual/12),
                "annual_variable_pay":round(assignment.custom_variable_pay),
                "total_ctc":round(annual_ctc+assignment.custom_variable_pay)


            })

        return {
            "status": "success",
            "employee": employee,
            "data": response_data
        }

    except Exception:
        frappe.log_error(frappe.get_traceback(), "generate_salary_slip error")
        return {
            "status": "failed",
            "message": "An unexpected error occurred while generating salary slip"
        }
