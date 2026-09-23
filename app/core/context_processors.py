from django.http import HttpRequest
from django.conf import settings
from core.nav_tree import SIDEBAR_NAV_TREE
from core.url_names import ACCOUNTS, BUSINESS_DATA, CUSTOMERS, PRODUCTS, INVOICES, METRICS


def url_name_registry(request: HttpRequest):
    return {
        "ACCOUNTS": ACCOUNTS,
        "CUSTOMERS": CUSTOMERS,
        "PRODUCTS": PRODUCTS,
        "INVOICES": INVOICES,
        "BUSINESS_DATA": BUSINESS_DATA,
        "METRICS": METRICS,
    }
    
def template_context(request: HttpRequest):
    is_previledged = False
    if request.user.is_authenticated:
        is_previledged = True if request.user.email in settings.PREVILEDGE_USERS else False # type: ignore
    return {
        "sidebar_nav_tree": SIDEBAR_NAV_TREE,
        "is_previledged": is_previledged,
    }