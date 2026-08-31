from django.contrib.auth import get_user_model
from django.views.generic import View
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse

from core.template_names import APP_TEMPLATES, LANDING_PAGES
from core.url_names import ACCOUNTS
from mailer.exceptions import EmailSendError
from ..services import AccountOnboardingService
from ..domains.exceptions import AccountsDomainException
from ..serializers import UserRegistrationSchema, AuthActionResponseSchema

from pydantic import ValidationError


import logging

logger = logging.getLogger(__name__)


class AccountRegistrationView(View):
    model = get_user_model()
    
    def get(self, request: HttpRequest):
        return render(request, template_name=APP_TEMPLATES.ACCOUNTS.AUTH.REGISTER)
    
    def post(self, request: HttpRequest):
        try:
            payload = UserRegistrationSchema.model_validate_json(request.body, strict=True)
            user_service = AccountOnboardingService(request)
            user_service.create_account(payload)
            user_service.send_activation_link(payload)
            response_data = AuthActionResponseSchema(
                message="Registration successful! Please check your email to activate your account.",
                status="success",
                redirect=True,
                url=reverse(ACCOUNTS.AUTH.LOGIN),
            )
                    
            return JsonResponse(response_data.model_dump(mode="json"), status=201)
            
        except ValidationError as err:
            response_data = AuthActionResponseSchema(
                message="Invalid data format. Please check your input.",
                status="warning",
                redirect=False
            )
            return JsonResponse(response_data.model_dump(mode="json"), status=422)
        
        except AccountsDomainException as err:
            response_data = AuthActionResponseSchema(
                message=err.message,
                status="success",
                redirect=False
            )
            return JsonResponse(response_data.model_dump(mode="json"), status=400)
        
        except EmailSendError as err:
            logger.warning(
                "Activation email failed: status=%s response=%s",
                err.status_code, err.raw_response,
            )
            response_data = AuthActionResponseSchema(
                message=err.user_message,
                status="warning",
                redirect=True,
                url=reverse(ACCOUNTS.AUTH.LOGIN),
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
     
class AccountActivationView(View):
    def get(self, request:HttpRequest, **kwargs):
        token = kwargs.get("token", "")
        was_verified = AccountOnboardingService(request).activate_account(token=token)
        if was_verified:
            title = "Email Verified!"
            message = "Your email address has been successfully confirmed. You can now access your SalesIQ dashboard."
            status = "success"
            btn_label = "Go to dashboard"
            btn_url = reverse(ACCOUNTS.DASHBOARD)
        else:
            title = "Verification Failed"
            message = "The activation link is invalid or has expired. Please request a new verification email."
            status = "error"
            btn_label = "Login to request one"
            btn_url = reverse(ACCOUNTS.AUTH.LOGIN) 

        return render(request, LANDING_PAGES.FEEDBACK, {
            "status": status,
            "title": title,
            "message": message,
            "primary_btn_label": btn_label,
            "primary_btn_url": btn_url,
            "verified": was_verified,
        })
