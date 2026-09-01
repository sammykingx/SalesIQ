from pydantic import BaseModel, EmailStr, Field, model_validator
from pydantic import HttpUrl
from typing import Union, Literal, Optional
import re


class BasePasswordSchema(BaseModel):
    """Base schema containing password fields and shared validation rules."""
    
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    
    @model_validator(mode='after')
    def validate_passwords(self) -> 'BasePasswordSchema':
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match.')
            
        password = self.password
        if not re.search(r'[A-Z]', password):
            raise ValueError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', password):
            raise ValueError('Password must contain at least one lowercase letter.')
        if not re.search(r'\d', password):
            raise ValueError('Password must contain at least one number.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError('Password must contain at least one special character.')
            
        return self


class PasswordChangeSchema(BasePasswordSchema):
    """Schema for validating password changes."""
    pass


class UserRegistrationSchema(BasePasswordSchema):
    """Schema for validating user registration data, ensuring proper name lengths,
    valid email formatting, minimum password requirements, and matching passwords.
    """
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: EmailStr = Field(..., max_length=70)


class AuthActionResponseSchema(BaseModel):
    message: str
    status: Literal["success", "warning", "error", "info"] = "success"
    redirect: bool
    url: Union[str, None] = None
    
class SocialLinksSchema(BaseModel):
    """Represents the digital and social media presence channels for a business."""
    
    instagram_url: Optional[str] = Field(None, description="Official Instagram profile URL.")
    tiktok_url: Optional[str] = Field(None, description="Official TikTok profile URL.")
    website_url: Optional[str] = Field(None, description="Primary business website or online storefront URL.")


class BusinessOnboardingSchema(BaseModel):
    """
    Schema for capturing core business registration details during the user onboarding flow.
    
    This model validates the initial information provided by new users, including their 
    operational identity, contact channels, business model type, location requirements, 
    and online presence links.
    """
    
    business_name: str = Field(
        ..., 
        min_length=2, 
        max_length=60, 
        description="The official registered or trading name of the business."
    )
    phone_number: str = Field(
        ..., 
        description="Primary official phone number for customer contact and verification."
    )
    business_type: Literal["online", "physical", "both"] = Field(
        ..., 
        description="The operational model of the business (Online only, Physical storefront, or Hybrid)."
    )
    address: Optional[str] = Field(
        None, 
        description="Physical street address. Required if business type is physical or hybrid."
    )
    socials: Optional[SocialLinksSchema] = Field(
        default_factory=SocialLinksSchema, # type: ignore
        description="Optional collection of online and social media links."
    )
