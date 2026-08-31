from django.views.generic import View
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from core.template_names import APP_TEMPLATES
from core.url_names import ACCOUNTS
from accounts.services import PasswordResetService, TokenService
from mailer.exceptions import EmailSendError

import json

class RequestPassowrdResetView(View):
    """
        Handles user password reset requests.

        This view serves the password reset request page via GET and 
        processes incoming JSON payloads containing the user's email 
        to trigger the password reset workflow via POST.
    """
    def get(self, request: HttpRequest, **kwargs):
        return render(request, template_name=APP_TEMPLATES.ACCOUNTS.AUTH.PASSWORD_RESET)
    
    def post(self, request: HttpRequest):
        """
            Processes the password reset request submission.

            Parses the JSON body to extract the user's email, initiates the 
            password reset sequence using `PasswordResetService`, and returns 
            a JSON response indicating success or failure.

            Args:
                request (HttpRequest): The HTTP request object containing a JSON body 
                    with an "email" field.

            Returns:
                JsonResponse: A JSON dictionary with status and message information.
                    - Status 200: Reset email initiated successfully.
                - Status 400: Failed due to an `EmailSendError`.
        """
        try:
            data:dict = json.loads(request.body)
            email = data.get("email", "")
            service = PasswordResetService(request=request)
            service.initiate_password_reset(user_email=email)
            
            return JsonResponse({ 
                "message": "Check your inbox! We've sent a secure link to get your password sorted.", 
                "status": "success",
            }, status=200)
        
        except EmailSendError as err:
            return JsonResponse({
                "status": "error",
                "message": err.user_message,
            }, status=400)
            
        except Exception:
            import traceback
            traceback.print_exc()
            return JsonResponse({
                "title": "System Glitch",
                "message": "We encountered an unexpected hiccup. Please try again shortly!",
                "status": "error",
                "redirect": False,
            }, status=500)
        