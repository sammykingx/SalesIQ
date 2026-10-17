from django.db import models
from customers.domains.customer_code import build_unique_customer_code

class Customers(models.Model):
    """Canonical identity, used only for dedup matching across businesses."""
    
    first_name = models.CharField(max_length=30, default=None)
    last_name = models.CharField(max_length=30, default=None)
    # code = models.CharField(max_length=100, unique=True, editable=False, null=True, blank=True, help_text="A unique code to reference a customer")
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by_business = models.ForeignKey(
            "accounts.Business",
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name="originally_created_customers"
        ) 
    
    businesses = models.ManyToManyField(
        "accounts.Business",
        through="BusinessCustomers",
        related_name="registered_customers"
        # from a customer object you can acces all businesses customer.businesses.all()
    )
    
    # def save(self, *args, **kwargs):
    #     if not self.code:
    #         self.code = build_unique_customer_code(
    #             f_name=self.first_name, 
    #             l_name=self.last_name
    #         )
    #     return super().save(*args, **kwargs)
    
    class Meta:
        db_table = "customers"
        # constraints = [
        #     models.CheckConstraint(
        #         condition=models.Q(email__isnull=False) | models.Q(phone_number__isnull=False),
        #         name="customer_requires_email_or_phone",
        #     )
        # ]


class BusinessCustomers(models.Model):
    """The only thing a business actually sees/queries"""
    
    business = models.ForeignKey("accounts.Business", on_delete=models.CASCADE, related_name="clients")
    client = models.ForeignKey(Customers, on_delete=models.PROTECT, related_name="business_links", to_field="email")

    display_name = models.CharField(max_length=50, blank=True, help_text="Optional Per business overide")
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
