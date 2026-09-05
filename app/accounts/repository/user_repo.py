# manage write operations (creating, updating, and deleting) to db
from django.contrib.auth import get_user_model
from django.db import transaction
from accounts.serializers import UserRegistrationSchema
from typing import Optional


class UserRepository:
    def __init__(self) -> None:
        self.model = get_user_model()

    @transaction.atomic
    def create_user(self, user: UserRegistrationSchema) -> None:
        """Persists a UserEntity by creating a new database record and returns the saved entity."""
        instance = self.model(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
        )
        instance.set_password(user.password)
        instance.save()
        return None
    
    def mark_as_verified(self, email: str) -> None:
        self.model.objects.filter(
            email=email, is_verified=False
        ).update(is_verified=True)
    
    @transaction.atomic
    def update_password(self, *, user_email, new_password:str):
        instance = (
            self.model.objects
            .select_for_update()
            .filter(email=user_email)
            .first()
        )
        if instance:
            instance.set_password(new_password)
            instance.save(update_fields=["password"])
            
    def complete_onboarding(self, *, user_email: str):
        self.model.objects.filter(
            email=user_email, onboarded=False
        ).update(onboarded=True)
        
    def update_social_links(self, *, user_email: str, instagram_url: Optional[str] = None, tiktok_url: Optional[str] = None, website_url: Optional[str] = None):
        self.model.objects.filter(
            email=user_email
        ).update(
            instagram_url=instagram_url,
            tiktok_url=tiktok_url,
            website_url=website_url
        )
        
    def update_multiple_fields(self, *, user_id, **kwargs):
        """
        Safely updates fields, ignoring any keys that do not 
        match actual model fields to prevent FieldErrors.
        """
        valid_fields = {f.name for f in self.model._meta.get_fields()}
        filtered_kwargs = {key: val for key, val in kwargs.items() if key in valid_fields}
        
        if not filtered_kwargs:
            return 0
            
        return self.model.objects.filter(pk=user_id).update(**filtered_kwargs)
