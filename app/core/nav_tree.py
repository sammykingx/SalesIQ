from django.urls import reverse_lazy
from .url_names import PRODUCTS, CUSTOMERS, SALES, INVOICES


SIDEBAR_NAV_TREE = [
    {
        "group_name": "products",
        "group_label": "Products",
        "group_icon": "store",
        "group_url": PRODUCTS.LIST,
        "group_children": [
            {"child_name": "products_list", "child_label": "All Products", "child_url": PRODUCTS.LIST},
            {"child_name": "products_add", "child_label": "Add Product", "child_url": PRODUCTS.ADD},
        ],
    },
    {
        "group_name": "customers",
        "group_label": "Customers",
        "group_icon": "users",
        "group_url": CUSTOMERS.LIST,
        "group_children": [
            {"child_name": "customers_list", "child_label": "All Customers", "child_url": reverse_lazy(CUSTOMERS.LIST)},
            {"child_name": "customers_add", "child_label": "Add Customer", "child_url": CUSTOMERS.ADD},
        ],
    },
    {
        "group_name": "sales",
        "group_label": "Sales",
        "group_icon": "shopping-cart",
        "group_url": SALES.LIST,
        "group_children": [
            {"child_name": "sales_list", "child_label": "All Sales", "child_url": SALES.LIST},
            {"child_name": "sales_add", "child_label": "Record Sale", "child_url": SALES.ADD},
        ],
    },
    {
        "group_name": "invoices",
        "group_label": "Invoices",
        "group_icon": "file-text",
        "group_url":  "#" #INVOICES.LIST,
    },
    {
        "group_name": "reports",
        "group_label": "Reports",
        "group_icon": "bar-chart-2",
        "group_url": "#",
    },
]
