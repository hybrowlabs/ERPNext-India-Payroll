# import frappe

# from cn_indian_payroll.cn_indian_payroll.overrides.salary_appraisal_calculation import (
#     appraisal_calculation,
# )


# def on_cancel(self, method):
#     cancel_additional_salary(self)
#     cancel_appraisal_calculation(self)


# def validate(self, methd):
#     create_salary_appraisal_calculation(self)


# def on_submit(self, method):
#     self.custom_status = "Completed"


# def create_salary_appraisal_calculation(self):
#     if self.custom_status == "Payroll Configured":
#         get_appraisal_calculation = frappe.get_list(
#             "Salary Appraisal Calculation",
#             filters={"promotion_reference": self.name, "docstatus": 1},
#             fields=["*"],
#         )
#         if not get_appraisal_calculation:
#             result = appraisal_calculation(
#                 promotion_id=self.name,
#                 employee_id=self.employee,
#                 company=self.company,
#                 date=self.custom_additional_salary_date,
#                 effective_from=self.promotion_date,
#             )


# def cancel_additional_salary(self):
#     get_appraisal_additional = frappe.get_list(
#         "Additional Salary",
#         filters={"custom_employee_promotion_id": self.name},
#         fields=["*"],
#     )
#     if get_appraisal_additional:
#         for each_appraisal_doc in get_appraisal_additional:
#             get_each_doc = frappe.get_doc("Additional Salary", each_appraisal_doc.name)
#             get_each_doc.docstatus = 2
#             get_each_doc.save()

#             frappe.delete_doc("Additional Salary", each_appraisal_doc.name)


# def cancel_appraisal_calculation(self):
#     get_appraisal_calculation = frappe.get_list(
#         "Salary Appraisal Calculation",
#         filters={"employee_promotion_id": self.name},
#         fields=["*"],
#     )
#     if get_appraisal_calculation:
#         for each_appraisal_doc in get_appraisal_calculation:
#             get_each_doc = frappe.get_doc(
#                 "Salary Appraisal Calculation", each_appraisal_doc.name
#             )
#             get_each_doc.docstatus = 2
#             get_each_doc.save()

#             frappe.delete_doc("Salary Appraisal Calculation", each_appraisal_doc.name)


import frappe
from frappe.utils import nowdate
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip


def validate(self, method):
    if self.custom_status == "Payroll Configured":
        create_salary_appraisal_calculation(self)


def create_salary_appraisal_calculation(self):
    if not self.promotion_date:
        return

    arrear_array = {}
    bonus_array = {}
    reimbursement_array = {}

    # -----------------------------------
    # Latest Salary Structure
    # -----------------------------------
    salary_structure_assignment = frappe.get_list(
        "Salary Structure Assignment",
        filters={"employee": self.employee, "company": self.company, "docstatus": 1},
        fields=["salary_structure", "from_date"],
        order_by="from_date desc",
        limit=1,
    )

    if not salary_structure_assignment:
        frappe.throw("No Salary Structure Assignment found")

    latest_structure = salary_structure_assignment[0]

    new_salary_slip = make_salary_slip(
        source_name=latest_structure.salary_structure,
        employee=self.employee,
        posting_date=latest_structure.from_date,
        for_preview=1,
    )

    # -----------------------------------
    # Collect New Structure Components
    # -----------------------------------
    new_amounts = {}
    new_bonus_amounts = {}

    for row in new_salary_slip.earnings + new_salary_slip.deductions:
        component = frappe.get_doc("Salary Component", row.salary_component)

        if component.custom_is_part_of_appraisal:
            new_amounts[row.salary_component] = row.amount

        if component.custom_is_accrual:
            new_bonus_amounts[row.salary_component] = row.amount

    total_working_days_latest = 31

    # -----------------------------------
    # Get Salary Slips
    # -----------------------------------
    sal_slips = frappe.get_list(
        "Salary Slip",
        filters={
            "employee": self.employee,
            "start_date": [">=", self.promotion_date],
            "docstatus": 1,
        },
        fields=[
            "name",
            "custom_month",
            "total_working_days",
            "custom_total_leave_without_pay",
            "payment_days",
            "custom_salary_structure_assignment",
        ],
    )

    for slip in sal_slips:
        slip_doc = frappe.get_doc("Salary Slip", slip.name)

        # LOP Reversal
        lop_reversal_days = (
            frappe.db.sql(
                """
            SELECT SUM(number_of_days)
            FROM `tabLOP Reversal`
            WHERE employee=%s
            AND company=%s
            AND salary_slip=%s
            AND docstatus=1
        """,
                (self.employee, self.company, slip.name),
            )[0][0]
            or 0
        )

        total_payment_days = slip_doc.payment_days + lop_reversal_days

        # -----------------------------------
        # Call Calculation Functions
        # -----------------------------------
        calculate_arrear_components(
            slip_doc,
            new_amounts,
            arrear_array,
            total_working_days_latest,
            total_payment_days,
            lop_reversal_days,
        )

        calculate_bonus_components(
            slip_doc,
            new_bonus_amounts,
            bonus_array,
            total_working_days_latest,
            total_payment_days,
            lop_reversal_days,
        )

        # calculate_reimbursements(
        #     slip_doc,
        #     reimbursement_array,
        #     total_payment_days,
        #     lop_reversal_days
        # )

    # -----------------------------------
    # Insert Appraisal Document
    # -----------------------------------
    insert_appraisal = frappe.get_doc(
        {
            "doctype": "Salary Appraisal Calculation",
            "employee": self.employee,
            "posting_date": self.custom_additional_salary_date,
            "company": self.company,
            "promotion_reference": self.name,
            "status": "Draft",
        }
    )

    # Arrear Components
    for slip_rows in arrear_array.values():
        for row in slip_rows:
            insert_appraisal.append("salary_arrear_components", row)

    # Bonus Components
    for slip_rows in bonus_array.values():
        for row in slip_rows:
            insert_appraisal.append("salary_appraisal_bonus", row)

    # Reimbursements
    for slip_rows in reimbursement_array.values():
        for row in slip_rows:
            insert_appraisal.append("salary_appraisal_reimbursement", row)

    insert_appraisal.insert(ignore_permissions=True)
    frappe.db.commit()

    return insert_appraisal.name


# =========================================================
# Function 1 → Arrear Components
# =========================================================


def calculate_arrear_components(
    slip_doc,
    new_amounts,
    arrear_array,
    total_working_days_latest,
    total_payment_days,
    lop_reversal_days,
):
    old_components = {}

    for earning in slip_doc.earnings:
        component = frappe.get_doc("Salary Component", earning.salary_component)

        if not component.custom_is_part_of_appraisal:
            continue

        old_amount = (
            earning.custom_actual_amount / slip_doc.total_working_days
        ) * total_payment_days

        old_components[earning.salary_component] = old_amount

        if earning.salary_component in new_amounts:
            new_amount = (
                new_amounts[earning.salary_component] / total_working_days_latest
            ) * total_payment_days

            difference = new_amount - old_amount

        else:
            new_amount = 0
            difference = -old_amount

        arrear_array.setdefault(slip_doc.name, []).append(
            {
                "salary_component": earning.salary_component,
                "salary_slip_id": slip_doc.name,
                "month": slip_doc.custom_month,
                "working_days": slip_doc.total_working_days,
                "lop_days": slip_doc.custom_total_leave_without_pay,
                "payment_days": total_payment_days,
                "lop_reversal": lop_reversal_days,
                "old_amount": old_amount,
                "expected_amount": new_amount,
                "difference": difference,
            }
        )


# =========================================================
# Function 2 → Bonus Components
# =========================================================


def calculate_bonus_components(
    slip_doc,
    new_bonus_amounts,
    bonus_array,
    total_working_days_latest,
    total_payment_days,
    lop_reversal_days,
):
    for earning in slip_doc.earnings:
        component = frappe.get_doc("Salary Component", earning.salary_component)

        if not component.custom_is_accrual:
            continue

        old_amount = (
            earning.custom_actual_amount / slip_doc.total_working_days
        ) * total_payment_days

        if earning.salary_component in new_bonus_amounts:
            new_amount = (
                new_bonus_amounts[earning.salary_component] / total_working_days_latest
            ) * total_payment_days

            difference = new_amount - old_amount

        else:
            new_amount = 0
            difference = -old_amount

        bonus_array.setdefault(slip_doc.name, []).append(
            {
                "salary_component": earning.salary_component,
                "salary_slip_id": slip_doc.name,
                "month": slip_doc.custom_month,
                "working_days": slip_doc.total_working_days,
                "lop_days": slip_doc.custom_total_leave_without_pay,
                "payment_days": total_payment_days,
                "lop_reversal": lop_reversal_days,
                "old_amount": old_amount,
                "expected_amount": new_amount,
                "difference": difference,
            }
        )


# =========================================================
# Function 3 → Reimbursements
# =========================================================

# def calculate_reimbursements(
#     slip_doc,
#     reimbursement_array,
#     latest_structure,
#     total_payment_days,
#     lop_reversal_days
# ):

#     old_components = {}

#     # OLD ASSIGNMENT
#     if slip_doc.custom_salary_structure_assignment:

#         assignment = frappe.get_cached_doc(
#             "Salary Structure Assignment",
#             slip_doc.custom_salary_structure_assignment
#         )

#         for row in assignment.custom_employee_reimbursements:

#             old_amount = (
#                 row.monthly_total_amount /
#                 slip_doc.total_working_days
#             ) * total_payment_days

#             old_components[row.reimbursements] = old_amount

#     # NEW ASSIGNMENT
#     new_components = {}

#     latest_assignment = frappe.get_cached_doc(
#         "Salary Structure Assignment",
#         latest_structure.name
#     )

#     for row in latest_assignment.custom_employee_reimbursements:

#         new_amount = (
#             row.monthly_total_amount /
#             slip_doc.total_working_days
#         ) * total_payment_days

#         new_components[row.reimbursements] = new_amount

#     # Compare old components
#     for component, old_amount in old_components.items():

#         if component in new_components:
#             expected_amount = new_components[component]
#             difference = expected_amount - old_amount
#         else:
#             expected_amount = 0
#             difference = -old_amount

#         reimbursement_array.setdefault(slip_doc.name, []).append({
#             "salary_slip_id": slip_doc.name,
#             "salary_component": component,
#             "month": slip_doc.custom_month,
#             "working_days": slip_doc.total_working_days,
#             "lop_days": slip_doc.custom_total_leave_without_pay,
#             "payment_days": total_payment_days,
#             "lop_reversal": lop_reversal_days,
#             "old_amount": old_amount,
#             "expected_amount": expected_amount,
#             "difference": difference
#         })

#     # New components not in old
#     for component, new_amount in new_components.items():

#         if component not in old_components:

#             reimbursement_array.setdefault(slip_doc.name, []).append({
#                 "salary_slip_id": slip_doc.name,
#                 "salary_component": component,
#                 "month": slip_doc.custom_month,
#                 "working_days": slip_doc.total_working_days,
#                 "lop_days": slip_doc.custom_total_leave_without_pay,
#                 "payment_days": total_payment_days,
#                 "lop_reversal": lop_reversal_days,
#                 "old_amount": 0,
#                 "expected_amount": new_amount,
#                 "difference": new_amount
#             })
