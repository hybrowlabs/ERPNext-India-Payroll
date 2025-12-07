import frappe
from frappe.handler import execute_cmd
from frappe.core.doctype.user.user import update_password as core_update_password


@frappe.whitelist(allow_guest=True)
def direct_reset_password(user, new_password):
    """Reset password without email link"""

    # Check user exists
    if not frappe.db.exists("User", user):
        return {"status": "failed", "message": "User does not exist"}

    try:
        # Load user doc
        user_doc = frappe.get_doc("User", user)

        # Set the new password
        user_doc.new_password = new_password
        user_doc.save(ignore_permissions=True)

        return {"status": "success", "message": "Password updated successfully"}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Password Reset Error")
        return {"status": "failed", "message": str(e)}
