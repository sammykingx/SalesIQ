from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils import timezone
from django.views.generic import View
from django.shortcuts import render
from .template_names import ERROR_PAGES

from accounts.selectors import BusinessSelector
from customers.selectors import CustomerSelector
from invoices.selectors import InvoiceSelectors
from products.selectors import ProductsSelector

from products.serializers import ProductListItemSchema
from invoices.serializers import InvoiceListResponseSchema
from public.adapters import WaitlistStorage
from datetime import datetime

import json


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
    
    
def custom_404(request: HttpRequest, exception):
    return render(request, ERROR_PAGES.NOT_FOUND, status=404)

import sys
import traceback

def custom_500(request: HttpRequest):
    exc_type, exc_value, exc_tb = sys.exc_info()
    if exc_type is not None:
        print("\n" + "="*60)
        print("--- CAPTURED 500 ERROR TRACEBACK ---")
        traceback.print_exception(exc_type, exc_value, exc_tb)
        print("="*60 + "\n")
        
    return render(request, ERROR_PAGES.INETERNAL_ERROR, status=500)
    