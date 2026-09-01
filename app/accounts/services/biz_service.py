from accounts.repository import BusinessRepo,UserRepository
from accounts.domains.exceptions import MultipleBusinessNotAllowedError
from accounts.serializers import BusinessOnboardingSchema
from django.contrib.auth.models import AbstractUser


class BusinessService:
    def __init__(self, owner: AbstractUser) -> None:
        self.biz_owner = owner
        self.biz_repo = BusinessRepo()
        self.user_repo = UserRepository()
        
    def register_business(self, data:BusinessOnboardingSchema):
        if not self.biz_owner.onboarded: # type: ignore
            created = self.biz_repo.create_business(biz_owner=self.biz_owner, biz_data=data)
            if not created:
                raise MultipleBusinessNotAllowedError()
            self.user_repo.complete_onboarding(user_email=self.biz_owner.email)
        