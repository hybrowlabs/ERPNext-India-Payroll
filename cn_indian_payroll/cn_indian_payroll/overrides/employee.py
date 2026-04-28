import frappe
import requests
from urllib.parse import urljoin


def before_save(doc, method):
    payroll_settings = frappe.get_single("Payroll Settings")

    allowed_types = [
        d.employment_type
        for d in payroll_settings.custom_hide_salary_structure_configuration or []
    ]

    if doc.employment_type in allowed_types and not doc.custom_bank_account_in_erp:
        if doc.custom_supplier_id and (
            not doc.custom_bank_account_in_erp
            or doc.has_value_changed("custom_supplier_id")
        ):
            bank_accounts = get_bank_accounts_by_supplier(doc.custom_supplier_id)

            if bank_accounts:
                doc.custom_bank_account_in_erp = bank_accounts[0]



def fetch_from_remote(resource, filters=None):

    settings = frappe.get_single("Integration Settings")

    if not settings.url or not settings.api_key or not settings.api_secret:
        frappe.throw("Integration Settings is incomplete")

    url = urljoin(settings.url, f"/api/resource/{resource}")

    headers = {
        "Authorization": f"token {settings.api_key}:{settings.api_secret}",
        "Accept": "application/json"
    }

    params = {
            "limit_page_length": 1,   
            "fields": '["name"]'      
        }

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
def get_bank_accounts_by_supplier(custom_supplier_id):

    if not custom_supplier_id:
        return []

    filters = [
        ["party_type", "=", "Supplier"],
        ["party", "=", custom_supplier_id]
    ]

    data = fetch_from_remote("Bank Account", filters)

    # Return only names
    # bank_accounts = [d.get("name") for d in data]

    return [d.get("name") for d in data]