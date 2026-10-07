import pytest
from accounts.tests.factories import UserFactory


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
    
    Comes from the 'unverified_business' fixture, which creates a business with an unverified owner from the app/conftest.py file.
    """
    return unverified_business.owner


# ---- Clients for each user type ----------------

@pytest.fixture
def new_user_client(make_client, new_user):
    return make_client(new_user)


@pytest.fixture
def verified_not_onboarded_client(make_client, verified_not_onboarded_user):
    return make_client(verified_not_onboarded_user)


@pytest.fixture
def unverified_onboarded_client(make_client, unverified_onboarded_user):
    return make_client(unverified_onboarded_user)
