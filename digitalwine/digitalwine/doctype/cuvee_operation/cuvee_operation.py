# Copyright (c) 2022, Aurélien Cibrario and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class CuveeOperation(Document):
    """
    NOTE : this is a child document.

    As far as I understood, child document can only be updated
    via their parent.
    
    And it seems that validate() or save() method are not called when
    updating the parent document. So the usefullness of this class might
    be rather limited ....
    """
