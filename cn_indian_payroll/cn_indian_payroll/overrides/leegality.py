


import frappe
import base64
import requests
from frappe.utils.pdf import get_pdf


@frappe.whitelist()
def send_salary_slip_for_esign(salary_slip):
    """
    Button click entry point
    Generates PDF dynamically and sends to Leegality
    """


    slip = frappe.get_doc("Salary Slip", salary_slip)


    employee = frappe.get_doc("Employee", slip.employee)

    if not employee.personal_email or not employee.cell_number:
        frappe.throw("Please fill Employee Personal Email and Mobile Number")



    email = employee.personal_email
    phone = employee.cell_number

    html = frappe.get_print(
        doctype="Salary Slip",
        name=salary_slip,
        print_format="Consultant",
        doc=slip,
        as_pdf=False
    )

    pdf_bytes = get_pdf(html)


    pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

    return _push_to_leegality(pdf_base64, slip, email, phone)


def _push_to_leegality(pdf_base64, slip, email, phone):
    """
    Internal helper
    """

    # ✅ Single DocType
    leegality_setting = frappe.get_single("Leegality Settings")

    API_URL = leegality_setting.api_base_url
    X_AUTH_TOKEN = leegality_setting.api_key
    PROFILE_ID = leegality_setting.profile_id

    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": X_AUTH_TOKEN
    }

    payload = {
        "profileId": PROFILE_ID,
        "file": {
            "name": f"{slip.name}.pdf",
            "file": pdf_base64
        },
        "invitees": [
            {
                "name": slip.employee_name,
                "email": email,
                "phone": phone
            }
        ],
        "requestSignOrder": True
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=60
    )


    frappe.log_error(
        f"STATUS: {response.status_code}\nRESPONSE: {response.text}",
        "Leegality v3.0 Test"
    )

    response.raise_for_status()
    result = response.json()


    slip.db_set("custom_document_id", result["data"]["documentId"])
    slip.db_set("custom_e_sign_status", "Send")

    return {
        "result": result,
        "documentId": result["data"]["documentId"],
        "signUrl": result["data"]["invitees"][0]["signUrl"]
    }




import frappe
import requests


@frappe.whitelist()
def view_signed_payslip(salary_slip):

    slip = frappe.get_doc("Salary Slip", salary_slip)

    documentId=slip.custom_document_id

    leegality_setting = frappe.get_single("Leegality Settings")
    X_AUTH_TOKEN = leegality_setting.api_key


    url = leegality_setting.post_url

    headers = {
        "X-Auth-Token": X_AUTH_TOKEN
    }

    params = {
        "documentId": documentId,
        "documentDownloadType": "DOCUMENT"
    }

    r = requests.get(url, headers=headers, params=params, timeout=60)

    if r.status_code != 200 or not r.content:
        frappe.throw("Unable to fetch signed document from Leegality")

    frappe.local.response.filename = f"{slip.name}_Signed.pdf"
    frappe.local.response.filecontent = r.content
    frappe.local.response.type = "pdf"

    return




# import frappe
# import requests
# import base64
# from io import BytesIO
# from pypdf import PdfReader, PdfWriter


# @frappe.whitelist()
# def view_signed_payslip(salary_slip):

#     slip = frappe.get_doc("Salary Slip", salary_slip)

#     # -----------------------------
#     # 1️⃣ Fetch PDF from Leegality
#     # -----------------------------
#     resp = requests.get(
#         "https://app1.leegality.com/api/v3.1/document/fetchDocument",
#         headers={"X-Auth-Token": "iwzXO8JH8pTaP4AdFM7nRan502vWaLv0"},
#         params={
#             "documentId": "01KG1XYRAMCGY14RPRY2PRMWZ7",
#             "documentDownloadType": "DOCUMENT"
#         },
#         timeout=60
#     )

#     if resp.status_code != 200:
#         frappe.throw("Leegality API failed")

#     content_type = resp.headers.get("Content-Type", "").lower()

#     if "application/pdf" in content_type:
#         pdf_bytes = resp.content

#     elif "application/json" in content_type:
#         data = resp.json()
#         pdf_bytes = base64.b64decode(data["data"]["fileContent"])

#     else:
#         frappe.throw(f"Unexpected Leegality response: {content_type}")

#     # -----------------------------
#     # 2️⃣ Normalize PDF (important)
#     # -----------------------------
#     reader = PdfReader(BytesIO(pdf_bytes))
#     writer = PdfWriter()

#     for page in reader.pages:
#         writer.add_page(page)

#     final_pdf = BytesIO()
#     writer.write(final_pdf)
#     final_pdf.seek(0)

#     # -----------------------------
#     # 3️⃣ SAVE FILE (ERPNext)
#     # -----------------------------
#     file_doc = frappe.get_doc({
#         "doctype": "File",
#         "file_name": f"{slip.name}_Signed.pdf",
#         "attached_to_doctype": "Salary Slip",
#         "attached_to_name": slip.name,
#         "is_private": 1,
#         "content": final_pdf.getvalue()
#     })

#     file_doc.save(ignore_permissions=True)

#     # 🔥 THIS IS THE MISSING PIECE
#     frappe.db.commit()

#     # -----------------------------
#     # 4️⃣ Stream to browser
#     # -----------------------------
#     frappe.local.response.filename = file_doc.file_name
#     frappe.local.response.filecontent = final_pdf.getvalue()
#     frappe.local.response.type = "pdf"




@frappe.whitelist()
def get_salary_slip_for_esign(month, company, employment_type):
    """
    Fetch salary slips based on month, company, and employment type
    """



    filters = {
        "company": company,
        "custom_employment_type": employment_type,
        "docstatus": 0  ,
        "custom_month":month
    }

    salary_slips = frappe.get_all(
        "Salary Slip",
        filters=filters,
        fields=[
            "name",
            "employee",
            "employee_name",
            "start_date",
            "end_date",
            "posting_date",
            "net_pay"
        ]
    )



    return salary_slips

@frappe.whitelist()
def send_bulk_salary_slip_for_esign(month, company, employment_type):
    """
    Send multiple salary slips for e-sign
    """

    salary_slips = get_salary_slip_for_esign(
        month=month,
        company=company,
        employment_type=employment_type
    )

    if not salary_slips:
        frappe.throw("No Salary Slips found for the given criteria")

    success = []
    failed = []

    for slip in salary_slips:
        try:
            send_salary_slip_for_esign_bulk(slip["name"])
            success.append(slip["name"])
        except Exception as e:
            failed.append({
                "salary_slip": slip["name"],
                "error": str(e)
            })

    # ✅ Final user-friendly message
    # frappe.msgprint(
    #     title="Bulk e-Sign Result",
    #     message=(
    #         f"<b>Total:</b> {len(salary_slips)}<br>"
    #         f"<b>Successfully Sent:</b> {len(success)}<br>"
    #         f"<b>Failed:</b> {len(failed)}"
    #     ),
    #     indicator="green" if not failed else "orange"
    # )

    return {
        "total": len(salary_slips),
        "success_count": len(success),
        "failed_count": len(failed),
        "success": success,
        "failed": failed
    }



@frappe.whitelist()
def send_salary_slip_for_esign_bulk(salary_slip):
    """
    Generate Salary Slip PDF and send to Leegality
    """

    slip = frappe.get_doc("Salary Slip", salary_slip)
    employee = frappe.get_doc("Employee", slip.employee)

    if not employee.personal_email or not employee.cell_number:
        frappe.throw(
            f"Employee {slip.employee_name} is missing Personal Email or Mobile Number"
        )

    html = frappe.get_print(
        doctype="Salary Slip",
        name=salary_slip,
        print_format="Consultant",
        doc=slip,
        as_pdf=False
    )

    pdf_bytes = get_pdf(html)
    pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

    return _push_to_leegality_bulk(
        pdf_base64=pdf_base64,
        slip=slip,
        email=employee.personal_email,
        phone=employee.cell_number
    )


def _push_to_leegality_bulk(pdf_base64, slip, email, phone):
    """
    Internal helper to send document to Leegality
    """

    settings = frappe.get_single("Leegality Settings")

    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": settings.api_key
    }

    payload = {
        "profileId": settings.profile_id,
        "file": {
            "name": f"{slip.name}.pdf",
            "file": pdf_base64
        },
        "invitees": [{
            "name": slip.employee_name,
            "email": email,
            "phone": phone
        }],
        "requestSignOrder": True
    }

    response = requests.post(
        settings.api_base_url,
        headers=headers,
        json=payload,
        timeout=60
    )

    frappe.log_error(
        f"STATUS: {response.status_code}\nRESPONSE: {response.text}",
        "Leegality Bulk e-Sign"
    )

    response.raise_for_status()
    result = response.json()

    # Update Salary Slip

    document_id = result["data"]["documentId"]
    sign_url = result["data"]["invitees"][0].get("signUrl")


    # slip.db_set("custom_document_id", result["data"]["documentId"])
    # slip.db_set("custom_e_sign_status", "Send")


    slip.db_set("custom_document_id", document_id)
    slip.db_set("custom_e_sign_url", sign_url)
    slip.db_set("custom_e_sign_status", "Send")

    frappe.db.commit()

    return {
        "document_id": result["data"]["documentId"],
        "sign_url": result["data"]["invitees"][0]["signUrl"]
    }
