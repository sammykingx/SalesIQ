from core.nav_tree import SIDEBAR_NAV_TREE
from core.url_names import ACCOUNTS, CUSTOMERS, PRODUCTS, INVOICES, SALES


def url_name_registry(request):
    return {
        "ACCOUNTS": ACCOUNTS,
        "CUSTOMERS": CUSTOMERS,
        "PRODUCTS": PRODUCTS,
        "INVOICES": INVOICES,
        "SALES": SALES,
    }
    
def template_context(request):
    return {
        "sidebar_nav_tree": SIDEBAR_NAV_TREE,
    }