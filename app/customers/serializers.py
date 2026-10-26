from pydantic import BaseModel, EmailStr, Field, model_validator, field_validator
from decimal import Decimal
from typing import Optional


class CreateCustomerSchema(BaseModel):
    """Payload schema for creating a customer record"""

    first_name: str = Field(..., min_length=3, max_length=28)
    last_name: str = Field(..., min_length=3, max_length=28)
    display_name: str
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(default=None, min_length=3, max_length=18)
    
    
    @field_validator('email', 'phone_number', 'display_name', mode='before')
    @classmethod
    def value_empty_as_none(cls, value):
        if isinstance(value, str) and not value.strip():
            return None
        return value
    
    @model_validator(mode="before")
    @classmethod
    def set_display_name(cls, values:dict) -> dict:
        if not values.get('display_name') and values.get('first_name') and values.get('last_name'):
            values['display_name'] = f"{values['first_name']} {values['last_name']}"
        return values
    
    @model_validator(mode="after")
    def ensure_email_or_phone(self) -> 'CreateCustomerSchema':
        if not self.email and not self.phone_number:
            raise ValueError("Either a customer email or phone number is required to proceed.")
        return self
    
class CustomerMetricsSchema(BaseModel):
    total_customers: int
    avg_lifetime_value: Decimal
    repeat_rate: float = Field(..., description="Percentage of ordering customers who ordered more than once")
    total_revenue: Decimal
