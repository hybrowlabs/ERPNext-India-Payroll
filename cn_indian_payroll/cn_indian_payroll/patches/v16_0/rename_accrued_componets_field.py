import frappe


def execute():
    dt = "Accrued Components"
    old_name = "accrued_componets"
    new_name = "accrued_components"

    if not frappe.db.exists("Custom Field", {"fieldname": old_name, "dt": dt}):
        if frappe.db.has_column(f"tab{dt}", old_name):
            frappe.db.sql(  # noqa: S608
                f"ALTER TABLE `tab{dt}` CHANGE `{old_name}` `{new_name}` VARCHAR(140) DEFAULT NULL"
            )
        return

    frappe.db.set_value("Custom Field", {"fieldname": old_name, "dt": dt}, "fieldname", new_name)

    if frappe.db.has_column(f"tab{dt}", old_name):
        frappe.db.sql(  # noqa: S608
            f"ALTER TABLE `tab{dt}` CHANGE `{old_name}` `{new_name}` VARCHAR(140) DEFAULT NULL"
        )

    frappe.clear_cache(doctype=dt)
