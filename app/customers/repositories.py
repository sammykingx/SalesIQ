from django.utils import timezone
from django.db import transaction, IntegrityError
from django.db.models import Q
from accounts.models import Business
from customers.domains.exceptions import CustomerAlreadyExistsError
from customers.models import Customers, BusinessCustomers
from customers.serializers import CreateCustomerSchema
from customers.domains.customer_code import build_business_customer_slug, build_unique_customer_code
from uuid import UUID
from typing import Optional

class CustomersRepo:
    def __init__(self) -> None:
        self.customer_model = Customers
        self.biz_customer_model = BusinessCustomers
        
    def _build_lookup_query(self, *, data: CreateCustomerSchema) -> Q:
        """Builds a dynamic Q object for deduplication lookups."""
        query = Q()
        if data.email:
            query |= Q(email=data.email)
        if data.phone_number:
            query |= Q(phone_number=data.phone_number)
        return query
    
    def _find_existing_customer(self, *, data: CreateCustomerSchema) -> Optional[Customers]:
        """Searches for an existing customer matching the unique identifiers."""
        lookup_query = self._build_lookup_query(data=data)
        if not lookup_query:
            return None
        return self.customer_model.objects.filter(lookup_query).first()

    def _resolve_customer_email(self, *, data: CreateCustomerSchema, customer_code: str) -> tuple[str, bool]:
        """Resolves whether to use the user's email or a system-generated fallback temp email."""
        if data.email:
            return data.email, False
        return f"{customer_code}@example.com", True
    
    def _create_new_customer(
        self, *, data: CreateCustomerSchema, created_by_business: Business
    ) -> Customers:
        """Provisions and saves a brand-new canonical customer entity."""
        customer_code = build_unique_customer_code(
            f_name=data.first_name, 
            l_name=data.last_name
        )
        resolved_email, using_temp = self._resolve_customer_email(
            data=data, 
            customer_code=customer_code
        )
    
        try:
            return self.customer_model.objects.create(
                first_name=data.first_name,
                last_name=data.last_name,
                email=resolved_email,
                phone_number=data.phone_number,
                code=customer_code,
                created_by_business=created_by_business,
                using_temp_email=using_temp
            )
    
        except IntegrityError:
            raise CustomerAlreadyExistsError()
    
    def get_or_create_canonical_customer(
        self, *, data: CreateCustomerSchema, created_by_business: Business
    ) -> Customers:
        """Retrieves an existing canonical customer or creates a new global identity.

        Performs a deduplication check based on the customer's email address or phone number.
        If an existing record is found, it is returned untouched; otherwise, a new global 
        identity is provisioned.

        Args:
            data (CreateCustomerSchema): The validated incoming payload containing customer 
                details (first name, last name, email, phone number).
            created_by_business (Business): The business instance that originally 
                imported or created this canonical customer record.

        Returns:
            Customers: The retrieved or newly created canonical customer model instance.
        """
        return (
            self._find_existing_customer(data=data)
            or self._create_new_customer(data=data, created_by_business=created_by_business)
        )

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
    def update_business_customer_info(
        self, 
        *, 
        business_id: UUID, 
        customer_data: CreateCustomerSchema, 
        client_id:Optional[int] = None,
        profile_slug:Optional[int] = None
    ):
        """Updates tenant-specific information for a customer linked to a business.

        This method performs a bulk or targeted update on the `BusinessCustomers` 
        through model, allowing a business to override shared customer profile details 
        (such as display name or phone number) for their own scoped view without 
        modifying the global customer identity. Executed within an atomic transaction.

        Args:
            business_id (UUID): The unique identifier of the business performing 
                the update. Acts as the primary tenancy scope.
            customer_data (CreateCustomerSchema): The validated payload containing 
                the updated information (`display_name`, `phone_number`).
            client_id (Optional[int], optional): Specific client ID to narrow down 
                the target record. Defaults to None.
            profile_slug (Optional[int], optional): URL-safe string identifier 
                (`slug`) to narrow down the target record. Defaults to None.

        Returns:
            int: The number of rows successfully updated in the database.
        """
        updated_rows = 0
        if not client_id and not profile_slug:
            return updated_rows
        
        filters = Q(business_id=business_id)
        if client_id:
            filters &= Q(client_id=client_id)
            
        if profile_slug:
            filters &= Q(slug=profile_slug)
            
        updated_rows = self.biz_customer_model.objects.filter(
            filters
        ).update(
            display_name=customer_data.display_name,
            phone_number=customer_data.phone_number,
            email=customer_data.email,
            updated_at=timezone.now()   
        )
        
        return updated_rows
    