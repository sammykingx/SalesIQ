from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View, TemplateView
from django_weasyprint import WeasyTemplateView

from core.template_names import APP_TEMPLATES
from core.url_names import INVOICES
from invoices.serializers import CreateSalesInvoiceSchema
from utils.pydantic_formatter import format_pydantic_errors

from pydantic import ValidationError
from typing import Any, Dict

class RecordSalesInvoiceView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, APP_TEMPLATES.SALES.ADD)
    
    def post(self, request:HttpRequest):
        try:
            data = CreateSalesInvoiceSchema.model_validate_json(request.body, strict=True)
            print(data.model_dump_json(indent=2))
            return JsonResponse({
                "title": "Sale Logged! 📈",
                "message":"Sale transaction recorded successfully. Your revenue metrics are updating.",
                "status": "success",
                "redirect": True,
                "redirec_url": reverse(INVOICES.VIEW),
            }, status=201)
            
        except ValidationError as err:
            print(format_pydantic_errors(err))
            return JsonResponse({
                "message": "Your data is looking a bit tragic. Fix your typos and try again.", 
                "error": format_pydantic_errors(err), 
                "status": "warning"
            }, status=422)
            
        except Exception as err:
            import traceback
            traceback.print_exc()
            return JsonResponse({
                "message": "The hamsters powering our servers just went on an unscheduled coffee break. We're waking them up.",
                "status": "error"
            }, status=500)        

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
