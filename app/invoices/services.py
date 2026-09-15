from django.db import transaction, IntegrityError, DataError, OperationalError
from django.http import HttpRequest
from invoices.repository import InvoiceRepository
from accounts.models import Business
from accounts.domains.exceptions import BusinessNotFoundError
from accounts.selectors import BusinessSelector
from customers.repositories import CustomersRepo
from invoices.domains.entity import InvoiceEntity, InvoiceItemEntity
from invoices.domains.exceptions import (
    InvoiceIdentifierCollisionError, 
    InvalidInvoiceDataError, 
    InvoiceWriteFailedError, 
    InvoiceServiceUnavailableError
)
from invoices.serializers import CreateSalesInvoiceSchema
from products.repository import ProductsRepo
from decimal import Decimal


class InvoiceService:
    def __init__(self, *, request: HttpRequest) -> None:
        self.request = request
        self.inv_repo = InvoiceRepository()
        self.biz_selector = BusinessSelector()
        self.customer_repo = CustomersRepo()

    def record_sale(self, *, sale_data: CreateSalesInvoiceSchema) -> InvoiceEntity:
        """
            Entry point for recording a completed sale.

            Resolves the requesting user's business, then hands off to
            `_persist_sale_records` for the actual writes.
        """
        business = self.biz_selector.get_user_business(
            user_email=self.request.user.email, as_instance=True  # type: ignore
        )
        if business is None:
            raise BusinessNotFoundError

        invoice = self._persist_sale_records(business=business, sale_data=sale_data) #type: ignore
        return self._map_invoice_to_entity(invoice_obj=invoice)

    @transaction.atomic
    def _persist_sale_records(self, *, business: Business, sale_data: CreateSalesInvoiceSchema):
        """
            Writes one sale to the database as a single unit: links or
            creates the customer, creates the invoice, then creates every
            line item.
        """
        try:
            product_repo = ProductsRepo(business_instance=business)  # type: ignore

            customer_obj = self.customer_repo.create_and_link_customer(
                business=business,  # type: ignore
                customer_data=sale_data.customer,
                display_name=sale_data.customer.display_name,
            )

            invoice_obj = self.inv_repo.create_invoice(
                business_instance=business, customer_instance=customer_obj, data=sale_data  # type: ignore
            )

            for product in sale_data.products:
                product_obj = product_repo.get_or_create_product(data=product)  # type: ignore
                self.inv_repo.create_invoice_line_item(
                    invoice_obj=invoice_obj, product_obj=product_obj, line_item=product
                )

            return invoice_obj
        
        except InvoiceIdentifierCollisionError:
            raise
        except DataError as e:
            # logger.exception("Data error persisting sale for business %s", business.id)
            raise InvalidInvoiceDataError() from e
        except IntegrityError as e:
            # logger.exception("Integrity error persisting sale for business %s", business.id)
            raise InvoiceWriteFailedError() from e
        except OperationalError as e:
            # logger.exception("DB operational error persisting sale for business %s", business.id)
            raise InvoiceServiceUnavailableError() from e
    
    def _map_invoice_to_entity(self, invoice_obj) -> InvoiceEntity:
        """
        Converts an actual Django Invoice model instance and its related 
        line items into the corresponding InvoiceEntity dataclass.
        """
        items = [
            InvoiceItemEntity(
                id=item.id,
                name=item.product_name,
                product_type=item.product_type,
                quantity=item.quantity,
                unit_price=Decimal(item.unit_price),
                line_subtotal=Decimal(item.line_subtotal),
            )
            for item in invoice_obj.line_items.all()
        ]

        return InvoiceEntity(
            display_id=invoice_obj.display_id,
            slug=invoice_obj.slug,
            status=invoice_obj.status,
            created_at=invoice_obj.created_at,
            currency=invoice_obj.currency,
            business_id=invoice_obj.business_id,
            customer_id=invoice_obj.customer_id,
            sub_total=Decimal(invoice_obj.subtotal),
            discount_type=invoice_obj.discount_type,
            discount_percentage=Decimal(invoice_obj.discount_value),
            discount_amount=Decimal(invoice_obj.discount_amount),
            tax_name=invoice_obj.tax_name,
            tax_percentage=Decimal(invoice_obj.tax_percentage),
            tax_amount=Decimal(invoice_obj.tax_amount or 0),
            total_amount=Decimal(invoice_obj.total),
            line_items=items,
        )
