import base64
import json
from calendar import month_name
from collections import defaultdict

import frappe
from frappe import _
from frappe.utils import flt

# Maps first two characters of the quarter_ended select value to calendar month numbers.
# Q4 spans Jan-Mar (fiscal year end), so months are 1-3.
_QUARTER_MONTHS: dict[str, list[int]] = {
    "Q1": [4, 5, 6],
    "Q2": [7, 8, 9],
    "Q3": [10, 11, 12],
    "Q4": [1, 2, 3],
}


def _parse_quarter(quarter_ended: str) -> list[int]:
    key = (quarter_ended or "").strip()[:2].upper()
    months = _QUARTER_MONTHS.get(key)
    if not months:
        frappe.throw(_("Invalid quarter value: {0}").format(quarter_ended))
    return months


@frappe.whitelist()
def month_wise_tds_value(company, fiscal_year, quarter_ended, payroll_period=None):
    frappe.only_for("HR Manager")

    months = _parse_quarter(quarter_ended)

    slip_filters: dict = {"company": company, "docstatus": 1}
    if payroll_period:
        slip_filters["custom_payroll_period"] = payroll_period

    slips = frappe.get_all(
        "Salary Slip",
        filters=slip_filters,
        fields=["name", "employee", "employee_name", "start_date", "current_month_income_tax", "gross_pay"],
    )

    # Filter to the quarter's months (start_date.month in the target list)
    slips = [s for s in slips if s.start_date and s.start_date.month in months]
    if not slips:
        return {"data": []}

    emp_ids = list({s.employee for s in slips})

    # Batch-fetch employee PAN (pan_number is the native HRMS field)
    pan_map: dict[str, str] = {
        row.name: row.pan_number or ""
        for row in frappe.get_all(
            "Employee",
            filters={"name": ["in", emp_ids]},
            fields=["name", "pan_number"],
        )
    }

    # Group salary slips by calendar month number
    month_groups: dict[int, list] = defaultdict(list)
    for s in slips:
        month_groups[s.start_date.month].append(s)

    result = []
    for month_num in sorted(months):
        month_slips = month_groups.get(month_num)
        if not month_slips:
            continue

        total_tds_with_cess = sum(flt(s.current_month_income_tax) for s in month_slips)
        # Education cess is 4% of base tax; total = base * 1.04 → cess = total * 4/104
        total_cess = round(total_tds_with_cess * 4 / 104, 2)
        total_base_tds = round(total_tds_with_cess - total_cess, 2)

        employees = []
        for s in month_slips:
            emp_total = flt(s.current_month_income_tax)
            emp_cess = round(emp_total * 4 / 104, 2)
            employees.append(
                {
                    "employee": s.employee,
                    "employee_name": s.employee_name,
                    "employee_pan": pan_map.get(s.employee, ""),
                    "tds": round(emp_total - emp_cess, 2),
                    "education_cess": emp_cess,
                    "surcharge": 0,
                    "total_amount": flt(s.gross_pay),
                }
            )

        result.append(
            {
                "month": month_name[month_num],
                "total_tds": total_base_tds,
                "total_education_cess": total_cess,
                "total_surcharge": 0,
                "employees": employees,
            }
        )

    return {"data": result}


@frappe.whitelist()
def insert_tds_details(challan_data, annexure_data, fieldData):
    frappe.only_for("HR Manager")

    if isinstance(challan_data, str):
        challan_data = json.loads(challan_data)
    if isinstance(annexure_data, str):
        annexure_data = json.loads(annexure_data)
    if isinstance(fieldData, str):
        fieldData = json.loads(fieldData)

    doc = frappe.get_doc(
        {
            "doctype": "TDS Return",
            "company": fieldData.get("company"),
            "fiscal_year": fieldData.get("fiscal_year"),
            "quarter": (fieldData.get("quarter_ended") or "")[:2],
            "payroll_period": fieldData.get("payroll_period") or None,
            "branch": fieldData.get("branch") or None,
            "tan_number": fieldData.get("tan_number", ""),
            "deductor_name": fieldData.get("deductor_name", ""),
            "status": "Saved",
            "challan_data": json.dumps(challan_data),
            "annexure_data": json.dumps(annexure_data),
            "form_data": json.dumps(fieldData),
        }
    )
    doc.insert()

    frappe.msgprint(
        _("TDS Return {0} saved successfully.").format(frappe.bold(doc.name)),
        indicator="green",
        alert=True,
    )
    return {"tds_return": doc.name}


@frappe.whitelist()
def upload_csi_file(file_name, file_data, attached_to_doctype, attached_to_name):
    frappe.only_for("HR Manager")
    frappe.has_permission("TDS Return", "write", attached_to_name, throw=True)

    file_content = base64.b64decode(file_data)
    file_doc = frappe.get_doc(
        {
            "doctype": "File",
            "file_name": file_name,
            "content": file_content,
            "attached_to_doctype": "TDS Return",
            "attached_to_name": attached_to_name,
            "is_private": 1,
        }
    )
    file_doc.insert(ignore_permissions=True)

    return {"file_url": file_doc.file_url}


@frappe.whitelist()
def create_txt_file(basic_data, attached_to_name):
    frappe.only_for("HR Manager")
    frappe.has_permission("TDS Return", "write", attached_to_name, throw=True)

    if isinstance(basic_data, str):
        basic_data = json.loads(basic_data)

    tds_doc = frappe.get_doc("TDS Return", attached_to_name)
    challan_rows = json.loads(tds_doc.challan_data or "[]")
    annexure_rows = json.loads(tds_doc.annexure_data or "[]")

    lines = _build_24q_text(basic_data, challan_rows, annexure_rows)
    content = "\n".join(lines).encode("utf-8")

    quarter_key = (basic_data.get("quarter_ended") or "Q1")[:2]
    fy = (basic_data.get("fiscal_year") or "").replace("/", "-")
    file_name = f"24Q_{fy}_{quarter_key}.txt"

    file_doc = frappe.get_doc(
        {
            "doctype": "File",
            "file_name": file_name,
            "content": content,
            "attached_to_doctype": "TDS Return",
            "attached_to_name": attached_to_name,
            "is_private": 1,
        }
    )
    file_doc.insert(ignore_permissions=True)

    return {"file_url": file_doc.file_url}


def _build_24q_text(form_data: dict, challan_rows: list, annexure_rows: list) -> list[str]:
    """
    Build a pipe-delimited 24Q text file compatible with NSDL RPU batch upload.

    Record types:
      BH — Batch Header (one per file)
      CD — Challan Detail (one per monthly challan)
      DD — Deductee Detail (one per employee per challan)
      BT — Batch Trailer (one per file, with record counts)
    """

    def v(row: dict, *keys: str) -> str:
        for k in keys:
            val = row.get(k)
            if val is not None and str(val).strip():
                return str(val).strip()
        return ""

    lines: list[str] = []

    # --- Batch Header ---
    lines.append(
        "|".join(
            [
                "BH",
                "24Q",
                v(form_data, "fiscal_year"),
                (v(form_data, "quarter_ended") or "")[:2],
                v(form_data, "tan_number"),
                v(form_data, "pan_number"),
                v(form_data, "deductor_name"),
                v(form_data, "type_of_deductor"),
                v(form_data, "flat_no"),
                v(form_data, "road_name"),
                v(form_data, "city_district"),
                v(form_data, "pin_code"),
                v(form_data, "state_name"),
                v(form_data, "telephone_number"),
                v(form_data, "email"),
                v(form_data, "responsible_person_name"),
                v(form_data, "responsible_person_pan"),
                v(form_data, "designation"),
            ]
        )
    )

    # --- Challan Detail records ---
    for i, row in enumerate(challan_rows, 1):
        lines.append(
            "|".join(
                [
                    "CD",
                    str(i),
                    v(row, "Month"),
                    v(row, "TDS (₹)"),
                    v(row, "Education Cess (₹)"),
                    v(row, "Surcharge (₹)"),
                    v(row, "Fee (₹)"),
                    v(row, "BSR Code / Receipt No. (Form 24G)"),
                    v(row, "Date Deposited (Challan / Voucher)"),
                    v(row, "Challan Serial No. / DDO Serial No. (Form 24G)"),
                    v(row, "Total Amount Deposited (₹)"),
                    v(row, "Section Code"),
                    v(row, "Minor Head of Challan"),
                    v(row, "Mode of Deposit (Book Adjustment)"),
                ]
            )
        )

    # --- Deductee Detail records ---
    for i, row in enumerate(annexure_rows, 1):
        lines.append(
            "|".join(
                [
                    "DD",
                    str(i),
                    v(row, "Challan Serial No."),
                    v(row, "Name of Employee"),
                    v(row, "PAN of the Employee"),
                    v(row, "TDS (₹)"),
                    v(row, "Health & Education Cess (₹)"),
                    v(row, "Surcharge (₹)"),
                    v(row, "Amount Paid/Credited (₹)"),
                    v(row, "Date of Payment/Credit"),
                    v(row, "Date of Deduction"),
                    v(row, "Section Under Which Payment Made"),
                    v(row, "Certificate No. u/s 197"),
                    v(row, "Remarks"),
                ]
            )
        )

    # --- Batch Trailer ---
    lines.append("|".join(["BT", str(len(challan_rows)), str(len(annexure_rows))]))

    return lines
