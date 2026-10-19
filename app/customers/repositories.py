from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from accounts.models import Business
from customers.models import Customers, BusinessCustomers
from customers.serializers import CreateCustomerSchema
from customers.domains.customer_code import build_business_customer_slug
from uuid import UUID
from typing import Optional

class CustomersRepo:
    def __init__(self) -> None:
        self.customer_model = Customers
        self.biz_customer_model = BusinessCustomers
        
    def get_or_create_canonical_customer(self, *, data: CreateCustomerSchema, created_by_business:Business) -> Customers:
        """Retrieves an existing canonical customer or creates a new global identity.

        Performs a deduplication check based primarily on the customer's email address. 
        If a customer record already exists, it is returned untouched; otherwise, a 
        new global identity is provisioned with attribution to the creating business.

        Args:
            data (CreateCustomerSchema): The validated incoming payload containing customer 
                details (first name, last name, email, phone number).
            created_by_business (UUID): The unique identifier of the business that originally 
                imported or created this canonical customer record.

        Returns:
            Customers: The retrieved or newly created canonical customer model instance.
        """
        customer, _ = self.customer_model.objects.get_or_create(
            email=data.email,
            defaults={
                "first_name": data.first_name,
                "last_name": data.last_name,
                "phone_number": data.phone_number,
                "created_by_business": created_by_business
                
            }
        )

        return customer

    def link_to_business(self, business: Business, customer: Customers, display_name: str, notes: str = "") -> BusinessCustomers:
        """Handles only the business-specific relationship link."""
        link, _ = self.biz_customer_model.objects.get_or_create(
            business=business,
            client=customer,
            defaults={
                "display_name": display_name,
                "notes": notes,
                "slug": build_business_customer_slug(display_name),
            }
        )
        return link

    def create_and_link_customer(
        self,
        *,
        business: Business, 
        customer_data: CreateCustomerSchema, 
        display_name: str, 
        notes: str = ""
    ) -> BusinessCustomers:
        """Coordinates the workflow to retrieve or create a canonical customer and link them to a business.

        Args:
            business (Business): The authenticated business adding the customer to its client list.
            entity (Union[CreateCustomerSchema, CustomerEntity]): The customer payload or entity to process.
            display_name (str): Custom name shown when this specific business views their clients, 
                leaving the underlying customer model untouched.
            notes (str, optional): Special notes attached by the business regarding this customer relationship. 
                Defaults to "".

        Returns:
            BusinessCustomers: The created association record linking the business and the customer.
        """
        customer = self.get_or_create_canonical_customer(data=customer_data, created_by_business=business)
        return self.link_to_business(business, customer, display_name, notes)
    
    @transaction.atomic
    def update_business_customer_info(self, *, business_id: UUID, customer_data: CreateCustomerSchema, client_id:Optional[int], profile_slug:Optional[int],):
        filters = Q(business_id=business_id)
        if client_id:
            filters &= Q(client_id=client_id)
            
        if profile_slug:
            filters &= Q(slug=profile_slug)
            
        self.biz_customer_model.objects.filter(
            filters
        ).update(
            display_name=customer_data.display_name,
            phone_number=customer_data.phone_number,
            updated_at=timezone.now()   
        )
    