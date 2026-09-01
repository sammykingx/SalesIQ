from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.views.generic import View
from django.shortcuts import render
from core.template_names import APP_TEMPLATES
from accounts.domains.exceptions import AccountsDomainException
from accounts.serializers import BusinessOnboardingSchema
from accounts.services import BusinessService
from pydantic import ValidationError


class BizAccountOnboardingView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
       return render(request, APP_TEMPLATES.ACCOUNTS.ONBOARDING)
   
    def post(self, request: HttpRequest):
        try:
            data = BusinessOnboardingSchema.model_validate_json(request.body, strict=True)
            BusinessService(self.request.user).register_business(data) # type: ignore
            return JsonResponse({
                "message": "Your business has been successfully registered.",
                "status": "success",
            }, stauts=201)
            
        except ValidationError:
            return JsonResponse({
                "message": "Please review the data provided",
                "status": "warning"
            }, status=422)
            
        except AccountsDomainException as err:
            return JsonResponse({
                "status": "error",
                "message": err.message
            })
            
        except Exception:
            import traceback
            traceback.print_exc()
            return JsonResponse({
                "title": "System Glitch",
                "message": "We encountered an unexpected hiccup. Please try again shortly!",
                "status": "error",
                "redirect": False,
            }, status=500)
                    