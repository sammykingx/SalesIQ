from django.views.generic import View
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from core.template_names import APP_TEMPLATES
from core.url_names import ACCOUNTS


class GuestPasswordChangeView(View):
    """For unauthenticated users to change passwords"""
    
    def get(self, request: HttpRequest):
        return render(request, template_name=APP_TEMPLATES.ACCOUNTS.AUTH.PASSWORD_CHANGE)
    
    def post(self, request: HttpRequest):
        return JsonResponse({
                "message": "Guest password Change Action successful",
                "satus": "success",
                "redirect": True, 
                "url": reverse(ACCOUNTS.AUTH.LOGIN)
            }, status=204
        )
    