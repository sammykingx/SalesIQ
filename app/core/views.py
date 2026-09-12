from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils import timezone
from django.views.generic import View
from django.shortcuts import render
from .template_names import ERROR_PAGES


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
    

class BusinessSearchDataView(LoginRequiredMixin, View):
    """
    Returns a unified payload of customers, products, and sales records 
    for client-side live search and autocomplete.
    """
    def get(self, request: HttpRequest) -> JsonResponse:
        from products.domain.demo_data import PRODUCTS_DATA
        return JsonResponse({
            "products": PRODUCTS_DATA,
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
    