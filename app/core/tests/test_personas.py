import pytest
from django.urls import reverse

from accounts.models import Business
from core.url_names import ACCOUNTS

pytestmark = pytest.mark.django_db


PROTECTED_URL = ACCOUNTS.DASHBOARD
ONBOARDING_URL = ACCOUNTS.ONBOARDING


def has_business(user) -> bool:
    return Business.objects.filter(owner=user).exists()


# ---- 1. data state: does each user fixture match its name? -------------
@pytest.mark.parametrize(
    "fixture_name, verified, onboarded, has_biz",
    [
        ("unverified_not_onboarded_user", False, False, False),
        ("verified_not_onboarded_user",   True,  False, False),
        ("unverified_onboarded_user",     False, True,  True),
        ("verified_onboarded_user",       True,  True,  True),
    ],
)
def test_user_fixture_state(request, fixture_name, verified, onboarded, has_biz):
    user = request.getfixturevalue(fixture_name)
    assert user.is_verified is verified
    assert user.onboarded is onboarded
    assert has_business(user) is has_biz


def test_businesses_are_distinct_tenants(business, other_business, unverified_business):
    owners = {business.owner_id, other_business.owner_id, unverified_business.owner_id}
    assert len(owners) == 3


def test_privileged_user_is_in_settings(privileged_user, settings):
    assert privileged_user.email in settings.PREVILEDGE_USERS


# ---- 2. client state: is each client logged in as the matching user? ---
@pytest.mark.parametrize(
    "client_fixture, user_fixture",
    [
        ("unverified_not_onboarded_client", "unverified_not_onboarded_user"),
        ("verified_not_onboarded_client",   "verified_not_onboarded_user"),
        ("unverified_onboarded_client",     "unverified_onboarded_user"),
        ("verified_onboarded_client",       "verified_onboarded_user"),
        ("privileged_client",               "privileged_user"),
    ],
)
def test_client_is_logged_in_as_matching_user(request, client_fixture, user_fixture):
    client = request.getfixturevalue(client_fixture)
    user = request.getfixturevalue(user_fixture)
    assert client.session["_auth_user_id"] == str(user.pk)


def test_anon_client_is_not_logged_in(anon_client):
    assert "_auth_user_id" not in anon_client.session


# ---- 3. middleware: do the personas behave as the funnel intends? ------
@pytest.mark.parametrize(
    "client_fixture",
    ["unverified_not_onboarded_client", "verified_not_onboarded_client"],
)
def test_not_onboarded_is_redirected_to_onboarding(request, client_fixture):
    client = request.getfixturevalue(client_fixture)
    response = client.get(reverse(PROTECTED_URL))
    assert response.status_code == 302
    assert response.url == reverse(ONBOARDING_URL)


@pytest.mark.parametrize(
    "client_fixture",
    ["unverified_onboarded_client", "verified_onboarded_client", "privileged_client"],
)
def test_onboarded_is_not_redirected_to_onboarding(request, client_fixture):
    client = request.getfixturevalue(client_fixture)
    response = client.get(reverse(PROTECTED_URL))
    assert response.url != reverse(ONBOARDING_URL) if response.status_code == 302 else True
    