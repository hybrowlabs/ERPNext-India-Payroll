# cn_indian_payroll/cn_indian_payroll/overrides/api.py

import frappe
from frappe.utils import getdate
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip

@frappe.whitelist(allow_guest=True)
def generate_salary_slip(employee):
    target_employee = frappe.request.headers.get("X-Target-Employee-Id")
    if target_employee:
        employee = target_employee
    earning_component_part_of_ctc = []
    deduction_component_part_of_ctc = []

    try:
        if not employee:
            return {"error": "Employee not provided"}

        salary_structure = frappe.get_list(
            "Salary Structure Assignment",
            filters={"employee": employee, "docstatus": 1},
            fields=["*"],
            order_by="from_date desc",
            limit=1
        )

        if not salary_structure:
            return {"error": f"No active Salary Structure Assignment found for {employee}"}

        assignment = salary_structure[0]

        slip = make_salary_slip(
            source_name=assignment.salary_structure,
            employee=employee,
            print_format='Salary Slip Standard',
            for_preview=1,
            posting_date=assignment.from_date
        )

        # Loop over earnings
        if slip and slip.earnings:
            for earning in slip.earnings:
                try:
                    earning_component = frappe.get_doc("Salary Component", earning.salary_component)
                    if earning_component.custom_is_part_of_ctc == 1:
                        earning_component_part_of_ctc.append({
                            "component": earning_component.name,
                            "amount": round(earning.amount),
                            "annual_amount": round(earning.amount * 12)
                        })
                except:
                    pass

        # Loop over deductions
        if slip and slip.deductions:
            for deduction in slip.deductions:
                try:
                    deduction_component = frappe.get_doc("Salary Component", deduction.salary_component)
                    if deduction_component.custom_is_part_of_ctc == 1:
                        deduction_component_part_of_ctc.append({
                            "component": deduction_component.name,
                            "amount": round(deduction.amount),
                            "annual_amount": round(deduction.amount * 12)
                        })
                except:
                    pass

        net_pay=slip.rounded_total or 0


        # Get reimbursement and other details
        assignment_doc = frappe.get_doc("Salary Structure Assignment", assignment.name)

        return {
            "salary_slip": slip,
            "net_pay":net_pay,
            "earning_component_part_of_ctc": earning_component_part_of_ctc,
            "deduction_component_part_of_ctc": deduction_component_part_of_ctc,
            "reimbursements_part_of_ctc": assignment_doc.custom_employee_reimbursements,
            "total_reimbursement_amount": assignment_doc.custom_total_reimbursement_amount
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in generate_salary_slip")
        return {"error": str(e)}



@frappe.whitelist()
def get_eligible_payslips(employee, salary_slip_id):
    target_employee = frappe.request.headers.get("X-Target-Employee-Id")
    if target_employee:
        employee = target_employee
    if not employee or not salary_slip_id:
        return {"error": "Employee or Salary Slip ID not provided"}

    # Initialize flags
    off_payslip_exists = 0
    tds_payslip_exists = 0
    benefit_payslip_exists = 0
    regular_payslip_exists = 0

    # Fetch salary slip
    ss = frappe.get_doc("Salary Slip", salary_slip_id)

    # Check for TDS payslip
    if ss.current_month_income_tax:
        tds_payslip_exists = 1

    # Check for regular payslip
    if ss.gross_pay:
        regular_payslip_exists = 1

    # Loop through earnings
    for earning in ss.earnings:
        salary_component = frappe.get_doc("Salary Component", earning.salary_component)

        # Check off-cycle component
        if salary_component.custom_is_offcycle_component == 1:
            off_payslip_exists = 1

        # Check reimbursement / benefit component
        if salary_component.custom_is_reimbursement == 1:
            benefit_payslip_exists = 1

    # Return results
    return {
        # "employee": employee,
        # "salary_slip_id": salary_slip_id,
        "off_payslip_exists": off_payslip_exists,
        "tds_payslip_exists": tds_payslip_exists,
        "benefit_payslip_exists": benefit_payslip_exists,
        "regular_payslip_exists": regular_payslip_exists
    }
