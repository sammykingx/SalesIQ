from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django_weasyprint import WeasyTemplateView
from core.template_names import APP_TEMPLATES
from typing import Any, Dict

class RecordSalesView(LoginRequiredMixin, View):
    pass

class InvoicesWebView(TemplateView):
    template_name = APP_TEMPLATES.INVOICE.VIEW
    
    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(self.template_context())
        return context
    
    def template_context(self) -> Dict[str, Any]:
        from invoices.domains import demo_data
        return demo_data.get_demo_invoice_context()
    
class InvoicePDFDownloadView(WeasyTemplateView):
    template_name = APP_TEMPLATES.INVOICE.INVOICE_PDF
    pdf_filename = "invoice-INV-2026-08711.pdf"
    find_staticfiles_with_django = True
    
    # Set PDF filename dynamically
    # def get_pdf_filename(self):
    #     invoice_ref = self.kwargs.get("invoice_ref", "invoice")
    #     return f"Invoice_{invoice_ref}.pdf"
    
    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(self.template_context())
        return context
        
    def template_context(self) -> Dict[str, Any]:
        from invoices.domains import demo_data
        return demo_data.get_demo_invoice_context()
