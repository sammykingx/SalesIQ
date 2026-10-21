from django.db.models import Count, QuerySet, Sum
from django.db.models.functions import TruncDate
from django.utils import timezone

from invoices.models import InvoiceStatus
from ._base import InvoiceSelectorBase
from ._trends import PERIOD_DAYS

from datetime import timedelta
from decimal import Decimal
from typing import Iterable
from uuid import UUID

class InvoicePlatformSelector(InvoiceSelectorBase):
    """Selector for platform-wide invoice analytics and aggregate metrics across all businesses."""
    
    def _paid(self) -> QuerySet:
        """Returns a base QuerySet filtered exclusively for paid invoices."""
        return self.invoice_model.objects.filter(status=InvoiceStatus.PAID)
    
    def get_platform_gmv_trend(self, *, period: str = "7d") -> dict:
        """
            Returns the daily Gross Merchant Value (GMV) trend across the entire platform.

            GMV represents total transaction volume across all businesses, not platform revenue.
            Missing days are filled with zero-value entries for contiguous charting.

            Returns:
                dict: {"labels": list[str], "gmv": list[float], "has_data": bool}
        """
        days = PERIOD_DAYS.get(period, 7)
        start = timezone.localdate() - timedelta(days=days - 1)
    
        rows = (
            self._paid()
            .filter(created_at__date__gte=start)
            .annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(gmv=Sum("total"))
        )
        
        by_day = {r["day"]: r["gmv"] for r in rows}
    
        labels, gmv = [], []
        for i in range(days):
            d = start + timedelta(days=i)
            labels.append(d.strftime("%b %d"))
            gmv.append(float(by_day.get(d, 0)))
    
        return {"labels": labels, "gmv": gmv, "has_data": bool(by_day)}
    
    def get_platform_volume(self) -> Decimal:
        """
            Returns the total lifetime Gross Merchant Value (GMV) across all 
            paid platform invoices.

            Returns:
                Decimal: Total sum of all paid invoice totals.
        """
        return self._paid().aggregate(total=Sum("total"))["total"] or Decimal("0")
    
    def count_active_businesses(self, *, start, end=None) -> int:
        """
            Returns the count of distinct businesses with at least one 
            paid invoice in a date range.

            Returns:
                int: Number of active businesses.
        """
        qs = self._paid().filter(created_at__date__gte=start)
        if end:
            qs = qs.filter(created_at__date__lte=end)
        return qs.values("business_id").distinct().count()

    def count_businesses_with_min_paid(self, *, threshold: int) -> int:
        """
            Returns the count of distinct businesses that have reached 
            or exceeded a threshold of paid invoices.

            Returns:
                int: Number of businesses meeting the threshold.
        """
        return (
            self._paid()
            .values("business_id")
            .annotate(paid=Count("id"))
            .filter(paid__gte=threshold)
            .count()
        )

    def get_paid_counts(self, *, business_codes: Iterable[str]) -> dict[str, int]:
        """
            Returns a mapping of paid invoice counts for a specific set of business codes.
            Businesses with zero paid invoices are omitted from the result.

            Returns:
                dict[str, int]: Mapping of business ID to its paid invoice count.
        """
        rows = (
            self._paid()
            .filter(business__code__in=business_codes)
            .values("business__code")
            .annotate(paid=Count("id"))
        )
        return {row["business__code"]: row["paid"] for row in rows}
