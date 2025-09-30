# import frappe
# from frappe.utils import (
# 	add_days,
# 	ceil,
# 	cint,
# 	cstr,
# 	date_diff,
# 	floor,
# 	flt,
# 	formatdate,
# 	get_first_day,
# 	get_link_to_form,
# 	getdate,
# 	money_in_words,
# 	rounded,
# )



# def validate(self,method):
#     if self.custom_status=="Approved" and self.from_date and self.to_date:
#         payroll_setting=frappe.get_doc("Payroll Settings")
#         if payroll_setting.custom_configure_attendance_cycle:
#             attendance_start_day=payroll_setting.custom_attendance_start_date
#             attendance_end_day=payroll_setting.custom_attendance_end_date


#             start_date=getdate(self.from_date)
#             end_date=getdate(self.to_date)


#             attendance_start_date = start_date.replace(day=attendance_start_day)
#             attendance_end_date = end_date.replace(day=attendance_end_day)


#             frappe.msgprint(str(attendance_start_date))
#             frappe.msgprint(str(attendance_end_date))

#             days_including_start = date_diff(end_date, start_date)+1

#             frappe.msgprint(str(days_including_start))

#             # if start_date and end_date between  attendance_start_date and attendance_end_date



#             # attendance_start_date = (attendance_end_date - relativedelta(months=1)).replace(day=attendance_start_day)
