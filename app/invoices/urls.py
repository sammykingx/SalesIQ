from django.views.generic import TemplateView
from django.urls import path, reverse_lazy
from core.template_names import APP_TEMPLATES
from core.url_names import INVOICES
from .views import InvoicePDFDownloadView, InvoicesWebView, RecordSalesInvoiceView
from django.views.generic import RedirectView


urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy(INVOICES.VIEW))),
    path("view-pdf/", InvoicesWebView.as_view(), name=INVOICES.VIEW),
    path("download-receipt/", InvoicePDFDownloadView.as_view(), name=INVOICES.DOWNLOAD),
    path("record-sale/", RecordSalesInvoiceView.as_view(), name=INVOICES.CREATE),
    path("sales/", TemplateView.as_view(template_name=APP_TEMPLATES.SALES.LIST), name=INVOICES.LIST_SALES),
]
