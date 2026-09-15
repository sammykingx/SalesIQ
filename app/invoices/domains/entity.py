from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List, Union
from uuid import UUID


@dataclass
class InvoiceItemEntity:
    id: UUID
    name: str
    product_type: str
    quantity: int
    unit_price: Decimal
    line_subtotal: Decimal


@dataclass
class InvoiceEntity:
    """Represents a sale invoice with financial breakdowns, item lists, and metadata.

    Attributes:
        display_id: Human-readable invoice identifier.
        slug: URL-friendly unique identifier for the invoice.
        status: Current state of the invoice (e.g., draft, paid, pending).
        created_at: Timestamp when the invoice was generated.
        currency: Three-letter ISO currency code (e.g., USD, EUR).
        business_id: Unique identifier of the issuing business.
        customer_id: Unique identifier of the customer.
        sub_total: Total amount before discounts and taxes.
        discount_type: Type of discount applied (e.g., percentage, fixed).
        discount_percentage: Percentage rate of the discount (e.g 5% is represented as 0.05).
        discount_amount: Absolute monetary value of the discount.
        tax_name: Name of the applied tax, if any.
        tax_percentage: Percentage rate of the tax.
        tax_amount: Absolute monetary value of the tax.
        total_amount: Final payable amount after discounts and taxes.
        items: List of line items associated with the invoice.
    """
    display_id: str
    slug: str
    status: str
    created_at: datetime
    currency: str
    business_id: UUID
    customer_id: int
    sub_total: Decimal
    discount_type: str
    discount_percentage: Decimal
    discount_amount: Decimal
    tax_name: Union[str, None]
    tax_percentage: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    line_items: List[InvoiceItemEntity]
