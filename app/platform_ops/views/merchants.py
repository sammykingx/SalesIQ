from typing import Any

from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, TemplateView

from accounts.selectors import BusinessPlatformSelector
from core.template_names import APP_TEMPLATES
from platform_ops.mixins import BackofficeAccessMixin
from platform_ops.serializer import MerchantLeaderboardSchema
class AllMerchantListsView(BackofficeAccessMixin, ListView):
    template_name = APP_TEMPLATES.PLATFORM_OPS.ALL_MERCHANTS
    selector_cls = BusinessPlatformSelector()
    context_object_name = "recent_signups"
    paginate_by = 15

    def get_queryset(self) -> QuerySet:
        """
            Retrieves the paginated queryset of all merchants utilizing the centralized 
            BusinessPlatformSelector query logic. This ensures performance consistency 
            and eliminates query duplication across backoffice features.
        """
        qs = self.selector_cls.get_annotated_queryset()
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            qs = qs.filter(
                Q(name__icontains=search_query) |
                Q(code__icontains=search_query) |
                Q(owner__first_name__icontains=search_query) |
                Q(owner__last_name__icontains=search_query)
            )
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['total_merchants'] = self.selector_cls.get_total_count()
        return context
    

class LeaderBoardView(BackofficeAccessMixin, TemplateView):
    template_name = APP_TEMPLATES.PLATFORM_OPS.LEADERBOARD

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        ldr_json = self.leaderboard_json()
        context["leaderboard_json"] = ldr_json
        return context
    
    def leaderboard_json(self) -> list[dict[str, Any]]:
        timeframe = self.request.GET.get('timeframe', 'this_month')
        qs = BusinessPlatformSelector().merchant_leaderboard(time_frame=timeframe)
        json_payload = []
        for idx, biz in enumerate(qs, start=1):
            revenue_val = float(biz.total_revenue or 0)
            owner_name = f"{biz.owner.first_name} {biz.owner.last_name}".title().strip()
            data = MerchantLeaderboardSchema(
                rank=idx,
                name=biz.name.title(),
                code=biz.code,
                owner=owner_name,
                biz_type=biz.business_type,
                total_sales=biz.total_sales,
                revenue_raw=revenue_val,
                revenue=f"₦{revenue_val:,.2f}",
                growth="+0.0%",
            )
            json_payload.append(data.model_dump())
        return json_payload
