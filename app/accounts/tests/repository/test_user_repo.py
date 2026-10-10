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
    obj.refresh_from_db()
    return obj

@pytest.fixture
def repo():
    """Provides an instance of the UserRepository."""
    return UserRepository()

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
    

@pytest.mark.parametrize(
    ("kwargs", "applied"),
    [
        pytest.param({"first_name": "Zed"}, {"first_name": "Zed"}, id="one-valid-model-field"),
        pytest.param(
            {"first_name": "Zed", "last_name": "Arthur"},
            {"first_name": "Zed", "last_name": "Arthur"},
            id="several-valid-model-fields",
        ),
        pytest.param({"bogus": "x"}, {}, id="one-unknown-field"),
        pytest.param({"bogus": "x", "also_fake": 1}, {}, id="several-unknown-fields"),
        pytest.param({"first_name": "Zed", "bogus": "x"}, {"first_name": "Zed"}, id="mixed-valid-with-invalid-model-fields"),
    ],
)
def test_update_multiple_fields_ignores_unknown_model_fields(repo, new_user, kwargs, applied):
    before = {"first_name": new_user.first_name, "last_name": new_user.last_name}
    updated = repo.update_multiple_fields(user_id=new_user.pk, **kwargs)

    user = reload_from_db(new_user)
    after_update = {**before, **applied}
    
    assert updated == (1 if applied else 0)
    assert {"first_name": user.first_name, "last_name": user.last_name} == after_update #type: ignore
    
    
def test_repo_update_password(repo, new_user):
    repo.update_password(user_email=new_user.email, new_password=PASSWORD)
    prev_pwd_hash = new_user.password
    user = reload_from_db(new_user)
    
    assert user.password != prev_pwd_hash   # type: ignore
    