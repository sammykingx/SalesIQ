from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils import timezone

from accounts.selectors import UserSelector, BusinessSelector
from core.template_names import APP_TEMPLATES
from invoices.selectors import InvoiceSelectors

from typing import Any, Dict


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = APP_TEMPLATES.ACCOUNTS.DASHBOARD
    bix_selector = BusinessSelector
    inv_selector = InvoiceSelectors
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.template_context())
        return context
    
    def template_context(self) -> Dict[str, Any]:
        user_biz = BusinessSelector().get_user_business(user_email=self.request.user.email, as_instance=True) # type:ignore
        since = timezone.now().date().replace(day=1)

        top_products = InvoiceSelectors().get_top_products(
            business_id=user_biz.id, limit=5, since=since # type:ignore
        )
        
        empty_product_slots = range(5 - len(top_products))
        
        return {
            "has_business": True if user_biz else False,
            "top_products": top_products,
            "empty_product_slots": empty_product_slots,
        }
        

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = APP_TEMPLATES.ACCOUNTS.PROFILE
    user_selector = UserSelector()
    business_selector = BusinessSelector()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.template_context())
        return context
    
    def template_context(self):
        user_entity = self.user_selector.get_by_email(email=self.request.user.email) #type: ignore
        biz_entity = self.business_selector.get_user_business(user_email=self.request.user.email) #type: ignore
        return {
            "user": user_entity,
            "business": biz_entity,
        }
