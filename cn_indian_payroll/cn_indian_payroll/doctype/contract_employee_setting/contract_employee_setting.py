# # Copyright (c) 2026, Hybrowlabs technologies and contributors
# # For license information, please see license.txt

import frappe
from frappe.model.document import Document

import requests


from urllib.parse import urljoin


class ContractEmployeeSetting(Document):
	pass




# def fetch_from_remote(resource):

#     settings = frappe.get_single("Integration Settings")

#     if not settings.url or not settings.api_key or not settings.api_secret:
#         frappe.throw("Integration Settings is incomplete")

#     url = urljoin(
#         settings.url,
#         f"/api/resource/{resource}"
#     )

#     headers = {
#         "Authorization": f"token {settings.api_key}:{settings.api_secret}",
#         "Accept": "application/json"
#     }

#     params = {
#         "limit_page_length": 0 
#     }

#     try:
#         resp = requests.get(
#             url,
#             headers=headers,
#             params=params,
#             timeout=30
#         )

#     except Exception as e:
#         frappe.throw(f"Connection failed: {str(e)}")

#     if resp.status_code != 200:
#         frappe.throw(f"{resource} API failed: {resp.text}")

#     return resp.json().get("data", [])


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


@frappe.whitelist()
def get_item_list():
    return fetch_from_remote("Item")


@frappe.whitelist()
def get_company_list():
    return fetch_from_remote("Company")


@frappe.whitelist()
def get_item_tax_template():
    return fetch_from_remote("Item Tax Template")


@frappe.whitelist()
def get_payment_terms_template():
    return fetch_from_remote("Purchase Taxes and Charges Template")



@frappe.whitelist()
def get_department_list():
    return fetch_from_remote("Department")


@frappe.whitelist()
def get_worklocation_list():
    return fetch_from_remote("Branch")


@frappe.whitelist()
def get_tax_with_hold_category_list():
    return fetch_from_remote("Tax Withholding Category")



@frappe.whitelist()
def get_business_category_list():
    return fetch_from_remote("Business Category")


@frappe.whitelist()
def get_business_segment_list():
    return fetch_from_remote("Business Segment")



@frappe.whitelist()
def get_workflow_policy_list():
    return fetch_from_remote("Workflow Policy")


@frappe.whitelist()
def get_bank_accounts_by_supplier(supplier_id):

    if not supplier_id:
        return []

    filters = [
        ["party_type", "=", "Supplier"],
        ["party", "=", supplier_id]
    ]

    data = fetch_from_remote("Bank Account", filters)

    # Return only names (for dropdown)
    bank_accounts = []

    for d in data:
        bank_accounts.append(d.get("name"))

    return bank_accounts