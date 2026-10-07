import pytest
from django.test import Client

from accounts.tests.factories import BusinessFactory


# ---- business tenants ----------------

@pytest.fixture
def business(db):
    """A Business whose owner email is verified + onboarded."""
    return BusinessFactory(online=True, owner__verified=True, owner__onboarded=True)

@pytest.fixture
def unverified_business(db):
    """A Business whose owner is onboarded but has NOT verified their email."""
    return BusinessFactory(online=True, owner__verified=False)


@pytest.fixture
def other_business(db):
    """A second tenant, for isolation/permission tests."""
    return BusinessFactory(both=True, owner__verified=True, owner__onboarded=True)


# ---- owners (for billing/subscriptions) -------------
@pytest.fixture
def business_owner(business):
    """Returns the owner of the standard test business (verified and onboarded)."""
    return business.owner

verified_onboarded_user = business_owner

@pytest.fixture
def privileged_owner(business, settings):
    """Returns the business owner and adds their email to the privileged users setting."""
    user = business.owner
    settings.PREVILEDGE_USERS = [user.email]
    return user


# ---- clients -------------------------------------------

@pytest.fixture
def make_client():
    """Factory: logged-in client for any user allowing dynamic creation of test clients for different user fixtures."""
    def _make(user) -> Client:
        c = Client()
        c.force_login(user)
        return c
    return _make

@pytest.fixture
def anon_client(client):
    """Not logged in."""
    return client

@pytest.fixture
def business_client(make_client, business_owner):
    """A business owner client who is logged in and has verified their email and completed onboarding."""
    return make_client(business_owner)

@pytest.fixture
def other_business_client(make_client, other_business):
    return make_client(other_business.owner)

