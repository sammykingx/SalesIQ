from pydantic import BaseModel, ConfigDict, Field, field_validator
from decimal import Decimal
from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

import string


class CreateProductsSchema(BaseModel):
    """
        Schema used for validating input data when a user 
        is creating a new product for their business.
    """
    name: str = Field(..., max_length=100)
    product_type: Literal["digital", "physical", "service"]
    price: Decimal = Field(..., max_digits=10, decimal_places=2)
    description: Optional[str] = None

class ModifyProductSchema(CreateProductsSchema):
    """
        Schema used for validating input data when updating or 
        modifying an existing single product. Inherits base product 
        fields and requires the product_id for identification.
    """
    product_id: UUID


class ProductListItemSchema(BaseModel):
    """
        Schema used for returning a summarized list of product objects 
        to the frontend. Excludes the heavy description field and includes 
        computed metrics like total sales and a string-formatted creation date.
    """
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    price: Decimal
    product_type: Literal["digital", "physical", "service"]
    total_sales: int = Field(..., description="Computed total number of sales for this product")
    created_at: datetime = Field(..., description="ISO formatted string of when the product was created")
    url: str
    
    @field_validator("name", mode="before")
    @classmethod
    def format_title_case(cls, v: str) -> str:
        if isinstance(v, str):
            return string.capwords(v.lower())
        return v
