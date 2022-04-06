# Copyright (c) 2022, Aurélien Cibrario and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Parcelle(Document):

    # It seems that Virtual DocField is very buggy ...
    # @property
    # def full_name(self):
    #     """
    #     Give a value to a virtual DocField by extending the DocType controller

    #     the property name is the same than the DocField name
    #     """
    #     return f"hello world - {self.no_cadastre}"

    def before_save(self):
        self.full_name = f"{self.no} - {self.lieu_dit} ({self.no_cadastre})"
