
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

            if ssa:
                valid_employees.append({
                    "employee": emp.employee,
                    "employee_name": emp.employee_name,
                    "department": emp.department,
                    "designation": emp.designation
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
