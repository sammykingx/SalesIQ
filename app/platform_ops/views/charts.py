from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.generic import View

from platform_ops.mixins import PlatformJsonChartMixin
from platform_ops.selectors import PlatformDashboardChartSelector
from platform_ops.selectors.charts import ADOPTION_THRESHOLDS

from typing import Any, Dict



class GMVCharTrendView(PlatformJsonChartMixin, View):
    """
        API view serving platform-wide Gross Merchant Value (GMV) trend data 
        as JSON for Alpine.js chart components.
    """
    
    def get(self, request:HttpRequest):
        selector = PlatformDashboardChartSelector()
        period = request.GET.get("period", "7d")
        data = selector.gmv_trend(period=period)
        return JsonResponse(data)
    

class AdoptionChartView(PlatformJsonChartMixin, View):
    """
        API view serving platform adoption breakdown metrics as JSON 
        for Alpine.js chart components, with query parameter validation.
    """
        
    def get(self, request:HttpRequest):
        try:
            threshold = int(request.GET.get("threshold", 1))
        except (TypeError, ValueError):
            threshold = 1

        if threshold not in ADOPTION_THRESHOLDS:
            threshold = 1

        selector = PlatformDashboardChartSelector()
        data = selector.adoption_breakdown(threshold=threshold)
        return JsonResponse(data)
    