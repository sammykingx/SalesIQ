from django.http import HttpRequest
from django.conf import settings
from core.nav_tree import SIDEBAR_NAV_TREE, BACK_OFFICE_URLS
from core.url_names import ACCOUNTS, BUSINESS_DATA, CUSTOMERS, PRODUCTS, INVOICES, METRICS, PLATFORM_OPS


def url_name_registry(request: HttpRequest):
    return {
        "ACCOUNTS": ACCOUNTS,
        "CUSTOMERS": CUSTOMERS,
        "PRODUCTS": PRODUCTS,
        "INVOICES": INVOICES,
        "BUSINESS_DATA": BUSINESS_DATA,
        "METRICS": METRICS,
        "PLATFORM_OPS": PLATFORM_OPS, 
    }
    
def template_context(request: HttpRequest):
    is_previledged = False
    user = getattr(request, "user", None)
    logged_in = getattr(user, "is_authenticated", False)
    if logged_in:
        is_previledged = True if request.user.email in settings.PREVILEDGE_USERS else False # type: ignore
    return {
        "sidebar_nav_tree": SIDEBAR_NAV_TREE,
        "back_office_urls": BACK_OFFICE_URLS,
        "is_previledged": is_previledged,
    }
