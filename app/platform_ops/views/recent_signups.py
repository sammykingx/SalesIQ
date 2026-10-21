from platform_ops.mixins import BackofficeAccessMixin
from django.views.generic import ListView
from core.template_names import APP_TEMPLATES
from platform_ops.selectors import PlatformDashboardMetricsSelector
from accounts.models import Business


class RecentSignupsView(BackofficeAccessMixin, ListView):
    model = Business
    template_name = APP_TEMPLATES.PLATFORM_OPS.RECENT_SIGNUPS
    context_object_name = "bizz_signups"
    paginate_by = 2

    # def get_queryset(self):
    #     # Most recent signups first, annotating sale counts to calculate status
    #     return Business.objects.annotate(
    #         sale_count=Count('sales') # Update 'sales' to match your related_name if different
    #     ).order_by('-created_at') # Assumes 'created_at' timestamp field exists

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selector = PlatformDashboardMetricsSelector()
        signups = selector.recent_business_signups()
        context["recent_signups"] = signups
        
        # for biz in context.get('recent_signups', []):
        #     biz.is_dormant = biz.sale_count == 0
        #     biz.joined_display = biz.created_at.strftime("%b %d, %Y") # Format representation
        return context
    
