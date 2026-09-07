from customers.models import Customers, BusinessCustomers
from django.db.models import QuerySet
from customers.domains.entities import BusinessClientEntity, CustomerEntity
from uuid import UUID


class CustomerSelector:
    def __init__(self) -> None:
        self.model = BusinessCustomers
        
    def _to_entity(self, link: BusinessCustomers) -> BusinessClientEntity:
        """Maps a BusinessCustomers model instance to a nested BusinessClient domain entity."""
        customer_entity = CustomerEntity(
            id=link.client.id, # type: ignore
            first_name=link.client.first_name,
            last_name=link.client.last_name,
            email=link.client.email,
            phone_number=link.client.phone_number,
        )
        return BusinessClientEntity(
            customer=customer_entity,
            business_id=link.business_id, #type: ignore
            display_name=link.display_name,
            notes=link.notes,
            added_at=link.added_at,
            updated_at=link.updated_at,
        )
        
    def get_all_for_business(self, biz_id: UUID) -> list[BusinessClientEntity]:
        """Retrieve all client relationships for a specific business, mapped to entities."""
        links = self.model.objects.filter(business=biz_id).select_related("client")
        return [self._to_entity(link) for link in links]

    def get_single_for_business(self, biz, customer_id: int) -> BusinessClientEntity | None:
        """Retrieve a specific customer relationship for a given business, mapped to an entity."""
        link = (
            self.model.objects.filter(business=biz, client_id=customer_id)
            .select_related("client")
            .first()
        )
        return self._to_entity(link) if link else None
