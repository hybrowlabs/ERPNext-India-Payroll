

import frappe
from frappe.utils import flt, add_months, getdate,flt
import datetime



def before_submit(self, method):
    if  not self.custom_note_remarks:
        frappe.throw("Please add Note/Remarks before Submit")

    self.custom_total_balance_amount = (self.advance_amount or 0) - (self.custom_total_paid_amount or 0)


@frappe.whitelist()
def get_advance_details(employee, company, posting_date, id):
    """
    Fetch advance details and generate installments from Additional Salary
    """
    if not (employee and company and posting_date and id):
        return None

    # Get Employee Advance
    get_loan = frappe.get_doc('Employee Advance', id)
    advance_amount = get_loan.advance_amount
    advance_type = get_loan.custom_advance_type
    paid_amount = get_loan.custom_total_paid_amount
    balance_amount = get_loan.custom_total_balance_amount
    months_paid = get_loan.custom_total_paid_amount or 0

    # Get all Additional Salary records linked to this advance
    additional_salary = frappe.get_all(
        'Additional Salary',
        filters={
            'employee': employee,
            'company': company,
            'ref_doctype': 'Employee Advance',
            'ref_docname': id,
            'docstatus': 1
        },
        fields=['name', 'from_date', 'to_date', 'amount'],
        order_by='from_date asc'
    )

    installments = []
    idx = 0
    date = []

    for rec in additional_salary:
        from_date = getdate(rec.from_date)
        to_date = getdate(rec.to_date)

        total_months = ((to_date.year - from_date.year) * 12 +
                        (to_date.month - from_date.month)) + 1

        current_date = from_date
        for i in range(total_months):
            idx += 1

            start_dt = current_date.replace(day=1)
            end_dt = add_months(start_dt, 1) - datetime.timedelta(days=1)

            salary_slips = frappe.get_all(
                "Salary Slip",
                filters={
                    "employee": employee,
                    "company": company,
                    "docstatus": 1,
                    "start_date": start_dt,
                    "end_date": end_dt
                },
                fields=["name", "start_date", "end_date"],
                limit=1
            )

            deducted = 1 if salary_slips else 0

            installments.append({
                "sl": idx,
                "date": current_date.strftime("%d-%m-%Y"),
                "amount": flt(rec.amount),
                "additional_salary_id": rec.name,
                "deducted": deducted,

            })

            current_date = add_months(current_date, 1)


    balance_months = max(0, idx - months_paid)




    return {
        "advance_type": advance_type,
        "total_loan_amount": advance_amount,
        "total_paid": paid_amount,
        "balance_amount": balance_amount,
        "months_paid": months_paid,
        "balance_months": balance_months,
        "installments": installments
    }






# import frappe
# from frappe.utils import getdate, add_months, flt,add_days,get_last_day

# @frappe.whitelist()
# def hold_installments(additional_salary_id, hold_option=None, hold_months=1, holding_date=None, previous_date=None, advance_amount=None, number_of_months=None):
#     if not additional_salary_id:
#         return "failed"


#     get_additional_salary = frappe.get_doc("Additional Salary", additional_salary_id)
#     last_date = getdate(get_additional_salary.to_date)

#     if previous_date:
#         get_additional_salary.to_date = getdate(previous_date)

#         get_additional_salary.save(ignore_permissions=True)
#     else:
#         get_additional_salary.from_date=add_days(holding_date,1)
#         get_additional_salary.to_date = add_months(holding_date, 1)
#         get_additional_salary.save(ignore_permissions=True)




#     employee = get_additional_salary.employee
#     company = get_additional_salary.company
#     salary_component = get_additional_salary.salary_component
#     base_amount = flt(get_additional_salary.amount)
#     ref_doctype = get_additional_salary.ref_doctype
#     ref_docname = get_additional_salary.ref_docname





#     if hold_option == "Recover Pending in Next Month":
#         if not holding_date or not number_of_months:
#             frappe.throw("Holding date and number of months are required.")

#         holding_date = getdate(holding_date)
#         number_of_months = int(number_of_months)

#         recovery_date = add_months(holding_date, number_of_months)

#         if recovery_date > last_date:
#             recovery_date = last_date

    #     recovery_salary = frappe.new_doc("Additional Salary")
    #     recovery_salary.employee = employee
    #     recovery_salary.company = company
    #     recovery_salary.salary_component = salary_component
    #     recovery_salary.amount = base_amount * (number_of_months + 1)
    #     recovery_salary.is_recurring = 1
    #     recovery_salary.from_date = recovery_date
    #     recovery_salary.to_date = recovery_date
    #     recovery_salary.ref_doctype = ref_doctype
    #     recovery_salary.ref_docname = ref_docname

    #     recovery_salary.insert(ignore_permissions=True)
    #     recovery_salary.submit()

    #     # 2️⃣ Create Additional Salary for remaining period after recovery
    #     remaining_start_date = add_months(recovery_date, 1)
    #     if remaining_start_date <= last_date:
    #         recovery_salary_2 = frappe.new_doc("Additional Salary")
    #         recovery_salary_2.employee = employee
    #         recovery_salary_2.company = company
    #         recovery_salary_2.salary_component = salary_component
    #         recovery_salary_2.amount = base_amount
    #         recovery_salary_2.is_recurring = 1
    #         recovery_salary_2.from_date = remaining_start_date
    #         recovery_salary_2.to_date = last_date
    #         recovery_salary_2.ref_doctype = ref_doctype
    #         recovery_salary_2.ref_docname = ref_docname

    #         recovery_salary_2.insert(ignore_permissions=True)
    #         recovery_salary_2.submit()

    # elif hold_option == "Distribute Across Future Months":
    #     if not holding_date or not number_of_months:
    #         frappe.throw("Holding date and number of months are required.")

    #     holding_date = getdate(holding_date)
    #     number_of_months = int(number_of_months)

    #     held_amount = base_amount * number_of_months
    #     from_date = add_months(holding_date, number_of_months)

    #     remaining_months = 0
    #     temp_date = from_date
    #     while temp_date <= last_date:
    #         remaining_months += 1
    #         temp_date = add_months(temp_date, 1)


    #     if remaining_months <= 0:
    #         frappe.throw("No future months available to distribute the hold amount.")

    #     total_amount = (base_amount /remaining_months) + held_amount
    #     distributed_salary = frappe.new_doc("Additional Salary")
    #     distributed_salary.employee = employee
    #     distributed_salary.company = company
    #     distributed_salary.salary_component = salary_component
    #     distributed_salary.amount = total_amount
    #     distributed_salary.is_recurring = 1
    #     distributed_salary.from_date = from_date
    #     distributed_salary.to_date = last_date
    #     distributed_salary.ref_doctype = ref_doctype
    #     distributed_salary.ref_docname = ref_docname

    #     distributed_salary.insert(ignore_permissions=True)
    #     distributed_salary.submit()

    # elif hold_option == "Extend Repayment Period":
    #     if not number_of_months:
    #         frappe.throw("Number of months is required.")

    #     number_of_months = int(number_of_months)

    #     new_start_date = add_months(last_date, 1)

    #     temp_end_date = add_months(new_start_date, number_of_months - 1)



    #     new_end_date = get_last_day(temp_end_date)

    #     extended_salary = frappe.new_doc("Additional Salary")
    #     extended_salary.employee = employee
    #     extended_salary.company = company
    #     extended_salary.salary_component = salary_component
    #     extended_salary.amount = base_amount
    #     extended_salary.is_recurring = 1
    #     extended_salary.from_date = last_date
    #     extended_salary.to_date = new_end_date
    #     extended_salary.ref_doctype = ref_doctype
    #     extended_salary.ref_docname = ref_docname

    #     extended_salary.insert(ignore_permissions=True)
    #     extended_salary.submit()


    # elif hold_option == "Custom Repayment":

    #     custom_salary = frappe.new_doc("Additional Salary")
    #     custom_salary.employee = employee
    #     custom_salary.company = company
    #     custom_salary.salary_component = salary_component
    #     custom_salary.amount = advance_amount
    #     custom_salary.is_recurring = 1
    #     custom_salary.from_date = holding_date
    #     custom_salary.to_date = add_months(holding_date, number_of_months - 1)
    #     custom_salary.ref_doctype = ref_doctype
    #     custom_salary.ref_docname = ref_docname

    #     custom_salary.insert(ignore_permissions=True)
    #     custom_salary.submit()




    # return "success"

from frappe.utils import getdate, add_days, add_months, flt

@frappe.whitelist()
def hold_installments(additional_salary_id, hold_option=None, hold_months=1, holding_date=None, previous_date=None, advance_amount=None, number_of_months=None, total_installments=None):
    if not additional_salary_id:
        return "failed"

    get_additional_salary = frappe.get_doc("Additional Salary", additional_salary_id)
    last_date = getdate(get_additional_salary.to_date)

    holding_date = getdate(holding_date)

    employee = get_additional_salary.employee
    company = get_additional_salary.company
    salary_component = get_additional_salary.salary_component
    base_amount = flt(get_additional_salary.amount)
    ref_doctype = get_additional_salary.ref_doctype
    ref_docname = get_additional_salary.ref_docname



    if hold_option == "Recover Pending in Next Month" and not previous_date:
        if not holding_date or not number_of_months:
            frappe.throw("Holding date and number_of_months are required.")

        holding_date = getdate(holding_date)
        number_of_months = int(number_of_months)

        get_additional_salary.from_date = add_months(holding_date, number_of_months)
        get_additional_salary.to_date = add_months(holding_date, number_of_months)
        get_additional_salary.amount = (base_amount * number_of_months )+base_amount
        get_additional_salary.save(ignore_permissions=True)

        recovery_date = add_months(holding_date, number_of_months)

        if recovery_date > last_date:
            recovery_date = last_date

        remaining_start_date = add_months(recovery_date, 1)
        if remaining_start_date <= last_date:
            remaining_salary = frappe.new_doc("Additional Salary")
            remaining_salary.employee = employee
            remaining_salary.company = company
            remaining_salary.salary_component = salary_component
            remaining_salary.amount = base_amount
            remaining_salary.is_recurring = 1
            remaining_salary.from_date = remaining_start_date
            remaining_salary.to_date = last_date
            remaining_salary.ref_doctype = ref_doctype
            remaining_salary.ref_docname = ref_docname
            remaining_salary.insert(ignore_permissions=True)
            remaining_salary.submit()

    elif hold_option=="Recover Pending in Next Month" and previous_date:
        if not holding_date or not number_of_months:
            frappe.throw("Holding date and number of months are required.")



        get_additional_salary.to_date = getdate(previous_date)
        get_additional_salary.save(ignore_permissions=True)

        holding_date = getdate(holding_date)
        number_of_months = int(number_of_months)

        recovery_date = add_months(holding_date, number_of_months)

        if recovery_date > last_date:
            recovery_date = last_date

        recovery_salary = frappe.new_doc("Additional Salary")
        recovery_salary.employee = employee
        recovery_salary.company = company
        recovery_salary.salary_component = salary_component
        recovery_salary.amount = base_amount * (number_of_months + 1)
        recovery_salary.is_recurring = 1
        recovery_salary.from_date = recovery_date
        recovery_salary.to_date = recovery_date
        recovery_salary.ref_doctype = ref_doctype
        recovery_salary.ref_docname = ref_docname

        recovery_salary.insert(ignore_permissions=True)
        recovery_salary.submit()

        remaining_start_date = add_months(recovery_date, 1)
        if remaining_start_date <= last_date:
            recovery_salary_2 = frappe.new_doc("Additional Salary")
            recovery_salary_2.employee = employee
            recovery_salary_2.company = company
            recovery_salary_2.salary_component = salary_component
            recovery_salary_2.amount = base_amount
            recovery_salary_2.is_recurring = 1
            recovery_salary_2.from_date = remaining_start_date
            recovery_salary_2.to_date = last_date
            recovery_salary_2.ref_doctype = ref_doctype
            recovery_salary_2.ref_docname = ref_docname

            recovery_salary_2.insert(ignore_permissions=True)
            recovery_salary_2.submit()


    return "success"
