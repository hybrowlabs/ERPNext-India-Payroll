import frappe

import frappe
from datetime import datetime
import calendar




@frappe.whitelist()
def count_benefit_details(company=None, payroll_period=None, month=None):


    total_filters = {"docstatus": ("in", [0, 1])}

    pending_filter = {
        "docstatus": ("in", [0, 1]),
        "custom_status": "Pending"
    }

    approved_filter = {
        "docstatus": ("in", [0, 1]),
        "custom_status": "Approved"
    }

    rejected_filter = {
        "docstatus": ("in", [0, 1]),
        "custom_status": "Rejected"
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
            f["claim_date"] = ["between", [from_date, to_date]]


    total_claims = frappe.db.count("Employee Benefit Claim", filters=total_filters)
    pending_claims = frappe.db.count("Employee Benefit Claim", filters=pending_filter)
    approved_claims = frappe.db.count("Employee Benefit Claim", filters=approved_filter)
    rejected_claims = frappe.db.count("Employee Benefit Claim", filters=rejected_filter)


    


    return {
        "total": total_claims,
        "pending": pending_claims,
        "approved": approved_claims,
        "rejected": rejected_claims,
        "from_date": from_date,
        "to_date": to_date,
    }






    
@frappe.whitelist()
def benefit_data_table(company=None, payroll_period=None, month=None, status=None, limit=20, offset=0):



    from_date = None
    to_date = None

    if month:
        month_number = datetime.strptime(month, "%B").month
        year = datetime.now().year

        last_day = calendar.monthrange(year, month_number)[1]

        from_date = f"{year}-{month_number:02d}-01"
        to_date = f"{year}-{month_number:02d}-{last_day}"

    # -------------------------
    # FILTERS
    # -------------------------
    filters = {}

    if company:
        filters["company"] = company

    if from_date and to_date:
        filters["claim_date"] = ["between", [from_date, to_date]]

    if status == "Pending":
        filters["custom_status"] = "Pending"

    elif status == "Approved":
        filters["custom_status"] = "Approved"

    elif status == "Rejected":
        filters["custom_status"] = "Rejected"

    else:
        filters["docstatus"] = ("in", [0, 1])

    # -------------------------
    # LIMIT HANDLING
    # -------------------------
    limit = None if str(limit).lower() == "all" else int(limit)
    offset = int(offset or 0)

    # -------------------------
    # DATA FETCH
    # -------------------------
    data = frappe.get_all(
        "Employee Benefit Claim",
        filters=filters,
        fields=[
            "name",
            "employee",
            "employee_name",
            "claim_date",
            "claimed_amount",
            "custom_status",
            "earning_component",
            "custom_note_by_employee"
        ],
        order_by="claim_date desc",
        limit_page_length=limit,
        limit_start=offset
    )

    return {
        "status": "success",
        "data": data
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



    return {
        "status": "success",
        "total": total_claims,
        "pending": pending_claims,
        "submitted": submitted_claims,

    }


@frappe.whitelist()
def count_advance_details(company=None, payroll_period=None, month=None):

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



    
@frappe.whitelist()
def list_advance_details(company=None, payroll_period=None, month=None, status=None, limit=20, offset=0):

    import calendar
    from datetime import datetime

    from_date = None
    to_date = None

    if month:
        month_number = datetime.strptime(month, "%B").month
        year = datetime.now().year

        last_day = calendar.monthrange(year, month_number)[1]

        from_date = f"{year}-{month_number:02d}-01"
        to_date = f"{year}-{month_number:02d}-{last_day}"

    # -------------------------
    # FILTERS
    # -------------------------
    filters = {}

    if company:
        filters["company"] = company

    if from_date and to_date:
        filters["posting_date"] = ["between", [from_date, to_date]]

    if status == "Pending":
        filters["custom_final_status"] = "Pending"

    elif status == "Approved":
        filters["custom_final_status"] = "Approved"

    elif status == "Rejected":
        filters["custom_final_status"] = "Rejected"

    else:
        filters["docstatus"] = ("in", [0, 1])

    # -------------------------
    # LIMIT HANDLING
    # -------------------------
    limit = None if str(limit).lower() == "all" else int(limit)
    offset = int(offset or 0)

    # -------------------------
    # DATA FETCH
    # -------------------------
    data = frappe.get_all(
        "Employee Advance",
        filters=filters,
        fields=[
            "name",
            "employee_name",
            "posting_date",
            "advance_amount",
            "custom_final_status"
        ],
        order_by="posting_date desc",
        limit_page_length=limit,
        limit_start=offset
    )

    return {
        "status": "success",
        "data": data
    }



@frappe.whitelist()
def get_dashboard_filters(company=None):

    import calendar
    from datetime import datetime

    companies = frappe.get_all(
        "Company",
        fields=["name"],
        order_by="name asc"
    )

    payroll_filters = {}

    if company:
        payroll_filters["company"] = company   

    payroll_periods = frappe.get_all(
        "Payroll Period",
        filters=payroll_filters,
        fields=["name", "start_date", "end_date"],
        order_by="start_date desc"
    )

    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    current_month = datetime.now().strftime("%B")

    return {
        "companies": companies,
        "payroll_periods": payroll_periods,
        "months": months,
        "current_month": current_month
    }



@frappe.whitelist()
def list_resettlement_details(company=None, payroll_period=None, month=None):

    total_filters = {"docstatus": ("in", [0, 1])}

    pending_filter = {"docstatus": 0}

    approved_filter = {"docstatus": 1}

    from_date = None
    to_date = None

    if month:
        try:
            month_number = datetime.strptime(month, "%B").month
            year = datetime.now().year

            last_day = calendar.monthrange(year, month_number)[1]

            from_date = f"{year}-{month_number:02d}-01"
            to_date = f"{year}-{month_number:02d}-{last_day}"
        except Exception:
            frappe.log_error(f"Invalid month format: {month}")

    for f in [total_filters, pending_filter, approved_filter]:

        if company:
            f["company"] = company

        if from_date and to_date:
            f["transaction_date"] = ["between", [from_date, to_date]]

    total_claims = frappe.db.count("Resettlement", filters=total_filters)
    pending_claims = frappe.db.count("Resettlement", filters=pending_filter)
    approved_claims = frappe.db.count("Resettlement", filters=approved_filter)

    return {
        "status": "success",
        "total": total_claims,
        "pending": pending_claims,
        "approved": approved_claims,
        "from_date": from_date,
        "to_date": to_date
    }




@frappe.whitelist()
def list_fandf_details(company=None, payroll_period=None, month=None):

    total_filters = {"docstatus": ("in", [0, 1])}

    pending_filter = {"docstatus": 0}

    approved_filter = {"docstatus": 1}

    from_date = None
    to_date = None

    if month:
        try:
            month_number = datetime.strptime(month, "%B").month
            year = datetime.now().year

            last_day = calendar.monthrange(year, month_number)[1]

            from_date = f"{year}-{month_number:02d}-01"
            to_date = f"{year}-{month_number:02d}-{last_day}"
        except Exception:
            frappe.log_error(f"Invalid month format: {month}")

    for f in [total_filters, pending_filter, approved_filter]:

        if company:
            f["company"] = company

        if from_date and to_date:
            f["transaction_date"] = ["between", [from_date, to_date]]

    total_claims = frappe.db.count("Full and Final Statement", filters=total_filters)
    pending_claims = frappe.db.count("Full and Final Statement", filters=pending_filter)
    approved_claims = frappe.db.count("Full and Final Statement", filters=approved_filter)

    return {
        "status": "success",
        "total": total_claims,
        "pending": pending_claims,
        "approved": approved_claims,
        "from_date": from_date,
        "to_date": to_date
    }



@frappe.whitelist()
def list_salary_details(company=None, payroll_period=None, month=None):


    total_filter = {"docstatus": ("in", [0, 1])}
    pending_filter = {"docstatus": 0}
    approved_filter = {"docstatus": 1}

    
    for f in [total_filter, pending_filter, approved_filter]:

        if company:
            f["company"] = company

        if payroll_period:
            f["custom_payroll_period"] = payroll_period

        if month:
            f["custom_month"] = month

    total = frappe.db.count("Salary Slip", filters=total_filter)
    pending = frappe.db.count("Salary Slip", filters=pending_filter)
    approved = frappe.db.count("Salary Slip", filters=approved_filter)



    claim_total_filters = {"docstatus": ("in", [0, 1])}

    claim_pending_filter = {
        "docstatus": ("in", [0, 1]),
        "custom_status": "Pending"
    }

    claim_approved_filter = {
        "docstatus": ("in", [0, 1]),
        "custom_status": "Approved"
    }

    
    from_date = None
    to_date = None

    if month:
        month_number = datetime.strptime(month, "%B").month

        year = datetime.now().year

        last_day = calendar.monthrange(year, month_number)[1]

        from_date = f"{year}-{month_number:02d}-01"
        to_date = f"{year}-{month_number:02d}-{last_day}"

    for f in [claim_total_filters, claim_pending_filter, claim_approved_filter]:

        if company:
            f["company"] = company

        if from_date and to_date:
            f["claim_date"] = ["between", [from_date, to_date]]


    total_claims = frappe.db.count("Employee Benefit Claim", filters=claim_total_filters)
    pending_claims = frappe.db.count("Employee Benefit Claim", filters=claim_pending_filter)
    approved_claims = frappe.db.count("Employee Benefit Claim", filters=claim_approved_filter)


    



    return {
        "status": "success",
        "total": total,
        "pending": pending,
        "approved": approved,

        "claim_total":total_claims,
        "claim_pending":pending_claims,
        "claim_approved":approved_claims

    }