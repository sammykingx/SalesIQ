from django.db.models import Count, Q, Sum
from django.utils import timezone

from accounts.domains.entities import BusinessEntity
from accounts.models import Business
from invoices.models import InvoiceStatus
from invoices.selectors import InvoiceSelectors

from decimal import Decimal
from datetime import timedelta
from typing import Union


ADOPTION_THRESHOLDS = [1, 5, 10, 15, 20]

class BusinessSelector:
    """Selector class responsible for querying and mapping Business records from the database.

    Acts as a data retrieval layer, fetching user-associated business data 
    and converting ORM model instances into domain-level business entities.
    """

    def __init__(self) -> None:
        """Initializes the BusinessSelector with the default Business model."""
        self.model = Business

    def get_user_business(
        self, *, user_email: str, as_instance=False
    ) -> Union[BusinessEntity, Business, None]:
        """Retrieves a business record associated with a specific user email.

        Args:
            user_email (str): The email address of the business owner.
            as_instance (bool, optional): If True, returns the raw ORM model instance. 
                If False, converts and returns a BusinessEntity. Defaults to False.

        Returns:
            Union[BusinessEntity, Business, None]: The business record as a 
            BusinessEntity or model instance if found, otherwise None.
        """
        obj = self.model.objects.filter(owner=user_email).first()
        if as_instance:
            return obj
        return self._to_business_entity(instance=obj) if obj else None
    
    
    # Metrics
    def get_adoption_breakdown(self, *, threshold: int = 1) -> dict:
        """Businesses with `threshold`+ paid invoices, vs everyone else.
        Two COUNT(*) queries — no rows materialized, safe as adoption threshold grows."""
        
        annotated = self.model.objects.annotate(
            sale_count=Count("invoices", filter=Q(invoices__status=InvoiceStatus.PAID), distinct=True)
        )

        total = annotated.count()
        adopted = annotated.filter(sale_count__gte=threshold).count()
        not_adopted = total - adopted
        adoption_rate = round((adopted / total) * 100) if total else 0

        return {
            "adopted": adopted,
            "not_adopted": not_adopted,
            "total": total,
            "adoption_rate": adoption_rate,
            "threshold": threshold,
            "has_data": total > 0,
        }
        
    def get_recent_signups(self, *, limit: int = 7) -> list[dict]:
        businesses = (
            self.model.objects
            .select_related("owner")
            .annotate(sale_count=Count("invoices", filter=Q(invoices__status=InvoiceStatus.PAID), distinct=True))
            .order_by("-created_at")[:limit]
        )

        return [
            {
                "name": biz.name,
                "owner_name": f"{biz.owner.first_name} {biz.owner.last_name}".strip(),
                "code": biz.code,
                "business_type": biz.get_business_type_display() if biz.business_type else "—", # type: ignore
                "is_dormant": biz.sale_count == 0, # type: ignore
                "sale_count": biz.sale_count, # type: ignore
                "joined_display": biz.created_at.strftime("%b %d, %Y"),
            }
            for biz in businesses
        ]
        
    def get_platform_summary(self, *, active_window_days: int = 30) -> dict:
        today = timezone.localdate()
        window_start = today - timedelta(days=active_window_days)

        total_businesses = self.model.objects.count()

        active_merchants = (
            self.model.objects
            .filter(invoices__status=InvoiceStatus.PAID, invoices__created_at__date__gte=window_start)
            .distinct()
            .count()
        )

        active_today = (
            self.model.objects
            .filter(invoices__status=InvoiceStatus.PAID, invoices__created_at__date=today)
            .distinct()
            .count()
        )
        active_today_rate = round((active_today / total_businesses) * 100, 1) if total_businesses else 0.0

        platform_volume = InvoiceSelectors().get_platform_volume()

        return {
            "active_merchants": active_merchants,
            "platform_volume": float(platform_volume),
            "active_today_rate": active_today_rate,
        }

    def _to_business_entity(self, instance) -> BusinessEntity:
        """Maps a raw Business database model instance to a domain BusinessEntity.

        Args:
            instance: The database model instance of the Business.

        Returns:
            BusinessEntity: A domain entity populated with fields from the model instance.
        """
        return BusinessEntity(
            id=instance.id,
            code=instance.code,
            owner_email=instance.owner.email,
            name=instance.name,
            phone_number=instance.phone_number,
            business_type=instance.business_type,
            address=instance.address,
            instagram_url=instance.instagram_url,
            tiktok_url=instance.tiktok_url,
            whatsapp_number=instance.whatsapp_number,
            website_url=instance.website_url,
            created_at=instance.created_at,
            updated_at=instance.updated_at,
        )
        