from pydantic import BaseModel, EmailStr, Field, model_validator
from pydantic import HttpUrl
from typing import Union, Literal
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
    first_name: str = Field(..., max_length=150)
    last_name: str = Field(..., max_length=150)
    email: EmailStr = Field(..., max_length=254)


class AuthActionResponseSchema(BaseModel):
    message: str
    status: Literal["success", "warning", "error", "info"] = "success"
    redirect: bool
    url: Union[str, None] = None
    
    