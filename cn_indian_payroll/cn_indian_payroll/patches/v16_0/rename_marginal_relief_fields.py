import frappe


def execute():
    """Rename misspelled Custom Field fieldnames on Income Tax Slab."""
    renames = [
        ("custom_minmum_value", "custom_minimum_value"),
        ("custom_maximun_value", "custom_maximum_value"),
    ]

    for old_name, new_name in renames:
        if frappe.db.exists("Custom Field", {"fieldname": old_name, "dt": "Income Tax Slab"}):
            frappe.db.set_value(
                "Custom Field",
                {"fieldname": old_name, "dt": "Income Tax Slab"},
                "fieldname",
                new_name,
            )

            if frappe.db.has_column("tabIncome Tax Slab", old_name):
                frappe.db.sql(  # noqa: S608
                    f"ALTER TABLE `tabIncome Tax Slab`"
                    f" CHANGE `{old_name}` `{new_name}` DECIMAL(21,9) DEFAULT NULL"
                )

    frappe.clear_cache(doctype="Income Tax Slab")
