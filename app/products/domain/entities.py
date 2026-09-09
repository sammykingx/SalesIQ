from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from uuid import UUID


@dataclass
class ProductEntity:
    """
    Pure domain entity representing a Product. 
    Decoupled from the Django ORM, used across domain services and use cases.
    """
    id: UUID
    name: str
    price: Decimal
    product_type: str
    description: str
    business_id: UUID
    created_at: datetime
    updated_at: datetime
