from django.urls import path

from core.url_names import METRICS
from metrics.views import RevenueTrendView


urlpatterns = [
    path("business-revenue/", RevenueTrendView.as_view(), name=METRICS.BIZ_REVENUE),
]
