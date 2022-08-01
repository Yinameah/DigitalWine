import frappe


def get_context(context):

    products = frappe.get_list(
        "Product Wine",
        filters={"published": 1},
        order_by="cuvee",
        fields=["cuvee", "cepage"],
    )

    cur_cuvee = None

    cuvees = []

    for product in products:
        if product.cuvee != cur_cuvee:
            cur_cuvee = product.cuvee
            cuvees.append(product)

    context["cuvees"] = cuvees
