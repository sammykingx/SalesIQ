from dataclasses import asdict, dataclass
from datetime import datetime
from uuid import UUID
from typing import Optional


@dataclass
class CustomerEntity:
    """
    Represents an individual customer entity who is not associated with any business.

    Attributes:
        id (int): The primary database identifier for the customer record.
        code (str): A system-unique, human-friendly reference code for the customer 
            that is also utilized for relationships/lookups in the `BusinessCustomers` through model.
        first_name (str): The customer's first name.
        last_name (str): The customer's last name.
        email (Optional[str]): The customer's email address, if available.
        using_temp_email (bool): Flag indicating whether the record was created using a 
            system-generated temporary email (True) or the customer's actual email (False).
        phone_number (Optional[str]): The customer's phone number, if available.
    """
    id: int
    code: str
    first_name: str
    last_name: str
    email: Optional[str]
    using_temp_email: bool
    phone_number: Optional[str]
    
    def to_dict(self) -> dict:
        """Convert the customer entity to a standard dictionary."""
        return {
            "id": self.id,
            "code": self.code,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": None if self.using_temp_email else self.email,
            "phone_number": self.phone_number,
        }
    

@dataclass
class BusinessClientEntity:
    customer: CustomerEntity
    business_id: UUID
    display_name: str
    email: Optional[str]
    phone_number: Optional[str]
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
    