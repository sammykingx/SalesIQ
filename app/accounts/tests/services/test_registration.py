import pytest

from django.db.models import Model
from django.urls import reverse
from django.template.loader import render_to_string as django_render_to_String
from django.test import RequestFactory

from accounts.models.user_token import TokenType
from accounts.services import AccountOnboardingService, TokenService
from accounts.tests.factories import UserFactory
from core.url_names import ACCOUNTS
from core.template_names import EMAIL_TEMPLATES

from unittest.mock import MagicMock
from types import SimpleNamespace


SERVICES = "accounts.services.registration"

@pytest.fixture(autouse=True)
def mailer(monkeypatch):
    """
    Replaces AppMailerService for EVERY test in this file, so nothing can reach Resend,
    even a test that forgets to ask for it. Returns the instance the service will use.
    """
    mailer_cls = MagicMock(name="AppMailerService")
    instance = mailer_cls.return_value
    instance.prepare_message.return_value = instance
    monkeypatch.setattr(f"{SERVICES}.AppMailerService", mailer_cls)
    return instance

@pytest.fixture
def token_service(monkeypatch):
    """Fake TokenService for the email tests only, where the token's value is all we need."""
    cls = MagicMock(name="TokenService")
    cls.return_value.create_token.return_value = SimpleNamespace(token="tok-123")
    monkeypatch.setattr(f"{SERVICES}.TokenService", cls)
    return cls.return_value

@pytest.fixture
def service(rf: RequestFactory, new_user: UserFactory):
    req = rf.get("/")
    req.user = new_user # type:ignore
    return AccountOnboardingService(req)

@pytest.fixture
def render_spy(monkeypatch):
    """Records render_to_string calls made by the service, but still renders for real."""
    spy = MagicMock(wraps=django_render_to_String)
    monkeypatch.setattr(f"{SERVICES}.render_to_string", spy)
    return spy

@pytest.fixture
def bystander(db):
    """Provides a second, newly registered user on the platform."""
    return UserFactory()


# ---------------- Test send_activation_link ----------------
def test_activation_email_is_sent_once_to_new_user(service, mailer, new_user, token_service):
    service.send_activation_link(email=new_user.email, first_name=new_user.first_name)
    mailer.prepare_message.assert_called_once()
    assert mailer.prepare_message.call_args.kwargs["recipients"] == new_user.email
    mailer.send_email.assert_called_once()


def test_template_is_rendered_with_the_expected_context(service, new_user, render_spy, token_service):
    service.send_activation_link(email=new_user.email, first_name="Ada")

    render_spy.assert_called_once()
    call = render_spy.call_args.kwargs
    assert call["template_name"] == EMAIL_TEMPLATES.ACCOUNT_ACTIVATION
    assert call["request"] is service.request
    assert call["context"] == {
        "host": service.request.build_absolute_uri("/"),
        "first_name": "Ada",
        "url": service.request.build_absolute_uri(
            reverse(ACCOUNTS.ACTIVATION, kwargs={"token": "tok-123"})
        ),
    }
    
    
# ---------------- activate_account ----------------
def issue_token(user) -> str:
    return TokenService().create_token(
        user_email=user.email, token_type=TokenType.EMAIL_VERIFICATION
    ).token


def reload(obj: Model):
    obj.refresh_from_db()
    return obj


def test_valid_token_verifies_the_user(service, new_user):
    assert service.activate_account(issue_token(new_user)) is True
    assert reload(new_user).is_verified # type:ignore


def test_activation_does_not_complete_onboarding(service, new_user):
    service.activate_account(issue_token(new_user))

    user = reload(new_user)
    assert user.is_verified     # type:ignore
    assert not user.onboarded   # type:ignore


def test_activation_keeps_an_onboarded_owner_onboarded(service, unverified_onboarded_user):
    service.activate_account(issue_token(unverified_onboarded_user))

    user = reload(unverified_onboarded_user)
    assert user.is_verified     # type:ignore
    assert user.onboarded       # type:ignore


def test_activation_only_verifies_the_token_owner(service, new_user, bystander):
    service.activate_account(issue_token(new_user))
    assert not reload(bystander).is_verified    # type: ignore


def test_invalid_token_returns_false_and_verifies_nobody(service, new_user):
    assert service.activate_account("not-a-real-token") is False
    assert not reload(new_user).is_verified     # type: ignore
