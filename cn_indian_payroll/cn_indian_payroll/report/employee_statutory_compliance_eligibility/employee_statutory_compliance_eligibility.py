import frappe

def execute(filters=None):
	columns = get_columns()
	data = get_all_employee(filters)
	return columns, data


def get_all_employee(filters=None):
	if filters is None:
		filters = {}

	conditions = {}

	if filters.get("employee"):
		conditions["name"] = filters["employee"]

	if filters.get("company"):
		conditions["company"] = filters["company"]

	data = []

	employees = frappe.get_all(
		"Employee",
		filters=conditions,
		fields=[
			"name",
			"employee_name",
			"company",
			"department",
			"designation",
			"employment_type",
			"branch"
		]
	)

	for emp in employees:
		latest_salary_structure = frappe.get_list(
			'Salary Structure Assignment',
			filters={'employee': emp.name, 'docstatus': 1},
			fields=["custom_is_epf", "custom_epf_type"],
			order_by='from_date desc',
			limit=1
		)

		pf_eligible = "Yes" if latest_salary_structure and latest_salary_structure[0].get("custom_is_epf") else "No"
		pf_type = latest_salary_structure[0].get("custom_epf_type") if latest_salary_structure and latest_salary_structure[0].get("custom_is_epf") else None

		data.append({
			"employee": emp.name,
			"employee_name": emp.employee_name,
			"company": emp.company,
			"department": emp.department,
			"designation": emp.designation,
			"employment_type": emp.employment_type,
			"branch": emp.branch,
			"pf_eligible": pf_eligible,
			"pf_type": pf_type,
			# "pan":emp.
			# "uan":
			# "pf_number":

		})

	return data


def get_columns():
	return [
		{"label": "Employee ID", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 150},
		{"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
		{"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
		{"label": "Department", "fieldname": "department", "fieldtype": "Link", "options": "Department", "width": 150},
		{"label": "Designation", "fieldname": "designation", "fieldtype": "Link", "options": "Designation", "width": 150},
		{"label": "Employment Type", "fieldname": "employment_type", "fieldtype": "Data", "width": 150},
		{"label": "Branch", "fieldname": "branch", "fieldtype": "Link", "options": "Branch", "width": 150},

		{"label": "PF Eligible", "fieldname": "pf_eligible", "fieldtype": "Data", "width": 120},
		{"label": "PF Type", "fieldname": "pf_type", "fieldtype": "Data", "width": 150},
		{"label": "PAN Number", "fieldname": "pan", "fieldtype": "Data", "width": 150},
		{"label": "UAN Number", "fieldname": "uan", "fieldtype": "Data", "width": 150},
		{"label": "PF Number", "fieldname": "pf_number", "fieldtype": "Data", "width": 150},
		{"label": "PF Enrollment Status", "fieldname": "pf_enrolment_status", "fieldtype": "Data", "width": 150},

		{"label": "ESIC Eligible", "fieldname": "esic_eligible", "fieldtype": "Data", "width": 120},
		{"label": "ESIC Number", "fieldname": "esic_number", "fieldtype": "Data", "width": 150},
		{"label": "ESIC Enrollment Status", "fieldname": "esic_enrollment_status", "fieldtype": "Data", "width": 150},

		{"label": "PT Applicable", "fieldname": "pt_eligible", "fieldtype": "Data", "width": 120},
		{"label": "PT State", "fieldname": "pt_state", "fieldtype": "Data", "width": 120},


		{"label": "LWF Applicable", "fieldname": "lwf_eligible", "fieldtype": "Data", "width": 120},
		{"label": "LWF State", "fieldname": "lwf_state", "fieldtype": "Data", "width": 120},
		{"label": "LWF Frequency", "fieldname": "lwf_frequency", "fieldtype": "Data", "width": 120},

		{"label": "NPS Applicable", "fieldname": "nps_eligible", "fieldtype": "Data", "width": 120},
		{"label": "NPS Percentage", "fieldname": "nps_percentage", "fieldtype": "Data", "width": 120},




	]
