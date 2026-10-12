from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import Optional


@dataclass
class CustomerEntity:
    id: int
    first_name: str
    last_name: str
    email: Optional[str]
    phone_number: Optional[str]
    

@dataclass
class BusinessClientEntity:
    customer: CustomerEntity
    business_id: UUID
    display_name: str
    notes: str
    added_at: datetime
    updated_at: datetime
    