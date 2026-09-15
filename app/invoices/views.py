from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View, TemplateView
from django_weasyprint import WeasyTemplateView

from accounts.domains.exceptions import AccountsDomainException
from core.template_names import APP_TEMPLATES
from core.url_names import INVOICES
from invoices.domains.exceptions import InvoiceDomainException
from invoices.serializers import CreateSalesInvoiceSchema, InvoiceDetailResponseSchema
from invoices.selectors import InvoiceSelectors
from invoices.services import InvoiceService
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
            invoice = InvoiceService(request=request).record_sale(sale_data=data)
            return JsonResponse({
                "title": "Sale Logged! 📈",
                "message":"Sale transaction recorded successfully. Your revenue metrics are updating.",
                "status": "success",
                "redirect": True,
                "redirect_url": reverse(INVOICES.VIEW, kwargs={ "slug": invoice.slug}),
            }, status=201)
            
        except ValidationError as err:
            return JsonResponse({
                "message": "Your data is looking a bit tragic. Fix your typos and try again.", 
                "error": format_pydantic_errors(err), 
                "status": "warning"
            }, status=422)
            
        except (AccountsDomainException, InvoiceDomainException) as err:
            return JsonResponse({
                "title": err.title,
                "message": err.message,
                "status": err.err_type,
            }, status=400)
            
        except Exception as err:
            import traceback
            traceback.print_exc()
            return JsonResponse({
                "message": "The hamsters powering our servers just went on an unscheduled coffee break. We're waking them up.",
                "status": "error"
            }, status=500)        


class InvoicesWebView(TemplateView):
    template_name = APP_TEMPLATES.INVOICE.VIEW
    invoice_selector = InvoiceSelectors()
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        inv_slug = self.kwargs.get("slug", None)
        self._invoice = self.invoice_selector.get_invoice_by_slug(slug=inv_slug)
        if self._invoice is None:
            return redirect(reverse(INVOICES.CREATE))
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        invoice = InvoiceDetailResponseSchema.model_validate(self._invoice)
        context.update({"invoice": invoice})
        return context
    

class InvoicePDFDownloadView(WeasyTemplateView):
    template_name = APP_TEMPLATES.INVOICE.INVOICE_PDF
    # pdf_attachment = True
    invoice_selector = InvoiceSelectors()
    
    def get_invoice(self):
        """
            Memoize the invoice object. It queries the DB on the first call 
            and reuses the cached instance for all subsequent calls in this request.
        """
        if not hasattr(self, '_invoice'):
            inv_slug = self.kwargs.get("slug", None)
            self._invoice = self.invoice_selector.get_invoice_by_slug(slug=inv_slug)
        return self._invoice
    
    def get_pdf_filename(self): # type:ignore
        invoice = self.get_invoice()
        return f"Invoice-{invoice.display_id}.pdf" # type: ignore
    
    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        invoice = InvoiceDetailResponseSchema.model_validate(self.get_invoice())
        context.update({"invoice": invoice})
        return context
        
