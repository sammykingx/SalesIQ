from django.urls import reverse
from core.url_names import INVOICES
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import AliasPath, BaseModel, ConfigDict, Field, field_validator, model_validator


class BusinessSummarySchema(BaseModel):
    """Schema representing the business issuing the invoice."""
    model_config = ConfigDict(from_attributes=True)
    
    code: str
    name: str
    phone_number: str
    business_type: Optional[str]
    address: Optional[str]
    
    instagram_url: Optional[str]
    tiktok_url: Optional[str]
    website_url: Optional[str]


class CustomerSummarySchema(BaseModel):
    """Schema representing the customer receiving the invoice."""
    
    model_config = ConfigDict(from_attributes=True)
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str]


class InvoiceLineItemResponseSchema(BaseModel):
    """Schema representing an individual line item associated with an invoice."""
    model_config = ConfigDict(from_attributes=True)

    product_name: str
    product_type: str
    unit_price: Decimal = Field(..., description="Sale price set for this specific transaction line.")
    quantity: int
    line_subtotal: Decimal = Field(..., description="Calculated total for this line item (unit_price * quantity).")


class InvoiceDetailResponseSchema(BaseModel):
    """
        Comprehensive schema for serializing a complete Invoice instance, 
        including its relationships with the business, customer, and nested line items.
    """
    model_config = ConfigDict(from_attributes=True)
    
    display_id: str = Field(..., description="Public facing invoice identifier.")
    slug: str = Field(..., description="Public receipt URL slug.")
    
    business: BusinessSummarySchema
    customer: CustomerSummarySchema = Field(
        ..., validation_alias=AliasPath("customer", "client")
    )
    
    subtotal: Decimal
    discount_type: str
    discount_value: Decimal = Field(..., description="Decimal percentage representation (e.g., 0.05 for 5%).")
    discount_amount: Decimal
    
    tax_name: Optional[str] = None
    tax_percentage: Decimal
    tax_amount: Optional[Decimal] = None
    
    total: Decimal
    currency: str = "NGN"
    status: str
    
    items: List[InvoiceLineItemResponseSchema] = Field(default_factory=list, validation_alias="line_items")
    
    # Timestamps
    created_at: datetime
    
    @field_validator("items", mode="before")
    @classmethod
    def resolve_items(cls, v):
        if hasattr(v, "all"):
            return list(v.all())
        return v


class InvoiceListResponseSchema(BaseModel):
    """Schema for representing an invoice item within a list view.

    Attributes:
        display_id: The public-facing or human-readable identifier for the invoice.
        created_at: The timestamp when the invoice was created.
        customer: Summary details of the customer associated with the invoice.
        status: The current status of the invoice (e.g., paid, pending, overdue).
        total: The total monetary amount for the invoice.
        url: The URL to the individual invoice detail page.
    """
    model_config = ConfigDict(from_attributes=True)
    
    display_id: str
    created_at: datetime
    customer: CustomerSummarySchema = Field(
        ..., validation_alias=AliasPath("customer", "client")
    )
    status: str
    total: Decimal
    url: str
    
    @model_validator(mode="before")
    @classmethod
    def _inject_detail_url(cls, invoice):
        if not hasattr(invoice, "url"):
            invoice.url = reverse(INVOICES.VIEW, kwargs={"slug": invoice.slug})
        return invoice
    