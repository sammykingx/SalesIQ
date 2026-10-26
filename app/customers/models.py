from django.db import models
from customers.domains.customer_code import build_unique_customer_code

class Customers(models.Model):
    """
    Represents a global canonical customer identity used for deduplication 
    and cross-business matching.

    A single customer record can be associated with multiple businesses via 
    the `BusinessCustomers` through model. This allows different businesses 
    to share the same underlying identity while maintaining independent 
    tenant-specific relationships and metadata.

    The internal `code` field acts as a stable, human-readable identifier 
    used as the target for backend foreign key relationships (e.g., in `BusinessCustomers`), 
    guaranteeing a reliable relational reference even when optional fields like 
    email or phone number are null. It is strictly internal and never exposed to the frontend.
    """
    
    first_name = models.CharField(max_length=30, default=None)
    last_name = models.CharField(max_length=30, default=None)
    code = models.CharField(
        max_length=100, 
        unique=True, 
        editable=False, 
        null=True, 
        blank=True, 
        help_text=(
            "Internal human-readable unique reference code. Acts as the target "
            "foreign key for the BusinessCustomers model to ensure stable relational "
            "linking even when contact fields are null. Never exposed to the frontend."
        )
    )
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    using_temp_email = models.BooleanField(default=False, help_text="Designates whether this customer is using an auto-generated temporary email.")
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
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = build_unique_customer_code(
                f_name=self.first_name, 
                l_name=self.last_name
            )
        return super().save(*args, **kwargs)
    
    class Meta:
        db_table = "customers"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(email__isnull=False) | models.Q(phone_number__isnull=False),
                name="customer_requires_email_or_phone",
            )
        ]


class BusinessCustomers(models.Model):
    """
        Through model representing the scoped relationship between a Business and a Customer.

        This acts as the tenant-specific bridge. It is the primary model individual 
        businesses use to query, view, and manage their clients. It allows each business 
        to attach custom, localized context (such as business-specific display names, 
        slugs, and notes) to a shared global customer identity without affecting other businesses.
    """
    
    business = models.ForeignKey("accounts.Business", on_delete=models.CASCADE, related_name="clients")
    client = models.ForeignKey(Customers, on_delete=models.PROTECT, related_name="business_links", to_field="email")
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, help_text="URL safe string to identify customer")
    display_name = models.CharField(max_length=50, blank=True, help_text="Optional Per business overide")
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(
        max_length=20, 
        null=True, 
        blank=True, 
        help_text="Business-specific phone override. Changes apply only to this business, leaving the global profile untouched."
    )
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
