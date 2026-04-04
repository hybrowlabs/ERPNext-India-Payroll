# import frappe
# from frappe.utils import nowdate
# from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip


# def validate(self, method):
#     if self.custom_status == "Payroll Configured":
#         create_salary_appraisal_calculation(self)


# def create_salary_appraisal_calculation(self):
#     if not self.promotion_date:
#         return

#     arrear_array = {}
#     bonus_array = {}
#     reimbursement_array = {}

#     # -----------------------------------
#     # Latest Salary Structure
#     # -----------------------------------
#     salary_structure_assignment = frappe.get_list(
#         "Salary Structure Assignment",
#         filters={"employee": self.employee, "company": self.company, "docstatus": 1},
#         fields=["salary_structure", "from_date"],
#         order_by="from_date desc",
#         limit=1,
#     )

#     if not salary_structure_assignment:
#         frappe.throw("No Salary Structure Assignment found")

#     latest_structure = salary_structure_assignment[0]

#     new_salary_slip = make_salary_slip(
#         source_name=latest_structure.salary_structure,
#         employee=self.employee,
#         posting_date=latest_structure.from_date,
#         for_preview=1,
#     )

#     # -----------------------------------
#     # Collect New Structure Components
#     # -----------------------------------
#     new_amounts = {}
#     new_bonus_amounts = {}

#     for row in new_salary_slip.earnings + new_salary_slip.deductions:
#         component = frappe.get_doc("Salary Component", row.salary_component)

#         if component.custom_is_part_of_appraisal:
#             new_amounts[row.salary_component] = row.amount

#         if component.custom_is_accrual:
#             new_bonus_amounts[row.salary_component] = row.amount

#     # -----------------------------------
#     # Get Salary Slips
#     # -----------------------------------
#     sal_slips = frappe.get_list(
#         "Salary Slip",
#         filters={
#             "employee": self.employee,
#             "start_date": [">=", self.promotion_date],
#             "docstatus": 1,
#         },
#         fields=[
#             "name",
#             "custom_month",
#             "total_working_days",
#             "custom_total_leave_without_pay",
#             "payment_days",
#             "custom_salary_structure_assignment",
#         ],
#     )

#     for slip in sal_slips:
#         slip_doc = frappe.get_doc("Salary Slip", slip.name)

#         # -----------------------------------
#         # LOP Reversal
#         # -----------------------------------
#         lop_reversal_days = (
#             frappe.db.sql(
#                 """
#                 SELECT SUM(number_of_days)
#                 FROM `tabLOP Reversal`
#                 WHERE employee=%s
#                 AND company=%s
#                 AND salary_slip=%s
#                 AND docstatus=1
#                 """,
#                 (self.employee, self.company, slip.name),
#             )[0][0]
#             or 0
#         )

#         total_payment_days = slip_doc.payment_days + lop_reversal_days

#         # -----------------------------------
#         # Calculate Arrears
#         # -----------------------------------
#         calculate_arrear_components(
#             slip_doc,
#             new_amounts,
#             arrear_array,
#             total_payment_days,
#             lop_reversal_days,
#         )

#         # -----------------------------------
#         # Calculate Bonus
#         # -----------------------------------
#         calculate_bonus_components(
#             slip_doc,
#             new_bonus_amounts,
#             bonus_array,
#             total_payment_days,
#             lop_reversal_days,
#         )

#     # -----------------------------------
#     # Insert Appraisal Document
#     # -----------------------------------
#     insert_appraisal = frappe.get_doc(
#         {
#             "doctype": "Salary Appraisal Calculation",
#             "employee": self.employee,
#             "posting_date": self.custom_additional_salary_date,
#             "company": self.company,
#             "promotion_reference": self.name,
#             "status": "Draft",
#         }
#     )

#     # Arrear
#     for slip_rows in arrear_array.values():
#         for row in slip_rows:
#             insert_appraisal.append("arrear_breakdown", row)

#     # Bonus
#     for slip_rows in bonus_array.values():
#         for row in slip_rows:
#             insert_appraisal.append("salary_appraisal_bonus", row)

#     # Reimbursement
#     for slip_rows in reimbursement_array.values():
#         for row in slip_rows:
#             insert_appraisal.append("salary_appraisal_reimbursement", row)

#     insert_appraisal.insert(ignore_permissions=True)
#     frappe.db.commit()

#     return insert_appraisal.name


# # =========================================================
# # Arrear Calculation
# # =========================================================


# def calculate_arrear_components(
#     slip_doc,
#     new_amounts,
#     arrear_array,
#     total_payment_days,
#     lop_reversal_days,
# ):
#     for earning in slip_doc.earnings:
#         component = frappe.get_doc("Salary Component", earning.salary_component)


#         if not component.custom_is_part_of_appraisal:
#             continue

#         # OLD AMOUNT
#         old_amount = (
#             earning.custom_actual_amount / slip_doc.total_working_days
#         ) * total_payment_days

#         # NEW AMOUNT
#         if earning.salary_component in new_amounts:
#             new_amount = (
#                 new_amounts[earning.salary_component] / slip_doc.total_working_days
#             ) * total_payment_days

#             difference = new_amount - old_amount

#         else:
#             new_amount = 0
#             difference = -old_amount

#         arrear_array.setdefault(slip_doc.name, []).append(
#             {
#                 "salary_component": earning.salary_component,
#                 "salary_slip_id": slip_doc.name,
#                 "month": slip_doc.custom_month,
#                 "working_days": slip_doc.total_working_days,
#                 "lop_days": slip_doc.custom_total_leave_without_pay,
#                 "payment_days": total_payment_days,
#                 "lop_reversal": lop_reversal_days,
#                 "old_amount": old_amount,
#                 "expected_amount": new_amount,
#                 "difference": difference,
#             }
#         )


#     for deduction in slip_doc.deductions:
#         component = frappe.get_doc("Salary Component", deduction.salary_component)

#         if not component.custom_is_part_of_appraisal:
#             continue


#         # OLD AMOUNT
#         old_amount = (
#             deduction.custom_actual_amount / slip_doc.total_working_days
#         ) * total_payment_days

#         # NEW AMOUNT
#         if deduction.salary_component in new_amounts:
#             new_amount = (
#                 new_amounts[deduction.salary_component] / slip_doc.total_working_days
#             ) * total_payment_days

#             difference = new_amount - old_amount

#         else:
#             new_amount = 0
#             difference = -old_amount

#         arrear_array.setdefault(slip_doc.name, []).append(
#             {
#                 "salary_component": deduction.salary_component,
#                 "salary_slip_id": slip_doc.name,
#                 "month": slip_doc.custom_month,
#                 "working_days": slip_doc.total_working_days,
#                 "lop_days": slip_doc.custom_total_leave_without_pay,
#                 "payment_days": total_payment_days,
#                 "lop_reversal": lop_reversal_days,
#                 "old_amount": old_amount,
#                 "expected_amount": new_amount,
#                 "difference": difference,
#             }
#         )


# # =========================================================
# # Bonus Calculation
# # =========================================================


# def calculate_bonus_components(
#     slip_doc,
#     new_bonus_amounts,
#     bonus_array,
#     total_payment_days,
#     lop_reversal_days,
# ):
#     for earning in slip_doc.earnings:
#         component = frappe.get_doc("Salary Component", earning.salary_component)

#         if not component.custom_is_accrual:
#             continue

#         # OLD AMOUNT
#         old_amount = (
#             earning.custom_actual_amount / slip_doc.total_working_days
#         ) * total_payment_days

#         # NEW AMOUNT
#         if earning.salary_component in new_bonus_amounts:
#             new_amount = (
#                 new_bonus_amounts[earning.salary_component]
#                 / slip_doc.total_working_days
#             ) * total_payment_days

#             difference = new_amount - old_amount

#         else:
#             new_amount = 0
#             difference = -old_amount

#         bonus_array.setdefault(slip_doc.name, []).append(
#             {
#                 "salary_component": earning.salary_component,
#                 "salary_slip_id": slip_doc.name,
#                 "month": slip_doc.custom_month,
#                 "working_days": slip_doc.total_working_days,
#                 "lop_days": slip_doc.custom_total_leave_without_pay,
#                 "payment_days": total_payment_days,
#                 "lop_reversal": lop_reversal_days,
#                 "old_amount": old_amount,
#                 "expected_amount": new_amount,
#                 "difference": difference,
#             }
#         )


import frappe
from frappe.utils import nowdate
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip


# =========================================================
# VALIDATE
# =========================================================


def validate(self, method):
    if self.custom_status == "Payroll Configured":
        create_salary_appraisal_calculation(self)


# =========================================================
# MAIN FUNCTION
# =========================================================


def create_salary_appraisal_calculation(self):
    if not self.promotion_date:
        return

    arrear_array = {}
    bonus_array = {}
    reimbursement_array = {}

    # -----------------------------------
    # Fetch Previous Paid Arrears (IMPORTANT)
    # -----------------------------------
    paid_map = get_paid_from_appraisals(
        self.employee,
        self.promotion_date,
        self.custom_additional_salary_date,
        self.name,
    )

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
        ],
    )

    for slip in sal_slips:
        slip_doc = frappe.get_doc("Salary Slip", slip.name)

        # -----------------------------------
        # LOP Reversal
        # -----------------------------------
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
        # Calculate Arrears
        # -----------------------------------
        calculate_arrear_components(
            slip_doc,
            new_amounts,
            arrear_array,
            total_payment_days,
            lop_reversal_days,
            paid_map,
        )

        # -----------------------------------
        # Calculate Bonus
        # -----------------------------------
        calculate_bonus_components(
            slip_doc,
            new_bonus_amounts,
            bonus_array,
            total_payment_days,
            lop_reversal_days,
        )

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

    for slip_rows in arrear_array.values():
        for row in slip_rows:
            insert_appraisal.append("arrear_breakdown", row)

    for slip_rows in bonus_array.values():
        for row in slip_rows:
            insert_appraisal.append("salary_appraisal_bonus", row)

    insert_appraisal.insert(ignore_permissions=True)
    frappe.db.commit()

    return insert_appraisal.name


# =========================================================
# FETCH PREVIOUS PAID ARREARS (KEY LOGIC)
# =========================================================

# def get_paid_from_appraisals(employee, current_posting_date):

#     paid_map = {}

#     appraisals = frappe.get_list(
#         "Salary Appraisal Calculation",
#         filters={
#             "employee": employee,
#             "posting_date": ["<", current_posting_date],
#             "docstatus": 1
#         },
#         fields=["name"]
#     )

#     for app in appraisals:
#         doc = frappe.get_doc("Salary Appraisal Calculation", app.name)

#         for row in doc.arrear_breakdown:
#             key = (row.salary_slip_id, row.salary_component)
#             paid_map[key] = paid_map.get(key, 0) + row.difference

#     return paid_map


def get_paid_from_appraisals(
    employee, promotion_date, custom_additional_salary_date, current_docname=None
):
    paid_map = {}

    appraisals = frappe.get_list(
        "Salary Appraisal Calculation",
        filters={
            "employee": employee,
            "posting_date": [
                "between",
                [promotion_date, custom_additional_salary_date],
            ],
            "docstatus": 1,
        },
        fields=["name"],
    )

    for app in appraisals:
        if current_docname and app.name == current_docname:
            continue

        doc = frappe.get_doc("Salary Appraisal Calculation", app.name)

        for row in doc.arrear_breakdown:
            # key = (row.salary_slip_id, row.salary_component)
            component_key = (
                frappe.get_value(
                    "Salary Component", row.salary_component, "custom_component"
                )
                or row.salary_component
            )

            key = (row.salary_slip_id, component_key)
            paid_map[key] = paid_map.get(key, 0) + row.difference

    return paid_map


# =========================================================
# ARREAR CALCULATION
# =========================================================


def calculate_arrear_components(
    slip_doc, new_amounts, arrear_array, total_payment_days, lop_reversal_days, paid_map
):
    for row in slip_doc.earnings + slip_doc.deductions:
        component = frappe.get_doc("Salary Component", row.salary_component)

        if not component.custom_is_part_of_appraisal:
            continue

        # -----------------------------------
        # OLD AMOUNT (BASE)
        # -----------------------------------
        base_old_amount = (
            row.custom_actual_amount / slip_doc.total_working_days
        ) * total_payment_days

        # -----------------------------------
        # ADD ALREADY PAID ARREARS
        # -----------------------------------
        # already_paid = paid_map.get((slip_doc.name, row.salary_component), 0)

        component_key = (
            frappe.get_value(
                "Salary Component", row.salary_component, "custom_component"
            )
            or row.salary_component
        )

        already_paid = paid_map.get((slip_doc.name, component_key), 0)

        old_amount = base_old_amount + already_paid

        # -----------------------------------
        # NEW AMOUNT
        # -----------------------------------
        if row.salary_component in new_amounts:
            new_amount = (
                new_amounts[row.salary_component] / slip_doc.total_working_days
            ) * total_payment_days

            difference = new_amount - old_amount
        else:
            new_amount = 0
            difference = -old_amount

        if abs(difference) < 1:
            continue

        arrear_array.setdefault(slip_doc.name, []).append(
            {
                "salary_component": row.salary_component,
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
# BONUS CALCULATION (UNCHANGED)
# =========================================================


def calculate_bonus_components(
    slip_doc,
    new_bonus_amounts,
    bonus_array,
    total_payment_days,
    lop_reversal_days,
):
    for row in slip_doc.earnings:
        component = frappe.get_doc("Salary Component", row.salary_component)

        if not component.custom_is_accrual:
            continue

        old_amount = (
            row.custom_actual_amount / slip_doc.total_working_days
        ) * total_payment_days

        if row.salary_component in new_bonus_amounts:
            new_amount = (
                new_bonus_amounts[row.salary_component] / slip_doc.total_working_days
            ) * total_payment_days

            difference = new_amount - old_amount
        else:
            new_amount = 0
            difference = -old_amount

        bonus_array.setdefault(slip_doc.name, []).append(
            {
                "salary_component": row.salary_component,
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
