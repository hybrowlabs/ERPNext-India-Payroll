"""
App lifecycle helpers — called by install.py and uninstall.py.

Keeping the logic here (separate from the thin CLI entry points) means
it can also be invoked from migration patches or test fixtures without
duplicating code.
"""

import click
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

from cn_indian_payroll.cn_indian_payroll.constants.custom_fields import CUSTOM_FIELDS
from cn_indian_payroll.cn_indian_payroll.utils.custom_fields import delete_custom_fields


def after_install() -> None:
    """Create all custom fields for the Indian Payroll app."""
    try:
        create_custom_fields(CUSTOM_FIELDS, ignore_validate=True)
        frappe.db.commit()
        click.secho("Indian Payroll — custom fields installed.", fg="green")
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Indian Payroll install error")
        click.secho(
            "Indian Payroll — custom field installation failed. Check Error Log.",
            fg="red",
        )
        raise


def before_uninstall() -> None:
    """Remove all custom fields owned by this app."""
    try:
        delete_custom_fields(CUSTOM_FIELDS)
        frappe.db.commit()
        click.secho("Indian Payroll — custom fields removed.", fg="green")
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Indian Payroll uninstall error")
        click.secho(
            "Indian Payroll — custom field removal failed. Check Error Log.",
            fg="red",
        )
        raise
