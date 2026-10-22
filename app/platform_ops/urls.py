from django.urls import path

from core.url_names import PLATFORM_OPS
from platform_ops.views import PlatformDashboardView, AdoptionChartView, GMVTrendCharView, AllMerchantListsView


urlpatterns = [
    path("dashboard/", PlatformDashboardView.as_view(), name=PLATFORM_OPS.DASHBOARD),
    path("gmv/", GMVTrendCharView.as_view(), name=PLATFORM_OPS.CHARTS.GMV),
    path("adoption/", AdoptionChartView.as_view(), name=PLATFORM_OPS.CHARTS.ADOPTION),
    path("all-merchants/", AllMerchantListsView.as_view(), name=PLATFORM_OPS.MERCHANTS),
]
