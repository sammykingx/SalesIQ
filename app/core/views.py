from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils import timezone
from django.views.generic import View
from django.shortcuts import render


from accounts.selectors import BusinessSelector
from customers.selectors import CustomerSelector
from invoices.selectors import InvoiceSelectors
from invoices.serializers import InvoiceListResponseSchema
from products.selectors import ProductsSelector
from products.serializers import ProductListItemSchema
from public.adapters import WaitlistStorage
from .template_names import ERROR_PAGES

from datetime import datetime
from typing import Any


import json


from django_weasyprint import WeasyTemplateView
from django.views.generic import TemplateView
from decimal import Decimal

from decouple import config


class HostingerInvoiceView(WeasyTemplateView):
    template_name="invoices/hostinger-inv-v2.html"
    inv_id = "INV-2026-4ZHG-7KVI"
    
    def get_pdf_filename(self) -> str: #type:ignore
        return f"HTNGR-{self.inv_id}.pdf"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(self.invoice_context())
        return context
    
    def invoice_context(self):
        conv_rate = Decimal("1330")
        usd_subtotal = self._calc_subtotal()
        sub_total = (usd_subtotal * conv_rate).quantize(Decimal("0.01"))

        tax_rate = Decimal("7.65")
        tax_amount = ((tax_rate / Decimal("100")) * sub_total).quantize(Decimal("0.01"))
        total_amount = (sub_total + tax_amount).quantize(Decimal("0.01"))
        
        return {
            "conv_rate": conv_rate,
            "invoice_number": self.inv_id,
            "client_name": config("CUSTOMER_NAME"),
            "client_email": config("CUSTOMER_EMAIL"),
            "client_phone": config("CUSTOMER_PHONE"),
            "client_company": "The Rebirth Initiative",
            
            "issue_date": "2026-09-10",
            "due_date": "2026-10-07",
            "sub_total": sub_total,
            "tax_amount": tax_amount,
            "total_amount": total_amount,
            "items": self._line_items()
        }
        
    def _calc_subtotal(self):
        line_items = self._line_items()
        total_usd = sum(Decimal(str(item["amount"])) for item in line_items)
        return total_usd
        
    def _line_items(self):
        return [
            {
                "description": "Hosting Package Renewal",
                "details": "Includes Storage, SSL, Daily Backups & Hostinger CDN",
                "provider": "Hosting",
                "term": "12 Months",
                "amount": 189.00
            },
            {
                "description": "Primary Domain Renewal '.ORG'",
                "details": "therebirthinitiative.org",
                "provider": "Domain",
                "term": "1 Year",
                "amount": 20.99
            },
            {
                "description": "ICANN Domain Annual Fee",
                "details": "Mandatory Internet Corporation for Assigned Names and Numbers registry fee",
                "provider": "ICANN",
                "term": "1 Year",
                "amount": 7.99
            },
            {
                "description": "Domain WHOIS Privacy Protection",
                "details": "Identity Shield & Automated Spam Prevention",
                "provider": "WHOIS",
                "term": "1 Year",
                "amount": 11.85
            },
            {
                "description": "Core Infrastructure & Security",
                "details": "Secure FTP Protocols, Encrypted Mailbox, System Firewall & Core Security Hardening",
                "provider": "Hostinger",
                "term": "Annual",
                "amount": 36.50
            }
        ]

class ComingSoonView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        ctx = {
            "launch_date": timezone.make_aware(datetime(2026, 9, 25, 8, 0, 0))
        }
        return render(request, template_name="public/coming-soon.html", context=ctx)
        
    def post(self, request: HttpRequest)-> JsonResponse:
        if not request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"status": "error", "message": "Bad request."}, status=400)
        
        payload:dict = json.loads(request.body)
        payload.update(timestamp=timezone.now().isoformat())
        
        saved = WaitlistStorage().add_entry(payload)
        msg = (
            "You're on the VIP list, cheers my friend 🥂"
            if saved
            else "You're on-board ✨, stay tuned."
        )
        
        return JsonResponse({"message": msg}, status=200)
    

class BusinessJSONDataView(View):
    """
        Returns a unified payload of customers, products, and sales records 
        for client-side live search and autocomplete.
    """
    def get(self, request: HttpRequest) -> JsonResponse:
        business = BusinessSelector().get_user_business(user_email=self.request.user.email, as_instance=True) # type: ignore
        invoices = InvoiceSelectors().list_business_invoices(biz_id=business) # type: ignore
        invoices_data = [InvoiceListResponseSchema.model_validate(invoice).model_dump() for invoice in invoices ]
        
        products = ProductsSelector().get_business_products(business_id=business.id) # type: ignore
        products_data = [ProductListItemSchema.model_validate(product).model_dump() for product in products]
        
        customers_data = CustomerSelector().get_all_business_customers_frontend_json(biz_id=business.id) #type: ignore
         
        return JsonResponse({
            "customers_json": customers_data,
            "products_json": products_data,
            "invoice_json": invoices_data,
        }, status=200)
    
    
def custom_403(request: HttpRequest, exception):
    return render(request, ERROR_PAGES.FORBIDDEN, status=403)

def custom_404(request: HttpRequest, exception):
    return render(request, ERROR_PAGES.NOT_FOUND, status=404)

import sys, traceback

def custom_500(request: HttpRequest):
    exc_type, exc_value, exc_tb = sys.exc_info()
    if exc_type is not None:
        print("\n" + "="*60)
        print("--- CAPTURED 500 ERROR TRACEBACK ---")
        traceback.print_exception(exc_type, exc_value, exc_tb)
        print("="*60 + "\n")
        
    return render(request, ERROR_PAGES.INETERNAL_ERROR, status=500)
    