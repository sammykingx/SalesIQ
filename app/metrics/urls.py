from django.urls import path

from core.url_names import METRICS
from metrics.views import RevenueTrendView, BusinessBusiestDayBiew, PlatformGmvTrendView, PlatformAdoptionView


urlpatterns = [
    path("business/revenue/", RevenueTrendView.as_view(), name=METRICS.BIZ_REVENUE),
    path("business/busiest-day/", BusinessBusiestDayBiew.as_view(), name=METRICS.BUSIEST_DAYS),
    path("platform/gmv/", PlatformGmvTrendView.as_view(), name=METRICS.PLATFORM_GMV),
    path("platform/adoption/", PlatformAdoptionView.as_view(), name=METRICS.PLATFORM_ADOPTION),
]
