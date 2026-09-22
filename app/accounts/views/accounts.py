from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView

from accounts.selectors import UserSelector, BusinessSelector
from customers.selectors import CustomerSelector
from core.template_names import APP_TEMPLATES
from core.url_names import ACCOUNTS
from invoices.selectors import InvoiceSelectors
from products.selectors import ProductsSelector

from typing import Any, Dict


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = APP_TEMPLATES.ACCOUNTS.DASHBOARD
    invoice_selector = InvoiceSelectors()
    customer_selector = CustomerSelector()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.template_context())
        return context
    
    def template_context(self) -> Dict[str, Any]:
        user_biz = BusinessSelector().get_user_business(user_email=self.request.user.email, as_instance=True) # type:ignore
        since = timezone.now().date().replace(day=1)

        top_products = self.invoice_selector.get_top_products(
            business_id=user_biz.id, limit=5, since=since # type:ignore
        )
        recent_sales = self.invoice_selector.get_recent_sales(business_id=user_biz.id) #type: ignore
        revenue_change = self.invoice_selector.get_weekly_revenue_change(business_id=user_biz.id) # type: ignore
        top_customers = self.customer_selector.get_top_customers(business_id=user_biz.id) # type: ignore
        
        empty_product_slots = range(5 - len(top_products))
        empty_customers_slots = range(5 - len(top_customers))
        
        product_count = ProductsSelector().get_business_product_count(business_id=user_biz.id)  # type: ignore
        customer_count = self.customer_selector.get_customer_count(business_id=user_biz.id)  # type: ignore
        
        return {
            "has_business": True if user_biz else False,
            "top_products": top_products,
            "top_customers": top_customers,
            "recent_sales": recent_sales,
            "empty_product_slots": empty_product_slots,
            "empty_customers_slots": empty_customers_slots,
            "product_count": product_count,
            "customer_count": customer_count,
            **revenue_change
        }
        
class PlatformDashboardView(LoginRequiredMixin, TemplateView):
    template_name = APP_TEMPLATES.ACCOUNTS.ANALYST_DASHBOARD
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
            user = request.user
            if user.email not in settings.PREVILEDGE_USERS: # type: ignore
                return redirect(reverse(ACCOUNTS.DASHBOARD))
            
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.template_context())
        return context
    
    def template_context(self) -> Dict[str, Any]:
        recent_signups = BusinessSelector().get_recent_signups(limit=7)
        return {
            "recent_signups": recent_signups,
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
