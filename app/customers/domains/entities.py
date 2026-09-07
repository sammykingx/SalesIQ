from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class CustomerEntity:
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    

@dataclass
class BusinessClientEntity:
    customer: CustomerEntity
    business_id: UUID
    display_name: str
    notes: str
    added_at: datetime
    updated_at: datetime
    