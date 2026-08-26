from django.db import models
from django.conf import settings
from uuid6 import uuid7
from nanoid import generate



def generate_business_id():
    seed = "23456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    return "BIZ-" + generate(seed, 12)

class BusinessType(models.TextChoices):
        ONLINE = 'online', 'Online'
        PHYSICAL = 'physical', 'Physical'
        BOTH = 'both', 'Both'
        
class Business(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False, help_text="Django table id")
    code = models.CharField(max_length=20, unique=True, default=generate_business_id, editable=False, help_text="Business id")
    
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="my_business")
    name = models.CharField(max_length=50, help_text="Name of the buisness e.g ANNA EMPORIUM")
    phone_number = models.CharField(max_length=20)
    business_type = business_type = models.CharField(max_length=15, choices=BusinessType.choices, blank=True)
    
    address = models.TextField(blank=True)

    instagram_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "business"
    
    