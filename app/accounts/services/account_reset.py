from django.http import HttpRequest
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils import timezone

from core.url_names import ACCOUNTS
from core.template_names import EMAIL_TEMPLATES
from mailer.providers.base import Providers
from mailer.services import AppMailerService
from ..models.user_token import TokenType
from ..repository import UserRepository
from ..selectors import UserSelector
from ..services.token_manager import TokenService


class PasswordResetService:
    """
        Handles the entire password reset lifecycle, spanning from generating 
        and dispatching the reset email link to verifying the security token 
        and updating the user's password.
    """
    def __init__(self, request: HttpRequest) -> None:
        self.request = request
        self.model_selector = UserSelector()
        self.user_repo = UserRepository()
        
        
    def _get_reset_token(self, email: str) -> str:
        """
            Generates and returns a unique, secure password reset token string 
            associated with the given user email.
        """
        return TokenService().create_token(user_email=email, token_type=TokenType.PASSWORD_RESET).token
            
    def _load_message(self, f_name: str, email:str) -> str:
        """
            Renders the HTML email template for the password reset action, 
            injecting the dynamic reset URL containing the secure token.
        """
        template_context = {
            "host": self.request.build_absolute_uri("/"),
            "first_name": f_name,
            "url": self.request.build_absolute_uri(
                reverse(ACCOUNTS.AUTH.PASSWORD_RESET, kwargs={"token": self._get_reset_token(email)})
            )
        }
        return render_to_string(
            template_name=EMAIL_TEMPLATES.PASSWORD_RESET,
            context=template_context,
            request=self.request,
        )
        
    def _send_reset_link(self, *, first_name: str, user_email: str):
        (
            AppMailerService(Providers.RESEND)
            .prepare_message(
                subject="salesiq - let's reset your account password 🔓",
                html_msg=self._load_message(f_name=first_name, email=user_email),
                recipients=user_email,
            )
            .send_email()
        )
        
    def initiate_password_reset(self, user_email: str) -> None:
        """
            Looks up the user by email using the model selector. If found, 
            it triggers the password reset link delivery. 
        """
        user = self.model_selector.get_by_email(email=user_email)
        if user:
            self._send_reset_link(first_name=user.first_name, user_email=user.email)

    def update_password(self, token: str, new_password: str) -> None:
        """
        Orchestrates the final password change flow by first verifying 
        the security token and subsequently updating the user's password.
        """
        token_manager = TokenService()
        token_obj = token_manager.get_token_obj(
            token=token, tkn_type=TokenType.PASSWORD_RESET
        )
        if token_obj and token_manager.is_valid(token_obj):
            self.user_repo.update_password(
                user_email=token_obj.email, new_password=new_password
            )
            token_manager.invalidate_token(token_obj=token_obj)

