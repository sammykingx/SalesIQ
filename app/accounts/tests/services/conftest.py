import pytest

from django.template.loader import render_to_string as django_render_to_string
from unittest.mock import MagicMock
from types import SimpleNamespace



@pytest.fixture(autouse=True)
def mailer(request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch):
    """
    Replaces AppMailerService in the service module named by the test module's
    SERVICES constant, so nothing can reach Resend. Returns the mock instance
    the service will use.
    """
    mailer_cls = MagicMock(name="AppMailerService")
    instance = mailer_cls.return_value
    instance.prepare_message.return_value = instance

    services = getattr(request.module, "SERVICES", None)
    if services:
        monkeypatch.setattr(f"{services}.AppMailerService", mailer_cls)
    return instance

@pytest.fixture
def token_service(request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch):
    """Fake TokenService for the email tests only, where the token's value is all we need."""
    cls = MagicMock(name="TokenService")
    cls.return_value.create_token.return_value = SimpleNamespace(token="tok-123")
    services = getattr(request.module, "SERVICES", None)
    if services:
        monkeypatch.setattr(f"{services}.TokenService", cls)
    return cls.return_value

@pytest.fixture
def render_spy(request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch):
    """Records render_to_string calls made by the service, but still renders for real."""
    spy = MagicMock(wraps=django_render_to_string)
    services = getattr(request.module, "SERVICES", None)
    if services:
        monkeypatch.setattr(f"{services}.render_to_string", spy)
    return spy
