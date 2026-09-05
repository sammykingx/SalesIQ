from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from accounts.serializers import PasswordChangeSchema
from accounts.repository.user_repo import UserRepository
from pydantic import ValidationError
from core.url_names import ACCOUNTS


class UserPasswordUpdateView(LoginRequiredMixin, View):
    """_summary_
    FOr authenticated users to update their password

    Args:
        View (_type_): _description_
    """
    def patch(self, request: HttpRequest):
        try:
            data = PasswordChangeSchema.model_validate(request.body, strict=False)
            UserRepository().update_password(user_email=request.user.email, new_password=data.password) # type: ignore
            return JsonResponse({ "msg": "Action successful", }, status=200)
        
        except ValidationError as e:
            return JsonResponse({ "msg": "Invalid data provided", "errors": e.errors() }, status=422)
        
        except Exception as e:
            return JsonResponse({ "msg": "An error occurred while updating the password", "error": str(e) }, status=500)
    