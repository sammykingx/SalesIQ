from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.generic import View

from accounts.selectors import BusinessSelector
from accounts.selectors.business import ADOPTION_THRESHOLDS
from invoices.selectors import InvoiceSelectors
from typing import Any


class PlatformGmvTrendView(LoginRequiredMixin, View):
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        user = request.user
        if user.email not in settings.PREVILEDGE_USERS: # type: ignore
            return JsonResponse({"has_data": False})
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request:HttpRequest):
        period = request.GET.get("period", "7d")
        data = InvoiceSelectors().get_platform_gmv_trend(period=period)
        return JsonResponse(data)
    

class PlatformAdoptionView(LoginRequiredMixin, View):
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
            user = request.user
            if user.email not in settings.PREVILEDGE_USERS: # type: ignore
                return JsonResponse({"has_data": False})
            return super().dispatch(request, *args, **kwargs)
        
    def get(self, request:HttpRequest):
        try:
            threshold = int(request.GET.get("threshold", 1))
        except (TypeError, ValueError):
            threshold = 1

        if threshold not in ADOPTION_THRESHOLDS:
            threshold = 1

        data = BusinessSelector().get_adoption_breakdown(threshold=threshold)
        return JsonResponse(data)
