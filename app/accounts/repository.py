# manage write operations (creating, updating, and deleting) to db
from django.contrib.auth import get_user_model
from django.db import transaction
from .serializers import UserRegistrationSchema


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
        instance.set_password(user.password1)
        instance.save()
        return None
    