from django.urls import path
from django.views.generic import TemplateView
from core.url_names import ACCOUNTS
from core.template_names import APP_TEMPLATES


urlpatterns = [
    path("checkpoint/", TemplateView.as_view(template_name=APP_TEMPLATES.ACCOUNTS.AUTH.SIGNIN), name=ACCOUNTS.AUTH.LOGIN),
    path("join/", TemplateView.as_view(template_name=APP_TEMPLATES.ACCOUNTS.AUTH.SIGNUP), name=ACCOUNTS.AUTH.REGISTER),
    path("password/reset/", TemplateView.as_view(template_name=APP_TEMPLATES.ACCOUNTS.AUTH.PASSWORD_RESET), name=ACCOUNTS.AUTH.PASSWORD_RESET),
    path("password/change/", TemplateView.as_view(template_name=APP_TEMPLATES.ACCOUNTS.AUTH.PASSWORD_CHANGE), name=ACCOUNTS.AUTH.PASSWORD_CHANGE),
    
]
