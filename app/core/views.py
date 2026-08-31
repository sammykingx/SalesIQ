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
            "launch_date": timezone.make_aware(datetime(2026, 9, 15, 8, 0, 0))
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
    
    
    
def custom_404(request, exception):
    return render(request, ERROR_PAGES.NOT_FOUND, status=404)


def custom_500(request):
    return render(request, ERROR_PAGES.INETERNAL_ERROR, status=500)
    