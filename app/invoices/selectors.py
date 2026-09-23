from django.db.models import Count, Prefetch, Q, QuerySet, Sum
from django.db.models.functions import ExtractWeekDay, TruncDate
from django.utils import timezone

from invoices.models import Invoice, InvoiceLineItem, InvoiceStatus

from datetime import timedelta
from decimal import Decimal
from uuid import UUID


PERIOD_DAYS = {"7d": 7, "30d": 30, "90d": 90}
# Django's ExtractWeekDay is 1=Sunday..7=Saturday
WEEKDAY_LABELS = {1: "Sun", 2: "Mon", 3: "Tue", 4: "Wed", 5: "Thu", 6: "Fri", 7: "Sat"}
WEEKDAY_DISPLAY_ORDER = [2, 3, 4, 5, 6, 7, 1]  # Mon → Sun

class InvoiceSelectors:
    def __init__(self) -> None:
        self.inv_model = Invoice
        self.inv_line_item_model = InvoiceLineItem
        
    def list_business_invoices(self, *, biz_id:UUID) -> QuerySet[Invoice]:
        return (
            self.inv_model.objects
            .select_related("customer", "customer__client")
            .filter(business=biz_id)
        )
    
    def get_invoice_by_slug(self, *, slug: str) -> Invoice | None:
        return self._base_detail_queryset().filter(slug=slug).first()

    def get_invoice_with_details(self, *, display_id: str) -> Invoice | None:
        """retunrs an invoice with the business, customer"""
        return self._base_detail_queryset().filter(display_id=display_id).first()
    
    def get_recent_sales(self, *, business_id, limit: int = 7) -> list[dict]:
        """Last N sales regardless of status — a voided sale stays visible, not silently dropped."""
        invoices = (
            self.inv_model.objects
            .filter(business_id=business_id)
            .select_related("customer", "customer__client")
            .prefetch_related("line_items")
            .order_by("-created_at")[:limit]
        )

        today = timezone.localdate()
        results = []
        for invoice in invoices:
            line_items = list(invoice.line_items.all()) # type: ignore
            first_item = line_items[0].product_name if line_items else "—"
            extra_count = max(len(line_items) - 1, 0)

            local_dt = timezone.localtime(invoice.created_at)
            date_display = (
                local_dt.strftime("%-I:%M %p") if local_dt.date() == today
                else local_dt.strftime("%b %d")
            )

            customer = invoice.customer
            customer_name = customer.display_name or f"{customer.client.first_name} {customer.client.last_name}".strip()

            results.append({
                "display_id": invoice.display_id,
                "slug": invoice.slug,
                "customer_name": customer_name,
                "first_item": first_item,
                "extra_count": extra_count,
                "date_display": date_display,
                "status": invoice.status,
                "total": float(invoice.total),
            })
        return results

    # Metrics
    def get_revenue_trend(self, *, business, period="7d"):
        days = PERIOD_DAYS.get(period, 7)
        start = timezone.now().date() - timedelta(days=days - 1)

        rows = (
            self.inv_model.objects
            .filter(business=business, status=InvoiceStatus.PAID, created_at__date__gte=start)
            .annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(revenue=Sum("total"))
        )
        by_day = {r["day"]: r["revenue"] for r in rows}

        labels, revenue = [], []
        for i in range(days):
            d = start + timedelta(days=i)
            labels.append(d.strftime("%b %d"))
            revenue.append(float(by_day.get(d, 0)))
        return {"labels": labels, "revenue": revenue, "has_data": bool(by_day)}
    
    def get_busiest_days(self, *, business_id, window_days: int = 90):
        start = timezone.now().date() - timedelta(days=window_days - 1)

        rows = (
            self.inv_model.objects
            .filter(business_id=business_id, status=InvoiceStatus.PAID, created_at__date__gte=start)
            .annotate(weekday=ExtractWeekDay("created_at"))
            .values("weekday")
            .annotate(revenue=Sum("total"))
        )
        by_weekday = {r["weekday"]: float(r["revenue"]) for r in rows}

        labels = [WEEKDAY_LABELS[d] for d in WEEKDAY_DISPLAY_ORDER]
        revenue = [by_weekday.get(d, 0.0) for d in WEEKDAY_DISPLAY_ORDER]

        has_data = bool(by_weekday)
        peak_index = revenue.index(max(revenue)) if has_data else None
        total = sum(revenue)
        peak_pct = round((revenue[peak_index] / total) * 100) if peak_index is not None and total else None

        return {
            "labels": labels,
            "revenue": revenue,
            "has_data": has_data,
            "peak_index": peak_index,
            "peak_label": labels[peak_index] if peak_index is not None else None,
            "peak_pct": peak_pct,
        }
    
    def get_top_products(self, *, business_id, limit: int = 5, since=None) -> list[dict]:
        """Top products by revenue, grouped by snapshotted name — survives catalog edits/deletions."""
        
        queryset = self.inv_line_item_model.objects.filter(
            invoice__business_id=business_id,
            invoice__status=InvoiceStatus.PAID,
        )
        if since:
            queryset = queryset.filter(invoice__created_at__date__gte=since)

        return list(
            queryset
            .values("product_name")
            .annotate(total_sales=Count("id"), total_revenue=Sum("line_subtotal"))
            .order_by("-total_revenue")[:limit]
        )
        
    def get_weekly_revenue_change(self, *, business_id) -> dict:
        """One query, two conditional sums — no row fetching, no Python-side aggregation."""
        today = timezone.localdate()
        this_week_start = today - timedelta(days=today.weekday())  # Monday
        last_week_start = this_week_start - timedelta(days=7)

        totals = (
            self.inv_model.objects
            .filter(business_id=business_id, status=InvoiceStatus.PAID, created_at__date__gte=last_week_start)
            .aggregate(
                this_week=Sum("total", filter=Q(created_at__date__gte=this_week_start)),
                last_week=Sum("total", filter=Q(created_at__date__lt=this_week_start)),
            )
        )
        this_week = totals["this_week"] or Decimal("0")
        last_week = totals["last_week"] or Decimal("0")

        if last_week > 0:
            percent_change = round(((this_week - last_week) / last_week) * 100)
        elif this_week > 0:
            percent_change = 100  # 0 → something isn't a real percentage; cap the display rather than show "∞%"
        else:
            percent_change = 0

        return {"revenue_percent_change": percent_change, "revenue_is_increase": percent_change >= 0}
    
    def get_platform_gmv_trend(self, *, period: str = "7d") -> dict:
        """GMV = gross transaction volume across every business on the platform,
        not SalesIQ's own revenue."""
        days = PERIOD_DAYS.get(period, 7)
        start = timezone.now().date() - timedelta(days=days - 1)

        rows = (
            self.inv_model.objects
            .filter(status=InvoiceStatus.PAID, created_at__date__gte=start)
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
        platform_vol = (
            self.inv_model.objects
            .filter(status=InvoiceStatus.PAID).aggregate(total=Sum("total"))["total"]
            or Decimal("0")
        )
        return platform_vol
    
    def _base_detail_queryset(self):
        return (
            self.inv_model.objects
            .select_related("business", "customer", "customer__client")
            .prefetch_related(
                Prefetch("line_items", queryset=self.inv_line_item_model.objects.select_related("product"))
            )
        )
