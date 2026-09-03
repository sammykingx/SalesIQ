from django.urls import path, include, reverse_lazy
from django.views.generic import TemplateView, RedirectView
from core.template_names import APP_TEMPLATES
from core.url_names import CUSTOMERS



urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy(CUSTOMERS.LIST))),
    path("b/all/", TemplateView.as_view(template_name=APP_TEMPLATES.ACCOUNTS.CUSTOMERS.LIST), name=CUSTOMERS.LIST),
    # settings namespace
]