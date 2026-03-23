import frappe

import frappe
from datetime import datetime
import calendar



@frappe.whitelist()
def benefit_data_dashboard(company=None, payroll_period=None, status=None, month=None):

    filters = {
        "docstatus": ("in", [0, 1]),
    }

    if company:
        filters["company"] = company

    if payroll_period:
        filters["custom_payroll_period"] = payroll_period

    if status:
        filters["custom_status"] = status

    from_date = None
    to_date = None

    if month and payroll_period:

        period = frappe.db.get_value(
            "Payroll Period",
            payroll_period,
            ["start_date", "end_date"],
            as_dict=True
        )

        if period:

            start_year = period.start_date.year   
            end_year = period.end_date.year      

            month_number = datetime.strptime(month, "%B").month

            if month_number >= 4:
                year = start_year
            else:
                year = end_year

            last_day = calendar.monthrange(year, month_number)[1]

            from_date = f"{year}-{month_number:02d}-01"
            to_date = f"{year}-{month_number:02d}-{last_day}"

            filters["claim_date"] = ["between", [from_date, to_date]]

    claims = frappe.db.get_all(
        "Employee Benefit Claim",
        filters=filters,
        fields=[
            "name",
            "employee_name",
            "custom_payroll_period",
            "claim_date",
            "custom_status",
            "earning_component",
            "claimed_amount",
        ],
        order_by="claim_date desc",
    )

    return {
        "status": "success",
        "data": claims,
        "total_records": len(claims),
        "from_date": from_date,
        "to_date": to_date
    }




@frappe.whitelist()
def list_arrear_details(company=None, payroll_period=None, month=None):

    total_filters = {
        "docstatus": ("in", [0, 1]),
    }

    pending_filter = {
        "docstatus": 0
    }

    submitted_filter = {
        "docstatus": 1
    }

    if company:
        total_filters["company"] = company
        pending_filter["company"] = company
        submitted_filter["company"] = company

    if payroll_period:
        total_filters["payroll_period"] = payroll_period
        pending_filter["payroll_period"] = payroll_period
        submitted_filter["payroll_period"] = payroll_period

    if month:
        total_filters["lop_month_reversal"] = month
        pending_filter["lop_month_reversal"] = month
        submitted_filter["lop_month_reversal"] = month


    total_claims = frappe.db.count(
        "LOP Reversal",
        filters=total_filters,
    )

    pending_claims = frappe.db.count(
        "LOP Reversal",
        filters=pending_filter,
    )

    submitted_claims = frappe.db.count(
        "LOP Reversal",
        filters=submitted_filter,
    )


    # claims = frappe.get_all(
    #     "LOP Reversal",
    #     filters=total_filters,
    #     fields=[
    #         "name",
    #         "employee",
    #         "employee_name",
    #         "lop_month_reversal",
    #         "posting_date",
    #         "docstatus"
    #     ],
    #     order_by="creation desc"
    # )

    return {
        "status": "success",
        # "data": claims,
        # "total_records": len(claims),
        "total": total_claims,
        "pending": pending_claims,
        "submitted": submitted_claims,

    }


@frappe.whitelist()
def list_advance_details(company=None, payroll_period=None, month=None):

    import calendar
    from datetime import datetime


    total_filters = {"docstatus": ("in", [0, 1])}

    pending_filter = {
        "docstatus": ("in", [0, 1]),
        "custom_final_status": "Pending"
    }

    approved_filter = {
        "docstatus": ("in", [0, 1]),
        "custom_final_status": "Approved"
    }

    rejected_filter = {
        "docstatus": ("in", [0, 1]),
        "custom_final_status": "Rejected"
    }

    from_date = None
    to_date = None

    if month:
        month_number = datetime.strptime(month, "%B").month

        # Use current year (or you can customize)
        year = datetime.now().year

        last_day = calendar.monthrange(year, month_number)[1]

        from_date = f"{year}-{month_number:02d}-01"
        to_date = f"{year}-{month_number:02d}-{last_day}"

    for f in [total_filters, pending_filter, approved_filter, rejected_filter]:

        if company:
            f["company"] = company

        if from_date and to_date:
            f["posting_date"] = ["between", [from_date, to_date]]


    total_claims = frappe.db.count("Employee Advance", filters=total_filters)
    pending_claims = frappe.db.count("Employee Advance", filters=pending_filter)
    approved_claims = frappe.db.count("Employee Advance", filters=approved_filter)
    rejected_claims = frappe.db.count("Employee Advance", filters=rejected_filter)


    


    return {
        "total": total_claims,
        "pending": pending_claims,
        "approved": approved_claims,
        "rejected": rejected_claims,
        "from_date": from_date,
        "to_date": to_date,
    }




@frappe.whitelist()
def list_offcycle_details(company=None, payroll_period=None, month=None):

    import calendar
    from datetime import datetime

    total_filters = {"docstatus": ("in", [0, 1])}

    pending_filter = {
        "docstatus": 0,
    }

    approved_filter = {
        "docstatus": 1,
    }



    from_date = None
    to_date = None

    if month:
        month_number = datetime.strptime(month, "%B").month
        year = datetime.now().year

        last_day = calendar.monthrange(year, month_number)[1]

        from_date = f"{year}-{month_number:02d}-01"
        to_date = f"{year}-{month_number:02d}-{last_day}"

    for f in [total_filters, pending_filter, approved_filter]:

        if company:
            f["company"] = company

        if from_date and to_date:
            f["payroll_date"] = ["between", [from_date, to_date]]

    records = frappe.get_all(
        "Additional Salary",
        filters=total_filters,
        fields=["name", "salary_component"]
    )

    total = 0
    pending = 0
    approved = 0

    for r in records:

        sal_comp = frappe.get_value(
            "Salary Component",
            r.salary_component,
            "custom_is_offcycle_component"
        )

        if not sal_comp:
            continue

        total += 1

        docstatus = frappe.db.get_value("Additional Salary", r.name, "docstatus")

        if docstatus == 0:
            pending += 1
        elif docstatus == 1:
            approved += 1


    return {
        "status": "success",
        "total": total,
        "pending": pending,
        "approved": approved,
        "from_date": from_date,
        "to_date": to_date
    }

