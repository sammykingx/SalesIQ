from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from accounts.domains.entities import BusinessEntity
from accounts.selectors import UserSelector, BusinessSelector
from core.template_names import APP_TEMPLATES


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = APP_TEMPLATES.ACCOUNTS.DASHBOARD
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['user'] = self.request.user
    #     return context

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = APP_TEMPLATES.ACCOUNTS.PROFILE
    user_selector = UserSelector()
    business_selector = BusinessSelector()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.template_context())
        return context
    
    def template_context(self):
        user_entity = self.user_selector.get_user(email=self.request.user.email) #type: ignore
        biz_entity = self.business_selector.get_user_business(user_email=self.request.user.email) #type: ignore
        return {
            "user": user_entity,
            "business": biz_entity,
        }