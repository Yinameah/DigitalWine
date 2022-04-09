# Copyright (c) 2022, Aurélien Cibrario and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Cuvee(Document):
    """ """

    def autoname(self):

        self.name = f"{self.cepage} ({self.millesime})"

    def validate(self):

        for line_no, operation in enumerate(self.operations):

            if operation.type == "Transfer":
                if operation.cuvee_dest is None:
                    frappe.throw(f"Operation in line {line_no+1} needs a destination")
            else:
                operation.cuvee_dest = None

    def before_save(self):
        pass

        # print()
        # print("DEBUG ! before_save Cuvee")
        # print(self)
        # print(type(self))
