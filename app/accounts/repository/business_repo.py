from accounts.models import Business
from django.db import IntegrityError
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from accounts.serializers import BusinessOnboardingSchema
from typing import Tuple, Optional
import logging


logger = logging.getLogger(__name__)

class BusinessRepo:
    """Repository layer responsible for handling database persistence and queries for Business models."""
    
    def __init__(self) -> None:
        self.model = Business
        
     
    def create_business(
        self, *, biz_owner: AbstractUser, biz_data: BusinessOnboardingSchema
    ) -> Tuple[Optional[Business], bool]:
        """Create a new business record or return the existing one for the owner.

        Leverages Django's `get_or_create` to safely handle the OneToOneField relationship 
        between the owner and their business, avoiding integrity clashes if a record already exists.

        Args:
            biz_owner (AbstractUser): The user instance owning the business.
            biz_data (BusinessOnboardingSchema): Validated schema containing business details.

        Returns:
            Tuple[Optional[Business], bool]: A tuple containing:
                - The created or existing Business instance (or None if an integrity error occurs).
                - A boolean indicating whether a new business was created (True) or fetched (False).

        Raises:
            Exception: Bubbles up any unexpected database or system errors after logging.
        """
        try:
            business, created = self.model.objects.get_or_create(
                owner=biz_owner,
                defaults={
                    "name": biz_data.business_name,
                    "phone_number": biz_data.phone_number,
                    "business_type": biz_data.business_type,
                    "address": biz_data.address,
                    "instagram_url": getattr(biz_data.socials, "instagram_url", None),
                    "tiktok_url": getattr(biz_data.socials, "tiktok_url", None),
                    "website_url": getattr(biz_data.socials, "website_url", None),
                },
            )
            return business, created
            
        except IntegrityError as err:
            logger.warning(
                "Integrity error while creating/fetching business '%s' for owner: %s. Error: %s",
                biz_data.business_name,
                getattr(biz_owner, "email", biz_owner),
                err,
            )
            return None, False
            
        except Exception as err:
            logger.exception(
                "Unhandled exception occurred while creating business '%s' for owner: %s. Error: %s",
                biz_data.business_name,
                getattr(biz_owner, "email", biz_owner),
                err,
            )
            raise
            
        
    def update_multiple_fields(self, *, owner, **kwargs):
        """
            Safely updates fields, ignoring any keys that do not 
            match actual model fields to prevent FieldErrors.
        """
        valid_fields = {f.name for f in self.model._meta.get_fields()}
        filtered_kwargs = {key: val for key, val in kwargs.items() if key in valid_fields}
            
        if not filtered_kwargs:
            return 0

        return self.model.objects.filter(owner=owner).update(**filtered_kwargs, updated_at=timezone.now())
