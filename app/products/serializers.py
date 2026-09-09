from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Literal
from uuid import UUID


class CreateProductsSchema(BaseModel):
    """
        Schema used for validating input data when a user 
        is creating a new product for their business.
    """
    name: str = Field(..., max_length=100)
    price: Decimal = Field(..., max_digits=10, decimal_places=2)
    product_type: Literal["digital", "physical", "service"]
    description: str
    
    
class ModifyProducts(CreateProductsSchema):
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
    id: UUID
    name: str
    price: Decimal
    product_type: Literal["digital", "physical", "service"]
    total_sales: int = Field(..., description="Computed total number of sales for this product")
    created_at: str = Field(..., description="ISO formatted string of when the product was created")

    # class Config:
    #     from_attributes = True