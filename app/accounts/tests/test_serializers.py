import pytest
from accounts.serializers import BasePasswordSchema
from pydantic import ValidationError


VALID = "Str0ng!pass"


@pytest.mark.parametrize(
    ("password", "confirm_password"),
    [
        pytest.param(VALID, "Different1!", id="mismatch"),
        pytest.param("lower1!only", "lower1!only", id="no-uppercase"),
        pytest.param("UPPER1!ONLY", "UPPER1!ONLY", id="no-lowercase"),
        pytest.param("NoDigits!here", "NoDigits!here", id="no-digit"),
        pytest.param("NoSpecial1here", "NoSpecial1here", id="no-special-char"),
        pytest.param("        ", "        ", id="fails-every-rule"),
    ],
)
def test_invalid_passwords_raise_validation_error(password, confirm_password):
    with pytest.raises(ValidationError):
        BasePasswordSchema(password=password, confirm_password=confirm_password)


@pytest.mark.parametrize(
    "password",
    [
        pytest.param(VALID, id="typical"),
        pytest.param("Aa1!aaaa", id="exactly-8-chars"),
        pytest.param("Averylongpassword1!withmanychars", id="long"),
    ],
)
def test_valid_passwords_are_accepted(password):
    schema = BasePasswordSchema(password=password, confirm_password=password)

    assert schema.password == password
