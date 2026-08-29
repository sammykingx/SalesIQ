from django.contrib.auth import get_user_model
from django.views.generic import View
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse

from ..services import UserRegistrationService
from ..domains.exceptions import AccountsDomainException
from core.template_names import APP_TEMPLATES
from core.url_names import ACCOUNTS
from mailer.services import send_email

from ..serializers import UserRegistrationSchema, UserRegistrationResponseSchema
import json

from typing import cast


class AccountRegistrationView(View):
    model = get_user_model()
    
    def get(self, request: HttpRequest):
        print("This is the host", request.build_absolute_uri('/'))
        return render(request, template_name=APP_TEMPLATES.ACCOUNTS.AUTH.REGISTER)
    
    def post(self, request: HttpRequest):
        try:
            pasyload = UserRegistrationSchema.model_validate_json(request.body, strict=True)
            user_service = UserRegistrationService(request)
            user_service.create_account(pasyload)
            is_sent = user_service.send_activtivation_link(pasyload)
            # create user service
            # 1. call selector to get a record for that email if found raise domain
            #   duplicate exception which is caught in the view layer and proagated cleanly
            # 2. if no user is found then call repo create_user to save
            
            
        except json.JSONDecodeError:
            pass
        
        except AccountsDomainException:
            pass
        
        payload = json.loads(request.body)
        print(payload)
        
        # verifying the payload
        # try except to create the new record, send the confirmation email
        # flow completed
        # send_email(
        #     to=user.email,
        #     subject='Reset your SalesIQ password',
        #     template_name=TEMPLATES.ACCOUNTS.EMAILS.PASSWORD_RESET,
        #     context={'reset_link': reset_link},
        # )
        response_data = UserRegistrationResponseSchema(
            message="Account registration Action successful",
            status="success",
            redirect=True,
            url=reverse(ACCOUNTS.AUTH.LOGIN),
        )
        
        return JsonResponse(response_data.model_dump(mode="json"), status=201)
    