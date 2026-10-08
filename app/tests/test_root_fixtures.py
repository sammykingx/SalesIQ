from django.test import Client
from django.urls import reverse
from core.url_names import ACCOUNTS


ONBOARDING_URL = reverse(ACCOUNTS.ONBOARDING)
DASHBOARD_URL = reverse(ACCOUNTS.DASHBOARD)


def assert_onboarding_sends_to_dashboard(client: Client):
    response = client.get(ONBOARDING_URL)
    assert response.status_code in (301, 302)
    assert response.url == DASHBOARD_URL # type: ignore


# --------- Smoke Tests ---------
def test_tenants_are_distinct(business, other_business):
    assert business.pk != other_business.pk
    assert business.code != other_business.code
    assert business.owner_id != other_business.owner_id

def test_unverified_business_owner_is_actually_unverified(unverified_business):
    assert not unverified_business.owner.is_verified

def test_business_owner_is_sent_to_dashboard_from_onboarding(business_client):
    assert_onboarding_sends_to_dashboard(business_client)
