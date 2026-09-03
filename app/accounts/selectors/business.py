from accounts.domains.entities import BusinessEntity
from accounts.models import Business

from typing import Union

class BusinessSelector:
    def __init__(self) -> None:
        self.model = Business
    
    def get_user_business(self, *, user_email:str) -> Union[BusinessEntity, None]:
            obj = self.model.objects.filter(owner=user_email).first()
            return self._to_business_entity(instance=obj) if obj else None
        
    def _to_business_entity(self, instance): 
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
            website_url=instance.website_url,
            created_at=instance.created_at,
            updated_at=instance.updated_at
        )
        