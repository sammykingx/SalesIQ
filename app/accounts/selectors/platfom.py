from django.db.models import Count, Q, QuerySet, Sum
from django.utils import timezone

from invoices.models import InvoiceStatus
from ._base import BusinessSelectorBase

from datetime import timedelta


class BusinessPlatformSelector(BusinessSelectorBase):
    """
        Selector responsible for retrieving and aggregating business information 
        at the platform level (cross-merchant), rather than for a single business 
        or individual merchant. 

        Designed for backoffice operations, platform-wide analytics, admin dashboards, 
        and global summary widgets.
    """
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
            
            Args:
                limit (int): The maximum number of recent signups to return (default: 7).
                
            Returns:
                list[dict]: A list of dictionaries containing formatted business and owner details.
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

    def merchant_leaderboard(self, *, time_frame:str="this_month") -> QuerySet:
        """
        Returns a QuerySet of businesses ranked by platform performance metrics 
        (sales count and total revenue from paid invoices).
        
        Note:
            Constructs a dedicated annotation query from scratch to avoid 
            Cartesian product row-inflation caused by chaining multiple 
            reverse-relation (invoices) annotations.
        
        Optimizations included:
        - select_related("owner"): Avoids N+1 queries for owner details.
        - annotate(sale_count): Counts unique PAID invoices.
        - annotate(total_revenue): Sums the total monetary value of PAID invoices.
        - order_by: Ranks primarily by volume (-sale_count) then revenue (-total_revenue).
        """
        now = timezone.now()
        invoice_filter = Q(invoices__status=InvoiceStatus.PAID)
        
        if time_frame == 'this_week':
            start_date = now - timedelta(days=7)
            invoice_filter &= Q(invoices__created_at__gte=start_date)
        elif time_frame == 'this_month':
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            invoice_filter &= Q(invoices__created_at__gte=start_date)
            
        return (
            self.business_model.objects
            .select_related("owner")
            .annotate(
                total_sales=Count(
                    "invoices", 
                    filter=invoice_filter, 
                    distinct=True
                ),
                total_revenue=Sum("invoices__total", filter=invoice_filter)
            )
            .order_by("-total_sales", "-total_revenue")
        )
