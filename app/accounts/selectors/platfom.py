from django.db.models import Count, Q, QuerySet

from invoices.models import InvoiceStatus
from ._base import BusinessSelectorBase


class BusinessPlatformSelector(BusinessSelectorBase):
    # chart
    # def adoption_breakdown(self, *, threshold: int = 1) -> dict:
    #     """
    #         Businesses with `threshold`+ paid invoices, vs everyone else.
    #         Two COUNT(*) queries — no rows materialized, safe as adoption threshold grows.
    #     """
            
    #     annotated = self.business_model.objects.annotate(
    #         sale_count=Count("invoices", filter=Q(invoices__status=InvoiceStatus.PAID), distinct=True)
    #     )
    
    #     total = annotated.count()
    #     adopted = annotated.filter(sale_count__gte=threshold).count()
    #     not_adopted = total - adopted
    #     adoption_rate = round((adopted / total) * 100) if total else 0
    
    #     return {
    #         "adopted": adopted,
    #         "not_adopted": not_adopted,
    #         "total": total,
    #         "adoption_rate": adoption_rate,
    #         "threshold": threshold,
    #         "has_data": total > 0,
    #     }

    def get_total_count(self) -> int:
        return self.business_model.objects.count()
    
    def get_annotated_queryset(self) -> QuerySet:
        """
        Returns the base QuerySet for businesses optimized for platform-level 
        analytics and backoffice operations.
        
        Optimizations and Annotations included:
        - select_related("owner"): Pre-fetches the related owner user object to avoid N+1 queries.
        - annotate(sale_count): Computes the total number of unique PAID invoices 
          associated with the business.
        - order_by("-created_at"): Orders businesses by newest first.
        """
        return (
            self.business_model.objects
            .select_related("owner")
            .annotate(
                sale_count=Count(
                    "invoices", 
                    filter=Q(invoices__status=InvoiceStatus.PAID), 
                    distinct=True
                )
            )
            .order_by("-created_at")
        )

    
    def recent_signups(self, *, limit: int = 7) -> list[dict]:
        """
            Retrieves a formatted list of the most recent business signups, 
            mapping model instances into lightweight presentation dictionaries 
            for dashboard widgets or summary components.
        """
        businesses = self.get_annotated_queryset()[:limit]

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
            
    # platform dashboard selector
    # def summary(self, *, active_window_days: int = 30) -> dict:
    #     today = timezone.localdate()
    #     window_start = today - timedelta(days=active_window_days)
    
    #     total_businesses = self.business_model.objects.count()
    
    #     active_merchants = (
    #         self.business_model.objects
    #         .filter(invoices__status=InvoiceStatus.PAID, invoices__created_at__date__gte=window_start)
    #         .distinct()
    #         .count()
    #     )
    
    #     active_today = (
    #         self.business_model.objects
    #         .filter(invoices__status=InvoiceStatus.PAID, invoices__created_at__date=today)
    #         .distinct()
    #         .count()
    #     )
    #     active_today_rate = round((active_today / total_businesses) * 100, 1) if total_businesses else 0.0
    
    #     platform_volume = InvoicePlatformSelector().get_platform_volume()
    
    #     return {
    #         "active_merchants": active_merchants,
    #         "platform_volume": float(platform_volume),
    #         "active_today_rate": active_today_rate,
    #     }
