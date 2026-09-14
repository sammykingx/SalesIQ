from pydantic import BaseModel, Field, model_validator
from decimal import Decimal
from customers.serializers import CreateCustomerSchema
from typing import Dict, Literal, List, Optional, Union
from uuid import UUID


class CustomerSchema(CreateCustomerSchema):
    id: Optional[int] = None
    

class InvoiceSchema(BaseModel):
    """
    Validation schema for recording a sales invoice for a business owner.

    This schema handles financial calculations and ensures data integrity 
    across sub_totals, taxes, discounts, and final totals.

    Validation Rules:
    - **Discount Validation:** If `discount_percentage` is present, `discount_amount` 
      must equal `sub_total * discount_percentage`.
    - **Tax Validation:** If `tax_percentage` is present, `tax_amount` 
      must equal `sub_total * tax_percentage`.
    - **Total Calculation:** The `total` must equal `sub_total + tax_amount - discount_amount`.
    """
    sub_total: Decimal = Field(..., max_digits=12, decimal_places=2)
    total_amount: Decimal = Field(..., max_digits=12, decimal_places=2)
    discount_percentage: Optional[Decimal] = None
    discount_amount: Optional[Decimal] = None
    tax_name: Optional[str] = None
    tax_percentage: Optional[Decimal] = None
    tax_amount: Optional[Decimal] = None
    
    @model_validator(mode="after")
    def validate_invoice_calculations(self) -> "InvoiceSchema":
        tax_amt = self.tax_amount if self.tax_amount is not None else Decimal("0")
        discount_amt = self.discount_amount if self.discount_amount is not None else Decimal("0")

        if self.discount_percentage is not None:
            expected_discount = (self.sub_total * self.discount_percentage).quantize(Decimal("0.01"))
            if discount_amt != expected_discount:
                raise ValueError(
                    f"Invalid discount_amount. Expected {expected_discount} "
                    f", but got {discount_amt}."
                )

        if self.tax_percentage is not None:
            expected_tax = (self.sub_total * self.tax_percentage).quantize(Decimal("0.01"))
            if tax_amt != expected_tax:
                raise ValueError(
                    f"Invalid tax_amount. Expected {expected_tax} "
                    f"but got {tax_amt}."
                )

        expected_total = (self.sub_total + tax_amt - discount_amt).quantize(Decimal("0.01"))
        if self.total_amount != expected_total:
            raise ValueError(
                f"Invalid total. Expected {expected_total} "
                f"but got {self.total_amount}."
            )

        return self

    
class InvoiceLineItemSchema(BaseModel):
    id: Union[UUID, int, None] = None
    product_name: str = Field(..., max_length=70)
    sale_price: Decimal = Field(..., max_digits=12, decimal_places=2)
    product_type: Literal["physical", "digital", "service"] = "physical"
    quantity: int


class CreateSalesInvoiceSchema(InvoiceSchema):
    """
    Schema for creating a new sales invoice.

    This schema extends `InvoiceSchema` to encapsulate all necessary data 
    required to generate and record a complete sales invoice for a business owner. 
    It combines customer details, individual line items, and verified financial totals.

    Attributes:
        customer (CustomerSchema): The existing customer (including their ID and details) 
                                   associated with this invoice.
        products (List[InvoiceLineItemSchema]): A list of products or services purchased, 
                                                including their prices, quantities, and types.

    Inherited Validation Rules (from `InvoiceSchema`):
        - **Discount Validation:** If `discount_value` is present, `discount_amount` 
          must equal `sub_total * discount_value`.
        - **Tax Validation:** If `tax_percentage` is present, `tax_amount` 
          must equal `sub_total * tax_percentage`.
        - **Total Calculation:** The `total` must equal `sub_total + tax_amount - discount_amount`.
    """
    customer: CustomerSchema
    products: List[InvoiceLineItemSchema]
