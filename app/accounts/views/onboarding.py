from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.urls import reverse
from django.views.generic import View
from django.shortcuts import render, redirect
from core.template_names import APP_TEMPLATES
from accounts.domains.exceptions import AccountsDomainException
from accounts.serializers import BusinessOnboardingSchema
from accounts.services import BusinessService
from accounts.selectors import BusinessSelector
from core.url_names import ACCOUNTS
from pydantic import ValidationError
from utils.pydantic_formatter import format_pydantic_errors

import logging


logger = logging.getLogger(__name__)

class BizAccountOnboardingView(LoginRequiredMixin, View):
    # def dispatch(self, request: HttpRequest, *args, **kwargs):
    #     """
    #         Overrides the default dispatch to check if the user has a business
    #         account. If they do, redirect them to the dashboard.
    #     """
    #     try:
    #         business = BusinessSelector().get_user_business(user_email=request.user.email, as_instance=True) # type: ignore
    #         if business:
    #             return redirect(reverse(ACCOUNTS.DASHBOARD))
    #             # return JsonResponse({
    #             #     "message": "You already have a business account.",
    #             #     "status": "info",
    #             #     "redirect": True,
    #             #     "redirect_url": "/dashboard/",
    #             # }, status=302)
    #     except AccountsDomainException:
    #         pass

    #     return super().dispatch(request, *args, **kwargs)
    
    def get(self, request: HttpRequest):
       return render(request, APP_TEMPLATES.ACCOUNTS.ONBOARDING)
   
    def post(self, request: HttpRequest):
        try:
            data = BusinessOnboardingSchema.model_validate_json(request.body, strict=True)
            BusinessService(self.request.user).register_business(data) # type: ignore
            return JsonResponse({
                "message": "Your business has been successfully registered.",
                "status": "success",
            }, status=201)
            
        except ValidationError as err:
            return JsonResponse({
                "message": "Please review the data provided",
                "status": "warning",
                "errors": format_pydantic_errors(err),
            }, status=422)
            
        except AccountsDomainException as err:
            return JsonResponse({
                "status": "error",
                "message": err.message
            }, status=400)
            
        except Exception:
            logger.exception(
                "Unexpected error during business onboarding for user: %s with email: %s",
                request.user.get_full_name() or request.user.id, # type: ignore
                request.user.email # type: ignore
            )
            return JsonResponse({
                "title": "System Glitch",
                "message": "We encountered an unexpected hiccup. Please try again shortly!",
                "status": "error",
                "redirect": False,
            }, status=500)
                    