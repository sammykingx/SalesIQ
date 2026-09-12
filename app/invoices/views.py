from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django_weasyprint import WeasyTemplateView
from core.template_names import APP_TEMPLATES


class RecordSalesView(LoginRequiredMixin, View):
    pass

class InvoicePDFDownloadView(WeasyTemplateView):
    template_name = APP_TEMPLATES.INVOICE.VIEW
    pdf_filename = "invoice-INV-2026-08811.pdf"
    find_staticfiles_with_django = True
