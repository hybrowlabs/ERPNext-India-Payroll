import frappe
from openpyxl import Workbook, load_workbook
from frappe.utils.file_manager import save_file, get_file


@frappe.whitelist()
def download_additional_salary_template():
    wb = Workbook()
    ws = wb.active
    ws.title = "Additional Salary"

    headers = [
        "employee",
        "salary_component",
        "amount",
        "payroll_date",

    ]

    ws.append(headers)

    file_name = "Additional_Salary_Template.xlsx"
    file_path = f"/tmp/{file_name}"
    wb.save(file_path)

    with open(file_path, "rb") as f:
        file_doc = save_file(
            file_name,
            f.read(),
            None,
            None,
            is_private=0
        )

    return file_doc.file_url

import frappe
from openpyxl import load_workbook
from frappe.utils.file_manager import get_file
from io import BytesIO
import os


@frappe.whitelist()
def process_uploaded_excel(payroll_entry):
    payroll_doc = frappe.get_doc("Payroll Entry", payroll_entry)

    if not payroll_doc.custom_upload_file:
        frappe.throw("Please upload an Excel (.xlsx) file")

    file_name, file_content = get_file(payroll_doc.custom_upload_file)

    # Validate extension
    if not file_name.lower().endswith(".xlsx"):
        frappe.throw("Invalid file format. Please upload .xlsx file only")

    # ---- LOAD WORKBOOK SAFELY ----
    if isinstance(file_content, bytes):
        # File stored in DB / remote
        wb = load_workbook(filename=BytesIO(file_content), data_only=True)
    else:
        # File stored locally (path)
        wb = load_workbook(filename=file_content, data_only=True)

    ws = wb.active

    headers = [cell.value for cell in ws[1]]
    required_headers = {
        "employee",
        "salary_component",
        "amount",
        "payroll_date",

    }

    if not required_headers.issubset(set(headers)):
        frappe.throw(f"Invalid template. Required columns: {', '.join(required_headers)}")

    errors = []
    success = 0

    for idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        try:
            row_data = dict(zip(headers, row))
            create_additional_salary(row_data, payroll_doc)
            success += 1
        except Exception as e:
            errors.append(f"Row {idx}: {str(e)}")

    return {
        "success": success,
        "errors": errors
    }

# def create_additional_salary(row, payroll_doc):
#     if not row.get("employee"):
#         frappe.throw("Employee is mandatory")

#     if not row.get("salary_component"):
#         frappe.throw("Salary Component is mandatory")

#     if not row.get("payroll_date"):
#         frappe.throw("Payroll Date is mandatory")

#     # ---- DUPLICATE CHECK (BEFORE INSERT) ----
#     if frappe.db.exists(
#         "Additional Salary",
#         {
#             "employee": row.get("employee"),
#             "salary_component": row.get("salary_component"),
#             "payroll_date": row.get("payroll_date"),
#             "docstatus": ["!=", 2],  # exclude cancelled
#         },
#     ):
#         frappe.throw(
#             f"Duplicate Additional Salary found for Employee {row.get('employee')} "
#             f"and Component {row.get('salary_component')}"
#         )

#     # ---- CREATE ADDITIONAL SALARY ----
#     doc = frappe.new_doc("Additional Salary")
#     doc.employee = row.get("employee")
#     doc.salary_component = row.get("salary_component")
#     doc.amount = row.get("amount")
#     doc.payroll_date = row.get("payroll_date")
#     doc.company = payroll_doc.company
#     doc.currency = "INR"
#     # doc.remarks = row.get("remarks") or ""

#     doc.insert(ignore_permissions=True)
#     doc.submit()




# def create_additional_salary(row, payroll_doc):
#     # ---- BASIC VALIDATIONS ----
#     if not row.get("employee"):
#         frappe.throw("Employee is mandatory")

#     if not row.get("salary_component"):
#         frappe.throw("Salary Component is mandatory")

#     if not row.get("payroll_date"):
#         frappe.throw("Payroll Date is mandatory")

#     # ---- SALARY COMPONENT EXISTENCE CHECK ----
#     if not frappe.db.exists("Salary Component", row.get("salary_component")):
#         frappe.throw(
#             f"Salary Component '{row.get('salary_component')}' does not exist"
#         )

#     # ---- DUPLICATE CHECK ----
#     if frappe.db.exists(
#         "Additional Salary",
#         {
#             "employee": row.get("employee"),
#             "salary_component": row.get("salary_component"),
#             "payroll_date": row.get("payroll_date"),
#             "docstatus": ["!=", 2],
#         }
#     ):
#         frappe.throw(
#             f"Duplicate Additional Salary found for Employee {row.get('employee')} "
#             f"and Component {row.get('salary_component')}"
#         )

#     # ---- CREATE ADDITIONAL SALARY ----
#     doc = frappe.new_doc("Additional Salary")
#     doc.employee = row.get("employee")
#     doc.salary_component = row.get("salary_component")
#     doc.amount = row.get("amount")
#     doc.payroll_date = row.get("payroll_date")
#     doc.company = payroll_doc.company
#     doc.currency = "INR"

#     doc.insert(ignore_permissions=True)
#     doc.submit()



def create_additional_salary(row, payroll_doc):
    # ---- BASIC VALIDATIONS ----
    if not row.get("employee"):
        frappe.throw("Employee is mandatory")

    if not row.get("salary_component"):
        frappe.throw("Salary Component is mandatory")

    if not row.get("payroll_date"):
        frappe.throw("Payroll Date is mandatory")

    # ---- SALARY COMPONENT EXISTENCE CHECK ----
    if not frappe.db.exists("Salary Component", row.get("salary_component")):
        frappe.throw(
            f"Salary Component '{row.get('salary_component')}' does not exist"
        )

    # ---- DUPLICATE CHECK ----
    if frappe.db.exists(
        "Additional Salary",
        {
            "employee": row.get("employee"),
            "salary_component": row.get("salary_component"),
            "payroll_date": row.get("payroll_date"),
            "docstatus": ["!=", 2],
        }
    ):
        frappe.throw(
            f"Duplicate Additional Salary found for Employee {row.get('employee')} "
            f"and Component {row.get('salary_component')}"
        )

    # ---- CREATE ADDITIONAL SALARY ----
    additional_doc = frappe.new_doc("Additional Salary")
    additional_doc.employee = row.get("employee")
    additional_doc.salary_component = row.get("salary_component")
    additional_doc.amount = row.get("amount")
    additional_doc.payroll_date = row.get("payroll_date")
    additional_doc.company = payroll_doc.company
    additional_doc.currency = "INR"

    additional_doc.insert(ignore_permissions=True)
    additional_doc.submit()

    # ---- ADD TO PAYROLL ENTRY CHILD TABLE ----
    if hasattr(payroll_doc, "custom_additional_extra_payments_details"):
        payroll_doc.append("custom_additional_extra_payments_details", {
            "employee": row.get("employee"),
            "salary_component": row.get("salary_component"),
            "amount": row.get("amount")
        })
        payroll_doc.save(ignore_permissions=True)
