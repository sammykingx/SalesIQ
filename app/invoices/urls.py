from django.urls import path, reverse_lazy
from core.url_names import INVOICES
from .views import InvoicePDFDownloadView, InvoicesWebView
from django.views.generic import RedirectView


urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy(INVOICES.VIEW))),
    path("view-pdf/", InvoicesWebView.as_view(), name=INVOICES.VIEW),
    path("download-receipt/", InvoicePDFDownloadView.as_view(), name=INVOICES.DOWNLOAD),
]
