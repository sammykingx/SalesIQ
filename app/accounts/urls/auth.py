from django.urls import path, reverse_lazy
from django.views.generic import TemplateView, RedirectView
from core.url_names import ACCOUNTS
from core.template_names import APP_TEMPLATES
from ..views import (
    AccountRegistrationView, GuestPasswordChangeView, RequestPassowrdResetView,
    AccountLoginView, UserPasswordUpdateView,
)

urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy(ACCOUNTS.AUTH.LOGIN))),
    path("checkpoint/", AccountLoginView.as_view(), name=ACCOUNTS.AUTH.LOGIN),
    path("join/", AccountRegistrationView.as_view(), name=ACCOUNTS.AUTH.REGISTER),
    path("password/reset", RequestPassowrdResetView.as_view(), name=ACCOUNTS.AUTH.PASSWORD_RESET),
    path("password/change/<token>/", GuestPasswordChangeView.as_view(), name=ACCOUNTS.AUTH.PASSWORD_CHANGE),
    path("password/update/", UserPasswordUpdateView.as_view(), name=ACCOUNTS.AUTH.PASSWORD_UPDATE),
]
