from django.db import transaction
from django.http import HttpRequest
from invoices.repository import InvoiceRepository
from accounts.models import Business
from accounts.domains.exceptions import BusinessNotFoundError
from accounts.selectors import BusinessSelector
from customers.repositories import CustomersRepo
from invoices.serializers import CreateSalesInvoiceSchema
from products.repository import ProductsRepo


class InvoiceService:
    def __init__(self, request: HttpRequest) -> None:
        self.request = request
        self.inv_repo = InvoiceRepository()
        self.biz_selector = BusinessSelector()
        self.customer_repo = CustomersRepo()

    def record_sale(self, sale_data: CreateSalesInvoiceSchema):
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

        return self._persist_sale_records(business=business, sale_data=sale_data) #type: ignore

    @transaction.atomic
    def _persist_sale_records(self, *, business: Business, sale_data: CreateSalesInvoiceSchema):
        """
            Writes one sale to the database as a single unit: links or
            creates the customer, creates the invoice, then creates every
            line item.
        """
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