from django.contrib.auth import get_user_model
from django.views.generic import View
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse

from core.template_names import APP_TEMPLATES
from core.url_names import ACCOUNTS
from mailer.exceptions import EmailSendError, EmailTimeoutError
from ..services import UserRegistrationService, TokenService
from ..domains.exceptions import AccountsDomainException
from ..serializers import UserRegistrationSchema, UserRegistrationResponseSchema

from pydantic import ValidationError
from typing import cast

import json, logging

logger = logging.getLogger(__name__)


class AccountRegistrationView(View):
    model = get_user_model()
    
    def get(self, request: HttpRequest):
        return render(request, template_name=APP_TEMPLATES.ACCOUNTS.AUTH.REGISTER)
    
    def post(self, request: HttpRequest):
        try:
            payload = UserRegistrationSchema.model_validate_json(request.body, strict=True)
            user_service = UserRegistrationService(request)
            user_service.create_account(payload)
            
            # print(payload.model_dump_json(indent=2))
            
            user_service.send_activation_link(payload)
            response_data = UserRegistrationResponseSchema(
                message="Registration successful! Please check your email to activate your account.",
                status="success",
                redirect=True,
                url=reverse(ACCOUNTS.AUTH.LOGIN),
            )
                    
            return JsonResponse(response_data.model_dump(mode="json"), status=201)
            
        except ValidationError as err:
            print(err)
            response_data = UserRegistrationResponseSchema(
                message="Invalid data format. Please check your input.",
                status="warning",
                redirect=False
            )
            return JsonResponse(response_data.model_dump(mode="json"), status=400)
        
        except AccountsDomainException as err:
            response_data = UserRegistrationResponseSchema(
                message=err.message,
                status="success",
                redirect=False
            )
            return JsonResponse(response_data.model_dump(mode="json"), status=200)
        
        except EmailSendError as err:
            logger.warning(
                "Activation email failed: status=%s response=%s",
                err.status_code, err.raw_response,
            )
            response_data = UserRegistrationResponseSchema(
                message=err.user_message,
                status="warning",
                redirect=True,
                url=reverse(ACCOUNTS.AUTH.LOGIN),
            )
            return JsonResponse(response_data.model_dump(mode="json"), status=201)
        
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
        token = cast(str, kwargs.get("token"))
        token_manager = TokenService()
        token_obj = token_manager.get_user_token(token=token)
        ctx = {}
        if token_obj is None:
            ctx.update(
                verified=False,
            )
        else:
            token_manager.verify_email(token_obj)
            ctx.update(verified=True)

        return render(
            request,
            template_name=APP_TEMPLATES.ACCOUNTS.ACTIVATION,
            context=ctx,
        )
