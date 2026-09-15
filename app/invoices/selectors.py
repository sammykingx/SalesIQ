from invoices.models import Invoice, InvoiceLineItem
from django.db.models import Prefetch


class InvoiceSelectors:
    def __init__(self) -> None:
        self.inv_model = Invoice
        self.inv_line_item_model = InvoiceLineItem
    
    def get_invoice_by_slug(self, *, slug: str) -> Invoice | None:
        return self._base_detail_queryset().filter(slug=slug).first()

    def get_invoice_with_details(self, *, display_id: str) -> Invoice | None:
        """retunrs an invoice with the business, customer"""
        return self._base_detail_queryset().filter(display_id=display_id).first()

    def _base_detail_queryset(self):
        return (
            self.inv_model.objects
            .select_related("business", "customer", "customer__client")
            .prefetch_related(
                Prefetch("line_items", queryset=self.inv_line_item_model.objects.select_related("product"))
            )
        )
