from customers.models import BusinessCustomers
from django.db.models import Count, Q, Sum
from customers.domains.entities import BusinessClientEntity, CustomerEntity
from invoices.models import InvoiceStatus, Invoice
from uuid import UUID
from decimal import Decimal


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
        
    def get_customer_count(self, *, business_id) -> int:
        """Get the total number of customers for a specific business.

        Args:
            business_id (int|str): The unique identifier of the business.

        Returns:
            int: The total count of customers associated with the business.
        """
        return self.model.objects.filter(business_id=business_id).count()
        
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
    
    def get_all_business_customers_frontend_json(self, biz_id: UUID) -> list[dict]:
        """Retrieves and flattens business clients into a JSON-ready format for Alpine.js."""
        
        links = (
            self.model.objects.filter(business=biz_id)
            .select_related("client")
            .annotate(
            total_orders=Count("invoices", distinct=True),
            total_spend=Sum("invoices__total"),
            )
        )
        
        payload = []
        for link in links:
            client = link.client
            payload.append({
                "id": client.id, # type:ignore
                "first_name": client.first_name,
                "last_name": client.last_name,
                "display_name": link.display_name.title(),
                "email": client.email,
                "phone": client.phone_number,
                "total_spend": link.total_spend or Decimal("0"), # type:ignore
                "total_orders": link.total_orders, # type:ignore
                "status": "Active",
                "date_created": link.added_at.isoformat() if link.added_at else None,
                "avatar": None,
            })
        return payload
    
    def get_business_customer_metrics(self, biz_id: UUID) -> dict:
        """
            Aggregate metrics for the customer dashboard banner.
            Defines an "order" as a PAID invoice.
        """
        revenue_totals = Invoice.objects.filter(
            business_id=biz_id, status=InvoiceStatus.PAID
        ).aggregate(total_revenue=Sum("total"))
        total_revenue = revenue_totals["total_revenue"] or Decimal("0")

        per_customer = self.model.objects.filter(business=biz_id).annotate(
            order_count=Count(
                "invoices", filter=Q(invoices__status=InvoiceStatus.PAID), distinct=True
            ),
        )

        totals = per_customer.aggregate(
            total_customers=Count("id"),
            customers_with_orders=Count("id", filter=Q(order_count__gt=0)),
            repeat_customers=Count("id", filter=Q(order_count__gt=1)),
        )

        total_customers = totals["total_customers"] or 0
        customers_with_orders = totals["customers_with_orders"] or 0
        repeat_customers = totals["repeat_customers"] or 0

        avg_lifetime_value = (
            total_revenue / customers_with_orders if customers_with_orders else Decimal("0")
        )
        repeat_rate = (
            (repeat_customers / customers_with_orders) * 100 if customers_with_orders else 0.0
        )

        return {
            "total_customers": total_customers,
            "avg_lifetime_value": avg_lifetime_value,
            "repeat_rate": round(repeat_rate, 1),
            "total_revenue": total_revenue,
        }
        
    def get_top_customers(self, *, business_id, limit: int = 5):
        """
        Return the top customers by total spend for dashboard display.

        Args:
            business_id: The ID of the business.
            limit: Maximum number of customers to return (default 5).

        Returns:
            list: A list of dictionaries containing customer names, total spent, 
                  and total paid orders.
        """
        queryset = (
            BusinessCustomers.objects
            .filter(business_id=business_id)
            .annotate(
                total_spent=Sum("invoices__total", filter=Q(invoices__status=InvoiceStatus.PAID)),
                total_orders=Count("invoices", filter=Q(invoices__status=InvoiceStatus.PAID), distinct=True),
            )
            .filter(total_spent__gt=0)
            .order_by("-total_spent")[:limit]
            .select_related("client")
        )
        
        return [
            {
                "name": bc.display_name or f"{bc.client.first_name} {bc.client.last_name}".strip(),
                "total_spent": float(bc.total_spent), # type:ignore
                "total_orders": bc.total_orders, # type:ignore
            }
            for bc in queryset
        ]
