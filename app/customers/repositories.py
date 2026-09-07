from accounts.domains.entities import BusinessEntity
from customers.models import Customers, BusinessCustomers
from customers.domains.entities import CustomerEntity


class CustomersRepo:
    def __int__(self):
        self.customer_model = Customers
        self.biz_customer_model = BusinessCustomers
        
    def get_or_create_canonical_customer(self, entity: CustomerEntity) -> Customers:
        """Handles only the creation or retrieval of the global customer identity."""
        customer, _ = self.customer_model.objects.get_or_create(
            email=entity.email,
            phone_number=entity.phone_number,
            defaults={
                "first_name": entity.first_name,
                "last_name": entity.last_name,
                "email": entity.email,
                "phone_number": entity.phone_number,
            }
        )
        return customer

    def link_to_business(self, business: BusinessEntity, customer: Customers, display_name: str = "", notes: str = "") -> BusinessCustomers:
        """Handles only the business-specific relationship link."""
        link, _ = self.biz_customer_model.objects.get_or_create(
            business=business.id,
            client=customer,
            defaults={
                "display_name": display_name,
                # "notes": notes,
            }
        )
        return link

    def create_and_link_customer(self, business: BusinessEntity, entity: CustomerEntity, display_name: str = "", notes: str = "") -> BusinessCustomers:
        """Coordinates the workflow by delegating single-responsibility steps."""
        customer = self.get_or_create_canonical_customer(entity)
        return self.link_to_business(business, customer, display_name, notes)
    