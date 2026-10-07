import pytest
from django.urls import reverse
from core.url_names import ACCOUNTS, INVOICES, PRODUCTS, CUSTOMERS


PROTECTED_URLS = [
    reverse(ACCOUNTS.DASHBOARD),
    reverse(ACCOUNTS.SETTINGS),
    reverse(INVOICES.CREATE),
    reverse(PRODUCTS.LIST),
    reverse(CUSTOMERS.LIST),
]

def test_tenants_are_distinct(business, other_business):
    assert business.pk != other_business.pk
    assert business.code != other_business.code
    assert business.owner_id != other_business.owner_id
    

def test_unverified_business_owner_is_actually_unverified(unverified_business):
    assert not unverified_business.owner.is_verified
