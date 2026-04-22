"""
Helpers for programmatic creation, deletion and visibility-toggling of
Custom Fields.  Mirrors india_compliance.utils.custom_fields so the pattern
is consistent across the bench.
"""

import functools
from collections.abc import Iterable

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _normalise(doctypes_or_str: str | tuple, fields: list | dict) -> tuple[tuple, list]:
    """Return (tuple-of-doctypes, list-of-fields) regardless of input shape."""
    if isinstance(doctypes_or_str, str):
        doctypes_or_str = (doctypes_or_str,)
    if isinstance(fields, dict):
        fields = [fields]
    return doctypes_or_str, fields


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def make_custom_fields(
    custom_fields: dict,
    module_name: str,
    *args,
    **kwargs,
) -> None:
    """
    Stamp every field dict with ``module_name`` then delegate to
    ``frappe.custom…create_custom_fields``.

    Using the module stamp means the fields are tied to this app in the
    Frappe UI (Customize Form → Originates From).
    """
    for _doctypes, fields in custom_fields.items():
        if isinstance(fields, dict):
            fields = [fields]
        for field in fields:
            field.setdefault("module", module_name)

    create_custom_fields(custom_fields, *args, **kwargs)


def get_custom_fields_creator(module_name: str):
    """
    Return a ``create_custom_fields``-compatible callable that automatically
    stamps every field with *module_name*.

    Usage::

        _create = get_custom_fields_creator("Indian Payroll")
        _create(CUSTOM_FIELDS, ignore_validate=True)
    """
    return functools.partial(make_custom_fields, module_name=module_name)


def delete_custom_fields(custom_fields: dict) -> None:
    """
    Remove every Custom Field defined in *custom_fields* and clear the
    relevant DocType caches.

    *custom_fields* has the same shape used by ``create_custom_fields``::

        {
            "DocType": [{fieldname: "...", ...}, ...],
            ("DocTypeA", "DocTypeB"): [{fieldname: "...", ...}],
        }
    """
    for doctypes, fields in custom_fields.items():
        doctypes, fields = _normalise(doctypes, fields)

        for doctype in doctypes:
            frappe.db.delete(
                "Custom Field",
                {
                    "fieldname": ("in", [f["fieldname"] for f in fields]),
                    "dt": doctype,
                },
            )
            frappe.clear_cache(doctype=doctype)


def toggle_custom_fields(custom_fields: dict, *, show: bool) -> None:
    """
    Bulk-show or bulk-hide custom fields without recreating them.

    Useful when a dependent app is installed / uninstalled at runtime.

    :param custom_fields: same shape as ``create_custom_fields``
    :param show: ``True`` → unhide; ``False`` → hide
    """
    hidden_value = int(not show)

    for doctypes, fields in custom_fields.items():
        doctypes, fields = _normalise(doctypes, fields)

        for doctype in doctypes:
            frappe.db.set_value(
                "Custom Field",
                {
                    "dt": doctype,
                    "fieldname": ("in", [f["fieldname"] for f in fields]),
                },
                "hidden",
                hidden_value,
            )
            frappe.clear_cache(doctype=doctype)


def delete_fields_by_name(
    fieldnames: str | Iterable[str],
    doctypes: str | Iterable[str],
) -> None:
    """
    Delete specific fields by *fieldname* from one or more *doctypes*.

    Convenience wrapper for migration patches that need to clean up
    renamed or obsolete fields.
    """
    if isinstance(fieldnames, str):
        fieldnames = (fieldnames,)
    if isinstance(doctypes, str):
        doctypes = (doctypes,)

    frappe.db.delete(
        "Custom Field",
        {
            "fieldname": ("in", list(fieldnames)),
            "dt": ("in", list(doctypes)),
        },
    )
