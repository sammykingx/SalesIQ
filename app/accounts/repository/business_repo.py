from accounts.models import Business
from django.db import transaction, IntegrityError
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from accounts.serializers import BusinessOnboardingSchema
from typing import Union


class BusinessRepo:
    def __init__(self) -> None:
        self.model = Business
        
     
    def create_business(self, *, biz_owner:AbstractUser, biz_data:BusinessOnboardingSchema) -> Union[Business, None]:
        try:
            return self.model.objects.create(
                owner=biz_owner,
                name=biz_data.business_name,
                phone_number=biz_data.phone_number,
                business_type=biz_data.business_type,
                address=biz_data.address,
                instagram_url=biz_data.socials.instagram_url, #type: ignore
                tiktok_url=biz_data.socials.tiktok_url, #type: ignore
                website_url=biz_data.socials.website_url, #type: ignore
            )
            
        except IntegrityError:
            import traceback
            traceback.print_exc()
            return None
        
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
