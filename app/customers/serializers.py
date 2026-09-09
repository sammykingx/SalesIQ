from pydantic import BaseModel, EmailStr, Field, model_validator


class CreateCustomerSchema(BaseModel):
    """Payload schema for creating a customer record"""
    first_name: str = Field(..., min_length=3, max_length=28)
    last_name: str = Field(..., min_length=3, max_length=28)
    display_name: str
    email: EmailStr = Field(..., min_length=3, max_length=28)
    phone_number: str = Field(..., min_length=3, max_length=28)
    
    
    @model_validator(mode="before")
    @classmethod
    def set_display_name(cls, values:dict) -> dict:
        if not values.get('display_name') and values.get('first_name') and values.get('last_name'):
            values['display_name'] = f"{values['first_name']} {values['last_name']}"
        return values
