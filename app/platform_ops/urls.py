from django.urls import path

from core.url_names import PLATFORM_OPS
from platform_ops.views import PlatformDashboardView, AdoptionChartView, GMVTrendCharView, RecentSignupsView


urlpatterns = [
    path("dashboard/", PlatformDashboardView.as_view(), name=PLATFORM_OPS.DASHBOARD),
    path("gmv/", GMVTrendCharView.as_view(), name=PLATFORM_OPS.CHARTS.GMV),
    path("adoption/", AdoptionChartView.as_view(), name=PLATFORM_OPS.CHARTS.ADOPTION),
    path("recent-adoption/", RecentSignupsView.as_view(), name=PLATFORM_OPS.RECENT_SIGNUPS),
]
