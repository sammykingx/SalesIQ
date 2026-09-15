from django.db import models
from uuid6 import uuid7
from decimal import Decimal


class DiscountType(models.TextChoices):
    NONE = "none", "No Discount"
    FLAT = "flat", "Flat Amount"
    PERCENTAGE = "percentage", "Percentage"

class InvoiceStatus(models.TextChoices):
    PAID = "paid", "Paid"
    VOID = "void", "Void"


class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    display_id = models.CharField(max_length=20, unique=True, editable=False, help_text="public facing invoice id")
    slug = models.SlugField(max_length=72, unique=True, editable=False, help_text="public receipt URL, separate from display_id")
    business = models.ForeignKey("accounts.Business", on_delete=models.CASCADE, related_name="invoices")
    customer = models.ForeignKey("customers.BusinessCustomers", on_delete=models.PROTECT, related_name="invoices")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    discount_type = models.CharField(max_length=10, choices=DiscountType.choices, default=DiscountType.NONE)
    discount_value = models.DecimalField(
        max_digits=12,
        decimal_places=2, 
        default=Decimal("0"), 
        help_text="Enter as a decimal percentage (e.g., use 5.78 for 5.78%)."
    )

    discount_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=Decimal("0"), 
        help_text="The calculated discount amount (Subtotal × Discount Value)."
    )
    
    tax_name = models.CharField(max_length=50, blank=True, null=True)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0"))
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, default=Decimal("0"))

    total = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="NGN")

    status = models.CharField(max_length=10, choices=InvoiceStatus.choices, default=InvoiceStatus.PAID)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "invoices"
        # indexes = [
        #     models.Index(fields=["business", "-created_at"]),
        #     models.Index(fields=["customer", "-created_at"]),
        # ]


class InvoiceLineItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="line_items")
    product = models.ForeignKey(
        "products.Products", on_delete=models.SET_NULL, null=True, blank=True, related_name="line_items"
    )
    
    product_name = models.CharField(max_length=70)
    product_type = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Sale price the business decides to sell which is differnet from the product catalog price")

    quantity = models.PositiveIntegerField(default=1)
    line_subtotal = models.DecimalField(max_digits=12, decimal_places=2, help_text="(unit_price * quantity)")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "invoice_line_items"
        indexes = [models.Index(fields=["product"])]
        