import pytest

from django.db.models import Model
from django.db import IntegrityError
from accounts.repository import BusinessRepo
from accounts.serializers import BusinessOnboardingSchema, SocialLinksSchema
from unittest.mock import patch

@pytest.fixture
def repo():
    """Return an instance of BusinessRepo for testing."""
    return BusinessRepo()

def reload(model_obj: Model):
    """Refresh a Django model instance from the database and return it."""
    model_obj.refresh_from_db()
    return model_obj


@pytest.mark.parametrize(
    ("kwargs", "applied"),
    [
        pytest.param({"name": "Gomora Inc. limited"}, {"name": "Gomora Inc. limited"}, id="one-valid-model-field"),
        pytest.param(
            {"name": "Anna Emmporium", "phone_number": "+1 (565) 987-456"},
            {"name": "Anna Emmporium", "phone_number": "+1 (565) 987-456"},
            id="several-valid-model-fields",
        ),
        pytest.param({"bogus": "x"}, {}, id="one-unknown-field"),
        pytest.param({"bogus": "x", "also_fake": 1}, {}, id="several-unknown-fields"),
        pytest.param({"name": "Giant Star Limited", "bogus": "x"}, {"name": "Giant Star Limited"}, id="mixed-valid-with-invalid-model-fields"),
    ],
)
def test_update_multiple_fields_for_business_ignores_unknown_model_fields(repo, business, kwargs, applied):
    before = {"name": business.name, "phone_number": business.phone_number}
    updated = repo.update_multiple_fields(owner=business.owner, **kwargs)

    user = reload(business)
    after_update = {**before, **applied}
    
    assert updated == (1 if applied else 0)
    assert {"name": business.name, "phone_number": business.phone_number} == after_update
    
    
def create_new_business_succefully(repo, new_user):
    """Test that a brand new business is successfully created and returns (business, True)."""
    biz_data = BusinessOnboardingSchema( # type: ignore
        business_name="Acme Fashion",
        phone_number="+1234567890",
        business_type="online",
        socials=SocialLinksSchema(instagram_url="https://instagram.com/acme") #type: ignore
    )
    
    business, created = repo.create_business(biz_owner=new_user, biz_data=biz_data)
    
    assert created is True
    assert business is not None
    assert business.name == "Acme Fashion"


def test_get_existing_business_if_already_created(repo, new_user):
    """Test that calling create_business again fetches the existing record and returns (business, False)."""
    biz_data = BusinessOnboardingSchema(    # type: ignore
        business_name="Acme Fashion",
        phone_number="+1234567890",
        business_type="online"
    )
    
    business_first, created_first = repo.create_business(biz_owner=new_user, biz_data=biz_data)
    assert created_first is True

    business_second, created_second = repo.create_business(biz_owner=new_user, biz_data=biz_data)
    
    assert created_second is False
    assert business_second.pk == business_first.pk


def test_create_business_handles_integrity_error(repo, new_user):
    """Test that an IntegrityError is caught gracefully and returns (None, False)."""
    biz_data = BusinessOnboardingSchema(
        business_name="Error Shop",
        phone_number="+1234567890",
        business_type="physical",
        address="123 Main St"
    )
    
    with patch.object(repo.model.objects, 'get_or_create', side_effect=IntegrityError("Unique constraint violation")):
        business, created = repo.create_business(biz_owner=new_user, biz_data=biz_data)
        
        assert business is None
        assert created is False
