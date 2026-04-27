import frappe

def execute():
    data=[
            {

            "allow_in_quick_entry": 0,
            "allow_on_submit": 0,
            "bold": 0,
            "collapsible": 0,

            "columns": 0,



            "docstatus": 0,
            "doctype": "Custom Field",
            "dt": "Employee",

            "fetch_if_empty": 0,
            "fieldname": "custom_gst_number",
            "fieldtype": "Data",
            "hidden": 0,
            "hide_border": 0,
            "hide_days": 0,
            "hide_seconds": 0,
            "ignore_user_permissions": 0,
            "ignore_xss_filter": 0,
            "in_global_search": 0,
            "in_list_view": 0,
            "in_preview": 0,
            "in_standard_filter": 0,
            "insert_after": "salary_cb",
            "is_system_generated": 1,
            "is_virtual": 0,
            "label": "GST Number (In ERP)",
            "length": 0,


            "modified": "2026-02-18 09:34:51.870451",
            "module": "cn-indian-payroll",
            "name": "Employee-custom_gst_number",
            "no_copy": 0,
            "non_negative": 0,

            "permlevel": 0,

            "precision": "",
            "print_hide": 0,
            "print_hide_if_no_value": 0,

            "read_only": 0,

            "report_hide": 0,
            "reqd": 0,
            "search_index": 0,
            "show_dashboard": 0,
            "sort_options": 0,
            "translatable": 0,
            "unique": 0,

            },
            {
            "allow_in_quick_entry": 0,
            "allow_on_submit": 0,
            "bold": 0,
            "collapsible": 0,

            "columns": 0,



            "docstatus": 0,
            "doctype": "Custom Field",
            "dt": "Employee",

            "fetch_if_empty": 0,
            "fieldname": "custom_trade_name",
            "fieldtype": "Data",
            "hidden": 0,
            "hide_border": 0,
            "hide_days": 0,
            "hide_seconds": 0,
            "ignore_user_permissions": 0,
            "ignore_xss_filter": 0,
            "in_global_search": 0,
            "in_list_view": 0,
            "in_preview": 0,
            "in_standard_filter": 0,
            "insert_after": "custom_gst_number",
            "is_system_generated": 1,
            "is_virtual": 0,
            "label": "Trade Name (In ERP)",
            "length": 0,


            "modified": "2026-02-18 09:35:08.494555",
            "module": "cn-indian-payroll",
            "name": "Employee-custom_trade_name",
            "no_copy": 0,
            "non_negative": 0,

            "permlevel": 0,

            "precision": "",
            "print_hide": 0,
            "print_hide_if_no_value": 0,

            "read_only": 0,

            "report_hide": 0,
            "reqd": 0,
            "search_index": 0,
            "show_dashboard": 0,
            "sort_options": 0,
            "translatable": 0,
            "unique": 0,

            },
            {
            "allow_in_quick_entry": 0,
            "allow_on_submit": 0,
            "bold": 0,
            "collapsible": 0,

            "columns": 0,



            "docstatus": 0,
            "doctype": "Custom Field",
            "dt": "Employee",

            "fetch_if_empty": 0,
            "fieldname": "custom_supplier_id",
            "fieldtype": "Data",
            "hidden": 0,
            "hide_border": 0,
            "hide_days": 0,
            "hide_seconds": 0,
            "ignore_user_permissions": 0,
            "ignore_xss_filter": 0,
            "in_global_search": 0,
            "in_list_view": 0,
            "in_preview": 0,
            "in_standard_filter": 0,
            "insert_after": "custom_trade_name",
            "is_system_generated": 1,
            "is_virtual": 0,
            "label": "Supplier ID (In ERP)",
            "length": 0,


            "modified": "2026-02-18 09:35:22.478063",
            "module": "cn-indian-payroll",
            "name": "Employee-custom_supplier_id",
            "no_copy": 0,
            "non_negative": 0,

            "permlevel": 0,

            "precision": "",
            "print_hide": 0,
            "print_hide_if_no_value": 0,

            "read_only": 0,

            "report_hide": 0,
            "reqd": 0,
            "search_index": 0,
            "show_dashboard": 0,
            "sort_options": 0,
            "translatable": 0,
            "unique": 0,

            },
            {
            "allow_in_quick_entry": 0,
            "allow_on_submit": 0,
            "bold": 0,
            "collapsible": 0,

            "columns": 0,



            "docstatus": 0,
            "doctype": "Custom Field",
            "dt": "Employee",

            "fetch_if_empty": 0,
            "fieldname": "custom_work_flow_policy",
            "fieldtype": "Select",
            "hidden": 0,
            "hide_border": 0,
            "hide_days": 0,
            "hide_seconds": 0,
            "ignore_user_permissions": 0,
            "ignore_xss_filter": 0,
            "in_global_search": 0,
            "in_list_view": 0,
            "in_preview": 0,
            "in_standard_filter": 0,
            "insert_after": "custom_supplier_id",
            "is_system_generated": 1,
            "is_virtual": 0,
            "label": "Work Flow Policy",
            "length": 0,


            "modified": "2026-04-24 17:17:44.416902",
            "module": "cn-indian-payroll",
            "name": "Employee-custom_work_flow_policy",
            "no_copy": 0,
            "non_negative": 0,
            "options": "",
            "permlevel": 0,

            "precision": "",
            "print_hide": 0,
            "print_hide_if_no_value": 0,

            "read_only": 0,

            "report_hide": 0,
            "reqd": 0,
            "search_index": 0,
            "show_dashboard": 0,
            "sort_options": 0,
            "translatable": 0,
            "unique": 0,

            },
            {
            "allow_in_quick_entry": 0,
            "allow_on_submit": 0,
            "bold": 0,
            "collapsible": 0,

            "columns": 0,



            "docstatus": 0,
            "doctype": "Custom Field",
            "dt": "Employee",

            "fetch_if_empty": 0,
            "fieldname": "custom_business_category",
            "fieldtype": "Table",
            "hidden": 0,
            "hide_border": 0,
            "hide_days": 0,
            "hide_seconds": 0,
            "ignore_user_permissions": 0,
            "ignore_xss_filter": 0,
            "in_global_search": 0,
            "in_list_view": 0,
            "in_preview": 0,
            "in_standard_filter": 0,
            "insert_after": "custom_work_flow_policy",
            "is_system_generated": 1,
            "is_virtual": 0,
            "label": "Business Category",
            "length": 0,


            "modified": "2026-04-24 17:17:55.527857",
            "module": "cn-indian-payroll",
            "name": "Employee-custom_business_category",
            "no_copy": 0,
            "non_negative": 0,
            "options": "Business Category",
            "permlevel": 0,

            "precision": "",
            "print_hide": 0,
            "print_hide_if_no_value": 0,

            "read_only": 0,

            "report_hide": 0,
            "reqd": 0,
            "search_index": 0,
            "show_dashboard": 0,
            "sort_options": 0,
            "translatable": 0,
            "unique": 0,

            },
            {
            "allow_in_quick_entry": 0,
            "allow_on_submit": 0,
            "bold": 0,
            "collapsible": 0,

            "columns": 0,



            "docstatus": 0,
            "doctype": "Custom Field",
            "dt": "Employee",

            "fetch_if_empty": 0,
            "fieldname": "custom_business_segment",
            "fieldtype": "Table",
            "hidden": 0,
            "hide_border": 0,
            "hide_days": 0,
            "hide_seconds": 0,
            "ignore_user_permissions": 0,
            "ignore_xss_filter": 0,
            "in_global_search": 0,
            "in_list_view": 0,
            "in_preview": 0,
            "in_standard_filter": 0,
            "insert_after": "custom_business_category",
            "is_system_generated": 1,
            "is_virtual": 0,
            "label": "Business Segment",
            "length": 0,


            "modified": "2026-04-24 17:17:49.933726",
            "module": "cn-indian-payroll",
            "name": "Employee-custom_business_segment",
            "no_copy": 0,
            "non_negative": 0,
            "options": "Business Segment",
            "permlevel": 0,

            "precision": "",
            "print_hide": 0,
            "print_hide_if_no_value": 0,

            "read_only": 0,

            "report_hide": 0,
            "reqd": 0,
            "search_index": 0,
            "show_dashboard": 0,
            "sort_options": 0,
            "translatable": 0,
            "unique": 0,

            },
            {
            "allow_in_quick_entry": 0,
            "allow_on_submit": 0,
            "bold": 0,
            "collapsible": 0,

            "columns": 0,



            "docstatus": 0,
            "doctype": "Custom Field",
            "dt": "Employee",

            "fetch_if_empty": 0,
            "fieldname": "custom_bank_account_in_erp",
            "fieldtype": "Data",
            "hidden": 0,
            "hide_border": 0,
            "hide_days": 0,
            "hide_seconds": 0,
            "ignore_user_permissions": 0,
            "ignore_xss_filter": 0,
            "in_global_search": 0,
            "in_list_view": 0,
            "in_preview": 0,
            "in_standard_filter": 0,
            "insert_after": "custom_business_segment",
            "is_system_generated": 1,
            "is_virtual": 0,
            "label": "Bank Account (In ERP)",
            "length": 0,


            "modified": "2026-03-30 19:43:57.830101",
            "module": "cn-indian-payroll",
            "name": "Employee-custom_bank_account_in_erp",
            "no_copy": 0,
            "non_negative": 0,

            "permlevel": 0,

            "precision": "",
            "print_hide": 0,
            "print_hide_if_no_value": 0,

            "read_only": 0,

            "report_hide": 0,
            "reqd": 0,
            "search_index": 0,
            "show_dashboard": 0,
            "sort_options": 0,
            "translatable": 1,
            "unique": 0,

            },
            {
            "allow_in_quick_entry": 0,
            "allow_on_submit": 0,
            "bold": 0,
            "collapsible": 0,

            "columns": 0,



            "docstatus": 0,
            "doctype": "Custom Field",
            "dt": "Employee",

            "fetch_if_empty": 0,
            "fieldname": "custom_business_department",
            "fieldtype": "Table",
            "hidden": 0,
            "hide_border": 0,
            "hide_days": 0,
            "hide_seconds": 0,
            "ignore_user_permissions": 0,
            "ignore_xss_filter": 0,
            "in_global_search": 0,
            "in_list_view": 0,
            "in_preview": 0,
            "in_standard_filter": 0,
            "insert_after": "custom_business_segment",
            "is_system_generated": 1,
            "is_virtual": 0,
            "label": "Department",
            "length": 0,


            "modified": "2026-04-24 17:17:49.933726",
            "module": "cn-indian-payroll",
            "name": "Employee-custom_business_department",
            "no_copy": 0,
            "non_negative": 0,
            "options": "Business Department",
            "permlevel": 0,

            "precision": "",
            "print_hide": 0,
            "print_hide_if_no_value": 0,

            "read_only": 0,

            "report_hide": 0,
            "reqd": 0,
            "search_index": 0,
            "show_dashboard": 0,
            "sort_options": 0,
            "translatable": 0,
            "unique": 0,

            },

            {
            "allow_in_quick_entry": 0,
            "allow_on_submit": 0,
            "bold": 0,
            "collapsible": 0,

            "columns": 0,

            "docstatus": 0,
            "doctype": "Custom Field",
            "dt": "Employee",

            "fetch_if_empty": 0,
            "fieldname": "custom_location_in_erp",
            "fieldtype": "Select",
            "hidden": 0,
            "hide_border": 0,
            "hide_days": 0,
            "hide_seconds": 0,
            "ignore_user_permissions": 0,
            "ignore_xss_filter": 0,
            "in_global_search": 0,
            "in_list_view": 0,
            "in_preview": 0,
            "in_standard_filter": 0,
            "insert_after": "custom_business_department",
            "is_system_generated": 1,
            "is_virtual": 0,
            "label": "Location (In ERP)",
            "length": 0,


            "modified": "2026-03-30 19:43:57.830101",
            "module": "cn-indian-payroll",
            "name": "Employee-custom_location_in_erp",
            "no_copy": 0,
            "non_negative": 0,

            "permlevel": 0,

            "precision": "",
            "print_hide": 0,
            "print_hide_if_no_value": 0,

            "read_only": 0,
            "options":"",

            "report_hide": 0,
            "reqd": 0,
            "search_index": 0,
            "show_dashboard": 0,
            "sort_options": 0,
            "translatable": 1,
            "unique": 0,

            },
    ]
    for i in data:
        insert_record(i)

def insert_record(i):
    if not frappe.db.exists("Custom Field", i["name"]):
        doc = frappe.new_doc("Custom Field")
        doc.update(i)
        doc.save()