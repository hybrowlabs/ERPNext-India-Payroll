from frappe.utils import getdate,today,add_months,get_last_day
import datetime

import frappe
from frappe import _
from hrms.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry
# from datetime import datetime
import datetime
from frappe.utils import getdate, add_months


class PayrollEntryOverride(PayrollEntry):

    def on_submit(self):
        super().on_submit()
        self.submit_new_joinee_arrear()

    def on_cancel(self):
        super().on_cancel()
        self.cancel_new_joinee_arrear()

    def cancel_new_joinee_arrear(self):
        joinee_arrear=frappe.get_all("New Joining Arrear",filters={"payroll_entry":self.name,"docstatus":1})
        if joinee_arrear:
            for doc in joinee_arrear:
                doc=frappe.get_doc("New Joining Arrear",doc.name)
                doc.cancel()
                frappe.db.commit()


    def submit_new_joinee_arrear(self):
        joinee_arrear=frappe.get_all("New Joining Arrear",filters={"payroll_entry":self.name,"docstatus":0})
        if joinee_arrear:
            for doc in joinee_arrear:
                doc=frappe.get_doc("New Joining Arrear",doc.name)
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

            salary_structure_assignment=ssa[0].name

            if payroll_setting.custom_configure_attendance_cycle:
                attendance_end_day = int(payroll_setting.custom_attendance_end_date)
                attendance_start_day = int(payroll_setting.custom_attendance_start_date)

                attendance_final_end_date = datetime.date(end_date.year, end_date.month, attendance_end_day)
                next_month_end_date = get_last_day(add_months(end_date, 1))
                next_month_attendance_end_date = datetime.date(next_month_end_date.year, next_month_end_date.month, attendance_start_day)
                diff_days = (next_month_end_date - next_month_attendance_end_date).days + 1


                print(attendance_final_end_date, date_of_joinee, end_date)

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
                                    "payroll_entry": self.name,
                                    "salary_structure_assignment":salary_structure_assignment
                                })
                                arrear_doc.insert(ignore_permissions=True)
                                frappe.db.commit()

                    elif payroll_setting.payroll_based_on == "Leave":
                        existing_doc=frappe.db.exists("New Joining Arrear", {
                                "employee": emp.employee,
                                "company": self.company,
                                "payroll_entry": self.name,

                            })
                        if not existing_doc:
                            arrear_doc = frappe.get_doc({
                                "doctype": "New Joining Arrear",
                                "employee": emp.employee,
                                "company": self.company,
                                "number_of_present_days": diff_days,
                                "posting_date": today(),
                                "payout_date": get_last_day(add_months(end_date, 1)),
                                "payroll_entry": self.name,
                                "salary_structure_assignment":salary_structure_assignment
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


        if valid_employees:


            self.set("custom_employee_attendance_details_list", [])


            payroll_setting = frappe.get_doc("Payroll Settings")

            start_date = getdate(self.start_date)   # 2026-01-01
            end_date = getdate(self.end_date)       # 2026-01-31

            total_days = (end_date - start_date).days + 1

            attendance_start_day = int(payroll_setting.custom_attendance_start_date)  # 21
            attendance_end_day = int(payroll_setting.custom_attendance_end_date)      # 20


            attendance_start_date = datetime.date(
                start_date.year,
                start_date.month,
                attendance_start_day
            )
            attendance_start_date = add_months(attendance_start_date, -1)


            attendance_end_date = datetime.date(
                end_date.year,
                end_date.month,
                attendance_end_day
            )

            self.custom_attendance_from_date=attendance_start_date
            self.custom_attendance_to_date=attendance_end_date

            for emp in valid_employees:

                present_days = 0
                absent_days = 0
                lwp_days = 0
                half_days = 0
                on_leave=0

                attendance_records = frappe.get_all(
                    "Attendance",
                    filters={
                        "employee": emp["employee"],
                        "company": self.company,
                        "attendance_date": ["between", [attendance_start_date, attendance_end_date]],
                        "docstatus": 1
                    },
                    fields=["status", "leave_type"]
                )

                for att in attendance_records:
                    status = att.status
                    leave_type = att.leave_type

                    if status == "Present":
                        present_days += 1

                    elif status == "Absent":
                        absent_days += 1

                    elif status == "Half Day":
                        half_days += 0.5
                        if leave_type:
                            leave = frappe.get_doc("Leave Type", leave_type)
                            if leave.is_lwp:
                                lwp_days += 0.5

                    elif status == "On Leave" and leave_type:
                        leave = frappe.get_doc("Leave Type", leave_type)
                        if leave.is_lwp:
                            lwp_days += 1
                        else:
                            on_leave += 1

                    elif status == "Work From Home":
                        present_days += 1






                self.append("custom_employee_attendance_details_list", {
                "employee": emp["employee"],
                "working_days":total_days,
                "attendance_from_date": attendance_start_date,
                "attendance_to_date": attendance_end_date,
                "present_days": present_days,
                "absent_days": absent_days,
                "lwp_days": lwp_days,
                "half_days": half_days,
                "on_leave":on_leave,
                "total_lwf_days":lwp_days + absent_days,
                "payment_days":total_days-(lwp_days + absent_days)
                })






            employee_list = [e["employee"] for e in valid_employees]






            self.set("custom_attendance_regularize_child", [])
            self.set("custom_new_joinee_arrear_child", [])


            attendance_logs = frappe.get_all(
                "Attendance Log",
                filters={
                    "employee": ["in", employee_list],
                    "company": self.company,
                    "additional_salary_date": ["between", [self.start_date, self.end_date]],
                    "docstatus": 1,
                },
                fields=["name"]
            )

            for log in attendance_logs:
                log_doc = frappe.get_doc("Attendance Log", log.name)

                for wd in log_doc.attendance_log_working_days:
                    if wd.arrear_days>0:
                        # month_name = datetime.strptime(wd.month, "%b-%Y").strftime("%B")
                        self.append("custom_attendance_regularize_child", {
                            "employee": log_doc.employee,
                            "attendance_log": log_doc.name,
                            "additional_salary_date": log_doc.additional_salary_date,
                            "working_days": wd.working_days,
                            "arrear_days": wd.arrear_days,
                            "month_and_year": wd.month_and_year,
                            "month": wd.month,
                            "payroll_period": log_doc.payroll_period,
                            "salary_slip":wd.salary_slip
                        })

            new_joinee=frappe.get_all(
                "New Joining Arrear",
                filters={
                    "employee": ["in", employee_list],
                    "company": self.company,
                    "payout_date": ["between", [self.start_date, self.end_date]],
                    "docstatus":1
                },
                fields=["name","employee"]
            )

            for arrear in new_joinee:
                arrear_doc = frappe.get_doc("New Joining Arrear", arrear.name)
                self.append("custom_new_joinee_arrear_child", {
                    "employee": arrear_doc.employee,
                    "working_days": arrear_doc.working_days,
                    "arrear_days": arrear_doc.number_of_present_days,
                    "new_joining_arrear_id": arrear_doc.name,
                    "date_of_joining": arrear_doc.joining_date,
                    "total_earning_arrear": arrear_doc.total_earning,
                    "total_deduction_arrear": arrear_doc.total_deductions,
                    "total_benefit": arrear_doc.total_benefits,
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
