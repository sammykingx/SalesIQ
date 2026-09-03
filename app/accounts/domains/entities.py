from dataclasses import dataclass, field
from datetime import datetime
from pydantic import EmailStr, UUID7
from typing import Literal, Optional, Union
from uuid import UUID


@dataclass
class UserEntity:
    id: UUID7
    first_name: str
    last_name: str
    email: EmailStr
    mobile_number: Union[str, None]
    is_verified: bool
    
@dataclass
class BusinessEntity:
    id: UUID
    code: str
    owner_email: EmailStr
    name: str
    phone_number: str
    business_type: Literal["online", "physical", "both"]
    address: Optional[str] = None
    instagram_url: Optional[str] = None
    tiktok_url: Optional[str] = None
    website_url: Optional[str] = None
    created_at: Optional[datetime] = field(default=None)
    updated_at: Optional[datetime] = field(default=None)