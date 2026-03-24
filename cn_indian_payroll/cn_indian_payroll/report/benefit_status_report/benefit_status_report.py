import frappe

def execute(filters=None):
	columns = get_columns()
	data = get_all_benefit(filters)
	return columns, data


def get_all_benefit(filters=None):
	if filters is None:
		filters = {}

	conditions = {"docstatus": ["in", [0, 1]]}

	if filters.get("employee"):
		conditions["employee"] = filters["employee"]

	if filters.get("payroll_period"):
		conditions["custom_payroll_period"] = filters["payroll_period"]

	if filters.get("status") and filters.get("status") != "All":
		conditions["custom_status"] = filters["status"]

	if filters.get("company"):
		conditions["company"] = filters["company"]

	data = []

	claims = frappe.get_all(
		"Employee Benefit Claim",
		filters=conditions,
		fields=["name"]
	)

	for claim in claims:

		claim_doc = frappe.get_doc("Employee Benefit Claim", claim.name)
		employee_doc = frappe.get_doc("Employee", claim_doc.employee)

		employee_map = {
			d.user_id: (d.name, d.employee_name)
			for d in frappe.get_all(
				"Employee",
				filters={"user_id": ["!=", ""]},
				fields=["name", "employee_name", "user_id"]
			)
		}

		emp = employee_map.get(claim_doc.owner)

		if emp:
			created_by_value = f"{emp[0]} ({emp[1]})"
		else:
			created_by_value = claim_doc.owner

		data.append({
			"emp_id": claim_doc.employee,
			"employee_name": claim_doc.employee_name,
			"designation": employee_doc.designation,
			"department": employee_doc.department,
			"flexi_component": claim_doc.earning_component,

			"status": claim_doc.custom_status,
			"expense_claim_date": claim_doc.claim_date,

			"currency": claim_doc.currency,
			"bill_amount": claim_doc.claimed_amount,
			"invoice_number": claim_doc.name,

			"user_comments": claim_doc.custom_note_by_employee,
			"attachment": "Yes" if claim_doc.attachments else "No",

			"approved_amount": claim_doc.custom_paid_amount,
			"approver_comments": "",

			"taxable_amount": claim_doc.custom_taxable_amount,
			"non_taxable_amount": claim_doc.custom_non_taxable_amount,

			"payout_month": claim_doc.claim_date,
			"last_action_date": claim_doc.modified,

			"approver_name": created_by_value,
			"approved_on": claim_doc.creation
		})

	return data



def get_columns():
	return [

		{"label": "EMP ID", "fieldname": "emp_id", "fieldtype": "Link", "options": "Employee", "width": 140},
		{"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
		{"label": "Designation", "fieldname": "designation", "fieldtype": "Data", "width": 150},
		{"label": "Department", "fieldname": "department", "fieldtype": "Link", "options": "Department", "width": 150},

		{"label": "Flexi Component", "fieldname": "flexi_component", "fieldtype": "Data", "width": 180},

		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
		{"label": "Expense Claim Date", "fieldname": "expense_claim_date", "fieldtype": "Date", "width": 150},

		{"label": "Currency", "fieldname": "currency", "fieldtype": "Data", "width": 100},
		{"label": "Bill Amount", "fieldname": "bill_amount", "fieldtype": "Currency", "width": 130},

		{"label": "Invoice Number", "fieldname": "invoice_number", "fieldtype": "Data", "width": 150},

		{"label": "User Comments", "fieldname": "user_comments", "fieldtype": "Data", "width": 200},
		{"label": "Attachment", "fieldname": "attachment", "fieldtype": "Data", "width": 150},

		{"label": "Approved Amount", "fieldname": "approved_amount", "fieldtype": "Currency", "width": 150},
		{"label": "Approver Comments", "fieldname": "approver_comments", "fieldtype": "Data", "width": 200},

		{"label": "Taxable Amount", "fieldname": "taxable_amount", "fieldtype": "Currency", "width": 150},
		{"label": "Non Taxable Amount", "fieldname": "non_taxable_amount", "fieldtype": "Currency", "width": 180},

		{"label": "Payout Date", "fieldname": "payout_month", "fieldtype": "Data", "width": 130},

		{"label": "Last Action Date", "fieldname": "last_action_date", "fieldtype": "Datetime", "width": 180},

		{"label": "Approver Name", "fieldname": "approver_name", "fieldtype": "Data", "width": 150},
		{"label": "Approved On", "fieldname": "approved_on", "fieldtype": "Datetime", "width": 180},

	]