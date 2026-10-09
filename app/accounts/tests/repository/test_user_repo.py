# test create_user actually creates a user to the db raises possible errors that could happen
# like integrity or operational errors 

import pytest

from accounts.serializers import UserRegistrationSchema
from accounts.repository import UserRepository
from accounts.tests.factories import UserFactory
from django.db.models import Model

PASSWORD = "Str0ng!pass"
FACTORY_PASSWORD = "securepassword123"

def reload_from_db(obj: Model):
    """Refreshes and reloads a model instance from the database."""
    return obj.refresh_from_db()

@pytest.fixture
def repo():
    """Provides an instance of the UserRepository."""
    return UserRepository()

@pytest.fixture
def bystander(db):
    """Provides a second, newly registered user on the platform."""
    return UserFactory()

@pytest.fixture
def user_data(db):
    """Provides valid payload data for user registration tests."""
    return UserRegistrationSchema.model_validate({
        "first_name": "Ada", "last_name": "Obi", "email": "ada@example.com",
        "password": PASSWORD, "confirm_password": PASSWORD,
    })
    

def test_create_user_persists_fields_and_hashes_password(repo, user_data, django_user_model):
    repo.create_user(user_data)

    saved = django_user_model.objects.get(email="ada@example.com")
    assert (saved.first_name, saved.last_name) == ("Ada", "Obi")
    assert saved.password != PASSWORD
    assert saved.check_password(PASSWORD)


def test_create_user_starts_unverified_and_not_onboarded(repo, user_data, django_user_model):
    repo.create_user(user_data)

    saved = django_user_model.objects.get(email="ada@example.com")
    assert not saved.is_verified
    assert not saved.onboarded
    