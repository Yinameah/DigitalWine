# Copyright (c) 2022, Aurélien Cibrario and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe.contacts.address_and_contact import load_address_and_contact


class WineCustomer(Document):
    def onload(self):
        #####################
        # Addresse à la ERPNEXT
        #####################
        # This fucking function put 'addr_list' in frm.doc.__onload (js)
        # and this is required for frappe.contacts.render_address_and_contact (js)
        # to actually grab a HTML field named address_html and fill it with Addresses
        load_address_and_contact(self, key=None)
