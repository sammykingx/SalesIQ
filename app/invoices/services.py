from django.http import HttpRequest
from invoices.repository import InvoiceRepository
from accounts.selectors import BusinessSelector


class InvoiceService:
    def __init__(self, request: HttpRequest) -> None:
        self.request = request
        self.inv_repo = InvoiceRepository()
        self.biz_selector = BusinessSelector()
