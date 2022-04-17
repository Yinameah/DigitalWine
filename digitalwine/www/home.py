import frappe


def get_context(context):
    context["variable"] = " my very own injected variable"

    return context

    context = {
        "top_bar_items": [],
        "footer_items": [],
        "post_login": [
            {"label": "My Account", "url": "/me"},
            {"label": "Log out", "url": "/?cmd=web_logout"},
        ],
        "banner_html": None,
        "banner_image": None,
        "brand_html": None,
        "copyright": None,
        "disable_signup": 0,
        "hide_footer_signup": 0,
        "head_html": None,
        "title_prefix": None,
        "navbar_template": None,
        "footer_template": None,
        "navbar_search": 0,
        "enable_view_tracking": 0,
        "footer_logo": None,
        "call_to_action": None,
        "call_to_action_url": None,
        "show_language_picker": 0,
        "footer_powered": None,
        "facebook_share": 0,
        "google_plus_one": 0,
        "twitter_share": 0,
        "linked_in_share": 0,
        "url": "http://localhost:8000",
        "encoded_title": "",
        "web_include_js": ["website_script.js"],
        "web_include_css": [],
        "theme": "<WebsiteTheme: Standard>",
        "favicon": "/assets/frappe/images/frappe-favicon.svg",
        "hide_login": 0,
        "base_template": None,
        "basepath": "/home/aurelien/sketchbook/erpnext/digitalwine_bench/apps/digitalwine/digitalwine/www",
        "basename": "/home/aurelien/sketchbook/erpnext/digitalwine_bench/apps/digitalwine/digitalwine/www/home",
        "name": "home",
        "path": "home",
        "route": "home",
        "template": "www/home.html",
        "build_version": "LpHunzeK",
    }
