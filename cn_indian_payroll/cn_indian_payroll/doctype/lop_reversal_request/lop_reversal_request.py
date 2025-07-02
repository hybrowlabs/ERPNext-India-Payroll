# Copyright (c) 2025, Hybrowlabs technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class LOPReversalRequest(Document):
    def validate(self):
        # Fetch all other LOP Reversal Requests for this employee/salary_slip/month
        filters = {
            "employee": self.employee,
            "salary_slip": self.salary_slip,
            "select_the_month_to_reverse": self.select_the_month_to_reverse,
            "docstatus": ["in", [0, 1]],  # Include draft and submitted documents
        }

        # Exclude current document if it's already saved (update scenario)
        if self.name:
            filters["name"] = ["!=", self.name]

        existing_requests = frappe.get_all(
            "LOP Reversal Request", filters=filters, fields=["*"]
        )

        # Sum the existing planned days
        total_existing_days = sum(
            [
                d.get("number_of_days_planning_to_reverse", 0) or 0
                for d in existing_requests
            ]
        )

        total_planned = total_existing_days + (
            self.number_of_days_planning_to_reverse or 0
        )

        if total_planned > (self.max_days or 0):
            frappe.throw(
                _(
                    "The number of days planned for reversal cannot exceed the total Max days."
                )
            )
