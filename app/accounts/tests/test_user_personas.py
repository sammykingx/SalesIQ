from django.test import Client
from django.urls import reverse
from core.url_names import ACCOUNTS


ONBOARDING_URL = reverse(ACCOUNTS.ONBOARDING)
ACTIVATION_URL = reverse(ACCOUNTS.ACTIVATION, kwargs={"token": "dummy_token"})
LOGOUT_URL = reverse(ACCOUNTS.AUTH.LOGOUT)
LOGIN_URL = reverse(ACCOUNTS.AUTH.LOGIN)
DASHBOARD_URL = reverse(ACCOUNTS.DASHBOARD)

# shared assertions
def assert_redirected_to_onboarding(client: Client):
    response = client.get(DASHBOARD_URL)
    assert response.status_code in (301, 302)
    assert response.url == ONBOARDING_URL # type: ignore

def assert_onboarding_sends_to_dashboard(client: Client):
    response = client.get(ONBOARDING_URL)
    assert response.status_code in (301, 302)
    assert response.url == DASHBOARD_URL # type: ignore
    
def assert_exempt_views_reachable(client: Client):
    assert client.get(ONBOARDING_URL).status_code == 200
    assert client.get(ACTIVATION_URL).status_code == 200
    
    logout_response = client.post(LOGOUT_URL)
    
    assert logout_response.status_code in (301, 302)
    assert logout_response.url == LOGIN_URL # type: ignore


# tests
def test_onboarded_unverified_owner_is_sent_to_dashboard_from_onboarding(unverified_onboarded_client):
    assert_onboarding_sends_to_dashboard(unverified_onboarded_client)

def test_not_onboarded_user_is_redirected_to_onboarding(new_user_client, verified_not_onboarded_client):
    assert_redirected_to_onboarding(new_user_client)
    assert_redirected_to_onboarding(verified_not_onboarded_client)
    
def test_exempt_views_reachable_for_not_onboarded_user(new_user_client, verified_not_onboarded_client):
    assert_exempt_views_reachable(new_user_client)
    assert_exempt_views_reachable(verified_not_onboarded_client)
    