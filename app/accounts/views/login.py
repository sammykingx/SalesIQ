from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from core.url_names import ACCOUNTS
from core.template_names import APP_TEMPLATES


class AccountLoginView(LoginView):
    template_name = APP_TEMPLATES.ACCOUNTS.AUTH.LOGIN
    redirect_authenticated_user = True
    success_url = reverse_lazy(ACCOUNTS.DASHBOARD)

    def form_invalid(self, form) -> HttpResponse:
        errors = form.errors.as_json()
        
        response = super().form_invalid(form)
        return response
    