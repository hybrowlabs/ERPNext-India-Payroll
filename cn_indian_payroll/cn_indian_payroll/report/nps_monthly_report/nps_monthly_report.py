import frappe
import requests # type: ignore
from cn_indian_payroll.cn_indian_payroll.overrides.webapp_api.salary_structure_assignment import generate_salary_slip

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "EMP ID", "fieldname": "employee", "fieldtype": "Data"},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data"},
        {"label": "Location", "fieldname": "branch", "fieldtype": "Data"},
        {"label": "Designation", "fieldname": "designation", "fieldtype": "Data"},
        {"label": "Department", "fieldname": "department", "fieldtype": "Data"},
        {"label": "Payroll Month", "fieldname": "payroll_month", "fieldtype": "Data"},
        {"label": "NPS Employer Contribution", "fieldname": "nps", "fieldtype": "Currency"},
    ]

def get_data(filters):
    data = []

    employees = frappe.get_all("Employee",
        fields=["name", "employee_name", "designation", "department"]
    )

    for emp in employees:
        try:
            res = generate_salary_slip(employee=emp.name)
            for record in res.get("data", []):
                nps_amount = 0

                for comp in record.get("component_part_of_ctc", []):
                    if comp.get("component") == "NPS":
                        nps_amount = comp.get("amount", 0)
                        break

                data.append({
                    "employee": emp.name,
                    "employee_name": emp.employee_name,
                    "designation": emp.designation,
                    "department": emp.department,
                    "payroll_month": record.get("payroll_month"),
                    "nps": nps_amount
                })

        except Exception as e:
            frappe.log_error(str(e), "NPS Report Error")

    return data