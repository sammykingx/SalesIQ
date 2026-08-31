from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from core.template_names import APP_TEMPLATES


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = APP_TEMPLATES.ACCOUNTS.DASHBOARD
    # template_name="layouts/new_app_layout.html"


class UserProfileView(LoginRequiredMixin, TemplateView):
    pass