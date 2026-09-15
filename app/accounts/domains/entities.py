from dataclasses import dataclass, field
from datetime import datetime
from pydantic import EmailStr, UUID7
from typing import Literal, Optional, Union
from uuid import UUID


@dataclass
class UserEntity:
    """Represents a system user entity containing core identification and profile details.

    Attributes:
        id (UUID7): The unique identifier for the user.
        first_name (str): The user's given name.
        last_name (str): The user's surname or family name.
        email (EmailStr): The user's primary email address for communication and authentication.
        mobile_number (Union[str, None]): The user's mobile contact number, if provided.
        is_verified (bool): Flag indicating whether the user's account has been verified.
    """
    id: UUID7
    first_name: str
    last_name: str
    email: EmailStr
    mobile_number: Union[str, None]
    is_verified: bool
    
@dataclass
class BusinessEntity:
    """Represents a registered business entity linked to an owner, capturing operational and social details.

    Attributes:
        id (UUID): The unique identifier for the business.
        code (str): A unique alphanumeric code representing the business.
        owner_email (EmailStr): The email address of the user who owns or manages the business.
        name (str): The commercial or trading name of the business.
        phone_number (str): The primary contact phone number for the business.
        business_type (Literal["online", "physical", "both"]): The operational model of the business.
        address (Optional[str]): Physical location address of the business, if applicable.
        instagram_url (Optional[str]): Official Instagram profile URL.
        tiktok_url (Optional[str]): Official TikTok profile URL.
        website_url (Optional[str]): Official business website URL.
        whatsapp_number (Optional[str]): Dedicated WhatsApp contact number for business inquiries.
        created_at (Optional[datetime]): Timestamp when the business record was created.
        updated_at (Optional[datetime]): Timestamp when the business record was last updated.
    """
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
    whatsapp_number: Optional[str] = None
    created_at: Optional[datetime] = field(default=None)
    updated_at: Optional[datetime] = field(default=None)
    