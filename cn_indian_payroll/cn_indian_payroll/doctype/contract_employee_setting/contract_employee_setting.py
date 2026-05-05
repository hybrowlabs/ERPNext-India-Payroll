# # # Copyright (c) 2026, Hybrowlabs technologies and contributors
# # # For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
from urllib.parse import urljoin





class ContractEmployeeSetting(Document):
	pass



@frappe.whitelist()
def get_workflow_policy_details(policy_name):

    settings = frappe.get_single("Integration Settings")

    url = f"{settings.url}/api/resource/Workflow Policy/{policy_name}"

    headers = {
        "Authorization": f"token {settings.api_key}:{settings.api_secret}",
        "Accept": "application/json"
    }

    try:
        resp = requests.get(url, headers=headers, timeout=30)
    except Exception as e:
        frappe.throw(f"Connection failed: {str(e)}")

    if resp.status_code != 200:
        frappe.throw(f"API failed: {resp.text}")

    data = resp.json().get("data", {})

    categories = data.get("applicable_business_category", [])

    segments = data.get("applicable_business_segment", [])

    department = data.get("applicable_department", [])


    return {
    "categories": categories,
    "segments": segments,
    "department": department
    }


def fetch_from_remote(resource, filters=None):

    settings = frappe.get_single("Integration Settings")

    if not settings.url or not settings.api_key or not settings.api_secret:
        frappe.throw("Integration Settings is incomplete")

    url = urljoin(
        settings.url,
        f"/api/resource/{resource}"
    )

    headers = {
        "Authorization": f"token {settings.api_key}:{settings.api_secret}",
        "Accept": "application/json"
    }

    params = {
        "limit_page_length": 0
    }

    # ✅ Apply filters if provided
    if filters:
        params["filters"] = frappe.as_json(filters)

    try:
        resp = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30
        )

    except Exception as e:
        frappe.throw(f"Connection failed: {str(e)}")

    if resp.status_code != 200:
        frappe.throw(f"{resource} API failed: {resp.text}")

    return resp.json().get("data", [])


# # @frappe.whitelist()
# # def get_item_list():
# #     return fetch_from_remote("Item")




@frappe.whitelist()
def get_workflow_policy_list():
    return fetch_from_remote("Workflow Policy")

@frappe.whitelist()
def get_business_location_list():
    return fetch_from_remote("Location")




@frappe.whitelist()
def get_invoice_status(salary_slip):
    

    filters = [
        ["bill_no", "=", salary_slip],
        ["docstatus", "=", 1]
    ]

    fields = ["name", "workflow_state"]

    settings = frappe.get_single("Integration Settings")

    if not settings.url or not settings.api_key or not settings.api_secret:
        frappe.throw("Integration Settings is incomplete")

    url = urljoin(
        settings.url,
        "/api/resource/Purchase Invoice"
    )

    headers = {
        "Authorization": f"token {settings.api_key}:{settings.api_secret}",
        "Accept": "application/json"
    }

    params = {
        "limit_page_length": 1,
        "fields": frappe.as_json(fields)
    }

    # Apply filters
    if filters:
        params["filters"] = frappe.as_json(filters)

    try:
        resp = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30
        )

    except Exception as e:
        frappe.throw(f"Connection failed: {str(e)}")

    if resp.status_code != 200:
        frappe.throw(f"Purchase Invoice API failed: {resp.text}")

    data = resp.json().get("data", [])

    if not data:
        return "Draft"

    return data[0].get("workflow_state", "Draft")

