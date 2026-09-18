from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse
from django.views.generic import View

from accounts.selectors import BusinessSelector
from invoices.selectors import InvoiceSelectors
from typing import Union


class RevenueTrendView(LoginRequiredMixin, View):
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Union[HttpResponse, JsonResponse]:
        self.user_biz = BusinessSelector().get_user_business(user_email=self.request.user.email, as_instance=True) #type:ignore
        if self.user_biz is None:
            return JsonResponse({}, status=200)
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request:HttpRequest) -> JsonResponse:
        period = request.GET.get("period", "7d")
        revenue_data = InvoiceSelectors().get_revenue_trend(business=self.user_biz, period=period)
        return JsonResponse(revenue_data, status=200)
