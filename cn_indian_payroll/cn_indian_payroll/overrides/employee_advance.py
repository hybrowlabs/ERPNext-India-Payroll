

import frappe
from frappe.utils import flt, add_months, getdate
from frappe.utils import flt, getdate, add_months
import calendar
from frappe.utils import fmt_money
from frappe.utils import add_months, get_first_day
from frappe.utils import flt, cint, getdate, add_months, get_first_day




def before_submit(self, method):
    if self.custom_type == "Salary Advance":
        if not self.custom_note_remarks or not self.custom_deduction_component:
            frappe.throw("Please add Note/Remarks and select a Deduction Component in the Note Section before submitting.")

        self.custom_total_balance_amount = (self.advance_amount or 0) - (self.custom_total_paid_amount or 0)

    elif self.custom_type == "Reimbursement / Expense Advance":
        if not self.custom_note_remarks:
            frappe.throw("Please add Note/Remarks in the Note Section before submitting.")


    if self.custom_final_status=="Pending":
        frappe.throw("Please Select the Status Approved or Rejected")


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
            fields=['name', 'from_date', 'to_date', 'amount','payroll_date'],
            order_by='from_date asc'
        )

        if get_additional_salary:
            for rec in get_additional_salary:
                from_date = getdate(rec.payroll_date)
                to_date = getdate(rec.payroll_date)

                total_months = ((to_date.year - from_date.year) * 12 +
                                (to_date.month - from_date.month)) + 1

                current_date = from_date
                for i in range(total_months):
                    idx += 1
                    pay_amount = min(balance_amount, flt(rec.amount))
                    balance_amount -= pay_amount


                    salary_slips = frappe.db.get_all(
                        "Salary Slip",
                        filters=[
                            ["employee", "=", employee],
                            ["company", "=", advance.company],
                            ["docstatus", "=", 1],
                            ["start_date", "<=", current_date],
                            ["end_date", ">=", current_date],
                        ],
                        fields=["name"],
                        limit=1,
                    )

                    deducted = 1 if salary_slips else 0

                    repayment_schedule.append({
                        "idx": idx,
                        "payment_date": current_date,
                        "payment_amount": pay_amount,
                        "balance_amount": balance_amount,
                        "deducted": deducted,
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
            fields=['name', 'from_date', 'to_date', 'amount','payroll_date'],
            order_by='from_date asc'
        )


        if get_additional_salary:
            for rec in get_additional_salary:
                from_date = getdate(rec.payroll_date)
                to_date = getdate(rec.payroll_date)



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


                    salary_slips = frappe.db.get_all(
                        "Salary Slip",
                        filters=[
                            ["employee", "=", employee],
                            ["company", "=", advance.company],
                            ["docstatus", "=", 1],
                            ["start_date", "<=", current_date],
                            ["end_date", ">=", current_date],
                        ],
                        fields=["name"],
                        limit=1,
                    )

                    deducted = 1 if salary_slips else 0

                    repayment_schedule.append({
                        "idx": idx,
                        "payment_date": current_date,
                        "payment_amount": pay_amount,
                        "balance_amount": balance_amount,
                        "deducted": deducted,
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

    self.custom_total_paid_amount=0
    self.custom_total_balance_amount=self.advance_amount

    if self.employee and self.custom_type=="Salary Advance":
        self.repay_unclaimed_amount_from_salary=0
    elif self.employee and self.custom_type=="Reimbursement / Expense Advance":
        self.repay_unclaimed_amount_from_salary=1


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
    if self.custom_type=="Salary Advance":
        if self.custom_final_status=="Approved" and self.custom_repayment_type=="One Time":
            frappe.get_doc({
                "doctype": "Additional Salary",
                "employee": self.employee,
                "company": self.company,
                "salary_component": self.custom_deduction_component,
                "amount": self.advance_amount,
                "payroll_date": get_first_day(self.custom_repayment_start_date),
                "ref_doctype": "Employee Advance",
                "ref_docname": self.name
            }).insert(ignore_permissions=True).submit()



        elif (
            self.custom_final_status == "Approved"
            and self.custom_repayment_type == "Recurring"
            and self.custom_repayment_methods == "Repay Over Number of Periods"
        ):
            total_advance_amount = float(self.advance_amount or 0)
            total_months = int(self.custom_repayment_period_in_months or 0)
            start_date = self.custom_repayment_start_date

            if total_months > 0:
                emi = total_advance_amount / total_months

                for i in range(total_months):
                    current_date = add_months(start_date, i)
                    frappe.get_doc({
                        "doctype": "Additional Salary",
                        "employee": self.employee,
                        "company": self.company,
                        "salary_component": self.custom_deduction_component,
                        "amount": round(emi, 2),
                        "payroll_date":get_first_day(current_date),
                        "ref_doctype": "Employee Advance",
                        "ref_docname": self.name
                    }).insert(ignore_permissions=True).submit()



        elif (
            self.custom_final_status == "Approved"
            and self.custom_repayment_type == "Recurring"
            and self.custom_repayment_methods == "Repay Fixed Amount per Period"
        ):
            total_advance_amount = float(self.advance_amount or 0)
            fixed_amount = float(self.custom_monthly_repayment_amount or 0)
            start_date = self.custom_repayment_start_date

            if fixed_amount > 0:
                total_months = int(total_advance_amount // fixed_amount)
                remainder = total_advance_amount % fixed_amount

                for i in range(total_months):
                    current_date = add_months(start_date, i)
                    frappe.get_doc({
                        "doctype": "Additional Salary",
                        "employee": self.employee,
                        "company": self.company,
                        "salary_component": self.custom_deduction_component,
                        "amount": fixed_amount,
                        "payroll_date": get_first_day(current_date),
                        "ref_doctype": "Employee Advance",
                        "ref_docname": self.name
                    }).insert(ignore_permissions=True).submit()

                if remainder > 0:
                    last_month = add_months(start_date, total_months)
                    frappe.get_doc({
                        "doctype": "Additional Salary",
                        "employee": self.employee,
                        "company": self.company,
                        "salary_component": self.custom_deduction_component,
                        "amount": remainder,
                        "payroll_date": get_first_day(last_month),
                        "ref_doctype": "Employee Advance",
                        "ref_docname": self.name
                    }).insert(ignore_permissions=True).submit()


@frappe.whitelist()
def hold_installments(repayments, idx, hold_months, hold_option, employee, doc_id, component, company):
    import json
    repayments = json.loads(repayments)

    idx = int(idx)
    hold_months = int(hold_months)
    selected_row = next((r for r in repayments if r.get("idx") == idx), None)

    # frappe.msgprint(str(selected_row))
    if not selected_row:
        frappe.throw(f"No repayment found for idx {idx}")

    holding_date = getdate(selected_row.get("payment_date"))

    if hold_option == "Recover Pending in Next Month":
        next_date = add_months(holding_date, hold_months)
        held_rows = [r for r in repayments if idx <= r.get("idx") < idx + hold_months]
        next_row = next((r for r in repayments if r.get("idx") == idx + hold_months), None)
        held_additionals = [
            {
                "additional_salary_id": r.get("additional_salary_id"),
                "payment_date": r.get("payment_date"),
                "amount": flt(r.get("payment_amount") or 0)
            }
            for r in held_rows if r.get("additional_salary_id")
        ]

        next_amount_sum = sum(r["amount"] for r in held_additionals)

        for row in held_additionals:
            if row.get("additional_salary_id"):
                try:
                    addl_doc = frappe.get_doc("Additional Salary", row["additional_salary_id"])

                    if addl_doc.docstatus == 1:
                        addl_doc.cancel()

                    addl_doc.delete()
                except Exception as e:
                    frappe.log_error(message=frappe.get_traceback(), title="Hold Installments Delete Error")


        if next_row and next_row.get("additional_salary_id"):
            additional_salary = frappe.get_doc("Additional Salary", next_row.get("additional_salary_id"))
            additional_salary.amount = flt(additional_salary.amount) + next_amount_sum
            additional_salary.save(ignore_permissions=True)


    if hold_option == "Distribute Across Future Months":
        held_rows = [r for r in repayments if idx <= r.get("idx") < idx + hold_months]
        future_rows = [r for r in repayments if r.get("idx") >= idx + hold_months]

        held_additionals = [
            {
                "additional_salary_id": r.get("additional_salary_id"),
                "payment_date": r.get("payment_date"),
                "amount": flt(r.get("payment_amount") or 0)
            }
            for r in held_rows if r.get("additional_salary_id")
        ]
        total_held_amount = sum(r["amount"] for r in held_additionals)

        for row in held_additionals:
            if row.get("additional_salary_id"):
                try:
                    addl_doc = frappe.get_doc("Additional Salary", row["additional_salary_id"])
                    if addl_doc.docstatus == 1:
                        addl_doc.cancel()
                    addl_doc.delete()
                except Exception as e:
                    frappe.log_error(message=frappe.get_traceback(), title="Hold Installments Delete Error")

        if future_rows and total_held_amount > 0:
            per_month_extra = total_held_amount / len(future_rows)

            for r in future_rows:
                if r.get("additional_salary_id"):
                    try:
                        addl_doc = frappe.get_doc("Additional Salary", r["additional_salary_id"])
                        addl_doc.amount = flt(addl_doc.amount) + per_month_extra
                        addl_doc.save(ignore_permissions=True)
                    except Exception as e:
                        frappe.log_error(message=frappe.get_traceback(), title="Distribute Across Future Months Error")

    if hold_option == "Extend Repayment Period":
        held_rows = [r for r in repayments if idx <= r.get("idx") < idx + hold_months]

        held_additionals = [
            {
                "additional_salary_id": r.get("additional_salary_id"),
                "payment_date": r.get("payment_date"),
                "amount": flt(r.get("payment_amount") or 0)
            }
            for r in held_rows if r.get("additional_salary_id")
        ]
        total_held_amount = sum(r["amount"] for r in held_additionals)
        for row in held_additionals:
            if row.get("additional_salary_id"):
                try:
                    addl_doc = frappe.get_doc("Additional Salary", row["additional_salary_id"])
                    if addl_doc.docstatus == 1:
                        addl_doc.cancel()
                    addl_doc.delete()
                except Exception as e:
                    frappe.log_error(message=frappe.get_traceback(), title="Extend Repayment Period Delete Error")

        last_row = max(repayments, key=lambda r: r.get("payment_date"))

        if last_row and last_row.get("payment_date"):
            last_date = getdate(last_row.get("payment_date"))

            fixed_amount = flt(held_rows[0].get("payment_amount")) if held_rows else 0
            if fixed_amount > 0:
                full_months = int(total_held_amount // fixed_amount)
                remainder = total_held_amount % fixed_amount

                for i in range(full_months):
                    new_date = add_months(last_date, i + 1)
                    frappe.get_doc({
                        "doctype": "Additional Salary",
                        "employee": employee,
                        "company": company,
                        "salary_component": component,
                        "amount": fixed_amount,
                        # "is_recurring": 1,
                        # "from_date": new_date,
                        "payroll_date":new_date,
                        "ref_doctype": "Employee Advance",
                        "ref_docname": doc_id,
                    }).insert(ignore_permissions=True).submit()

                if remainder > 0:
                    new_date = add_months(last_date, full_months + 1)
                    frappe.get_doc({
                        "doctype": "Additional Salary",
                        "employee": employee,
                        "company": company,
                        "salary_component": component,
                        "amount": remainder,
                        # "is_recurring": 1,
                        # "from_date": new_date,
                        "payroll_date":new_date,
                        "ref_doctype": "Employee Advance",
                        "ref_docname": doc_id,
                    }).insert(ignore_permissions=True).submit()


    return "success"




@frappe.whitelist()
def edit_installment(repayments, idx, hold_months, hold_option, installment_id, installment_amount, employee, doc_id, component, company):
    """
    Edit an installment amount and adjust future installments based on hold_option.
    """
    import json
    repayments = json.loads(repayments)

    idx = int(idx)
    hold_months = int(hold_months)
    installment_amount = flt(installment_amount)

    selected_row = next((r for r in repayments if r.get("idx") == idx), None)
    if not selected_row:
        frappe.throw(f"No repayment found for idx {idx}")

    addl_doc = frappe.get_doc("Additional Salary", installment_id)
    old_amount = flt(addl_doc.amount)

    if installment_amount <= 0:
        frappe.throw("Installment amount must be greater than 0")

    addl_doc.amount = installment_amount
    addl_doc.save(ignore_permissions=True)

    balance_to_adjust = old_amount - installment_amount
    if balance_to_adjust <= 0:
        return "success"

    if hold_option == "Recover Pending in Next Month":
        held_rows = [r for r in repayments if idx <= r.get("idx") < idx + hold_months]

        for r in held_rows:
            if r.get("additional_salary_id"):
                try:
                    addl_doc = frappe.get_doc("Additional Salary", r["additional_salary_id"])
                    addl_doc.amount = installment_amount
                    addl_doc.save(ignore_permissions=True)
                except Exception:
                    frappe.log_error(frappe.get_traceback(), "Edit Installment - Update Held Rows")

        next_row = next((r for r in repayments if r.get("idx") == idx + hold_months), None)
        if next_row and next_row.get("additional_salary_id"):
            try:
                future_addl = frappe.get_doc("Additional Salary", next_row["additional_salary_id"])
                future_addl.amount = flt(future_addl.amount) + (balance_to_adjust * hold_months)
                future_addl.save(ignore_permissions=True)
            except Exception:
                frappe.log_error(frappe.get_traceback(), "Edit Installment - Recover Pending Adjustment")


    if hold_option == "Distribute Across Future Months":
        held_rows = [r for r in repayments if idx <= r.get("idx") < idx + hold_months]

        for r in held_rows:
            if r.get("additional_salary_id"):
                try:
                    addl_doc = frappe.get_doc("Additional Salary", r["additional_salary_id"])
                    addl_doc.amount = installment_amount
                    addl_doc.save(ignore_permissions=True)
                except Exception:
                    frappe.log_error(frappe.get_traceback(), "Edit Installment - Update Held Rows")

        total_held_amount = balance_to_adjust * hold_months

        future_rows = [r for r in repayments if r.get("idx") >= idx + hold_months]

        if future_rows and total_held_amount > 0:
            per_month_extra = total_held_amount / len(future_rows)

            for r in future_rows:
                if r.get("additional_salary_id"):
                    try:
                        addl_doc = frappe.get_doc("Additional Salary", r["additional_salary_id"])
                        addl_doc.amount = flt(addl_doc.amount) + per_month_extra
                        addl_doc.save(ignore_permissions=True)
                    except Exception:
                        frappe.log_error(
                            message=frappe.get_traceback(),
                            title="Distribute Across Future Months Error"
                        )

    return "success"



@frappe.whitelist()
def delete_un_deducted_additional_salaries(employee, id, company, settlement_date, remarks, settlement_amount):
    """
    Settles the advance fully and deletes all undeducted Additional Salary records.
    """
    doc = frappe.get_doc("Employee Advance", id)

    settlement_amount = flt(settlement_amount)
    total_paid = flt(doc.custom_total_paid_amount)

    doc.custom_total_paid_amount = settlement_amount + total_paid
    doc.custom_total_balance_amount = 0
    doc.custom_settlement_date = settlement_date
    doc.custom_remarks = remarks
    doc.save(ignore_permissions=True)

    results = get_advance_dashboard_erp(employee, id, company)

    for advance in results:
        for repayment in advance.get("repayments", []):
            if repayment.get("deducted") == 0 and repayment.get("additional_salary_id"):
                try:
                    addl_doc = frappe.get_doc("Additional Salary", repayment["additional_salary_id"])
                    if addl_doc.docstatus == 1:
                        addl_doc.cancel()
                    frappe.delete_doc("Additional Salary", repayment["additional_salary_id"], ignore_permissions=True, force=1)
                except Exception:
                    frappe.log_error(frappe.get_traceback(), "Cancel + Delete Additional Salary Failed")

    return {
        "status": "success",
        "settlement_amount": settlement_amount
    }
