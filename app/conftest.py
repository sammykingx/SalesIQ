import pytest
from django.test import Client

from accounts.tests.factories import BusinessFactory, UserFactory


def _login(user) -> Client:
    c = Client()
    c.force_login(user)
    return c


# ---- businesses (only exist for onboarded users) ----------------
@pytest.fixture
def business(db):
    """Business whose owner email is verified + onboarded."""
    return BusinessFactory(online=True)


@pytest.fixture
def unverified_business(db):
    """Business whose owner is onboarded but has NOT verified their email."""
    return BusinessFactory(online=True, owner__verified=False)


@pytest.fixture
def other_business(db):
    """A second tenant, for isolation/permission tests."""
    return BusinessFactory(online=True)


# ---- users: verified & onboarded ---------------------------------
@pytest.fixture
def new_user(db):
    """
        A brand-new user right after sign-up.
        - Email status: Unverified (`is_verified = False`)
        - Onboarding status: Not started / No business (`onboarded = False`)
        
        Use for testing registration flows, email verification triggers, 
        or onboarding steps.
    """
    return UserFactory()


@pytest.fixture
def verified_not_onboarded_user(db):
    """
    A user who has verified their email but has NOT completed onboarding.
    - Email status: Verified (`is_verified = True`)
    - Onboarding status: Not started / No business (`onboarded = False`)
    
    Use for testing middleware blocks, redirect rules to onboarding, 
    or the onboarding API endpoint itself.
    """
    return UserFactory(verified=True)


@pytest.fixture
def unverified_onboarded_user(unverified_business):
    """
    A user who has completed onboarding (has a registered business) 
    but has NOT verified their email yet.
    - Email status: Unverified (`is_verified = False`)
    - Onboarding status: Completed (`onboarded = True`)
    
    Use for testing edge cases where users interact with business features 
    before completing their email confirmation, or checking verification restrictions.
    """
    return unverified_business.owner


@pytest.fixture
def verified_onboarded_user(business):
    """
    A user who has both verified their email and completed onboarding.
    - Email status: Verified (`is_verified = True`)
    - Onboarding status: Completed (`onboarded = True`)
    
    Use for testing features that require a fully onboarded user.
    """
    return business.owner


@pytest.fixture
def privileged_user(db, settings):
    user = UserFactory(verified=True, onboarded=True)
    settings.PREVILEDGE_USERS = [user.email]
    return user


# ---- clients: same names, logged in ------------------------------------
@pytest.fixture
def anon_client(client):
    """Not logged in."""
    return client


@pytest.fixture
def unverified_not_onboarded_client(new_user):
    """
    Test client authenticated as a brand-new, unverified, and not onboarded user.
    - Email status: Unverified (`is_verified = False`)
    - Onboarding status: Not started / No business (`onboarded = False`)
    
    Use for testing middleware redirects, sign-up flows, 
    or permission blocks on protected routes for new users.
    """
    return _login(new_user)


@pytest.fixture
def verified_not_onboarded_client(verified_not_onboarded_user):
    """
    Test client authenticated as a user with a verified email but no business.
    - Email status: Verified (`is_verified = True`)
    - Onboarding status: Not started / No business (`onboarded = False`)
    
    Use for testing access to the onboarding flow or middleware redirect behaviors.
    """
    return _login(verified_not_onboarded_user)


@pytest.fixture
def unverified_onboarded_client(unverified_onboarded_user):
    """
    Test client authenticated as a business owner with an unverified email.
    - Email status: Unverified (`is_verified = False`)
    - Onboarding status: Completed / Has business (`onboarded = True`)
    
    Use for testing restriction rules or business-specific endpoints for unverified accounts.
    """
    return _login(unverified_onboarded_user)


@pytest.fixture
def verified_onboarded_client(verified_onboarded_user):
    """
    Test client authenticated as a fully verified business owner.
    - Email status: Verified (`is_verified = True`)
    - Onboarding status: Completed / Has business (`onboarded = True`)
    
    Use for testing full access to authorized business endpoints and features.
    """
    return _login(verified_onboarded_user)


@pytest.fixture
def privileged_client(privileged_user):
    return _login(privileged_user)
