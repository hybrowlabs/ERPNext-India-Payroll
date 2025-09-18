# Copyright (c) 2025, Hybrowlabs Technologies
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_all_net_pay(filters)
    return columns, data

def get_all_net_pay(filters=None):
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
    if filters.get("custom_employment_type"):
        conditions["custom_employment_type"] = filters["custom_employment_type"]

    data = []

    salary_slips = frappe.get_all(
        "Salary Slip",
        filters=conditions,
        fields=[
            "name", "employee", "employee_name", "company",
            "custom_payroll_period", "custom_month", "net_pay","custom_employment_type","payroll_entry","custom_net_pay_amount"
        ]
    )

    for slip in salary_slips:
        employee_doc = frappe.get_doc("Employee", slip.employee)

        payroll_entry=frappe.get_doc("Payroll Entry",slip.payroll_entry)



        address = frappe.get_all(
            "Address",
            filters={"custom_employee": employee_doc.name},
            fields=["address_line1", "address_line2", "city", "state", "pincode"]
        )

        address_detail = ""
        if address:
            addr = address[0]
            address_detail = f"{addr.address_line1}"

        data.append({
            "account_number":payroll_entry.custom_debit_account_number,
            "b_account_number": employee_doc.bank_ac_no,
            "employee_name": slip.employee_name,
            "net_pay": slip.custom_net_pay_amount,
            "pay_mode":payroll_entry.custom_pay_mode,
            "payment_instruction_date":payroll_entry.custom_payment_date,

            "ifsc_code": employee_doc.ifsc_code,
            "bene_mobile_no": employee_doc.cell_number,
            "bene_email_id": employee_doc.personal_email,
            "address_detail": address_detail,

            "remark":employee_doc.name,
            "credit_narration":payroll_entry.custom_credit_narration

        })


    return data

def get_columns():
    return [
        # {"label": "Salary Slip", "fieldname": "salary_slip", "fieldtype": "Link", "options": "Salary Slip", "width": 150},
        {"label": "Debit Ac No", "fieldname": "account_number", "fieldtype": "Data", "width": 150},
        {"label": "Beneficiary Ac No", "fieldname": "b_account_number", "fieldtype": "Int", "width": 150},
        {"label": "Beneficiary Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
        {"label": "Amt", "fieldname": "net_pay", "fieldtype": "Currency", "width": 200},
        {"label": "Pay Mod", "fieldname": "pay_mode", "fieldtype": "Data", "width": 180},
        {"label": "Payment_Instruction_Date", "fieldname": "payment_instruction_date", "fieldtype": "Data", "width": 180},
        {"label": "IFSC Code", "fieldname": "ifsc_code", "fieldtype": "Data", "width": 150},

        {"label": "Bene Mobile No", "fieldname": "bene_mobile_no", "fieldtype": "Data", "width": 150},
        {"label": "Bene email id", "fieldname": "bene_email_id", "fieldtype": "Data", "width": 150},
        {"label": "Add details 1", "fieldname": "address_detail", "fieldtype": "Data", "width": 150},
        {"label": "Remarks", "fieldname": "remark", "fieldtype": "Data", "width": 150},

        {"label": "Credit_Narration ", "fieldname": "credit_narration", "fieldtype": "Data",  "width": 150},
    ]
