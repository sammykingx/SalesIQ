from django.db import models
from django.contrib.auth.models import AbstractUser


# Fields from django user models
#   first_name, last_name, email, password,
#   is_active, date_joined, last_login
#   is_staff(can login into django admin), is_superuser(has all perms)

class CustomUserModel(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    mobile_number =  models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = "accounts"   
        
        
    def __str__(self) -> str:
        return (
            f"{self.first_name} {self.last_name} "
            f"<{self.email}> "
            f"{'(verified)' if self.is_verified else '(not verified)'}"
        )

    def __repr__(self) -> str:
        return (
            f"CustomUSerModel(first_name={self.first_name!r}, "
            f"last_name={self.last_name!r}, "
            f"email={self.email!r}, "
            f"is_verified={self.is_verified!r}, "
            f"is_active={self.is_active!r})"
        )
        
    