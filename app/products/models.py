from django.db import models
from uuid6 import uuid7



class ProductType(models.TextChoices):
    PHYSICAL = 'physical', 'Physical Product'
    DIGITAL = 'digital', 'Digital Product'
    SERVICE = 'service', 'Service'
    
    
class Products(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_type = models.CharField(max_length=50, choices=ProductType.choices, default=ProductType.PHYSICAL)
    description = models.TextField()
    business = models.ForeignKey("accounts.Business", on_delete=models.CASCADE, related_name="my_products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table = "products"
        constraints = [
            models.UniqueConstraint(
                fields=["business", "name"],
                name="unique_product_per_business"
            )
        ]
