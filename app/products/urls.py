from django.urls import path, include, reverse_lazy
from django.views.generic import TemplateView, RedirectView
from core.template_names import APP_TEMPLATES
from core.url_names import PRODUCTS
from products.views import CreateProductsView, ProductsListView, ProductDetailView, UpdateProductsView


urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy(PRODUCTS.LIST))),
    path("all/", ProductsListView.as_view(), name=PRODUCTS.LIST),
    path("update-product/", UpdateProductsView.as_view(), name=PRODUCTS.UPDATE),
    path("add-products/", CreateProductsView.as_view(), name=PRODUCTS.ADD),
    path("detail/", ProductDetailView.as_view(), name=PRODUCTS.DETAIL),
]
