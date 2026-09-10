from django.urls import path, include, reverse_lazy
from django.views.generic import TemplateView, RedirectView
from core.template_names import APP_TEMPLATES
from core.url_names import PRODUCTS
from products.views import CreateProductsView, ProductsListView, ModifyProductView


urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy(PRODUCTS.LIST))),
    path("all/", ProductsListView.as_view(), name=PRODUCTS.LIST),
    path("modify/", ModifyProductView.as_view(), name=PRODUCTS.DETAIL),
    path("add-products/", CreateProductsView.as_view(), name=PRODUCTS.ADD),
]
