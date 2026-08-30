from django.views.generic import View
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from core.template_names import APP_TEMPLATES
from core.url_names import ACCOUNTS
from accounts.services import TokenService, PasswordResetService
from accounts.models.user_token import TokenType


class GuestPasswordChangeView(View):
    """For unauthenticated users to change passwords""" 
    def get(self, request: HttpRequest, **kwargs):
        token = kwargs.get("token", "")
        token_manager = TokenService()
        token_obj = token_manager.get_token_obj(token=token, tkn_type=TokenType.PASSWORD_RESET)
        if token_obj is None or not token_obj.is_valid:
            # render bad token templates
            pass
        return render(request, template_name=APP_TEMPLATES.ACCOUNTS.AUTH.PASSWORD_CHANGE)
    
    def post(self, request: HttpRequest, **kwargs):
        token = kwargs.get("token", "")
        token_manager = TokenService()
        token_obj = token_manager.get_token_obj(token=token, tkn_type=TokenType.PASSWORD_RESET)
        if token_obj is None or not token_obj.is_valid:
            return JsonResponse({
                "status": "error",
                "message": "Invalid/malformed reset token",
            }, status=400)
        reset_service = PasswordResetService(request=request)
        return JsonResponse({
                "message": "Guest password Change Action successful",
                "satus": "success",
                "redirect": True, 
                "url": reverse(ACCOUNTS.AUTH.LOGIN)
            }, status=204
        )
        
    