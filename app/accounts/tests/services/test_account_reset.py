import pytest

from django.db.models import Model
from django.test import RequestFactory
from django.urls import reverse
from django.template.loader import render_to_string as django_render_to_string
from unittest.mock import MagicMock

from accounts.models.user_token import TokenType
from accounts.services import PasswordResetService, TokenService
from accounts.tests.factories import UserFactory
from core.template_names import EMAIL_TEMPLATES
from core.url_names import ACCOUNTS


SERVICES = "accounts.services.account_reset"

def reload(obj: Model):
    obj.refresh_from_db()
    return obj

def reset_token(user, token_type=TokenType.PASSWORD_RESET) -> str:
    return TokenService().create_token(user_email=user.email, token_type=token_type).token


# @pytest.fixture(autouse=True)
# def mailer(monkeypatch):
#     """
#     Replaces AppMailerService for EVERY test in this file, so nothing can reach Resend,
#     even a test that forgets to ask for it. Returns the instance the service will use.
#     """
#     mailer_cls = MagicMock(name="AppMailerService")
#     instance = mailer_cls.return_value
#     instance.prepare_message.return_value = instance
#     monkeypatch.setattr(f"{SERVICES}.AppMailerService", mailer_cls)
#     return instance

@pytest.fixture
def service(rf: RequestFactory, new_user):
    req = rf.get("/")
    req.user = new_user
    return PasswordResetService(request=req)

@pytest.fixture
def bystander(db):
    """Provides a second, newly registered user on the platform."""
    return UserFactory()

# @pytest.fixture
# def render_spy(monkeypatch):
#     """Records render_to_string calls but still renders the real template."""
#     spy = MagicMock(wraps=django_render_to_string)
#     monkeypatch.setattr(f"{SERVICES}.render_to_string", spy)
#     return spy

@pytest.fixture
def send_spy(monkeypatch):
    """Replaces _send_reset_link so initiate_password_reset is tested in isolation."""
    spy = MagicMock(name="_send_reset_link")
    monkeypatch.setattr(PasswordResetService, "_send_reset_link", spy)
    return spy



def test_pwd_reset_template_is_loaded_with_right_context(service, new_user, render_spy, token_service):
    service._load_message(f_name=new_user.first_name, email=new_user.email)
    
    token_service.create_token.assert_called_once_with(
        user_email=new_user.email, token_type=TokenType.PASSWORD_RESET
    )
    render_spy.assert_called_once()
    call_kwargs = render_spy.call_args.kwargs
    
    assert call_kwargs["template_name"] == EMAIL_TEMPLATES.ACCOUNT_RECOVERY
    assert call_kwargs["request"] is service.request
    assert call_kwargs["context"] == {
        "host": service.request.build_absolute_uri("/"),
        "first_name": new_user.first_name,
        "url": service.request.build_absolute_uri(
            reverse(ACCOUNTS.AUTH.PASSWORD_CHANGE, kwargs={"token": "tok-123"})
        ),
    }
