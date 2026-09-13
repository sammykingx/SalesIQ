from invoices.repository import InvoiceRepository
from accounts.selectors import BusinessSelector


class InvoiceService:
    def __init__(self) -> None:
        self.inv_repo = InvoiceRepository()
        self.biz_selector = BusinessSelector()