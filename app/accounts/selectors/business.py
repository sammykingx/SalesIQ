from accounts.domains.entities import BusinessEntity
from accounts.models import Business

from typing import Union
class BusinessSelector:
    """Selector class responsible for querying and mapping Business records from the database.

    Acts as a data retrieval layer, fetching user-associated business data 
    and converting ORM model instances into domain-level business entities.
    """

    def __init__(self) -> None:
        """Initializes the BusinessSelector with the default Business model."""
        self.model = Business

    def get_user_business(
        self, *, user_email: str, as_instance=False
    ) -> Union[BusinessEntity, Business, None]:
        """Retrieves a business record associated with a specific user email.

        Args:
            user_email (str): The email address of the business owner.
            as_instance (bool, optional): If True, returns the raw ORM model instance. 
                If False, converts and returns a BusinessEntity. Defaults to False.

        Returns:
            Union[BusinessEntity, Business, None]: The business record as a 
            BusinessEntity or model instance if found, otherwise None.
        """
        obj = self.model.objects.filter(owner=user_email).first()
        if as_instance:
            return obj
        return self._to_business_entity(instance=obj) if obj else None

    def _to_business_entity(self, instance) -> BusinessEntity:
        """Maps a raw Business database model instance to a domain BusinessEntity.

        Args:
            instance: The database model instance of the Business.

        Returns:
            BusinessEntity: A domain entity populated with fields from the model instance.
        """
        return BusinessEntity(
            id=instance.id,
            code=instance.code,
            owner_email=instance.owner.email,
            name=instance.name,
            phone_number=instance.phone_number,
            business_type=instance.business_type,
            address=instance.address,
            instagram_url=instance.instagram_url,
            tiktok_url=instance.tiktok_url,
            whatsapp_number=instance.whatsapp_number,
            website_url=instance.website_url,
            created_at=instance.created_at,
            updated_at=instance.updated_at,
        )
        