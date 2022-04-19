# Copyright (c) 2022, Aurélien Cibrario and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.website.website_generator import WebsiteGenerator

# This is added when making doctype "has web view" with annoying bug that remove mandatory line above
# from frappe.website.website_generator import WebsiteGenerator


def get_list_context(context):
    """
    This gives context to the list view
    """

    # context.parents = [{"name": "Home", "route": "/"}]
    #     context.title = "Products"
    #     context.products = frappe.get_all(
    #         "Product Wine",
    #         # fields=["name", "price", "millesime", "route"],
    #         fields=["*"],
    #         filters={"published": True},
    #     )

    #     # Ok, this doesn't work, plus it seems that get_list_context is called twice ...
    #     # need to dig this ...
    #     context.template = "my_custom_list_template.html"

    #############################
    ## LIST TEMPLATE
    #############################
    # So ...
    # In frappe/www/list.html, the {% block page_content %} make use of 3 variables :
    #   - {{introduction}}
    #        If set, it is displayed in a <p>
    #   - {{list_template}}
    #        If set, it includes the corresponding template ({{list_template}} is a path)
    #        If not, it default to /templates/includes/list/list.html (if frappe/)
    #        NOTE : if provided here, the path in context.list_template will start
    #        in apps/digitalwine/..., so not sure how it works to find the templates.
    #   - {{list_footer}}
    #        Is displayed as-if if set.
    #############################
    context.list_template = "templates/product_wine_list.html"

    # FOR DEBUG
    # contextCopy = dict(context)
    # context["all_list_context"] = contextCopy


class ProductWine(WebsiteGenerator):

    # Very weird way to declare a few stuff
    website = frappe._dict(
        # NOTE : Here, I can declare a template, for the Item Page.
        # If not declared, the defaults :
        #       - digitalwine/doctype/MyDoctype/template/mydoctype.html
        #       - digitalwine/doctype/MyDoctype/template/mydoctype_row.html
        # are used, which makes sense
        # template="... useless custom path ..."
        # NOTE : condition_field is mandatory, otherwise, everybody is shown
        # and unpublished items are routed with /None, which is a bug in my opinion..
        condition_field="published",
        # Which field to use as title in the item page
        page_title_field="name",
    )

    def get_context(self, context):
        """
        This gives context (available in jinja2) for the item page view
        """
        # This adds breadcrumbs, probably an {% if ... %} below
        # not sure about name/title, maybe a translation stuff, or something
        # with the title parameter in DocType
        context.parents = [
            {"name": "home", "title": "Home", "route": "/"},
            {"name": "product", "title": "Products", "route": "/product"},
        ]

        contextCopy = dict(context)
        context["all_context"] = contextCopy

    def autoname(self):
        cuvee = frappe.get_doc("Cuvee", self.cuvee)
        self.name = f"{cuvee.cepage} - {cuvee.millesime} - {self.bottle_capacity}"

    def before_save(self):
        # TODO : this should be achieved with fetch_from
        cuvee = frappe.get_doc("Cuvee", self.cuvee)
        self.millesime = cuvee.millesime
        self.cepage = cuvee.cepage
