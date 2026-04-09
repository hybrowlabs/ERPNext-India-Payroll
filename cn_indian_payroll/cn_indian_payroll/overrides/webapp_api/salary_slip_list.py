
import frappe
from cn_indian_payroll.cn_indian_payroll.doctype.contract_employee_setting.contract_employee_setting import get_invoice_status



@frappe.whitelist()
def get_salary_slip_list(employee=None, company=None,start=0,page_length=10,order_by=None,search_term=None,payroll_period=None):

    target_employee = frappe.request.headers.get("X-Target-Employee-Id")
    if target_employee:
        employee = target_employee

    salary_slips = frappe.get_all(
        "Salary Slip",
        filters={
            "employee": employee,
            "company": company,
            "docstatus": ["in", [0, 1]],
            "custom_payroll_period": payroll_period
        },
        fields=[
            "name",
            "employee_name",
            "start_date",
            "end_date",
            "gross_pay",
            "net_pay",
            "employee",
            "custom_payroll_period",
            "custom_month",
            "custom_attach",
            "status",
            
        ],
        # order_by="end_date desc",
        order_by=order_by
    )


    if search_term:
        search = search_term.lower()

        salary_slips = [
            row for row in salary_slips
            if (
                search in (row.get("name") or "").lower()
                or search in (row.get("employee_name") or "").lower()
                or search in (row.get("custom_month") or "").lower()
            )
        ]

    total_count = len(salary_slips)
    salary_slips = salary_slips[start:start + page_length]

    result = []

    for slip in salary_slips:

        # Call imported function
        invoice_status = get_invoice_status(slip["name"])

        # Add status to response
        slip["invoice_status"] = invoice_status

        result.append(slip)

    return {
        "status": "success",
        "total_count": total_count,
        "start": start,
        "page_length": page_length,
        "data": result
    }




@frappe.whitelist()
def get_consultant_payslip_pdf(slip_id):
    try:
        slip = frappe.get_doc("Salary Slip", slip_id)
    except frappe.DoesNotExistError:
        return {"html": "<p>No salary slip found.</p>"}

    context = {"doc": slip}

    html = frappe.render_template(
        "cn_indian_payroll/templates/includes/invoice.html",
        context
    )

    return {"html": html}



# http://127.0.0.1:8002/api/method/cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.salary_slip_list.salary_slip_list_view?employee=PW0220&company=Pen%20Pencil&payroll_period=25-26


@frappe.whitelist()
def salary_slip_list_view(employee=None, company=None, start=0, page_length=10, order_by=None, search_term=None, payroll_period=None):

    target_employee = frappe.request.headers.get("X-Target-Employee-Id")
    if target_employee:
        employee = target_employee

    start = int(start)
    page_length = int(page_length)

    filters = {
        "docstatus": ["in", [0, 1]]
    }

    if employee:
        filters["employee"] = employee
    if company:
        filters["company"] = company
    if payroll_period:
        filters["custom_payroll_period"] = payroll_period


    total_count = frappe.db.count("Salary Slip", filters)

    salary_slips = frappe.get_all(
        "Salary Slip",
        filters=filters,
        fields=[
            "name",
            "employee_name",
            "start_date",
            "end_date",
            "gross_pay",
            "net_pay",
            "employee",
            "custom_payroll_period",
            "custom_month",
            "custom_attach",
            "status"
        ],
        order_by=order_by,
        start=start,
        page_length=page_length
    )

    result = []

    for sal in salary_slips:
        salary_slip_type = "Regular"

        sal_slip = frappe.get_doc("Salary Slip", sal.name)

        for i in sal_slip.earnings:
            component = frappe.get_doc("Salary Component", i.salary_component)

            if component.custom_is_offcycle_component:
                salary_slip_type = "Regular + Offcycle"
                break  

        if sal.status == "Submitted":
            status = "Paid"
        else:
            status = "Draft"

        result.append({
            "salary_slip_id": sal.name,
            "employee_name": sal.employee_name,
            "start_date": sal.start_date,
            "end_date": sal.end_date,
            "gross_pay": round(sal.gross_pay),
            "net_pay": round(sal.net_pay),
            "employee": sal.employee,
            "custom_payroll_period": sal.custom_payroll_period,
            "custom_month": sal.custom_month,
            "status": status,
            "salary_slip_type": salary_slip_type
        })

    if search_term:
        search = search_term.lower()
        result = [
            row for row in result
            if (
                search in (row.get("salary_slip_id") or "").lower()
                or search in (row.get("employee_name") or "").lower()
                or search in (row.get("custom_month") or "").lower()
                or search in (row.get("gross_pay") or "").lower()
                or search in (row.get("net_pay") or "").lower()
            )
        ]

    return {
        "status": "success",
        "data": result,   
        "total_count": total_count,
        "start": start,
        "page_length": page_length,
        
    }