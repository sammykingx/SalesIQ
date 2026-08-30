from django.urls import path, include
from django.views.generic import TemplateView
from core.template_names import APP_TEMPLATES
from core.url_names import ACCOUNTS
from ..views import AccountActivationView


urlpatterns = [
    path("auth/", include("accounts.urls.auth")),
    path("activation/<token>/", AccountActivationView.as_view(), name=ACCOUNTS.ACTIVATION),
    path("onboarding/", TemplateView.as_view(template_name=APP_TEMPLATES.ACCOUNTS.ONBOARDING), name=ACCOUNTS.ONBOARDING),
    # onboarding
    # dashboard, profile
    # settings namespace
]