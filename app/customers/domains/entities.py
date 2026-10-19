from dataclasses import asdict, dataclass
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
    
    def to_dict(self) -> dict:
        """Convert the customer entity to a standard dictionary."""
        return asdict(self)
    

@dataclass
class BusinessClientEntity:
    customer: CustomerEntity
    business_id: UUID
    display_name: str
    slug: str
    notes: str
    added_at: datetime
    updated_at: datetime
    
    def to_dict(self) -> dict:
        """Convert the entity and its nested objects into a JSON-safe dictionary."""
        data = asdict(self)
        
        data['business_id'] = str(self.business_id)
        data['added_at'] = self.added_at.isoformat() if self.added_at else None
        data['updated_at'] = self.updated_at.isoformat() if self.updated_at else None
        
        if hasattr(self.customer, 'to_dict'):
            data['customer'] = self.customer.to_dict()
            
        return data
    