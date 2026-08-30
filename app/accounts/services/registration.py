from django.db.utils import IntegrityError
from django.http import HttpRequest
from django.urls import reverse
from django.template.loader import render_to_string

from core.url_names import ACCOUNTS
from core.template_names import EMAIL_TEMPLATES
from mailer.providers.base import Providers
from mailer.services import AppMailerService

from ..services.token_manager import TokenService
from ..models.user_token import TokenType
from ..domains.errors import AccountRegistrationErrors
from ..domains.exceptions import DuplicateEmailError
from ..repository import UserRepository
from ..selectors import UserSelector
from ..serializers import UserRegistrationSchema


class UserRegistrationService:
    """Orchestrates new user registration, data persistence, and verification communication."""

    def __init__(self, request: HttpRequest) -> None:
        """Initializes the registration service with request context and data access layers."""
        self.request = request
        self.user_repo = UserRepository()
        self.model_selector = UserSelector()
        self.mail_client = None
        
    def create_account(self, data: UserRegistrationSchema):
        """Persists the user record via the repository and triggers the activation email sequence."""
        try:
            self.user_repo.create_user(user=data)
        except IntegrityError:
            raise DuplicateEmailError(
                message="Your request has been successfully processed.",
                title=AccountRegistrationErrors.DUPLICATE_EMAIL.title,
                code=AccountRegistrationErrors.DUPLICATE_EMAIL.code
            )
    
    def html_message(self, user: UserRegistrationSchema, token: str) -> str:
        """Renders and returns the HTML activation email string using absolute URIs and template contexts."""
        template_context = {
            "host": "https://sales.com.ng/", #self.request.build_absolute_uri("/"),
            "first_name": user.first_name,
            "url": self.request.build_absolute_uri(reverse(ACCOUNTS.ACTIVATION, kwargs={"token": token}))
        }
        
        return render_to_string(
            template_name=EMAIL_TEMPLATES.ACCOUNT_ACTIVATION,
            context=template_context,
            request=self.request
        )
        
    def send_activation_link(self, data: UserRegistrationSchema):
        result = TokenService().create_token(user_email=data.email, token_type=TokenType.EMAIL_VERIFICATION)
        return (
            AppMailerService(Providers.RESEND)
            .prepare_message(
                subject="salesiq - Almost there! Activate your new account ✨",
                html_msg=self.html_message(data, token=result.token),
                recipients=data.email,
            )
            .send_email()
        )
        
    def send_reset_link(self, *, user_email: str):
        user = self.model_selector.get_by_email(email=user_email)
        if user:
            result = TokenService().create_token(user_email=user.email, token_type=TokenType.PASSWORD_RESET) 
            (
                AppMailerService(Providers.RESEND)
                .prepare_message(
                    subject="salesiq - Almost there! Activate your new account ✨",
                    html_msg=self.html_message(data, token=result.token),
                    recipients=user.email,
                )
                .send_email()
            )