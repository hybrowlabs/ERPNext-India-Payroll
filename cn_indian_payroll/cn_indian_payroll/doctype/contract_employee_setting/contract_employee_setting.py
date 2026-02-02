# Copyright (c) 2026, Hybrowlabs technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

import requests

import frappe
import requests
from urllib.parse import urljoin


class ContractEmployeeSetting(Document):
	pass




@frappe.whitelist()
def get_supplier_by_tax_id():
    """
    Fetch ALL Suppliers from another ERPNext using Integration Settings
    """

    settings = frappe.get_single("Integration Settings")

    if not settings.url or not settings.api_key or not settings.api_secret:
        frappe.throw("Integration Settings is incomplete")

    url = urljoin(settings.url, "/api/resource/Supplier")


    headers = {
        "Authorization": f"token {settings.api_key}:{settings.api_secret}",
        "Accept": "application/json"
    }

    params = {
        "limit_page_length": 20
    }

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=20)
    except Exception as e:
        frappe.throw(f"Connection failed: {str(e)}")

    if resp.status_code != 200:
        frappe.throw(f"Supplier API failed: {resp.text}")


    data = resp.json().get("data", [])

    return data



@frappe.whitelist()
def get_company_list():

    settings = frappe.get_single("Integration Settings")

    if not settings.url or not settings.api_key or not settings.api_secret:
        frappe.throw("Integration Settings is incomplete")

    url = urljoin(settings.url, "/api/resource/Company")


    headers = {
        "Authorization": f"token {settings.api_key}:{settings.api_secret}",
        "Accept": "application/json"
    }

    params = {
        "limit_page_length": 20
    }


    try:
        resp = requests.get(url, headers=headers, params=params, timeout=20)
    except Exception as e:
        frappe.throw(f"Connection failed: {str(e)}")


    if resp.status_code != 200:
        frappe.throw(f"Company API failed: {resp.text}")


    data = resp.json().get("data", [])

    return data




@frappe.whitelist()
def get_item_tax_template():

    settings = frappe.get_single("Integration Settings")

    if not settings.url or not settings.api_key or not settings.api_secret:
        frappe.throw("Integration Settings is incomplete")

    url = urljoin(settings.url, "/api/resource/Item Tax Template")


    headers = {
        "Authorization": f"token {settings.api_key}:{settings.api_secret}",
        "Accept": "application/json"
    }

    params = {
        "limit_page_length": 20
    }


    try:
        resp = requests.get(url, headers=headers, params=params, timeout=20)
    except Exception as e:
        frappe.throw(f"Connection failed: {str(e)}")


    if resp.status_code != 200:
        frappe.throw(f"Company API failed: {resp.text}")


    data = resp.json().get("data", [])

    return data


@frappe.whitelist()
def get_payment_terms_template():

    settings = frappe.get_single("Integration Settings")

    if not settings.url or not settings.api_key or not settings.api_secret:
        frappe.throw("Integration Settings is incomplete")

    url = urljoin(settings.url, "/api/resource/Payment Terms Template")


    headers = {
        "Authorization": f"token {settings.api_key}:{settings.api_secret}",
        "Accept": "application/json"
    }

    params = {
        "limit_page_length": 20
    }


    try:
        resp = requests.get(url, headers=headers, params=params, timeout=20)
    except Exception as e:
        frappe.throw(f"Connection failed: {str(e)}")


    if resp.status_code != 200:
        frappe.throw(f"Company API failed: {resp.text}")


    data = resp.json().get("data", [])

    return data



@frappe.whitelist()
def get_department_list():

    settings = frappe.get_single("Integration Settings")

    if not settings.url or not settings.api_key or not settings.api_secret:
        frappe.throw("Integration Settings is incomplete")

    url = urljoin(settings.url, "/api/resource/Department")


    headers = {
        "Authorization": f"token {settings.api_key}:{settings.api_secret}",
        "Accept": "application/json"
    }

    params = {
        "limit_page_length": 20
    }


    try:
        resp = requests.get(url, headers=headers, params=params, timeout=20)
    except Exception as e:
        frappe.throw(f"Connection failed: {str(e)}")


    if resp.status_code != 200:
        frappe.throw(f"Company API failed: {resp.text}")


    data = resp.json().get("data", [])

    return data



@frappe.whitelist()
def get_worklocation_list():

    settings = frappe.get_single("Integration Settings")

    if not settings.url or not settings.api_key or not settings.api_secret:
        frappe.throw("Integration Settings is incomplete")

    url = urljoin(settings.url, "/api/resource/Branch")


    headers = {
        "Authorization": f"token {settings.api_key}:{settings.api_secret}",
        "Accept": "application/json"
    }

    params = {
        "limit_page_length": 0
    }


    try:
        resp = requests.get(url, headers=headers, params=params, timeout=20)
    except Exception as e:
        frappe.throw(f"Connection failed: {str(e)}")


    if resp.status_code != 200:
        frappe.throw(f"Company API failed: {resp.text}")


    data = resp.json().get("data", [])

    return data


# @frappe.whitelist()
# def get_business_segment_list():

#     settings = frappe.get_single("Integration Settings")

#     if not settings.url or not settings.api_key or not settings.api_secret:
#         frappe.throw("Integration Settings is incomplete")

#     url = urljoin(settings.url, "/api/resource/Branch")


#     headers = {
#         "Authorization": f"token {settings.api_key}:{settings.api_secret}",
#         "Accept": "application/json"
#     }

#     params = {
#         "limit_page_length": 0
#     }


#     try:
#         resp = requests.get(url, headers=headers, params=params, timeout=20)
#     except Exception as e:
#         frappe.throw(f"Connection failed: {str(e)}")


#     if resp.status_code != 200:
#         frappe.throw(f"Company API failed: {resp.text}")


#     data = resp.json().get("data", [])

#     return data
