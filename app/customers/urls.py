from django.urls import path, include, reverse_lazy
from django.views.generic import TemplateView, RedirectView
from core.template_names import APP_TEMPLATES
from core.url_names import CUSTOMERS
from customers.views import CreateCustomersView, BusinessCustomersListView


urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy(CUSTOMERS.LIST))),
    path("b/all/", BusinessCustomersListView.as_view(template_name=APP_TEMPLATES.CUSTOMERS.LIST), name=CUSTOMERS.LIST),
    path("add-customer/", CreateCustomersView.as_view(), name=CUSTOMERS.ADD),
]
