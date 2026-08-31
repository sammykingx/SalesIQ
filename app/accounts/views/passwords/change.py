from django.views.generic import View
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from core.template_names import APP_TEMPLATES, LANDING_PAGES
from core.url_names import ACCOUNTS
from accounts.domains.exceptions import AccountsDomainException
from accounts.services import TokenService, PasswordResetService
from accounts.models.user_token import TokenType
from accounts.serializers import PasswordChangeSchema, AuthActionResponseSchema
from pydantic import ValidationError

class GuestPasswordChangeView(View):
    """For unauthenticated users to change passwords""" 
    def get(self, request: HttpRequest, **kwargs):
        token = kwargs.get("token", "")
        token_manager = TokenService()
        token_obj = token_manager.get_token_obj(token=token, tkn_type=TokenType.PASSWORD_RESET)
        if token_obj is None or not token_obj.is_valid:
            return render(request, LANDING_PAGES.FEEDBACK, {
                "status": "error",
                "title": "Invalid Link",
                "message": "We couldn't verify your password reset link. It may have expired or invalid. Kindly request a fresh one.",
                "primary_btn_label": "Try Again",
                "primary_btn_url": reverse(ACCOUNTS.AUTH.PASSWORD_RESET),
                "secondary_btn_label": "Login",
                "secondary_btn_url": reverse(ACCOUNTS.AUTH.LOGIN),
            })

        return render(request, template_name=APP_TEMPLATES.ACCOUNTS.AUTH.PASSWORD_CHANGE)
    
    def post(self, request: HttpRequest, **kwargs):
        try:
            token = kwargs.get("token", "")
            data = PasswordChangeSchema.model_validate_json(request.body, strict=True)
            reset_service = PasswordResetService(request=request)
            reset_service.update_password(token=token, new_password=data.password)
            return JsonResponse({
                "message": "Woohoo! Your password has been successfully updated. You are all set!",
                "satus": "success",
                "redirect": True, 
                "url": reverse(ACCOUNTS.AUTH.LOGIN)
            }, status=200)
        
        except ValidationError:
            response_data = AuthActionResponseSchema(
                message="Invalid data format. Please check your input.",
                status="warning",
                redirect=False
            )
            return JsonResponse(response_data.model_dump(mode="json"), status=422)
        
        except AccountsDomainException as err:
            response_data = AuthActionResponseSchema(
                message=err.message,
                status="warning",
                redirect=False
            )
            return JsonResponse(response_data.model_dump(mode="json"), status=400)
        
        except Exception:
            import traceback
            traceback.print_exc()
            return JsonResponse({
                "title": "System Glitch",
                "message": "We encountered an unexpected hiccup. Please try again shortly!",
                "status": "error",
                "redirect": False,
            }, status=500)