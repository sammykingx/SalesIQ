from django.contrib.auth.views import LogoutView
from django.urls import path, include, reverse_lazy
from django.views.generic import TemplateView, RedirectView
from core.template_names import APP_TEMPLATES
from core.url_names import ACCOUNTS
from ..views import (
    AccountActivationView, DashboardView, UserProfileView, BizAccountOnboardingView, 
    AccountSettingsView, UpdateAccountProfileDataView, UpdateBusinessDataView
)


urlpatterns = [
    path("auth/", include("accounts.urls.auth")),
    path("join/", RedirectView.as_view(url=reverse_lazy(ACCOUNTS.AUTH.REGISTER))),
    path("leave/", LogoutView.as_view(), name=ACCOUNTS.AUTH.LOGOUT),
    path("activation/<token>/", AccountActivationView.as_view(), name=ACCOUNTS.ACTIVATION),
    path("onboarding/", BizAccountOnboardingView.as_view(), name=ACCOUNTS.ONBOARDING),
    path("dashboard/", DashboardView.as_view(), name=ACCOUNTS.DASHBOARD),
    path("profile/", UserProfileView.as_view(), name=ACCOUNTS.PROFILE),
    path("settings/", AccountSettingsView.as_view(), name=ACCOUNTS.SETTINGS),
    path("settings/update-profile/", UpdateAccountProfileDataView.as_view(), name=ACCOUNTS.UPDATES.PROFILE),
    # path("settings/update-business/", UpdateBusinessDataView.as_view(), name=ACCOUNTS.UPDATES.BUSINESS),
]