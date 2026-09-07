from pydantic import BaseModel, EmailStr, Field


class CreateCustomerSchema(BaseModel):
    """Payload schema for creating a customer record"""
    first_name: str = Field(..., min_length=3, max_length=28)
    last_name: str = Field(..., min_length=3, max_length=28)
    email: EmailStr = Field(..., min_length=3, max_length=28)
    phone_number: str = Field(..., min_length=3, max_length=28)
