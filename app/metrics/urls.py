from django.urls import path

from core.url_names import METRICS
from metrics.views import RevenueTrendView, BusinessBusiestDayBiew


urlpatterns = [
    path("business-revenue/", RevenueTrendView.as_view(), name=METRICS.BIZ_REVENUE),
    path("busiest-day/", BusinessBusiestDayBiew.as_view(), name=METRICS.BUSIEST_DAYS),
]
