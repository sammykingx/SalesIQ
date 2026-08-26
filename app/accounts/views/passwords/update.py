from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from core.template_names import APP_TEMPLATES
from core.url_names import ACCOUNTS


class UserPasswordUpdateView(LoginRequiredMixin, View):
    """_summary_
    FOr authenticated users to update their password

    Args:
        View (_type_): _description_
    """
    def post(self, request: HttpRequest):
        return JsonResponse({ "msg": "Action successful", }, status=200)
    