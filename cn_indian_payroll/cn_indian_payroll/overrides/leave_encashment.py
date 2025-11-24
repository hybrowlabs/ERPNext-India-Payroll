import frappe

from hrms.hr.doctype.leave_encashment.leave_encashment import LeaveEncashment
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip


class CustomLeaveEncashment(LeaveEncashment):
    def create_additional_salary(self):
        pass
