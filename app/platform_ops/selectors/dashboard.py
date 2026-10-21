from django.utils import timezone

from invoices.selectors import InvoicePlatformSelector
from accounts.selectors import BusinessPlatformSelector

from datetime import timedelta


class PlatformDashboardMetricsSelector:
    """
        Everything the platform dashboard template needs, in one place.

        Combines business facts with invoice facts into dashboard figures. It has
        no ORM code and no model imports. 'Active', 'adopted' and 'dormant' are
        defined here because each needs both apps. Everything else is delegated.
    """
    def __init__(self) -> None:
        self.businesses = BusinessPlatformSelector()
        self.invoices = InvoicePlatformSelector()
        
    def summary(self, *, active_window_days: int = 30) -> dict:
        today = timezone.localdate()
        total = self.businesses.get_total_count()
        active_today = self.invoices.count_active_businesses(start=today, end=today)

        return {
            "active_merchants": self.invoices.count_active_businesses(
                start=today - timedelta(days=active_window_days)
            ),
            "platform_volume": float(self.invoices.get_platform_volume()),
            "active_today_rate": round(active_today / total * 100, 1) if total else 0.0,
        }
        
    def recent_business_signups(self, *, limit: int = 7) -> list[dict]:
        """Newest businesses, each with its paid sale count and a dormant flag if no sale recorded for the business"""
        biz_signups = self.businesses.recent_signups(limit=limit)
        counts = self.invoices.get_paid_counts(business_codes=[biz_signup.get("code") for biz_signup in biz_signups]) #type:ignore

        return [
            {**biz_signup, "sale_count": counts.get(biz_signup.get("code"), 0), "is_dormant": biz_signup.get("code") not in counts} #type:ignore
            for biz_signup in biz_signups
        ]
