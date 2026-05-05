import frappe

def execute(filters=None):
	columns = get_columns()
	data = get_all_extra_payment(filters)
	return columns, data


def get_all_extra_payment(filters=None):
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
			"name", "employee", "employee_name", "company",
			"custom_payroll_period", "custom_month",
			"total_working_days", "custom_total_leave_without_pay",
			"payment_days"
		]
	)

	for slip in salary_slips:

		extra_payment_amount = 0
		extra_payment_component = None

		effect_lop = "No"
		is_off_cycle = "No"
		offcycle_tds_auto_calculate = "No"
		offcycle_tds_non_taxable = "No"

		clockback_date = None
		created_by = None
		created_on = None

		slip_doc = frappe.get_doc("Salary Slip", slip.name)
		employee_doc = frappe.get_doc("Employee", slip.employee)

		for earning in slip_doc.earnings:

			salary_component_doc = frappe.get_doc(
				"Salary Component", earning.salary_component
			)

			if salary_component_doc.custom_is_extra_payment:

				extra_payment_amount += earning.amount
				extra_payment_component = salary_component_doc.name

				if earning.custom_is_tax_manual_calculate or earning.deduct_full_tax_on_selected_payroll_date:
					is_off_cycle = "Yes"
					offcycle_tds_auto_calculate = "Yes"

				if earning.additional_salary:
					add_sal = frappe.get_doc("Additional Salary", earning.additional_salary)

					clockback_date = add_sal.custom_clockback_date
					created_on = add_sal.creation

					user = add_sal.owner

					employee = frappe.db.get_value(
						"Employee",
						{"user_id": user},
						["name", "employee_name"],
						as_dict=True
					)

					if employee:
						created_by = f"{employee.name} - {employee.employee_name}"
					else:
						created_by = user

					start_date=add_sal.payroll_date
					end_date=add_sal.payroll_date
			if salary_component_doc.depends_on_payment_days:
				effect_lop = "Yes"

			if not salary_component_doc.is_tax_applicable:
				offcycle_tds_non_taxable = "Yes"

		if extra_payment_amount > 0:
			data.append({
				"salary_slip": slip.name,
				"employee": slip.employee,
				"employee_name": slip.employee_name,
				"department": employee_doc.department,
				"designation": employee_doc.designation,
				"branch": employee_doc.branch,
				"company": slip.company,
				"payroll_period": slip.custom_payroll_period,
				"month": slip.custom_month,
				"working_days": slip.total_working_days,
				"total_lwp": slip.custom_total_leave_without_pay,
				"payment_day": slip.payment_days,

				"extrapayment_type": "Fixed",
				"extrapayment_name": extra_payment_component,
				"category": extra_payment_component,

				"currency": "INR",
				"total_amount": extra_payment_amount,
				"unit": "Amount",
				"amount": extra_payment_amount,

				"no_of_payments": 1,
				"payment_frequency": "One-time",
				"tax_frequency": "One-Time",

				"impact_lop": effect_lop,
				"calculate_esic": "No",
				"calculate_pf": "No",
				"calculate_lwf": "No",
				"calculate_pt": "No",

				"is_off_cycle": is_off_cycle,
				"offcycle_tds_auto_calculate": offcycle_tds_auto_calculate,
				"offcycle_tds": slip_doc.custom_extra_payment_tds_deducted_value,
				"offcycle_tds_non_taxable": offcycle_tds_non_taxable,

				"reimbursement": 0,

				"clockback_date": clockback_date,
				"created_by": created_by,
				"created_on": created_on,
				"updated_by": None,
				"updated_on": None,

				"start_date": start_date,
				"end_date": end_date,
			})

	return data

def get_columns():
	return [

		{"label": "Salary Slip", "fieldname": "salary_slip", "fieldtype": "Link", "options": "Salary Slip", "width": 150},
		{"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 140},
		{"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
		{"label": "Department", "fieldname": "department", "fieldtype": "Link", "options": "Department", "width": 140},
		{"label": "Designation", "fieldname": "designation", "fieldtype": "Link", "options": "Designation", "width": 140},
		{"label": "Branch", "fieldname": "branch", "fieldtype": "Link", "options": "Branch", "width": 140},

		{"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 140},
		{"label": "Payroll Period", "fieldname": "payroll_period", "fieldtype": "Link", "options": "Payroll Period", "width": 150},
		{"label": "Month", "fieldname": "month", "fieldtype": "Data", "width": 100},

		{"label": "Working Days", "fieldname": "working_days", "fieldtype": "Float", "width": 120},
		{"label": "LWP Days", "fieldname": "total_lwp", "fieldtype": "Float", "width": 120},
		{"label": "Payment Days", "fieldname": "payment_day", "fieldtype": "Float", "width": 120},

		{"label": "Extra Payment Type", "fieldname": "extrapayment_type", "fieldtype": "Data", "width": 150},
		{"label": "Extra Payment Name", "fieldname": "extrapayment_name", "fieldtype": "Data", "width": 180},
		{"label": "Category", "fieldname": "category", "fieldtype": "Data", "width": 150},

		{"label": "Currency", "fieldname": "currency", "fieldtype": "Data", "width": 100},
		{"label": "Total Amount", "fieldname": "total_amount", "fieldtype": "Currency", "width": 140},
		{"label": "Unit", "fieldname": "unit", "fieldtype": "Data", "width": 100},
		{"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 120},

		{"label": "No of Payments", "fieldname": "no_of_payments", "fieldtype": "Int", "width": 140},
		{"label": "Payment Frequency", "fieldname": "payment_frequency", "fieldtype": "Data", "width": 160},
		{"label": "Tax Frequency", "fieldname": "tax_frequency", "fieldtype": "Data", "width": 150},

		{"label": "Impact LOP", "fieldname": "impact_lop", "fieldtype": "Data", "width": 120},
		{"label": "ESIC", "fieldname": "calculate_esic", "fieldtype": "Data", "width": 100},
		{"label": "PF", "fieldname": "calculate_pf", "fieldtype": "Data", "width": 100},
		{"label": "LWF", "fieldname": "calculate_lwf", "fieldtype": "Data", "width": 100},
		{"label": "PT", "fieldname": "calculate_pt", "fieldtype": "Data", "width": 100},

		{"label": "Is Off Cycle", "fieldname": "is_off_cycle", "fieldtype": "Data", "width": 120},
		{"label": "TDS Auto Calculate", "fieldname": "offcycle_tds_auto_calculate", "fieldtype": "Data", "width": 180},
		{"label": "TDS", "fieldname": "offcycle_tds", "fieldtype": "Data", "width": 120},
		{"label": "TDS Non Taxable", "fieldname": "offcycle_tds_non_taxable", "fieldtype": "Data", "width": 180},

		{"label": "Reimbursement", "fieldname": "reimbursement", "fieldtype": "Float", "width": 120},

		{"label": "Clockback Date", "fieldname": "clockback_date", "fieldtype": "Date", "width": 140},
		{"label": "Created By", "fieldname": "created_by", "fieldtype": "Data", "width": 150},
		{"label": "Created On", "fieldname": "created_on", "fieldtype": "Datetime", "width": 180},
		{"label": "Updated By", "fieldname": "updated_by", "fieldtype": "Data", "width": 150},
		{"label": "Updated On", "fieldname": "updated_on", "fieldtype": "Datetime", "width": 180},

		{"label": "Start Date", "fieldname": "start_date", "fieldtype": "Date", "width": 140},
		{"label": "End Date", "fieldname": "end_date", "fieldtype": "Date", "width": 140},
	]
