from frappe.utils import getdate,today,add_months
import datetime

import frappe
from frappe import _
from hrms.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry

class PayrollEntryOverride(PayrollEntry):
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

            custom_new_joinee = 0
            custom_new_joinee_with_salary_arrear=0

            if ssa:
                ssa_doc = ssa[0]
                employee_doc = frappe.get_doc("Employee", emp.employee)
                date_of_joinee = getdate(employee_doc.date_of_joining)

                payroll_setting = frappe.get_doc("Payroll Settings")


                if payroll_setting.payroll_based_on == "Leave" and payroll_setting.custom_configure_attendance_cycle:
                    attendance_end_date = payroll_setting.custom_attendance_end_date
                    start_date = getdate(self.start_date)
                    end_date = getdate(self.end_date)
                    attendance_end_day = int(payroll_setting.custom_attendance_end_date)

                    attendance_final_end_date = datetime.date(end_date.year, end_date.month, attendance_end_day)
                    if start_date <= date_of_joinee <= end_date:
                        custom_new_joinee = 1
                    if attendance_final_end_date< date_of_joinee <= end_date:
                        custom_new_joinee_with_salary_arrear=1

            valid_employees.append({
                "employee": emp.employee,
                "employee_name": emp.employee_name,
                "department": emp.department,
                "designation": emp.designation,
                "custom_new_joinee": custom_new_joinee,
                "custom_new_joinee_with_salary_arrear": custom_new_joinee_with_salary_arrear
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
    # Common optional filters
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

    # Active Employees (no date filter needed)
    active_filters = [
        ["company", "=", filters.company],
        ["status", "=", "Active"]
    ] + optional_filters

    active_employees = frappe.get_all(
        "Employee",
        filters=active_filters,
        fields=["name as employee", "employee_name", "department", "designation"]
    )

    # Left Employees (relieved within date range)
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

@frappe.whitelist()
def create_new_joinee_arrear(company, doc_id, start_date, end_date, employees):

    if isinstance(employees, str):
        employees = frappe.parse_json(employees)

    start_date = getdate(start_date)
    end_date = getdate(end_date)

    additional_salary_date = add_months(end_date, 1)

    if employees:
        payroll_setting = frappe.get_doc("Payroll Settings")
        if payroll_setting.payroll_based_on == "Leave" and payroll_setting.custom_configure_attendance_cycle:
            for emp in employees:
                if emp.get("custom_new_joinee_with_salary_arrear"):
                    ssa = frappe.get_all(
                        "Salary Structure Assignment",
                        filters={
                            "employee": emp.get("employee"),
                            "docstatus": 1,
                            "from_date": ["<=", end_date],
                        },
                        fields=["name", "from_date", "salary_structure"],
                        order_by="from_date desc",
                        limit=1,
                    )

                    if ssa:
                        ssa_doc = ssa[0]
                        emp_doc = frappe.get_doc("Employee", emp["employee"])
                        date_of_joining = getdate(emp_doc.date_of_joining)

                        # Total days between DOJ and end_date (inclusive)
                        days_diff = (end_date - date_of_joining).days + 1

                        present_day = 0
                        absent_day = 0
                        half_day = 0
                        work_from_home = 0

                        # Fetch attendance between joining date and end_date
                        attendance_records = frappe.get_all(
                            "Attendance",
                            filters={
                                "employee": emp.get("employee"),
                                "attendance_date": ["between", (date_of_joining, end_date)],
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
                                get_leave_type = frappe.get_doc("Leave Type", leave_type)
                                if get_leave_type.is_lwp:
                                    half_day += 0.5
                                else:
                                    present_day += 1

                            elif status == "Half Day" and not leave_type:
                                half_day += 1

                            elif status == "On Leave" and leave_type:
                                get_leave_type = frappe.get_doc("Leave Type", leave_type)
                                if get_leave_type.is_lwp:
                                    absent_day += 1
                                else:
                                    present_day += 1

                            elif status == "Work From Home":
                                work_from_home += 1

                        total_lop_days = absent_day + half_day
                        total_payment_days = days_diff - total_lop_days

                        if total_payment_days > 0:
                            # Create new arrear record
                            arrear_doc = frappe.get_doc({
                                "doctype": "New Joining Arrear",
                                "employee": emp.get("employee"),
                                "company": company,

                                "number_of_present_days": total_payment_days,

                                "posting_date": today(),
                                "payout_date": additional_salary_date,
                            })
                            arrear_doc.insert(ignore_permissions=True)
                            arrear_doc.submit()
                            frappe.db.commit()
                        get_payroll=frappe.get_doc("Payroll Entry",doc_id)
                        for d in get_payroll.employees:
                            if d.employee == emp.get("employee"):
                                get_payroll.remove(d)
                                break

                        get_payroll.custom_salary_arrear_created = 1
                        get_payroll.save(ignore_permissions=True)
                        frappe.db.commit()

    return total_payment_days
