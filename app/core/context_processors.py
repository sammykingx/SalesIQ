from django.http import HttpRequest
from core.nav_tree import SIDEBAR_NAV_TREE
from core.url_names import ACCOUNTS, CUSTOMERS, PRODUCTS, INVOICES


def url_name_registry(request: HttpRequest):
    return {
        "ACCOUNTS": ACCOUNTS,
        "CUSTOMERS": CUSTOMERS,
        "PRODUCTS": PRODUCTS,
        "INVOICES": INVOICES,
    }
    
def template_context(request: HttpRequest):
    return {
        "sidebar_nav_tree": SIDEBAR_NAV_TREE,
    }