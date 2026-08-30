from django.views.generic import View
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from core.template_names import APP_TEMPLATES
from core.url_names import ACCOUNTS
from accounts.services import UserRegistrationService

import json

class RequestPassowrdResetView(View):
    """_summary_
    FOr unatuhenticated(guest) to request a reset link sent to their email

    Args:
        View (_type_): _description_
    """
    def get(self, request: HttpRequest):
        return render(request, template_name=APP_TEMPLATES.ACCOUNTS.AUTH.PASSWORD_RESET)
    
    def post(self, request: HttpRequest):
        try:
            data:dict = json.loads(request.body)
            email = data.get("email", "")
            service = UserRegistrationService(request=request)
            service.send_reset_link(user_email=email)
        except Exception:
            pass
        return JsonResponse({ "message": "Password Reset email Action successful", "status": "success" }, status=200)
        