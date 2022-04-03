# Copyright (c) 2022, Aurélien Cibrario and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Cuvee(Document):
    """ """

    def before_save(self):

        print()
        print("DEBUG ! before_save Cuvee")
        print(self)
        print(type(self))

        self.dummy = "bar"
