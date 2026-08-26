from django.views.generic import View
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from core.template_names import APP_TEMPLATES
from core.url_names import ACCOUNTS
import json


class AccountRegistrationView(View):
    def get(self, request: HttpRequest):
        return render(request, template_name=APP_TEMPLATES.ACCOUNTS.AUTH.REGISTER)
    
    def post(self, request: HttpRequest):
        payload = json.loads(request.body)
        print(payload)
        
        return JsonResponse(
            {
                "message": "Account registration Action successful",
                "status": "success",
                "redirect": True, 
                "url": reverse(ACCOUNTS.AUTH.LOGIN)
            }, status=201
        )
    