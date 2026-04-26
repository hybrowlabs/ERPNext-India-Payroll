import frappe


def execute():
    old_table = "tabEmployee Perquisit Information"
    new_table = "tabEmployee Perquisite Information"

    # Only rename if the old table still exists and the new one doesn't
    if frappe.db.table_exists(old_table) and not frappe.db.table_exists(new_table):
        frappe.db.sql(  # noqa: S608
            f"RENAME TABLE `{old_table}` TO `{new_table}`"  # noqa: S608
        )

    # Update the DocType record name if it still has the old spelling
    if frappe.db.exists("DocType", "Employee Perquisit Information"):
        frappe.db.set_value(
            "DocType",
            "Employee Perquisit Information",
            "name",
            "Employee Perquisite Information",
            update_modified=False,
        )
