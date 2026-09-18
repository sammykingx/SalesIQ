from django.db.models import Count, Prefetch, QuerySet, Sum
from django.db.models.functions import TruncDate
from django.utils import timezone

from invoices.models import Invoice, InvoiceLineItem, InvoiceStatus

from datetime import timedelta
from typing import List
from uuid import UUID


PERIOD_DAYS = {"7d": 7, "30d": 30, "90d": 90}

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
        return {"labels": labels, "revenue": revenue}
    
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
    
    def _base_detail_queryset(self):
        return (
            self.inv_model.objects
            .select_related("business", "customer", "customer__client")
            .prefetch_related(
                Prefetch("line_items", queryset=self.inv_line_item_model.objects.select_related("product"))
            )
        )
