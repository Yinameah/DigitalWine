import frappe


@frappe.whitelist()
def test_action(*args, **kwargs):
    print("args:", args)
    print("kwargs:", kwargs)
    print("hello from an action ;-)")
