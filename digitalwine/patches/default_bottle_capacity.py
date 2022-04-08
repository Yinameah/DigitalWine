import frappe


def execute():
    default_bottle_capacity = [
        {
            "doctype": "Bottle Capacity",
            "name": "Magnum",
            "capacity_cl": 150.0,
        },
        {
            "doctype": "Bottle Capacity",
            "name": "75cl",
            "capacity_cl": 75.0,
        },
        {
            "doctype": "Bottle Capacity",
            "name": "50cl",
            "capacity_cl": 50.0,
        },
        {
            "doctype": "Bottle Capacity",
            "name": "37.5cl",
            "capacity_cl": 37.5,
        },
    ]
    for bottle_capacity in default_bottle_capacity:

        try:
            doc = frappe.get_doc(bottle_capacity)
            doc.insert()
        except frappe.exceptions.DuplicateEntryError:
            pass
