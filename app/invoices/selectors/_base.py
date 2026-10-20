# invoices/selectors/_base.py
from invoices.models import Invoice, InvoiceLineItem


class InvoiceSelectorBase:
    """
    Base configuration class for invoice selectors.
    
    Serves as a centralized provider of core model attributes (`invoice_model`, 
    `line_item_model`) for selector subclasses to inherit. This decouples 
    query logic from hardcoded model imports, keeping the architecture DRY, 
    modular, and flexible for maintenance or testing.
    """

    invoice_model = Invoice
    line_item_model = InvoiceLineItem
    