from django.contrib.auth import get_user_model
from accounts.domains.entities import UserEntity
from typing import Union

class UserSelector:
    def __init__(self) -> None:
        self.model = get_user_model()
        
    def get_by_email(self, *, email:str) -> Union[UserEntity, None]:
        obj = self.model.objects.filter(email=email).first()
        return self._to_user_entity(instance=obj) if obj else None
    
    def _to_user_entity(self, instance):
        return UserEntity(
            id=instance.id,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email,
            mobile_number=instance.mobile_number,
            is_verified=instance.is_verified,
        )
