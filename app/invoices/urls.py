from django.urls import path, reverse_lazy
from core.url_names import INVOICES
from .views import InvoicePDFDownloadView
from django.views.generic import RedirectView


urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy(INVOICES.DETAIL))),
    path("view-pdf/", InvoicePDFDownloadView.as_view(), name=INVOICES.DETAIL),
]
