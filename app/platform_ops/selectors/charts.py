from invoices.selectors import InvoicePlatformSelector
from accounts.selectors import BusinessPlatformSelector


ADOPTION_THRESHOLDS = [1, 5, 10, 15, 20]


class PlatformDashboardChartSelector:
    """
        Selector class responsible for fetching and aggregating platform-wide 
        metrics and chart JSON data consumed by Alpine.js dashboard components.
    """
    def __init__(self) -> None:
        self.businesses = BusinessPlatformSelector()
        self.invoices = InvoicePlatformSelector()
        
    def adoption_breakdown(self, *, threshold: int = 1) -> dict:
        """
            Calculates platform adoption metrics by comparing total businesses 
            against those that have reached a minimum number of completed sales.

            Returns:
                dict: {"adopted": int, "not_adopted": int, "total": int, "adoption_rate": int, "threshold": int, "has_data": bool}
        """
        total = self.businesses.get_total_count()
        adopted = self.invoices.count_businesses_with_min_paid(threshold=threshold)

        return {
            "adopted": adopted,
            "not_adopted": total - adopted,
            "total": total,
            "adoption_rate": round(adopted / total * 100) if total else 0,
            "threshold": threshold,
            "has_data": total > 0,
        }
        
    def gmv_trend(self, *, period: str = "7d") -> dict:
        """
            Returns the platform-wide Gross Merchandise Value (GMV) trend for charting 
            over a specified period, delegating to the invoice selector.

            Returns:
                dict: {"labels": list[str], "gmv": list[float], "has_data": bool}
        """
        return self.invoices.get_platform_gmv_trend(period=period)
