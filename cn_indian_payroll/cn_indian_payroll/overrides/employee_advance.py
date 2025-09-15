

import frappe
from frappe.utils import flt, add_months, getdate,flt
import datetime



def before_submit(self, method):
    if  not self.custom_note_remarks or not self.custom_deduction_component:
        frappe.throw("Please add Note/Remarks and Deduction component  in Note Section before Submit")

    self.custom_total_balance_amount = (self.advance_amount or 0) - (self.custom_total_paid_amount or 0)


# @frappe.whitelist()
# def get_advance_details(employee, company, posting_date, id):
#     """
#     Fetch advance details and generate installments from Additional Salary
#     """
#     if not (employee and company and posting_date and id):
#         return None

#     # Get Employee Advance
#     get_loan = frappe.get_doc('Employee Advance', id)
#     advance_amount = get_loan.advance_amount
#     advance_type = get_loan.custom_advance_type
#     paid_amount = get_loan.custom_total_paid_amount
#     balance_amount = get_loan.custom_total_balance_amount
#     months_paid = get_loan.custom_total_paid_amount or 0

#     # Get all Additional Salary records linked to this advance
#     additional_salary = frappe.get_all(
#         'Additional Salary',
#         filters={
#             'employee': employee,
#             'company': company,
#             'ref_doctype': 'Employee Advance',
#             'ref_docname': id,
#             'docstatus': 1
#         },
#         fields=['name', 'from_date', 'to_date', 'amount'],
#         order_by='from_date asc'
#     )

#     installments = []
#     idx = 0
#     date = []

#     for rec in additional_salary:
#         from_date = getdate(rec.from_date)
#         to_date = getdate(rec.to_date)

#         total_months = ((to_date.year - from_date.year) * 12 +
#                         (to_date.month - from_date.month)) + 1

#         current_date = from_date
#         for i in range(total_months):
#             idx += 1

#             start_dt = current_date.replace(day=1)
#             end_dt = add_months(start_dt, 1) - datetime.timedelta(days=1)

#             salary_slips = frappe.get_all(
#                 "Salary Slip",
#                 filters={
#                     "employee": employee,
#                     "company": company,
#                     "docstatus": 1,
#                     "start_date": start_dt,
#                     "end_date": end_dt
#                 },
#                 fields=["name", "start_date", "end_date"],
#                 limit=1
#             )

#             deducted = 1 if salary_slips else 0

#             installments.append({
#                 "sl": idx,
#                 "date": current_date.strftime("%d-%m-%Y"),
#                 "amount": flt(rec.amount),
#                 "additional_salary_id": rec.name,
#                 "deducted": deducted,

#             })

#             current_date = add_months(current_date, 1)


#     balance_months = max(0, idx - months_paid)




#     return {
#         "advance_type": advance_type,
#         "total_loan_amount": advance_amount,
#         "total_paid": paid_amount,
#         "balance_amount": balance_amount,
#         "months_paid": months_paid,
#         "balance_months": balance_months,
#         "installments": installments
#     }






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

#--------------------------------------------------------------------------------------------------


#     # return "success"

# from frappe.utils import getdate, add_days, add_months, flt,get_first_day
# from datetime import datetime
# from frappe.utils import flt, cint
# import re


# @frappe.whitelist()
# def hold_installments(additional_salary_id, hold_option=None, hold_months=1, holding_date=None, previous_date=None, advance_amount=None, number_of_months=None, total_installments=None,next_date=None,next_amount=None,next_additional_salary_id=None):
#     if not additional_salary_id:
#         return "failed"
#     # frappe.msgprint(str(next_date))
#     # frappe.msgprint(str(next_amount))
#     # frappe.msgprint(str(next_additional_salary_id))
#     # frappe.msgprint(str(advance_amount))

#     get_additional_salary = frappe.get_doc("Additional Salary", additional_salary_id)
#     last_date = getdate(get_additional_salary.to_date)

#     holding_date = getdate(holding_date)

#     employee = get_additional_salary.employee
#     company = get_additional_salary.company
#     salary_component = get_additional_salary.salary_component
#     base_amount = flt(get_additional_salary.amount)
#     ref_doctype = get_additional_salary.ref_doctype
#     ref_docname = get_additional_salary.ref_docname



#     # if hold_option=="Recover Pending in Next Month" and previous_date and next_date:
#     #     if not holding_date or not number_of_months:
#     #         frappe.throw("Holding date and number of months are required.")


#     #     day, month, year = map(int, previous_date.split("-"))
#     #     previous_date_obj = getdate(f"{year}-{month:02d}-{day:02d}")



#     # if hold_option == "Recover Pending in Next Month" and not previous_date:
#     #     if not holding_date or not number_of_months:
#     #         frappe.throw("Holding date and number_of_months are required.")

#     #     holding_date = getdate(holding_date)
#     #     number_of_months = int(number_of_months)

#     #     get_additional_salary.from_date = add_months(holding_date, number_of_months)
#     #     get_additional_salary.to_date = add_months(holding_date, number_of_months)
#     #     get_additional_salary.amount = (base_amount * number_of_months )+base_amount
#     #     get_additional_salary.save(ignore_permissions=True)

#     #     recovery_date = add_months(holding_date, number_of_months)

#     #     if recovery_date > last_date:
#     #         recovery_date = last_date

#     #     remaining_start_date = add_months(recovery_date, 1)
#     #     if remaining_start_date <= last_date:
#     #         remaining_salary = frappe.new_doc("Additional Salary")
#     #         remaining_salary.employee = employee
#     #         remaining_salary.company = company
#     #         remaining_salary.salary_component = salary_component
#     #         remaining_salary.amount = base_amount
#     #         remaining_salary.is_recurring = 1
#     #         remaining_salary.from_date = remaining_start_date
#     #         remaining_salary.to_date = last_date
#     #         remaining_salary.ref_doctype = ref_doctype
#     #         remaining_salary.ref_docname = ref_docname
#     #         remaining_salary.insert(ignore_permissions=True)
#     #         remaining_salary.submit()







#     if hold_option=="Recover Pending in Next Month" and previous_date and next_amount:
#         if not holding_date or not number_of_months:
#             frappe.throw("Holding date and number of months are required.")

#         # Debug raw value
#         frappe.msgprint(f"Raw Next Amount: {next_amount}")

#         # Clean ₹ and commas if present
#         if isinstance(next_amount, str):
#             next_amount = re.sub(r"[^\d.]", "", next_amount)  # keep only digits and .

#         # Now convert properly
#         next_amount = flt(next_amount)        # clean "2000" → 2000.0
#         base_amount = flt(base_amount)        # ensure float
#         number_of_months = cint(number_of_months)  # ensure int

#         total_amount = (base_amount * number_of_months) + next_amount

#         frappe.msgprint(f"Next Amount: {next_amount}")
#         frappe.msgprint(f"Base Amount: {base_amount}")
#         frappe.msgprint(f"Months: {number_of_months}")
#         frappe.msgprint(f"Total Amount: {total_amount}")

#         # total_amount = (base_amount * number_of_months) + next_amount
#         # frappe.msgprint(str(total_amount))


#         # day, month, year = map(int, previous_date.split("-"))
#         # previous_date_obj = getdate(f"{year}-{month:02d}-{day:02d}")

#         # get_additional_salary.to_date = getdate(previous_date_obj)
#         # get_additional_salary.save(ignore_permissions=True)

#         # holding_date = getdate(holding_date)
#         # number_of_months = int(number_of_months)

#         # recovery_date = add_months(holding_date, number_of_months)

#         # if recovery_date > last_date:
#         #     recovery_date = last_date

#         # recovery_salary = frappe.new_doc("Additional Salary")
#         # recovery_salary.employee = employee
#         # recovery_salary.company = company
#         # recovery_salary.salary_component = salary_component
#         # recovery_salary.amount = base_amount * (number_of_months + 1)
#         # recovery_salary.is_recurring = 1
#         # recovery_salary.from_date = get_first_day(recovery_date)
#         # recovery_salary.to_date = get_first_day(recovery_date)
#         # recovery_salary.ref_doctype = ref_doctype
#         # recovery_salary.ref_docname = ref_docname

#         # recovery_salary.insert(ignore_permissions=True)
#         # recovery_salary.submit()

#         # remaining_start_date = add_months(recovery_date, 1)
#         # if remaining_start_date <= last_date:

#         #     frappe.msgprint(str(remaining_start_date)+"--"+str(last_date))
#         #     recovery_salary_2 = frappe.new_doc("Additional Salary")



import frappe
import datetime
from frappe.utils import flt, getdate, add_months
import calendar
from frappe.utils import fmt_money
from frappe.utils import add_months, get_first_day

@frappe.whitelist()
def get_advance_dashboard(employee):
    if not employee:
        return []

    advance_details = frappe.get_all(
        "Employee Advance",
        filters={"employee": employee, "docstatus": ["in", [0, 1]]},
        fields=["*"]
    )

    results = []

    for advance in advance_details:
        repayment_schedule = []
        balance_amount = float(advance.advance_amount or 0)
        start_date = advance.custom_repayment_start_date
        idx = 0

        get_additional_salary = frappe.db.get_all(
            "Additional Salary",
            filters={
                "employee": employee,
                "company": advance.company,
                "ref_doctype": "Employee Advance",
                "ref_docname": advance.name,
                "docstatus": 1
            },
            fields=['name', 'from_date', 'to_date', 'amount'],
            order_by='from_date asc'
        )

        if get_additional_salary:
            for rec in get_additional_salary:
                from_date = getdate(rec.from_date)
                to_date = getdate(rec.to_date)

                total_months = ((to_date.year - from_date.year) * 12 +
                                (to_date.month - from_date.month)) + 1

                current_date = from_date
                for i in range(total_months):
                    idx += 1
                    start_dt = current_date.replace(day=1)
                    end_dt = add_months(start_dt, 1) - datetime.timedelta(days=1)

                    salary_slips = frappe.db.get_all(
                        "Salary Slip",
                        filters={
                            "employee": employee,
                            "company": advance.company,
                            "docstatus": 1,
                            "start_date": start_dt,
                            "end_date": end_dt
                        },
                        fields=["name"],
                        limit=1
                    )

                    deducted = 1 if salary_slips else 0

                    if balance_amount > 0:
                        pay_amount = min(balance_amount, flt(rec.amount))
                        balance_amount -= pay_amount

                        repayment_schedule.append({
                            "idx": idx,
                            "payment_date": current_date,
                            "payment_amount": pay_amount,
                            "balance_amount": balance_amount,
                            "deducted": deducted
                        })

                    current_date = add_months(current_date, 1)

        else:
            if advance.custom_repayment_type == "One Time":
                repayment_schedule.append({
                    "idx": 1,
                    "payment_date": start_date,
                    "payment_amount": float(advance.advance_amount or 0),
                    "balance_amount": float(advance.advance_amount or 0),
                    "deducted": 0,
                    "additional_salary_id": None
                })

            elif advance.custom_repayment_type == "Recurring":
                total_advance_amount = float(advance.advance_amount or 0)

                if advance.custom_repayment_methods == "Repay Fixed Amount per Period":
                    fixed_amount = float(advance.custom_monthly_repayment_amount or 0)

                    if fixed_amount > 0:
                        total_months = int(total_advance_amount // fixed_amount)
                        if total_advance_amount % fixed_amount != 0:
                            total_months += 1

                        for i in range(total_months):
                            idx += 1
                            payment_date = add_months(start_date, i)

                            pay_amount = min(balance_amount, fixed_amount)
                            balance_amount -= pay_amount

                            repayment_schedule.append({
                                "idx": idx,
                                "payment_date": payment_date,
                                "payment_amount": pay_amount,
                                "balance_amount": balance_amount,
                                "deducted": 0,
                                "additional_salary_id": None
                            })

                elif advance.custom_repayment_methods == "Repay Over Number of Periods":
                    total_months = int(advance.custom_repayment_period_in_months or 0)
                    if total_months > 0:
                        emi = total_advance_amount / total_months
                        for i in range(total_months):
                            idx += 1
                            payment_date = add_months(start_date, i)
                            balance_amount -= emi
                            repayment_schedule.append({
                                "idx": idx,
                                "payment_date": payment_date,
                                "payment_amount": round(emi, 2),
                                "balance_amount": round(balance_amount, 2),
                                "deducted": 0,
                                "additional_salary_id": None
                            })

        end_date = repayment_schedule[-1]["payment_date"] if repayment_schedule else None

        total_paid_amount = sum(r["payment_amount"] for r in repayment_schedule if r.get("deducted") == 1)
        final_balance = flt(advance.advance_amount) - total_paid_amount

        results.append({
            "advance_type": advance.custom_advance_type,
            "status": advance.status,
            "total_advance_amount": advance.advance_amount,
            "start_date": start_date,
            "end_date": end_date,
            "repayments": repayment_schedule,
            "total_paid_amount": total_paid_amount,
            "balance_amount": final_balance
        })

    return results




@frappe.whitelist()
def get_advance_dashboard_erp(employee,id,company):
    if not employee:
        return []

    advance_details = frappe.get_all(
        "Employee Advance",
        filters={"employee": employee,"name":id,"company":company, "docstatus": ["in", [0, 1]]},
        fields=["*"]
    )

    results = []

    for advance in advance_details:
        repayment_schedule = []
        balance_amount = float(advance.advance_amount or 0)
        start_date = advance.custom_repayment_start_date
        idx = 0

        get_additional_salary = frappe.db.get_all(
            "Additional Salary",
            filters={
                "employee": employee,
                "company": advance.company,
                "ref_doctype": "Employee Advance",
                "ref_docname": advance.name,
                "docstatus": 1
            },
            fields=['name', 'from_date', 'to_date', 'amount'],
            order_by='from_date asc'
        )


        if get_additional_salary:
            for rec in get_additional_salary:
                from_date = getdate(rec.from_date)
                to_date = getdate(rec.to_date)

                # Fix if to_date is before from_date
                if to_date < from_date:
                    to_date = from_date

                total_months = ((to_date.year - from_date.year) * 12 +
                                (to_date.month - from_date.month)) + 1

                current_date = from_date
                for i in range(total_months):
                    idx += 1
                    pay_amount = min(balance_amount, flt(rec.amount))
                    balance_amount -= pay_amount

                    repayment_schedule.append({
                        "idx": idx,
                        "payment_date": current_date,
                        "payment_amount": pay_amount,
                        "balance_amount": balance_amount,
                        "deducted": 0,
                        "additional_salary_id": rec.name
                    })

                    current_date = add_months(current_date, 1)

        else:
            if advance.custom_repayment_type == "One Time":
                repayment_schedule.append({
                    "idx": 1,
                    "payment_date": start_date,
                    "payment_amount": float(advance.advance_amount or 0),
                    "balance_amount": float(advance.advance_amount or 0),
                    "deducted": 0,
                    "additional_salary_id": None
                })

            elif advance.custom_repayment_type == "Recurring":
                total_advance_amount = float(advance.advance_amount or 0)

                if advance.custom_repayment_methods == "Repay Fixed Amount per Period":
                    fixed_amount = float(advance.custom_monthly_repayment_amount or 0)

                    if fixed_amount > 0:
                        total_months = int(total_advance_amount // fixed_amount)
                        if total_advance_amount % fixed_amount != 0:
                            total_months += 1

                        for i in range(total_months):
                            idx += 1
                            payment_date = add_months(start_date, i)

                            pay_amount = min(balance_amount, fixed_amount)
                            balance_amount -= pay_amount

                            repayment_schedule.append({
                                "idx": idx,
                                "payment_date": payment_date,
                                "payment_amount": pay_amount,
                                "balance_amount": balance_amount,
                                "deducted": 0,
                                "additional_salary_id": None
                            })

                elif advance.custom_repayment_methods == "Repay Over Number of Periods":
                    total_months = int(advance.custom_repayment_period_in_months or 0)
                    if total_months > 0:
                        emi = total_advance_amount / total_months
                        for i in range(total_months):
                            idx += 1
                            payment_date = add_months(start_date, i)
                            balance_amount -= emi
                            repayment_schedule.append({
                                "idx": idx,
                                "payment_date": payment_date,
                                "payment_amount": round(emi, 2),
                                "balance_amount": round(balance_amount, 2),
                                "deducted": 0,
                                "additional_salary_id": None
                            })

        end_date = repayment_schedule[-1]["payment_date"] if repayment_schedule else None

        total_paid_amount = sum(r["payment_amount"] for r in repayment_schedule if r.get("deducted") == 1)
        final_balance = flt(advance.advance_amount) - total_paid_amount

        results.append({
            "advance_type": advance.custom_advance_type,
            "status": advance.status,
            "total_advance_amount": advance.advance_amount,
            "start_date": start_date,
            "end_date": end_date,
            "repayments": repayment_schedule,
            "total_paid_amount": total_paid_amount,
            "balance_amount": final_balance
        })

    return results



def validate(self, method):
    if self.employee and self.posting_date and self.custom_advance_type:
        advance_amount = get_advance_amount_checking(self.employee, self.custom_advance_type, self.posting_date)

        if advance_amount is not None and flt(self.advance_amount) > flt(advance_amount):
            frappe.throw(
                f"Advance amount {fmt_money(self.advance_amount)} exceeds "
                f"the allowable limit of {fmt_money(advance_amount)} based on attendance and salary."
            )


@frappe.whitelist()
def get_advance_amount_checking(employee, advance_type, posting_date):
    if not (employee and advance_type and posting_date):
        return None

    emp_doc = frappe.get_doc("Employee", employee)
    holiday_list = emp_doc.holiday_list

    posting_date = getdate(posting_date)
    total_days = 0

    start_date = posting_date.replace(day=1)
    end_date = posting_date



    advance_type_doc = frappe.get_doc("Advance Type", advance_type)

    if advance_type_doc.policy_based_type == 1 and advance_type_doc.percentage:
        attendance = frappe.db.get_all(
            "Attendance",
            filters={
                "employee": employee,
                "attendance_date": ["between", [start_date, end_date]],
                "status": ["in", ["Present", "Half Day"]],
                "docstatus": 1
            },
            fields=["status"]
        )

        for att in attendance:
            if att.status == "Present":
                total_days += 1
            elif att.status == "Half Day":
                total_days += 0.5


        if holiday_list:
            holiday_doc = frappe.get_doc("Holiday List", holiday_list)
            for h in holiday_doc.holidays:
                if start_date <= h.holiday_date <= end_date:
                    total_days += 1

    get_salary_structure = frappe.db.get_all(
        "Salary Structure Assignment",
        filters={"employee": employee, "docstatus": 1},
        fields=["*"],
        order_by="from_date desc",
        limit=1
    )
    if get_salary_structure:
        salary_structure = frappe.get_doc("Salary Structure Assignment", get_salary_structure[0].name)
        if salary_structure and total_days:
            days_in_month = calendar.monthrange(posting_date.year, posting_date.month)[1]

            per_day_salary = (salary_structure.custom_fixed_gross_annual / 12) / days_in_month
            total_salary = per_day_salary * total_days

            advance_amount = (advance_type_doc.percentage / 100) * total_salary

            return round(advance_amount, 2)

    return None


def on_submit(self, method):
    if self.custom_final_status=="Approved" and self.custom_repayment_type=="One Time":
        frappe.get_doc({
            "doctype": "Additional Salary",
            "employee": self.employee,
            "company": self.company,
            "salary_component": self.custom_deduction_component,
            "amount": self.advance_amount,
            "is_recurring": 1,
            "from_date": get_first_day(self.custom_repayment_start_date),
            "to_date": get_first_day(self.custom_repayment_start_date),
            "ref_doctype": "Employee Advance",
            "ref_docname": self.name
        }).insert(ignore_permissions=True).submit()


    elif self.custom_final_status == "Approved" and self.custom_repayment_type == "Recurring" and self.custom_repayment_methods == "Repay Over Number of Periods":
        total_advance_amount = float(self.advance_amount or 0)
        total_months = int(self.custom_repayment_period_in_months or 0)
        start_date = self.custom_repayment_start_date

        if total_months > 0:
            emi = total_advance_amount / total_months
            end_date = add_months(start_date, total_months - 1)

            frappe.get_doc({
                "doctype": "Additional Salary",
                "employee": self.employee,
                "company": self.company,
                "salary_component": self.custom_deduction_component,
                "amount": round(emi, 2),
                "is_recurring": 1,
                "from_date": get_first_day(start_date),
                "to_date": get_first_day(end_date),
                "ref_doctype": "Employee Advance",
                "ref_docname": self.name
            }).insert(ignore_permissions=True).submit()

    elif (self.custom_final_status == "Approved" and self.custom_repayment_type == "Recurring" and self.custom_repayment_methods == "Repay Fixed Amount per Period"):
        total_advance_amount = float(self.advance_amount or 0)
        fixed_amount = float(self.custom_monthly_repayment_amount or 0)
        start_date = self.custom_repayment_start_date

        if fixed_amount > 0:
            # Step 1: Work out full months and remainder
            total_months = int(total_advance_amount // fixed_amount)  # 16 months
            remainder = total_advance_amount % fixed_amount           # 2000

            # Step 2: If we have full EMI months, create recurring Additional Salary
            if total_months > 0:
                end_date = add_months(start_date, total_months - 1)

                frappe.get_doc({
                    "doctype": "Additional Salary",
                    "employee": self.employee,
                    "company": self.company,
                    "salary_component": self.custom_deduction_component,
                    "amount": fixed_amount,
                    "is_recurring": 1,
                    "from_date": get_first_day(start_date),   # first month
                    "to_date": get_first_day(end_date),       # last full EMI month
                    "ref_doctype": "Employee Advance",
                    "ref_docname": self.name
                }).insert(ignore_permissions=True).submit()

            # Step 3: If remainder exists, create one-time Additional Salary
            if remainder > 0:
                last_month = add_months(start_date, total_months)

                frappe.get_doc({
                    "doctype": "Additional Salary",
                    "employee": self.employee,
                    "company": self.company,
                    "salary_component": self.custom_deduction_component,
                    "amount": remainder,
                    "is_recurring": 1,   # one-time
                    "from_date": get_first_day(last_month),
                    "to_date": get_first_day(last_month),
                    "ref_doctype": "Employee Advance",
                    "ref_docname": self.name
                }).insert(ignore_permissions=True).submit()



import frappe
from frappe.utils import flt, cint, getdate, add_months, get_first_day

@frappe.whitelist()
def hold_installments(repayments, idx, hold_months, hold_option, employee, doc_id, component, company):
    import json
    repayments = json.loads(repayments)

    idx = int(idx)
    hold_months = int(hold_months)



    selected_row = next((r for r in repayments if r.get("idx") == idx), None)
    if not selected_row:
        frappe.throw(f"No repayment found for idx {idx}")

    current_amt = flt(selected_row.get("payment_amount", 0))
    addl_salary_id = selected_row.get("additional_salary_id")
    holding_date = getdate(selected_row.get("payment_date"))

    if hold_option == "Recover Pending in Next Month" and idx==1:

        next_rows = [r for r in repayments if r.get("idx") > idx]
        hold_rows = [selected_row] + next_rows[:hold_months]

        total_amt = sum([flt(r.get("payment_amount", 0)) for r in hold_rows])

        from_date = get_first_day(getdate(selected_row.get("payment_date")))
        to_date = get_first_day(getdate(hold_rows[-1].get("payment_date")))

        next_unpaid_row = next((r for r in repayments if r.get("idx") > hold_rows[-1].get("idx")), None)
        if next_unpaid_row:
            next_addl_salary = frappe.get_doc("Additional Salary", next_unpaid_row.get("additional_salary_id"))
            next_addl_salary.from_date = get_first_day(getdate(next_unpaid_row.get("payment_date")))
            next_addl_salary.save(ignore_permissions=True)

        new_addl_salary = frappe.new_doc("Additional Salary")
        new_addl_salary.employee = employee
        new_addl_salary.company = company
        new_addl_salary.salary_component = component
        new_addl_salary.amount = total_amt
        new_addl_salary.from_date = to_date
        new_addl_salary.to_date = to_date
        new_addl_salary.ref_doctype = "Employee Advance"
        new_addl_salary.ref_docname = doc_id
        new_addl_salary.is_recurring = 1
        new_addl_salary.insert(ignore_permissions=True)
        new_addl_salary.submit()

    if hold_option == "Distribute Across Future Months" and idx == 1:
        hold_rows = [r for r in repayments if r.get("idx") >= idx][:hold_months]
        total_amt = sum([flt(r.get("payment_amount", 0)) for r in hold_rows])

        frappe.msgprint(f"Total Hold Amount: {total_amt}")

        future_rows = [r for r in repayments if r.get("idx") > hold_rows[-1].get("idx")]
        if not future_rows:
            frappe.throw("No future repayments found to distribute.")

        unique_salary_ids = list({r.get("additional_salary_id") for r in future_rows if r.get("additional_salary_id")})
        count_ids = len(unique_salary_ids)

        frappe.msgprint(f"Unique Additional Salaries: {unique_salary_ids}")
        frappe.msgprint(f"count_ids: {count_ids}")

        if count_ids == 0:
            frappe.throw("No Additional Salary found in future rows.")

        total_rows_to_distribute = len(repayments) - len(hold_rows)
        if total_rows_to_distribute <= 0:
            frappe.throw("No rows left to distribute.")

        per_share = flt(total_amt) / total_rows_to_distribute
        # frappe.msgprint(f"Per Row Share: {per_share}")

        for sal_id in unique_salary_ids:
            addl_salary = frappe.get_doc("Additional Salary", sal_id)
            addl_salary.amount = flt(addl_salary.amount) + per_share
            addl_salary.save(ignore_permissions=True)
            # frappe.msgprint(f"Updated {addl_salary.name} → New Amount: {addl_salary.amount}")


        first_future = future_rows[0]
        if first_future.get("additional_salary_id"):
            next_addl_salary = frappe.get_doc("Additional Salary", first_future.get("additional_salary_id"))
            new_from_date = get_first_day(getdate(first_future.get("payment_date")))
            next_addl_salary.from_date = new_from_date
            next_addl_salary.save(ignore_permissions=True)
            # frappe.msgprint(f"Shifted from_date of {next_addl_salary.name} → {new_from_date}")

        # frappe.msgprint(
        #     f"Held {hold_months} row(s). "
        #     f"Distributed {total_amt} equally across {count_ids} Additional Salaries "
        #     f"(each got +{per_share})."
        #     )


    return "success"
