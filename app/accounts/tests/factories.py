import factory
from accounts.models import CustomUserModel, Business
from accounts.models.business import BusinessType


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating `CustomUserModel` instances for testing.

    Defaults:
        - first_name: Random first name (Faker)
        - last_name: Random last name (Faker)
        - email: Unique sequential email (e.g., user0@example.com, user1@example.com)
        - password: Default hashed/raw secure password ("securepassword123")
        - mobile_number: Random phone number (Faker)
        - is_verified: False
        - onboarded: False

    Traits (Params):
        - verified (bool): Sets `is_verified = True` when passed as `UserFactory(verified=True)`.
        - onboarded (bool): Sets `onboarded = True` when passed as `UserFactory(onboarded=True)`.

    Example Usage:
        >>> # Create a standard default user
        >>> user = UserFactory()

        >>> # Create a user who is verified and onboarded
        >>> pro_user = UserFactory(verified=True, onboarded=True)
    """

    first_name = factory.Faker("first_name") # type: ignore
    last_name = factory.Faker("last_name") # type: ignore
    email = factory.Sequence(lambda n: f"user{n}@example.com") # type: ignore
    password = factory.django.Password("securepassword123")
    mobile_number = factory.Faker("phone_number") # type: ignore
    is_verified = False
    onboarded = False
    
    class Meta: # type: ignore
            model = CustomUserModel
            
    class Params: # type: ignore
        verified = factory.Trait(is_verified=True)  # type: ignore
        is_onboarded = factory.Trait(onboarded=True)   # type: ignore
        

class BusinessFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating `Business` model instances for testing.

    Defaults:
        - owner: Inline `UserFactory` instance (pre-verified and onboarded by default).
        - name: Unique sequential shop name (e.g., "Test Shop 0", "Test Shop 1").
        - phone_number: Unique sequential local phone format ("08030000000").
        - business_type: Defaults to `BusinessType.ONLINE`.
        - address: Random address (Faker).
        - whatsapp_number: Random phone number (Faker).
        - instagram_url: Unique sequential Instagram URL.
        - tiktok_url: Unique sequential TikTok URL.
        - website_url: Random URL (Faker).

    Traits (Params):
        - online (bool): Sets `business_type = BusinessType.ONLINE` and clears `address = None`.
        - physical (bool): Sets `business_type = BusinessType.PHYSICAL`.
        - both (bool): Sets `business_type = BusinessType.BOTH`.

    Example Usage:
        >>> # Create a default online business with an automatic owner
        >>> shop = BusinessFactory()

        >>> # Create a physical business shop
        >>> physical_shop = BusinessFactory(physical=True)

        >>> # Attach a business to an existing user instead of creating a new one
        >>> custom_shop = BusinessFactory(owner=my_user, both=True)
    """
    owner = factory.SubFactory(UserFactory, onboarded=True, verified=True) # type: ignore
    name = factory.Sequence(lambda n: f"Test Shop {n}")     # type: ignore
    phone_number = factory.Sequence(lambda n: f"0803{n:07d}")   # type: ignore
    business_type = BusinessType.ONLINE
    
    address = factory.Faker("address")      # type: ignore
    whatsapp_number = factory.Faker("phone_number")     # type: ignore
    instagram_url = factory.Sequence(lambda n: f"https://instagram.com/test_shop_{n}")        # type: ignore
    tiktok_url = factory.Sequence(lambda n: f"https://tiktok.com/test_shop_{n}")      # type: ignore
    website_url = factory.Faker("url")      # type: ignore
    
    class Meta: # type: ignore
        model = Business

    class Params:
        online = factory.Trait(business_type=BusinessType.ONLINE, address=None)     # type: ignore
        physical = factory.Trait(business_type=BusinessType.PHYSICAL)               # type: ignore
        both = factory.Trait(business_type=BusinessType.BOTH)                       # type: ignore
    