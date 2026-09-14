from pydantic import BaseModel, Field, model_validator
from decimal import Decimal
from customers.serializers import CreateCustomerSchema
from products.serializers import BaseProductSchema
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
            discount_rate = self.discount_percentage / Decimal("100")
            expected_discount = (self.sub_total * discount_rate).quantize(Decimal("0.01"))
            if discount_amt != expected_discount:
                raise ValueError(
                    f"Invalid discount_amount. Expected {expected_discount} "
                    f", but got {discount_amt}"
                )

        if self.tax_percentage is not None:
            tax_rate = self.tax_percentage / Decimal("100")
            expected_tax = (self.sub_total * tax_rate).quantize(Decimal("0.01"))
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

    
class InvoiceLineItemSchema(BaseProductSchema):
    id: Union[UUID, int, None] = None
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
    
    @model_validator(mode="after")
    def validate_sub_total_from_products(self) -> "CreateSalesInvoiceSchema":
        """
        Ensures that the invoice sub_total matches the exact sum 
        of all line item costs (quantity * price).
        """
        calculated_sub_total = sum(
            (Decimal(str(item.quantity)) * item.price for item in self.products),
            Decimal("0")
        ).quantize(Decimal("0.01"))

        if self.sub_total != calculated_sub_total:
            raise ValueError(
                f"Invalid sub total. Expected {calculated_sub_total} "
                f"based on line items, but got {self.sub_total}."
            )
        return self
