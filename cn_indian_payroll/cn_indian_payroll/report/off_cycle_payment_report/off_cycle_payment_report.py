# Copyright (c) 2025, Hybrowlabs Technologies
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns = get_columns()
	data = get_all_offcycle(filters)
	return columns, data

def get_all_offcycle(filters=None):
	if filters is None:
		filters = {}

	conditions = {"docstatus": ["in", [0, 1]]}

	if filters.get("employee"):
		conditions["employee"] = filters["employee"]
	if filters.get("payroll_period"):
		conditions["custom_payroll_period"] = filters["payroll_period"]
	if filters.get("month"):
		conditions["custom_month"] = filters["month"]
	if filters.get("company"):
		conditions["company"] = filters["company"]

	data = []

	salary_slips = frappe.get_all(
		"Salary Slip",
		filters=conditions,
		fields=[
			"*"
		]
	)

	for slip in salary_slips:
		slip_doc = frappe.get_doc("Salary Slip", slip.name)
		employee_doc = frappe.get_doc("Employee", slip.employee)

		component=None
		gross_earning=0
		tds=0

		for earning in slip_doc.earnings:
			salary_component_doc = frappe.get_doc("Salary Component", earning.salary_component)

			if salary_component_doc.custom_is_offcycle_component:
				component = salary_component_doc.name
				gross_earning=earning.amount
				tds=slip_doc.custom_offcycle_tds_deducted_value

			

		if component:
			data.append({
				"salary_slip": slip.name,
				"employee": slip.employee,
				"employee_name": slip.employee_name,
				"department":employee_doc.department,
				"designation":employee_doc.designation,
				"date_of_joining":employee_doc.date_of_joining,
				"department_cost_center":"",
				"work_location":employee_doc.branch,
				"bank_name":employee_doc.bank_name,
				"bank_acc_no":employee_doc.bank_ac_no,
				"ifsc":employee_doc.ifsc_code,
				"pan":employee_doc.pan_number,	
				"cost_center":"",			
				
				"working_days": slip.total_working_days,
				"total_lwp": slip.custom_total_leave_without_pay,
				"payment_day": slip.payment_days,

				"component": component,
				"gross_earning":gross_earning,
				"tds":tds,
				"net_pay":round(gross_earning-tds)
			})

	return data

def get_columns():
	return [
		{"label": "Salary Slip", "fieldname": "salary_slip", "fieldtype": "Link", "options": "Salary Slip", "width": 150},
		{"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 150},
		{"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},

		{"label": "Department", "fieldname": "department", "fieldtype": "Data", "width": 180},
		{"label": "Designation", "fieldname": "designation", "fieldtype": "Data", "width": 180},

		{"label": "Work Location", "fieldname": "work_location", "fieldtype": "Data", "width": 180},

		{"label": "Date Of Joining", "fieldname": "date_of_joining", "fieldtype": "Data", "width": 180},

		{"label": "Department Cost Center", "fieldname": "department_cost_center", "fieldtype": "Data", "width": 180},




		{"label": "Bank Name", "fieldname": "bank_name", "fieldtype": "Data", "width": 180},
		{"label": "Account Number", "fieldname": "bank_acc_no", "fieldtype": "Data", "width": 180},
		{"label": "IFSC", "fieldname": "ifsc", "fieldtype": "Data", "width": 180},
		{"label": "PAN", "fieldname": "pan", "fieldtype": "Data", "width": 180},

		{"label": "Cost Center", "fieldname": "cost_center", "fieldtype": "Data", "width": 180},


		{"label": "Working Days", "fieldname": "working_days", "fieldtype": "Float", "width": 120},
		{"label": "LWP Days", "fieldname": "total_lwp", "fieldtype": "Float", "width": 120},
		{"label": "Payment Days", "fieldname": "payment_day", "fieldtype": "Float", "width": 120},
		{"label": "Component", "fieldname": "component", "fieldtype": "Data", "width": 200},
		{"label": "Gross Earning", "fieldname": "gross_earning", "fieldtype": "Currency", "width": 200},

		{"label": "TDS", "fieldname": "tds", "fieldtype": "Currency", "width": 200},

		{"label": "Total Deduction", "fieldname": "tds", "fieldtype": "Currency", "width": 200},
		{"label": "Net Pay", "fieldname": "net_pay", "fieldtype": "Currency", "width": 200},
		{"label": "Total Pay", "fieldname": "net_pay", "fieldtype": "Currency", "width": 200},

	]
