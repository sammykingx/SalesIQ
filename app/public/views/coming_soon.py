from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils import timezone
from django.views.generic import View
from django.shortcuts import render

from datetime import datetime

import logging

logger = logging.getLogger(__name__)


class ComingSoonView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        ctx = {
            "launch_date": timezone.make_aware(datetime(2026, 9, 14, 8, 0, 0))
        }
        return render(request, template_name="public/coming-soon.html", context=ctx)
        
    def post(self, request: HttpRequest)-> JsonResponse:
        print("POST request body received: %s", request.body)
        return JsonResponse({"status": 200})
    