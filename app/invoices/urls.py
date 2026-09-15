from django.urls import path, reverse_lazy
from core.url_names import INVOICES
from .views import InvoicePDFDownloadView, InvoicesWebView, RecordSalesInvoiceView, InvoiceListView
from django.views.generic import RedirectView


urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy(INVOICES.LIST_SALES))),
    path("r/<slug:slug>/", InvoicesWebView.as_view(), name=INVOICES.VIEW),
    path("d/<slug:slug>/", InvoicePDFDownloadView.as_view(), name=INVOICES.DOWNLOAD),
    path("record-sale/", RecordSalesInvoiceView.as_view(), name=INVOICES.CREATE),
    path("sales/", InvoiceListView.as_view(), name=INVOICES.LIST_SALES),
]
