from django.views.generic import TemplateView

from platform_ops.mixins import BackofficeAccessMixin
from platform_ops.selectors import PlatformDashboardMetricsSelector
from core.template_names import APP_TEMPLATES

from typing import Any, Dict



class PlatformDashboardView(BackofficeAccessMixin, TemplateView):
    """
        View rendering the central platform management dashboard.

        Protected by `BackofficeAccessMixin` to ensure only authorized staff 
        can view system-wide analytics, recent merchant signups, and high-level summaries.
    """
    template_name = APP_TEMPLATES.PLATFORM_OPS.DASHBOARD
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.template_context())
        return context
        
    def template_context(self) -> Dict[str, Any]:
        selector = PlatformDashboardMetricsSelector()
        recent_signups = selector.recent_business_signups(limit=10)
        platform_summary = selector.summary()
            
        return {
            "recent_signups": recent_signups,
            **platform_summary,
        }
