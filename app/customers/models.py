from django.db import models

# Create your models here.

class Customers(models.Model):
    """Canonical identity, used only for dedup matching across businesses."""
    
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    businesses = models.ManyToManyField(
        "accounts.Business",
        through="BusinessCustomers",
        related_name="registered_customers"
        # from a customer object you can acces all businesses customer.businesses.all()
    )
    
    class Meta:
        db_table = "customers"


class BusinessCustomers(models.Model):
    """The only thing a business actually sees/queries"""
    
    business = models.ForeignKey("accounts.Business", on_delete=models.CASCADE, related_name="clients")
    client = models.ForeignKey(Customers, on_delete=models.PROTECT, related_name="business_links")

    display_name = models.CharField(max_length=50, blank=True, help_text="Optinal Per business overide")
    notes = models.TextField(blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "business_customers"
        constraints = [
            models.UniqueConstraint(
                fields=["business", "client"],
                name="unique_business_client"
            )
        ]
