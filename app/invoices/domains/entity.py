from accounts.domains.entities import BusinessEntity
from customers.domains.entities import CustomerEntity
from dataclasses import dataclass
from datetime import datetime
from typing import List, Literal


@dataclass
class InvoiceItemEntity:
    id: str
    name: str
    product_type: Literal['physical', 'digital', 'service']
    quantity: int
    unit_price: float
    total_price: float


@dataclass
class InvoiceEntity:
    ref: str
    status: str
    created_at: datetime
    payment_method: str
    channel: str
    business: BusinessEntity
    customer: CustomerEntity
    items: List[InvoiceItemEntity]
    sub_total: float
    discount_percentage: float
    discount_amount: float
    tax_name: str
    tax_percentage: float
    tax_amount: float
    total_amount_paid: float
