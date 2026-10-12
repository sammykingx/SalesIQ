import pytest

from django.db.models import Model
from django.test import RequestFactory
from django.urls import reverse
from unittest.mock import MagicMock

from accounts.domains.exceptions import InvalidTokenError
from accounts.models.user_token import TokenType
from accounts.services import PasswordResetService, TokenService
from accounts.tests.factories import UserFactory
from core.template_names import EMAIL_TEMPLATES
from core.url_names import ACCOUNTS


SERVICES = "accounts.services.account_reset"
NEW_PASSWORD = "N3w!password"
FACTORY_PASSWORD = "securepassword123"

def reload(obj: Model):
    obj.refresh_from_db() # type: ignore
    return obj

def reset_token(user, token_type=TokenType.PASSWORD_RESET) -> str:
    return TokenService().create_token(user_email=user.email, token_type=token_type).token

@pytest.fixture
def service(rf: RequestFactory, new_user):
    req = rf.get("/")
    req.user = new_user
    return PasswordResetService(request=req)

@pytest.fixture
def bystander(db):
    """Provides a second, newly registered user on the platform."""
    return UserFactory()

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
    
def test_initiate_password_reset_for_unverified_users(service, new_user, send_spy):
    service.initiate_password_reset(user_email=new_user.email)
    send_spy.assert_called_once_with(first_name=new_user.first_name, user_email=new_user.email)

def test_initiate_password_reset_for_verified_users(service, verified_not_onboarded_user, send_spy):
    service.initiate_password_reset(user_email=verified_not_onboarded_user.email)
    send_spy.assert_called_once_with(
        first_name=verified_not_onboarded_user.first_name, 
        user_email=verified_not_onboarded_user.email
    )

def test_update_password_with_valid_token_changes_the_password(service, new_user):
    service.update_password(token=reset_token(new_user), new_password=NEW_PASSWORD)

    user = reload(new_user)
    assert user.check_password(NEW_PASSWORD)            # type:ignore
    assert not user.check_password(FACTORY_PASSWORD)    # type:ignore
    
def test_reset_token_cannot_be_reused(service, new_user):
    token = reset_token(new_user)
    service.update_password(token=token, new_password=NEW_PASSWORD)

    with pytest.raises(InvalidTokenError):
        service.update_password(token=token, new_password="An0ther!pass")

    assert reload(new_user).check_password(NEW_PASSWORD)    # type:ignore
    
def test_unknown_token_is_rejected_and_nothing_changes(service, new_user):
    with pytest.raises(InvalidTokenError):
        service.update_password(token="not-a-real-token", new_password=NEW_PASSWORD)

    assert reload(new_user).check_password(FACTORY_PASSWORD)     # type:ignore

def test_email_verification_token_cannot_reset_a_password(service, new_user):
    token = reset_token(new_user, token_type=TokenType.EMAIL_VERIFICATION)

    with pytest.raises(InvalidTokenError):
        service.update_password(token=token, new_password=NEW_PASSWORD)

    assert reload(new_user).check_password(FACTORY_PASSWORD)     # type:ignore
