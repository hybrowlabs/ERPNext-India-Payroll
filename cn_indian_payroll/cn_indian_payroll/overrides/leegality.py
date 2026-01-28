# import frappe
# import base64
# import requests
# from frappe.utils.pdf import get_pdf


# @frappe.whitelist()
# def send_salary_slip_for_esign(salary_slip):
#     """
#     Button click entry point
#     Generates PDF dynamically and sends to Leegality
#     """

#     # 1️⃣ Get Salary Slip
#     slip = frappe.get_doc("Salary Slip", salary_slip)

#     employee = frappe.get_doc("Employee", slip.employee)
#     if not employee.personal_email and not employee.cell_number:
#         frappe.throw("please fill these")

#     else:
#         email=employee.personal_email
#         phone=employee.cell_number

#     # 2️⃣ Render Salary Slip → PDF
#     html = frappe.get_print(
#         doctype="Salary Slip",
#         name=salary_slip,
#         print_format="Consultant",
#         doc=slip,
#         as_pdf=False
#     )

#     pdf_bytes = get_pdf(html)

#     # 3️⃣ Convert PDF → base64 (DYNAMIC)
#     pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

#     # 4️⃣ Send to Leegality
#     return _push_to_leegality(pdf_base64, slip)


# def _push_to_leegality(pdf_base64, slip):
#     """
#     Internal helper
#     """


#     leegality_setting=frappe.get_doc("Leegality Settings")

#     API_URL = leegality_setting.api_base_url+"sign/request"
#     X_AUTH_TOKEN = leegality_setting.api_key
#     PROFILE_ID = leegality_setting.profile_id

#     # API_URL = "https://app1.leegality.com/api/v3.0/sign/request"
#     # X_AUTH_TOKEN = "iwzXO8JH8pTaP4AdFM7nRan502vWaLv0"
#     # PROFILE_ID = "mSqwYQ6"

#     headers = {
#         "Content-Type": "application/json",
#         "X-Auth-Token": X_AUTH_TOKEN
#     }

#     payload = {
#         "profileId": PROFILE_ID,
#         "file": {
#             "name": f"{slip.name}.pdf",
#             "file": pdf_base64
#         },
#         "invitees": [
#             {
#                 "name": slip.employee_name,
#                 "email": email,
#                 "phone": phone
#             }
#         ],
#         "requestSignOrder": True
#     }

#     response = requests.post(
#         API_URL,
#         headers=headers,
#         json=payload,
#         timeout=60
#     )

#     # 🔍 Log full response (VERY helpful while testing)
#     frappe.log_error(
#         f"STATUS: {response.status_code}\nRESPONSE: {response.text}",
#         "Leegality v3.0 Test"
#     )

#     response.raise_for_status()
#     result = response.json()

#     # 5️⃣ Save details in Salary Slip
#     slip.db_set("custom_document_id", result["data"]["documentId"])
#     slip.db_set("custom_e_sign_status", "Send")

#     return {
#         "result":result
#         "documentId": result["data"]["documentId"],
#         "signUrl": result["data"]["invitees"][0]["signUrl"]
#     }




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

    # 1️⃣ Get Salary Slip
    slip = frappe.get_doc("Salary Slip", salary_slip)

    # 2️⃣ Get Employee contact details
    employee = frappe.get_doc("Employee", slip.employee)

    if not employee.personal_email or not employee.cell_number:
        frappe.throw("Please fill Employee Personal Email and Mobile Number")



    email = employee.personal_email
    phone = employee.cell_number

    # 3️⃣ Render Salary Slip → PDF
    html = frappe.get_print(
        doctype="Salary Slip",
        name=salary_slip,
        print_format="Consultant",
        doc=slip,
        as_pdf=False
    )

    pdf_bytes = get_pdf(html)

    # 4️⃣ Convert PDF → base64
    pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

    # 5️⃣ Send to Leegality
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

    # 🔍 Log for debugging
    frappe.log_error(
        f"STATUS: {response.status_code}\nRESPONSE: {response.text}",
        "Leegality v3.0 Test"
    )

    response.raise_for_status()
    result = response.json()

    # 6️⃣ Save details in Salary Slip
    slip.db_set("custom_document_id", result["data"]["documentId"])
    slip.db_set("custom_e_sign_status", "Send")

    return {
        "result": result,
        "documentId": result["data"]["documentId"],
        "signUrl": result["data"]["invitees"][0]["signUrl"]
    }
