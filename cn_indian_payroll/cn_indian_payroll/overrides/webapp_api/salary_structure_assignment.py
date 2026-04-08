


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


def format_version_data(version_data, modified, modified_by):
    import json

    if not version_data:
        return {}

    data = json.loads(version_data)

    result = {
        "doc_changes": [],
        "row_changes": []
    }

    for change in data.get("changed", []):
        result["doc_changes"].append({
            "property": change[0],
            "old_value": change[1],
            "new_value": change[2],
            "modified": modified,
            "modified_by": modified_by
        })

    for row_change in data.get("row_changed", []):
        table_field = row_change[0]
        row_index = row_change[1]
        field_changes = row_change[3]

        for field in field_changes:
            result["row_changes"].append({
                "table_field": table_field,
                "row_no": row_index,
                "property": field[0],
                "old_value": field[1],
                "new_value": field[2],
                "modified": modified,
                "modified_by": modified_by
            })

    return result

    
# http://127.0.0.1:8002/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.salary_structure_assignment.generate_salary_slip?employee=PW0220&payroll_period=25-26&company=Pen%20Pencil

@frappe.whitelist()
def generate_salary_slip(employee=None, payroll_period=None, company=None,order_by=None,start=0,page_length=10,search_term=None,):
    try:

        if not employee:
            return {
                "status": "failed",
                "message": "Employee is mandatory"
            }

        target_employee = frappe.request.headers.get("X-Target-Employee-Id")
        if target_employee:
            employee = target_employee

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
            fields=[
                "name",
                "salary_structure",
                "from_date",
                "custom_fixed_gross_annual",
                "custom_variable_pay"
            ],
            order_by=order_by
        )

        if not salary_structures:
            return {
                "status": "failed",
                "message": "No active Salary Structure Assignments found"
            }


        if search_term:
            search = search_term.lower()
            salary_structures = [
                row for row in salary_structures
                if any([
                    search in (row.get("name") or "").lower(),
                    search in (row.get("salary_structure") or "").lower(),
                ])
            ]


        total_count = len(salary_structures)
        salary_structures = salary_structures[start:start + page_length]

        if not salary_structures:
            return {
                "status": "success",
                "data": [],
                "total_count": total_count
            }

        response_data = []

        

        response_data = []

        for idx, assignment in enumerate(salary_structures):

            version = []

            component_part_of_ctc = []
            variable_pay_include = []
            variable_pay_exclude = []

            monthly_ctc = 0
            annual_ctc = 0
            total_deduction = 0

            monthly_reimbursement=0
            annual_reimbursement=0

            active = 1 if idx == 0 else 0

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
                slip.earnings,
                ctc_component_names,
                "Earning"
            )

            component_part_of_ctc.extend(earnings_ctc)

            monthly_ctc += earnings_total
            annual_ctc += earnings_total * 12

            deductions_ctc, deductions_total = process_components(
                slip.deductions,
                ctc_component_names,
                "Deduction"
            )

            component_part_of_ctc.extend(deductions_ctc)

            monthly_ctc += deductions_total
            annual_ctc += deductions_total * 12

            total_deduction += deductions_total * 12

            assignment_doc = frappe.get_doc(
                "Salary Structure Assignment",
                assignment.name
            )

            # ---------------- Reimbursements ----------------

            if hasattr(assignment_doc, "custom_employee_reimbursements"):

                for r in assignment_doc.custom_employee_reimbursements:
                    amount = round(r.monthly_total_amount or 0)

                    monthly_ctc += amount
                    annual_ctc += amount * 12

                    monthly_reimbursement+=amount
                    annual_reimbursement+=amount*12

                    component_part_of_ctc.append({
                        "component": r.reimbursements,
                        "amount": amount,
                        "annual_amount": amount * 12,
                        "type": "Reimbursement"
                    })

            # ---------------- Variable Pay ----------------

            if hasattr(assignment_doc, "custom_variable_pay_components"):

                for v in assignment_doc.custom_variable_pay_components:

                    amount = round(v.amount or 0)

                    variable_data = {
                        "component": v.variable_name,
                        "annual_amount": amount,
                        "type": "Variable Pay"
                    }

                    if v.part_of_ctc == 1:

                        variable_pay_include.append(variable_data)
                        annual_ctc += amount

                    else:

                        variable_pay_exclude.append(variable_data)

            # ---------------- Version History ----------------

            version_list = frappe.get_all(
                "Version",
                filters={
                    "docname": assignment.name,
                    "ref_doctype": "Salary Structure Assignment"
                },
                order_by="creation desc",
                fields=["name", "data", "modified", "modified_by"]
            )

            for v in version_list:

                formatted = format_version_data(
                    v.data,
                    v.modified,
                    v.modified_by
                )

                version.append({
                    "salary_structure_assignment": assignment.name,
                    "version_name": v.name,
                    "values_changed": formatted.get("doc_changes", []),
                    "row_values_changed": formatted.get("row_changes", [])
                })

            response_data.append({
                "assignment_name": assignment.name,
                "docstatus": 1,
                "active": active,
                "from_date": assignment.from_date,
                "salary_structure": assignment.salary_structure,

                "component_part_of_ctc": component_part_of_ctc,

                "variable_pay_include_ctc": variable_pay_include,
                "variable_pay_exclude_ctc": variable_pay_exclude,

                "monthly_ctc": round(monthly_ctc),
                "annual_ctc": round(annual_ctc),

                "gross_pay": round(slip.gross_pay or 0),
                "net_pay": round(slip.rounded_total or 0),
                "total_deduction": round(total_deduction),

                "fixed_gross_annual": round(assignment.custom_fixed_gross_annual or 0),
                "fixed_gross_monthly": round((assignment.custom_fixed_gross_annual or 0) / 12),

                "monthly_reimbursement":monthly_reimbursement,
                "annual_reimbursement":annual_reimbursement,

                "total_ctc": round(annual_ctc),

                "version": version,
                
            })

        return {
            "status": "success",
            "employee": employee,
            "data": response_data
        }

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "generate_salary_slip error"
        )

        return {
            "status": "failed",
            "message": "An unexpected error occurred while generating salary slip"
        }


