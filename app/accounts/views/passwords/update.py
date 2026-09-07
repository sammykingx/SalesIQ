from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from accounts.serializers import PasswordChangeSchema
from accounts.repository.user_repo import UserRepository
from utils.pydantic_formatter import format_pydantic_errors
from pydantic import ValidationError
from core.url_names import ACCOUNTS


class UserPasswordUpdateView(LoginRequiredMixin, View):
    """_summary_
    Handles secure password updates for authenticated users.

    Expects a JSON payload containing 'password' and 'confirm_password',
    validating the input against the PasswordChangeSchema before modifying 
    the user record.
    """
    def patch(self, request: HttpRequest):
        try:
            data = PasswordChangeSchema.model_validate_json(request.body, strict=False)
            UserRepository().update_password(user_email=request.user.email, new_password=data.password) # type: ignore
            return JsonResponse({ "message": "Action successful", }, status=200)
        
        except ValidationError as e:
            return JsonResponse({ "message:": "Invalid data provided", "errors": format_pydantic_errors(e) }, status=422)
        
        except Exception as e:
            return JsonResponse({ "message": "An error occurred while updating the password", "error": str(e) }, status=500)
    