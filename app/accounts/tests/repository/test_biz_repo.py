import pytest

from django.db.models import Model
from accounts.repository import BusinessRepo

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
