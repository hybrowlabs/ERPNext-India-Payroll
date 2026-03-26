


import frappe
import base64
import requests
from frappe.utils.pdf import get_pdf
   
import json
from frappe.utils import add_days, formatdate
from frappe.utils.file_manager import get_file_path

import tempfile
import os


from io import BytesIO
from pypdf import PdfReader, PdfWriter



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

    leegality_setting = frappe.get_single("Leegality Settings")
    base_url = leegality_setting.api_base_url.rstrip("/")

    API_URL = f"{base_url}/api/v3.0/sign/request"

    # API_URL = leegality_setting.api_base_url
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



# @frappe.whitelist(allow_guest=True)
# def leegality_webhook():

#     try:

#         data = frappe.local.form_dict

#         # Raw JSON (important)
#         payload = frappe.request.get_data(as_text=True)

#         if not payload:
#             frappe.throw("Empty Payload")

#         event_data = json.loads(payload)

#         frappe.log_error(
#             json.dumps(event_data, indent=2),
#             "Leegality Webhook Received"
#         )

#         # -----------------------------
#         # Extract Values
#         # -----------------------------

#         document_id = event_data.get("documentId")

#         status = event_data.get("status")  # COMPLETED / SIGNED / etc

#         if not document_id:
#             return {"status": "ignored"}

#         # -----------------------------
#         # Find Salary Slip
#         # -----------------------------

#         slip_name = frappe.db.get_value(
#             "Salary Slip",
#             {"custom_document_id": document_id},
#             "name"
#         )

#         if not slip_name:
#             frappe.log_error(
#                 f"Doc ID Not Found: {document_id}",
#                 "Leegality Webhook Error"
#             )

#             return {"status": "not_found"}

#         slip = frappe.get_doc("Salary Slip", slip_name)

#         # -----------------------------
#         # Update Status
#         # -----------------------------

#         if status in ["COMPLETED", "SIGNED", "SUCCESS"]:

#             slip.db_set("custom_e_sign_status", "Signed")

#         elif status in ["REJECTED", "CANCELLED"]:

#             slip.db_set("custom_e_sign_status", "Rejected")

#         return {"status": "ok"}

#     except Exception:

#         frappe.log_error(
#             frappe.get_traceback(),
#             "Leegality Webhook Failed"
#         )

#         return {"status": "error"}


import hashlib

@frappe.whitelist(allow_guest=True)
def leegality_webhook():

    try:
        payload = frappe.request.get_data(as_text=True)

        if not payload:
            frappe.throw("Empty Payload")

        # 🔐 VERIFY SIGNATURE
        signature = frappe.get_request_header("X-Leegality-Signature")

        settings = frappe.get_single("Leegality Settings")
        private_salt = settings.private_salt

        generated_signature = hashlib.sha256(
            (payload + private_salt).encode()
        ).hexdigest()

        if signature != generated_signature:
            frappe.log_error("Invalid Signature", "Webhook Security")
            return {"status": "unauthorized"}

        # -----------------------------
        # Process JSON
        # -----------------------------
        event_data = json.loads(payload)

        frappe.log_error(
            json.dumps(event_data, indent=2),
            "Leegality Webhook Received"
        )

        document_id = event_data.get("documentId")
        status = event_data.get("status")

        if not document_id:
            return {"status": "ignored"}

        slip_name = frappe.db.get_value(
            "Salary Slip",
            {"custom_document_id": document_id},
            "name"
        )

        if not slip_name:
            return {"status": "not_found"}

        slip = frappe.get_doc("Salary Slip", slip_name)

        # ✅ Update status
        if status in ["COMPLETED", "SIGNED", "SUCCESS"]:
            slip.db_set("custom_e_sign_status", "Signed")

        elif status in ["REJECTED", "CANCELLED"]:
            slip.db_set("custom_e_sign_status", "Rejected")

        return {"status": "ok"}

    except Exception:
        frappe.log_error(frappe.get_traceback(), "Webhook Failed")
        return {"status": "error"}



@frappe.whitelist()
def view_signed_payslip_employee(salary_slip):

    slip = frappe.get_doc("Salary Slip", salary_slip)

    documentId=slip.custom_document_id

    leegality_setting = frappe.get_single("Leegality Settings")
    X_AUTH_TOKEN = leegality_setting.api_key


    base_url = leegality_setting.api_base_url.rstrip("/")

    url = f"{base_url}/api/v3.1/document/fetchDocument"


    # url = leegality_setting.post_url

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







@frappe.whitelist()
def get_salary_slip_for_esign(month, company, employment_type,payroll_period):
    """
    Fetch salary slips based on month, company, and employment type
    """



    filters = {
        "company": company,
        "custom_employment_type": employment_type,
        "docstatus": 0  ,
        "custom_month":month,
        "custom_payroll_period":payroll_period,
        "custom_e_sign_status":"Not Send"
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
def send_bulk_salary_slip_for_esign(month, company, employment_type,payroll_period):
    """
    Send multiple salary slips for e-sign
    """

    salary_slips = get_salary_slip_for_esign(
        month=month,
        company=company,
        employment_type=employment_type,
        payroll_period=payroll_period
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
    base_url = settings.api_base_url.rstrip("/")

    API_URL = f"{base_url}/api/v3.0/sign/request"

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
        "requestSignOrder": True,
        "callbackUrl": "http://127.0.0.1:8002/api/method/cn_indian_payroll.cn_indian_payroll.overrides.leegality.leegality_webhook"
    }

    response = requests.post(
        API_URL,
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



    document_id = result["data"]["documentId"]
    sign_url = result["data"]["invitees"][0].get("signUrl")




    
    frappe.db.set_value(
        "Salary Slip",
        slip.name,
        {
            "custom_document_id": document_id,
            "custom_e_sign_url": sign_url,
            "custom_e_sign_status": "Send"
        },
        
    )


    frappe.db.commit()

    employee = frappe.get_doc("Employee", slip.employee)
    send_email_from_template_to_employee(slip, employee, sign_url)

    return {
        "document_id": result["data"]["documentId"],
        "sign_url": result["data"]["invitees"][0]["signUrl"]
    }









@frappe.whitelist()
def view_signed_payslip(salary_slip):

    slip = frappe.get_doc("Salary Slip", salary_slip)

    if not slip.custom_document_id:
        frappe.throw("Document ID missing in Salary Slip")

    settings = frappe.get_single("Leegality Settings")

    if not settings.api_key or not settings.api_base_url:
        frappe.throw("Leegality Settings not configured")


    document_id = slip.custom_document_id
    token = settings.api_key
    # url = settings.post_url
    base_url = settings.api_base_url.rstrip("/")
    url = f"{base_url}/api/v3.1/document/fetchDocument"

    headers = {
        "X-Auth-Token": token
    }

    params = {
        "documentId": document_id,
        "documentDownloadType": "DOCUMENT"
    }

    # Call Leegality API
    resp = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=60
    )

    if resp.status_code != 200:
        frappe.throw("Failed to download signed PDF")

    if not resp.content:
        frappe.throw("Empty file received")

    # Handle PDF / Base64
    content_type = resp.headers.get("Content-Type", "").lower()

    if "application/pdf" in content_type:

        pdf_bytes = resp.content

    elif "application/json" in content_type:

        data = resp.json()

        if "fileContent" not in data.get("data", {}):
            frappe.throw("Invalid response")

        pdf_bytes = base64.b64decode(
            data["data"]["fileContent"]
        )

    else:
        frappe.throw("Unexpected response format")

    # Normalize PDF
    reader = PdfReader(BytesIO(pdf_bytes))
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    output = BytesIO()
    writer.write(output)
    output.seek(0)

    final_bytes = output.getvalue()

    # Save File in ERP
    file_name = f"{slip.name}_Signed.pdf"

    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": file_name,
        "attached_to_doctype": "Salary Slip",
        "attached_to_name": slip.name,
        "attached_to_field": "custom_slip_attach",
        "is_private": 1,
        "content": final_bytes
    })

    file_doc.insert(ignore_permissions=True)

    # Update field
    slip.db_set("custom_slip_attach", file_doc.file_url)

    frappe.db.commit()

    # Create Purchase Invoice
    create_purchase_invoice(slip.name)

    return {
        "status": "success",
        "file_url": file_doc.file_url
    }



def get_integration_settings():

    settings = frappe.get_single("Integration Settings")

    if not settings.url or not settings.api_key or not settings.api_secret:
        frappe.throw("Configure Integration Settings")

    return {
        "url": settings.url,
        "api_key": settings.api_key,
        "api_secret": settings.api_secret
    }


@frappe.whitelist()
def create_purchase_invoice(salary_slip):

    try:

        slip = frappe.get_doc("Salary Slip", salary_slip)

        month=slip.custom_month

        config = get_integration_settings()

        base_url = config["url"]
        api_key = config["api_key"]
        api_secret = config["api_secret"]

        token = f"token {api_key}:{api_secret}"

        headers = {
            "Authorization": token
        }


        file_attach_url = None
        file_challan_url = None


        # Upload custom_attach
        if slip.custom_attach:

            file_path = get_file_path(slip.custom_attach)

            if not file_path:
                frappe.throw("custom_attach file not found")

            file_attach_url = upload_file_to_target(
                base_url,
                headers,
                file_path
            )


        # Upload custom_slip_attach
        if slip.custom_slip_attach:

            file_path = get_file_path(slip.custom_slip_attach)

            if not file_path:
                frappe.throw("custom_slip_attach file not found")

            file_challan_url = upload_file_to_target(
                base_url,
                headers,
                file_path
            )



        employee = frappe.get_doc("Employee", slip.employee)

        supplier_id = employee.custom_supplier_id
        business_category=employee.custom_business_category
        business_segment=employee.custom_business_segment
        bank_acc=employee.custom_bank_account_in_erp
        work_flow_policy=employee.custom_work_flow_policy

        posting_date = frappe.utils.formatdate(
            slip.posting_date, "yyyy-mm-dd"
        )
        doc_name=slip.name

        due_date = frappe.utils.add_days(posting_date, 10)




        employee_setting = frappe.get_single("Contract Employee Setting")

        # Company
        company_name = None
        department_name=None
        worklocation_name=None

        for row in employee_setting.map_the_company:

            if row.company_in_oxygen == slip.company:
                company_name = row.company_in_erp
                break      

        if not company_name:
            frappe.throw("Company mapping missing")


        for row in employee_setting.map_the_department:

            if row.department_in_oxygen == employee.department:
                department_name = row.department_in_erp
                break      

        if not department_name:
            frappe.throw("Department mapping missing")



        for row in employee_setting.map_the_work_location:

            if row.location_in_oxygen == employee.branch:
                worklocation_name = row.location_in_erp
                break      

        if not worklocation_name:
            frappe.throw("Worklocation mapping missing")


        item_code = None
        amount = 0

        for m in employee_setting.table_peep:

            for e in slip.earnings:

                if m.salary_component == e.salary_component:

                    item_code = m.item
                    amount = e.amount
                    break                

            if item_code:
                break
                

        if not item_code:
            frappe.throw("Item mapping missing")



        gst = None
        for e in slip.earnings:
            component = frappe.get_cached_doc(
                "Salary Component",
                e.salary_component
            )

            if component.component_type == "GST":
                gst = component.name
                break

        item_tax_template = None
        if gst:
            for row in employee_setting.map_the_company:
                if row.company_in_oxygen == slip.company:
                    item_tax_template = row.item_tax_template
                    break
  

        payload = {
            "data": {
                "supplier": supplier_id,
                "company": company_name,
                "posting_date": posting_date,

                "bill_no": doc_name,
                "bill_date": posting_date,
                "bank_account": bank_acc,
                "workflow_policy":work_flow_policy ,
                "business_category": business_category,
                "business_segment": business_segment,
                "apply_tds":1,
                "supplier_bill_attachment":file_challan_url,

                "remarks":"invoice in the month of"+month,
                "location":worklocation_name,
                "department":department_name,


                "items": [
                    {
                        "item_code": item_code,
                        "qty": 1,
                        "rate": amount,
                        "price_list_rate":amount,
                        "amount":amount,
                        "item_tax_template":item_tax_template if gst else None
                    }

                
                ],
                "attachment_details":[{
                        "title":"Challan",
                        "attachment": file_attach_url or ""
                    }]
            }
        }

        pi_url = f"{base_url}/api/resource/Purchase Invoice"

        response = requests.post(
            pi_url,
            headers={
                **headers,
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )

        if response.status_code not in (200, 201):

            frappe.log_error(response.text, "PI Create Error")

            return {
                "status": "failed",
                "error": response.text
            }

        result = response.json()

        return {
            "status": "success",
            "pi_name": result["data"]["name"],
            "attach_url": file_attach_url,
            "challan_url": file_challan_url
        }

    except Exception as e:

        frappe.log_error(frappe.get_traceback(), "Create PI Error")

        return {
            "status": "error",
            "message": str(e)
        }




def upload_file_to_target(base_url, headers, file_path):

    upload_url = f"{base_url}/api/method/upload_file"

    with open(file_path, "rb") as f:

        files = {
            "file": f
        }

        data = {
            "is_private": 1
        }

        response = requests.post(
            upload_url,
            headers=headers,
            files=files,
            data=data,
            timeout=30
        )

    if response.status_code not in (200, 201):

        frappe.throw("File upload failed: " + response.text)

    result = response.json()

    return result["message"]["file_url"]






def send_email_from_template_to_employee(slip, employee, sign_url=None):
    settings = frappe.get_single("Leegality Settings")

    if not settings.email_template:
        return  # silently skip if no template configured

    template = frappe.get_doc("Email Template", settings.email_template)

    # Pass dynamic values to template
    context = {
        "employee_name": slip.employee_name,
        "salary_slip": slip.name,
        "company": slip.company,
        "sign_url": sign_url
    }

    subject = frappe.render_template(template.subject or "", context)
    message = frappe.render_template(template.response or "", context)

    frappe.sendmail(
        recipients=[employee.personal_email],
        subject=subject,
        message=message,
        reference_doctype="Salary Slip",
        reference_name=slip.name,
        # now=True
    )