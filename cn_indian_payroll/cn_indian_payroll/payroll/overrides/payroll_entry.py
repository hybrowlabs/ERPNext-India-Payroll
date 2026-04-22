from frappe.utils import getdate,today,add_months,get_last_day
import datetime

import frappe
from frappe import _
from hrms.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry

class PayrollEntryOverride(PayrollEntry):

    def on_submit(self):
        super().on_submit()
        self.submit_new_joinee_arrear()

    def on_cancel(self):
        super().on_cancel()
        self.cancel_new_joinee_arrear()

    def cancel_new_joinee_arrear(self):
        joinee_arrear=frappe.get_all("New Joining Arrear",filters={"payroll_entry":self.name,"docstatus":1},pluck="name")
        if joinee_arrear:
            for doc in joinee_arrear:
                doc=frappe.get_doc("New Joining Arrear",doc)
                doc.cancel()
                frappe.db.commit()


    def submit_new_joinee_arrear(self):
        joinee_arrear=frappe.get_all("New Joining Arrear",filters={"payroll_entry":self.name,"docstatus":0},pluck="name")
        if joinee_arrear:
            for doc in joinee_arrear:
                doc=frappe.get_doc("New Joining Arrear",doc)
                doc.submit()
                frappe.db.commit()

    def make_filters(self):
        filters = frappe._dict(
            company=self.company,
            branch=self.branch,
            department=self.department,
            designation=self.designation,
            grade=self.grade,
            currency=self.currency,
            start_date=self.start_date,
            end_date=self.end_date,
            payroll_payable_account=self.payroll_payable_account,
            salary_slip_based_on_timesheet=self.salary_slip_based_on_timesheet,
        )

        if not self.salary_slip_based_on_timesheet:
            filters["payroll_frequency"] = self.payroll_frequency

        if self.custom_employment_type:
            filters["employment_type"] = self.custom_employment_type

        return filters



    @frappe.whitelist()
    def fill_employee_details(self):
        filters = self.make_filters()
        self.set("employees", [])

        employees = get_filtered_employees_with_employment_type(filters)
        valid_employees = []

        for emp in employees:
            ssa = frappe.get_all(
                "Salary Structure Assignment",
                filters={
                    "employee": emp.employee,
                    "docstatus": 1,
                    "from_date": ["<=", self.end_date],
                },
                fields=["name", "from_date", "salary_structure"],
                order_by="from_date desc",
                limit=1
            )

            if not ssa:
                continue

            ssa_doc = ssa[0]
            employee_doc = frappe.get_doc("Employee", emp.employee)
            date_of_joinee = getdate(employee_doc.date_of_joining)

            payroll_setting = frappe.get_doc("Payroll Settings")
            start_date = getdate(self.start_date)
            end_date = getdate(self.end_date)

            if payroll_setting.custom_configure_attendance_cycle:
                attendance_end_day = int(payroll_setting.custom_attendance_end_date)
                attendance_start_day = int(payroll_setting.custom_attendance_start_date)

                attendance_final_end_date = datetime.date(end_date.year, end_date.month, attendance_end_day)
                next_month_end_date = get_last_day(add_months(end_date, 1))
                next_month_attendance_end_date = datetime.date(next_month_end_date.year, next_month_end_date.month, attendance_start_day)
                diff_days = (next_month_end_date - next_month_attendance_end_date).days + 1

                if attendance_final_end_date < date_of_joinee <= end_date:

                    if payroll_setting.payroll_based_on == "Attendance":
                        days_diff = (end_date - date_of_joinee).days + 1
                        present_day = 0
                        absent_day = 0
                        half_day = 0
                        work_from_home = 0

                        attendance_records = frappe.get_all(
                            "Attendance",
                            filters={
                                "employee": emp.employee,
                                "attendance_date": ["between", (date_of_joinee, end_date)],
                            },
                            fields=["status", "leave_type"],
                        )

                        for att in attendance_records:
                            status = att.get("status")
                            leave_type = att.get("leave_type")

                            if status == "Present":
                                present_day += 1
                            elif status == "Absent":
                                absent_day += 1
                            elif status == "Half Day" and leave_type:
                                leave_doc = frappe.get_doc("Leave Type", leave_type)
                                half_day += 0.5 if leave_doc.is_lwp else 0
                                if not leave_doc.is_lwp:
                                    present_day += 1
                            elif status == "Half Day" and not leave_type:
                                half_day += 1
                            elif status == "On Leave" and leave_type:
                                leave_doc = frappe.get_doc("Leave Type", leave_type)
                                absent_day += 1 if leave_doc.is_lwp else 0
                                if not leave_doc.is_lwp:
                                    present_day += 1
                            elif status == "Work From Home":
                                work_from_home += 1

                        total_lop_days = absent_day + half_day
                        total_payment_days = days_diff - total_lop_days

                        if total_payment_days > 0:

                            existing_doc=frappe.db.exists("New Joining Arrear", {
                                "employee": emp.employee,
                                "company": self.company,
                                "payroll_entry": self.name
                            })
                            if not existing_doc:
                                arrear_doc = frappe.get_doc({
                                    "doctype": "New Joining Arrear",
                                    "employee": emp.employee,
                                    "company": self.company,
                                    "number_of_present_days": total_payment_days,
                                    "posting_date": today(),
                                    "payout_date": get_last_day(add_months(end_date, 1)),
                                    "payroll_entry": self.name
                                })
                                arrear_doc.insert(ignore_permissions=True)
                                frappe.db.commit()

                    elif payroll_setting.payroll_based_on == "Leave":
                        existing_doc=frappe.db.exists("New Joining Arrear", {
                                "employee": emp.employee,
                                "company": self.company,
                                "payroll_entry": self.name
                            })
                        if not existing_doc:
                            arrear_doc = frappe.get_doc({
                                "doctype": "New Joining Arrear",
                                "employee": emp.employee,
                                "company": self.company,
                                "number_of_present_days": diff_days,
                                "posting_date": today(),
                                "payout_date": get_last_day(add_months(end_date, 1)),
                                "payroll_entry": self.name
                            })
                            arrear_doc.insert(ignore_permissions=True)
                            frappe.db.commit()

                    continue

            valid_employees.append({
                "employee": emp.employee,
                "employee_name": emp.employee_name,
                "department": emp.department,
                "designation": emp.designation,
                "custom_new_joinee": 0,
                "custom_new_joinee_with_salary_arrear": 0
            })

        if not valid_employees:
            error_msg = _(
                "No employees found for the mentioned criteria:<br>Company: {0}<br>Currency: {1}<br>Payroll Payable Account: {2}"
            ).format(
                frappe.bold(self.company),
                frappe.bold(self.currency),
                frappe.bold(self.payroll_payable_account),
            )
            if self.branch:
                error_msg += "<br>" + _("Branch: {0}").format(frappe.bold(self.branch))
            if self.department:
                error_msg += "<br>" + _("Department: {0}").format(frappe.bold(self.department))
            if self.designation:
                error_msg += "<br>" + _("Designation: {0}").format(frappe.bold(self.designation))
            if self.start_date:
                error_msg += "<br>" + _("Start Date: {0}").format(frappe.bold(self.start_date))
            if self.end_date:
                error_msg += "<br>" + _("End Date: {0}").format(frappe.bold(self.end_date))
            if self.custom_employment_type:
                error_msg += "<br>" + _("Employment Type: {0}").format(frappe.bold(self.custom_employment_type))

            frappe.throw(error_msg, title=_("No Employees Found"))

        for emp in valid_employees:
            self.append("employees", emp)

        self.number_of_employees = len(valid_employees)
        self.update_employees_with_withheld_salaries()
        return self.get_employees_with_unmarked_attendance()




def get_filtered_employees_with_employment_type(filters):

    optional_filters = []
    if filters.get("branch"):
        optional_filters.append(["branch", "=", filters.branch])
    if filters.get("department"):
        optional_filters.append(["department", "=", filters.department])
    if filters.get("designation"):
        optional_filters.append(["designation", "=", filters.designation])
    if filters.get("grade"):
        optional_filters.append(["grade", "=", filters.grade])
    if filters.get("employment_type"):
        optional_filters.append(["employment_type", "=", filters.employment_type])


    active_filters = [
        ["company", "=", filters.company],
        ["status", "=", "Active"]
    ] + optional_filters

    active_employees = frappe.get_all(
        "Employee",
        filters=active_filters,
        fields=["name as employee", "employee_name", "department", "designation"]
    )


    left_filters = [
        ["company", "=", filters.company],
        ["status", "=", "Left"],
        ["relieving_date", ">=", filters.start_date],
        # ["relieving_date", "<=", filters.end_date],
    ] + optional_filters

    left_employees = frappe.get_all(
        "Employee",
        filters=left_filters,
        fields=["name as employee", "employee_name", "department", "designation"]
    )

    return active_employees + left_employees
