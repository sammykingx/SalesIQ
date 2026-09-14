from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List, Union


@dataclass
class InvoiceItemEntity:
    id: str
    name: str
    product_type: str
    quantity: int
    unit_price: Decimal
    line_subtotal: Decimal


@dataclass
class InvoiceEntity:
    display_id: str
    slug: str
    status: str
    created_at: datetime
    currency: str
    business_id: str
    customer_id: str
    sub_total: Decimal
    discount_type: str
    discount_percentage: Decimal
    discount_amount: Decimal
    tax_name: Union[str, None]
    tax_percentage: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    items: List[InvoiceItemEntity]
