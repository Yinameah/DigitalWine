from frappe.contacts.doctype.address.address import Address


class CustomAddress(Address):
    def autoname(self):
        pass
