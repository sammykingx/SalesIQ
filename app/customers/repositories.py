from accounts.models import Business
from customers.models import Customers, BusinessCustomers
from customers.serializers import CreateCustomerSchema


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
    