
import frappe
from frappe.utils import getdate
from dateutil.relativedelta import relativedelta

def on_update_after_submit(self, method):
    insert_lop_reversal(self)

def insert_lop_reversal(self):
    attendance_date = getdate(self.attendance_date)

    if self.status == "Present" or (self.status == "Half Day" and is_half_day_lwp(self)):
        # Check for existing LOP Reversal
        if not frappe.get_list("LOP Reversal", filters={"date": attendance_date, "docstatus": 1}):
            # Get latest salary slip
            additional_salary_date = get_additional_salary_date(self.employee, self.company)

            # Get matching salary slip for the attendance date
            salary_slip = get_salary_slip_for_date(self.employee, self.company, attendance_date)

            if salary_slip:
                reversal = frappe.get_doc({
                    "doctype": "LOP Reversal",
                    "salary_slip": salary_slip.name,
                    "employee": self.employee,
                    "payroll_period": salary_slip.custom_payroll_period,
                    "company": self.company,
                    "lop_month_reversal": salary_slip.custom_month,
                    "additional_salary_date": additional_salary_date,
                    "number_of_days": 1 if self.status == "Present" else 0.5,
                    "date": attendance_date,
                    "absent_days": salary_slip.absent_days,
                    "lop_days": salary_slip.leave_without_pay,
                    "max_lop_days": salary_slip.custom_total_leave_without_pay
                })
                reversal.insert()
                reversal.submit()
                frappe.db.commit()

def is_half_day_lwp(self):
    if self.leave_type:
        leave_type_doc = frappe.get_doc("Leave Type", self.leave_type)
        return leave_type_doc.is_lwp == 1
    return False

def get_additional_salary_date(employee, company):
    latest_slip = frappe.get_list(
        "Salary Slip",
        filters={
            "employee": employee,
            "company": company,
            "docstatus": 1
        },
        fields=["start_date"],
        limit=1,
        order_by="start_date desc"
    )
    if latest_slip:
        latest_start_date = getdate(latest_slip[0].start_date)
        return latest_start_date + relativedelta(months=1)
    return None

def get_salary_slip_for_date(employee, company, date):
    salary_slips = frappe.get_list(
        "Salary Slip",
        filters={
            "employee": employee,
            "start_date": ["<=", date],
            "end_date": [">=", date],
            "docstatus": 1,
            "company": company
        },
        fields=["*"]
    )
    return salary_slips[0] if salary_slips else None
