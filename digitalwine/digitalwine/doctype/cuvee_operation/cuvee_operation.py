# Copyright (c) 2022, Aurélien Cibrario and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CuveeOperation(Document):
    """
    Apparently, validate & co should be in parent doctype
    So I wonder why this file only exists ...
    """
