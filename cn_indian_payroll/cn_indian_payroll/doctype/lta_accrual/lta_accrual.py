# Copyright (c) 2026, Hybrowlabs technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class LTAAccrual(Document):
    def validate(self):
        if self.date:
            self.year = getdate(self.date).year
