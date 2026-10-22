from platform_ops.mixins import BackofficeAccessMixin
from django.db.models import Q, QuerySet
from django.views.generic import ListView
from core.template_names import APP_TEMPLATES
from accounts.selectors import BusinessPlatformSelector


class AllMerchantListsView(BackofficeAccessMixin, ListView):
    template_name = APP_TEMPLATES.PLATFORM_OPS.ALL_MERCHANTS
    context_object_name = "recent_signups"
    paginate_by = 15

    def get_queryset(self) -> QuerySet:
        """
            Retrieves the paginated queryset of all merchants utilizing the centralized 
            BusinessPlatformSelector query logic. This ensures performance consistency 
            and eliminates query duplication across backoffice features.
        """
        qs = BusinessPlatformSelector().get_annotated_queryset()
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
        return context
