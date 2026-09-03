from core.nav_tree import SIDEBAR_NAV_TREE
from core.url_names import ACCOUNTS


def url_name_registry(request):
    return {
        "ACCOUNTS": ACCOUNTS,
    }
    
def template_context(request):
    return {
        "sidebar_nav_tree": SIDEBAR_NAV_TREE,
    }